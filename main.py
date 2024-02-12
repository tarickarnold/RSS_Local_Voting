import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from icecream import ic

url = 'https://www2.tulsacounty.org/electionboard/elections/election-calendar/'
response = requests.get(url)
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(30)
driver.get(url)

#Delay
WebDriverWait(driver,15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "e-subject")))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup.text)

date = []
for text in soup.find_all('div',class_='e-time'):
    date.append(text.get_text())
    print(date)