from pyomo.environ import *
import pandas as pd, matplotlib.pyplot as plt


#Import data
demand = pd.read_csv('Demand_Data.csv',header=0,index_col=[0,1])['value']
demand.index = list(range(1,len(demand.index.values)+1)) #relabel demand indices as ints starting at 1

fleet = pd.read_csv('fleet.csv',header=0,index_col=0)
storageunit = pd.read_csv('h2storage.csv',header=0,index_col=0)
fleet = pd.concat([fleet, storageunit])

smax = pd.read_csv('SolarCaps.csv',header=0,index_col=[0,1])['value']
wmax = pd.read_csv('WindCaps.csv',header=0,index_col=[0,1])['value']
hmax = pd.read_csv('HydroCaps.csv',header=0,index_col=[0,1])['value']
smax.index = pd.MultiIndex.from_product([['Sol'],demand.index.values]) #relabel time index so aligned w/ demand
wmax.index = pd.MultiIndex.from_product([['Wnd'],demand.index.values])
hmax.index = pd.MultiIndex.from_product([['Hydr'],demand.index.values])
rmax =  pd.concat([smax, wmax, hmax])
h2cost = 28.5
carbon_cost = 20

# Create a ConcreteModel object
model = ConcreteModel()

# Set of generators
model.generators = Set(initialize=fleet.index.values) 
model.times = Set(initialize=demand.index.values)
model.regenerators = Set(within=model.generators,initialize=fleet.loc[fleet['Fuel Type'].isin(['Solar', 'Wind', 'Hydro'])].index.values)
model.storage = Set(within=model.generators,initialize=storageunit.loc[storageunit['Fuel Type']=='Storage'].index.values)

# Parameters
model.pCaps = Param(model.generators,initialize=fleet['Maximum Capacity (MW)'].to_dict()) #capacities in MW
model.pCO2 = Param(model.generators,initialize=fleet['CO2 Emissions Rate (tons/MWh)'].to_dict()) #capacities in MW
model.pHRs = Param(model.generators,initialize=fleet['Heat Rate (MMBtu/MWh)'].to_dict()) #heat rates in MMBtu/MWh
model.pVOMs = Param(model.generators,initialize=fleet['Variable O&M ($/MWh)'].to_dict()) #variable O&M costs in $/MWh
model.pFCs = Param(model.generators,initialize=fleet['Fuel Cost ($/MMBtu)'].to_dict()) #fuel costs in $/MMBtu
model.pMaxs = Param(model.generators,model.times,initialize=rmax.to_dict()) #maximum gen renewables
model.pDemand = Param(model.times,initialize=demand.to_dict()) #demand in MWh
model.pX = Param(model.storage, initialize=storageunit['Maximum Energy Capacity (MWh)'].to_dict())
model.pRTE = Param(model.storage,initialize=storageunit['RTE'].to_dict())
model.pDCap = Param(model.storage,initialize=storageunit['Discharge Rate(MW)'].to_dict())
# Variables
model.vPower = Var(model.generators, model.times, within=NonNegativeReals)
model.vCharge = Var(model.storage, model.times, within=NonNegativeReals)
model.vStateofCharge = Var(model.storage, model.times, within=NonNegativeReals)

# Objective function
def objFunc(model):
    return sum((model.pHRs[gen] * model.pFCs[gen] + model.pVOMs[gen] + model.pCO2[gen]*carbon_cost) * model.vPower[gen,t] for gen in model.generators for t in model.times)
model.cost = Objective(rule=objFunc, sense=minimize)

# Constraints
def supplyDemandBalanceConstraint(model, t):
	return sum(model.vPower[gen,t]  for gen in model.generators) == model.pDemand[t] + sum(model.vCharge[stor, t] for stor in model.storage)
model.sd = Constraint(model.times, rule=supplyDemandBalanceConstraint)


def genMaxCapConstraint(model, gen, t):
    # exclude discharge of storage units 
    if gen in model.storage:
        return Constraint.Skip
    return model.vPower[gen,t] <= model.pCaps[gen]
model.cap = Constraint(model.generators,model.times,rule=genMaxCapConstraint)

def genMaxDisConstraint(model, gen, t):
    # limit on discharge rate is separate from charge limit
    return model.vPower[gen,t] <= model.pDCap[gen]
model.scap = Constraint(model.storage,model.times,rule=genMaxDisConstraint)

