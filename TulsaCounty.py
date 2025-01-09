import requests
import datetime
import pandas as pd
from pandas import json_normalize


#Get the first day and last day of the current year
starting_day_of_current_year = datetime.datetime.now().replace(month=1, day=1)    
ending_day_of_current_year = datetime.datetime.now().replace(month=12, day=31)

#Convert first day and last day to string format
FirstDay = starting_day_of_current_year.strftime('%m/%d/%Y')
LastDay = ending_day_of_current_year.strftime('%m/%d/%Y')
    
try:    
    url = "https://www2.tulsacounty.org/umbraco/BackOffice/Api/AppointmentsApi/LoadElectionData"
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

    #Request data from Tulsa County Voting Calendar in JSON    
    response = requests.request("POST", url, headers=headers).json()

    #Collect JSON data into a dataframe
    df = json_normalize(response)

    #Convert string to time in dataframe
    df['StartTime'] = pd.to_datetime(df['StartTime'], format = 'ISO8601')
    df['EndTime'] = pd.to_datetime(df['EndTime'], format='ISO8601')

    #Filter start date of event between first day and last day of the current year
    filtered_df = df.loc[(df['StartTime'] >= FirstDay) & (df['StartTime'] < LastDay)]

    #Sort start dates in chronological order
    sorted_df = filtered_df.sort_values(by='StartTime')

except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    raise SystemExit(e)

print(sorted_df)