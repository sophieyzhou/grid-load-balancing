import pandas as pd, matplotlib.pyplot as plt

df = pd.read_csv("Demand_Raw.csv")
df = df[['period','value']]

df['period'] = pd.to_datetime(df['period'])

# Extract the ISO calendar week number
df['week'] = df['period'].dt.isocalendar().week
# Group by week and find the row with the maximum value
weekly_max = df.loc[df.groupby('week')['value'].idxmax()]

# Drop the 'week' column if it's not needed
df = weekly_max.drop(columns=['week']).reset_index(drop=True)

df['day'] = df['period'].dt.dayofyear

#pull the subset of the renewable energy data that matches the demand periods to set maximum 
#since my data source is generation data i can directly take data generated = capacity factor * nameplate capacity

def match_data(sol):
    sol = sol[['period','value']]
    sol['period'] = pd.to_datetime(sol['period'])
    sol['day'] = sol['period'].dt.dayofyear
    sol = sol.loc[sol.groupby('day')['value'].idxmax()]
    return sol[sol['day'].isin(df['day'])]

#took max solar data for the given day 
sold = pd.read_csv("sol_generation.csv")
sold.drop_duplicates()
sold = sold[['period','value']]
sold['period'] = pd.to_datetime(sold['period'])
sold['day'] = sold['period'].dt.dayofyear
sold = sold.loc[sold.groupby('day')['value'].idxmax()]
sold = sold[sold['day'].isin(df['day'])]
sold.to_csv('SolarCaps.csv')

wnd = pd.read_csv("wnd_generation.csv")
wnd_data = match_data(wnd)
wnd_data.to_csv('WindCaps.csv')

hydr = pd.read_csv("hydr_generation.csv")
hydr_data = match_data(hydr)
hydr_data.to_csv('HydroCaps.csv')

df.to_csv("Demand_Data.csv")
