import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from icecream import ic

url = 'https://www2.tulsacounty.org/electionboard/elections/election-calendar/'
response = requests.get(url)
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# driver.implicitly_wait(30)
driver.get(url)

#Delay until page fully loads
WebDriverWait(driver,15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "e-subject")))

#Extract text for parsing
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'e-appointment')))

TotalEventCount =  len(driver.find_elements(By.CLASS_NAME, 'e-appointment'))
LoopCount= 1

#Get calendar month
Month= soup.find('button', class_='e-tbar-btn e-tbtn-txt e-control e-btn e-lib')['aria-label']
AppointmentXPath = '//*[@id="schedule"]/div[3]/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/div[2]/div'
DatePath = "//div[@class='e-date-time-details e-text-ellipsis']"
SubjectPath = "//div[@class='e-subject e-text-ellipsis']"
LocationPath = "//div[@class='e-location-details e-text-ellipsis']"
Events = driver.find_elements(By.CLASS_NAME, 'e-appointment')

Dates = []
Subjects = []
Locations = []

while (LoopCount < TotalEventCount):
    for Event in range(TotalEventCount):
        EventInstance = driver.find_element(By.XPATH, AppointmentXPath).click()
        
        Date = driver.find_element(By.XPATH, DatePath).text
        Dates.append(Date)
        print(Date)

        Subject = driver.find_element(By.XPATH, SubjectPath).text
        Subjects.append(Subject)
        print(Subject)

        Location = driver.find_element(By.XPATH, LocationPath).text
        Locations.append(Location)
        print(Location)

        LoopCount +=1 
