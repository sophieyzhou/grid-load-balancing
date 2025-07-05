import requests
from pyomo.environ import *
import pandas as pd, matplotlib.pyplot as plt

max_capacity = [['Coal', 0], ['Natural Gas', 0], 
       ['Nuclear', 0], ['Solar', 0], 
       ['Hydro', 0], ['Wind', 0]] 

mean_cf = [['Solar', 0], ['Hydro', 0], ['Wind', 0]] 


# no way to enforce ramp rates because we are only evaluating one hour of demand per week


def get_data(link, link2, regen=False):
    response = requests.get(link)
    data = response.json()
    # print(response.json())
    df = pd.DataFrame(data['response']['data'])
    
    response = requests.get(link2)
    # Convert JSON response to a DataFrame
    data = response.json()
    # print(response.json())
    df2 = pd.DataFrame(data['response']['data'])
    df =  pd.concat([df, df2], ignore_index=True)
    df.drop_duplicates()
    df = df.sort_values(by='period')
    df = df.reset_index(drop=True)

    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    if(regen):
        return df['value'].max(), df
    return df['value'].max()
    
        
# coal data
url = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=COL&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
# api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&
url2 = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=COL&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)
# coal = get_data(url, url2)
max_capacity[0][1] = get_data(url, url2)
# print(max_capacity[0])

#natural gas
url = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=NG&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
# api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&
url2 = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=NG&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)

max_capacity[1][1] = get_data(url, url2)
# print(max_capacity[1])

#nuclear
url = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=NUC&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
# api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&
url2 = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=NUC&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)

max_capacity[2][1] = get_data(url, url2)
# print(max_capacity[2])

#petroleum excluded because relative generation (always < 100 MWhrs is so low as to ne negligible)

#solar
url = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=SUN&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
# api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&
url2 = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=SUN&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)

max_capacity[3][1], dat = get_data(url, url2, True)
dat.to_csv("sol_generation.csv")

# print(max_capacity[3])

#hydro
url = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=WAT&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
# api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&
url2 = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=WAT&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)
max_capacity[4][1], dat = get_data(url, url2, True)
dat.to_csv("hydr_generation.csv")


# print(max_capacity[4])

#wind
url = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=WND&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)
# api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&
url2 = (
    "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key=9D1WgTwRcH11wdAfwL5hALgKfsP6aB0TbsZZfdqX&frequency=hourly&data[0]=value&facets[respondent][]=CAL&facets[fueltype][]=WND&start=2023-01-01T00-08:00&end=2023-12-31T00-08:00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
)
max_capacity[5][1], dat = get_data(url, url2, True)
dat.to_csv("wnd_generation.csv")
# print(max_capacity[5])

df = pd.DataFrame(max_capacity, columns =['Fuel Type', 'Maximum Capacity (MW)']) 

df.to_csv("Max_Capacity.csv")


