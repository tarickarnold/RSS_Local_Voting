import requests
import datetime
import pandas as pd
from pandas import json_normalize

starting_day_of_current_year = datetime.datetime.now().replace(month=1, day=1)    
ending_day_of_current_year = datetime.datetime.now().replace(month=12, day=31)

FirstDay = starting_day_of_current_year.strftime('%m/%d/%Y')
LastDay = ending_day_of_current_year.strftime('%m/%d/%Y')                                

url = "https://www2.tulsacounty.org/umbraco/BackOffice/Api/AppointmentsApi/LoadElectionData"

headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

response = requests.request("POST", url, headers=headers).json()

df = json_normalize(response)
