import requests
from bs4 import BeautifulSoup
from icecream import ic

r = requests.get('https://www2.tulsacounty.org/electionboard/elections/election-calendar/')
html = r.text

soup = BeautifulSoup(html,'html.parser')

ic(soup)