def genDischargeEnergyConstraint(model, gen, t):
    return model.vPower[gen,t] <= model.vStateofCharge[gen,t] * model.pRTE[gen]
model.discharge_energy = Constraint(model.storage, model.times, rule=genDischargeEnergyConstraint)

# upper limit on charge rate is maximum capacity
def genMaxChargeConstraint(model, gen, t):
    return model.vCharge[gen,t] <= model.pCaps[gen]
model.mcharge = Constraint(model.storage,model.times,rule=genMaxChargeConstraint)

def genChargeStateConstraint(model, gen, t):
    return model.vStateofCharge[gen,t] <= (model.pX[gen])
model.chargest = Constraint(model.storage,model.times,rule=genChargeStateConstraint)

def genMinChargeStateConstraint(model, gen, t):
    return model.vStateofCharge[gen,t] >=0
model.mchargest = Constraint(model.storage,model.times,rule=genMinChargeStateConstraint)

def genChargeStateChangeConstraint(model, gen, t):
    if t == 1:
        return model.vStateofCharge[gen, t] == 0 - model.vPower[gen, t]/(model.pRTE[gen]**0.5) + model.vCharge[gen, t]*(model.pRTE[gen]**0.5)
    else:
        return model.vStateofCharge[gen, t] == model.vStateofCharge[gen,t-1] - model.vPower[gen, t]/(model.pRTE[gen]**0.5) + model.vCharge[gen, t]*(model.pRTE[gen]**0.5)
model.chargech = Constraint(model.storage,model.times,rule=genChargeStateChangeConstraint)


def genCFLimit(model, gen, t):
    return model.vPower[gen,t] <= model.pMaxs[gen,t]
model.cf = Constraint(model.regenerators,model.times,rule=genCFLimit)

# Solve the model
solver = SolverFactory('glpk')  
model.dual = Suffix(direction=Suffix.IMPORT)
results = solver.solve(model)

# Print model
# model.pprint()

# Display results
gen = pd.DataFrame(index=demand.index.values,columns=fleet.index.values)
if results.solver.termination_condition == TerminationCondition.optimal:
    print(f"Optimal solution found. Total cost: ${model.cost():.2f}") 

    for g in model.generators:
    	for t in model.times:
            gen.loc[t,g] = model.vPower[g,t].value
    
    print('Generation decisions:')
    for g in model.generators:
        sumj = 0
        for j in model.times:
            # print(f"{g, j}: {model.vPower[g, j].value} MWh")  
            sumj = sumj + model.vPower[g, j].value
        print(f"Total Energy Produced by {g}:", sumj)

else:
    print("Solver did not find an optimal solution.")

#Calculate system emissions
totalEmissions = (gen*fleet['CO2 Emissions Rate (tons/MWh)']).sum().sum()
print('Total system emissions (tons CO2):',totalEmissions)

#Plot system dispatch
gen.to_csv('GenerationWithoutSto.csv')
gen.plot.bar(stacked=True)
plt.ylabel('Generation (MWh)'), plt.xlabel('Time')
plt.gca().xaxis.set_ticklabels([])  
plt.title(f"RTE = 0.55, Tax = {carbon_cost}, Generation Mix")
plt.savefig('GenerationWithoutSto.png')

charge = pd.DataFrame(index=demand.index.values, columns=model.storage)
discharge = pd.DataFrame(index=demand.index.values, columns=model.storage)
state_of_charge = pd.DataFrame(index=demand.index.values, columns=model.storage)

# Extract values from the model for charging, discharging, and state of charge
for s in model.storage:
    for t in model.times:
        charge.loc[t, s] = model.vCharge[s, t].value
        discharge.loc[t, s] = model.vPower[s, t].value  # Assuming discharging is represented as power output
        state_of_charge.loc[t, s] = model.vStateofCharge[s, t].value

# Plot storage operations
plt.figure(figsize=(10, 6))

for s in model.storage:
    plt.plot(charge.index, charge[s], label=f'Charging {s}')
    plt.plot(discharge.index, discharge[s], label=f'Discharging {s}')
    plt.plot(state_of_charge.index, state_of_charge[s], label=f'State of Charge {s}')

plt.xlabel('Time')
plt.ylabel('Power / State of Charge (MWh)')
plt.title('Storage Facility Operations: Charging, Discharging, and State of Charge')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('Storage.png')