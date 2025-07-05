import requests
from pyomo.environ import *
import pandas as pd, matplotlib.pyplot as plt

api_key = "9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX"
start_date = "2023-01-01T00"
end_date = "2023-12-31T23"
# Fetch data for 2023 (replace with desired year)
url = (
    "https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[type][]=D&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
response = requests.get(url)

# Convert JSON response to a DataFrame
data = response.json()
# print(response.json())
df = pd.DataFrame(data['response']['data'])


# Need to load 2x because there's constraints on how much data you can get at once out of the EIA API
url2 = (
    "https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[type][]=D&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)
response2 = requests.get(url2)

# Convert JSON response to a DataFrame
data2 = response2.json()
# print(response.json())
df2 = pd.DataFrame(data2['response']['data'])
df = pd.concat([df, df2], ignore_index=True)
df = df[['period','value']]
print(df.head())
df.drop_duplicates()
df.to_csv("Demand_Raw.csv")
# print(df.head())


# Ensure datettime
