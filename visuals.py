from pyomo.environ import *
import pandas as pd, matplotlib.pyplot as plt

solar = pd.read_csv('SolarCaps.csv',header=0,index_col=0)

#Import data
demand = pd.read_csv('Demand_Data.csv')
demand.index = list(range(1,len(demand.index.values)+1)) #relabel demand indices as ints starting at 1

# Plot solar against demand to show that we expect the hydrogen cell to charge in winter and discharge in summer
plt.figure(figsize=(10, 5))  # Optional: Set the figure size
plt.plot(solar['day'], solar['value'], marker='o', linestyle='-', label='Solar Generation')
plt.plot(demand['day'], demand['value'], marker='o', linestyle='-', label='Demand')
plt.title('Solar Generation and Demand \n Throughout the Year')
plt.xlabel('Day of Year')
plt.ylabel('Energy (MW)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()  # Optional: Add a legend
plt.grid(True)  # Optional: Add a grid
plt.tight_layout()  # Adjust layout to prevent label overlap
plt.savefig('Seasonality.png')


df = pd.read_csv("Model_outputs.csv")
fixed_rte = 0.75

# Filter and sort the DataFrame for fixed RTE
df_fixed_rte = df[df["RTE"] == fixed_rte].sort_values("Tax ($/Ton CO2)")

# Plot CO2 emissions vs. Tax Rate
plt.figure(figsize=(10, 6))
plt.plot(df_fixed_rte["Tax ($/Ton CO2)"], df_fixed_rte["Emissions (Tons/MWh)"], marker='o')
plt.title(f"CO2 Emissions vs. Tax Rate (RTE = {fixed_rte})")
plt.xlabel("Tax Rate ($/Ton CO2)")
plt.ylabel("CO2 Emissions (Tons/MWh)")
plt.grid(True)
plt.savefig('Model.png')



fixed_tax = 50

# Filter and sort the DataFrame for fixed RTE
df_fixed_tax = df[df["Tax ($/Ton CO2)"] == fixed_tax].sort_values("RTE")

# Plot CO2 emissions vs. Tax Rate
plt.figure(figsize=(10, 6))
plt.plot(df_fixed_tax["RTE"], df_fixed_tax["Emissions (Tons/MWh)"], marker='o')
plt.title(f"CO2 Emissions vs. RTE (Tax Rate = {fixed_tax})")
plt.xlabel("RTE")
plt.ylabel("CO2 Emissions (Tons/MWh)")
plt.grid(True)
plt.savefig('plots.png')

df_fixed_rte = df[df["RTE"] == fixed_rte].sort_values("Tax ($/Ton CO2)")

# Plot CO2 emissions vs. Tax Rate
plt.figure(figsize=(10, 6))
plt.plot(df_fixed_rte["Tax ($/Ton CO2)"], df_fixed_rte["Emissions (Tons/MWh)"], marker='o')
plt.title(f"CO2 Emissions vs. Tax Rate (RTE = {fixed_rte})")
plt.xlabel("Tax Rate ($/Ton CO2)")
plt.ylabel("CO2 Emissions (Tons/MWh)")
plt.grid(True)
plt.savefig('Model.png')
