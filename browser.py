import logging
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from terminator import close_app
from screenshot import take_screenshot

browser_logger = logging.getLogger(__name__)

def scrape(birthdate, firstname, lastname, browser) -> None:

    data = []
    total_transactions = 0
    success = 0 
    business_exception = 0
    system_exception = 0


    options = ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("https://okvoterportal.okelections.us/")

    browser_logger.info("Set driver settings for browser")

    try:

        # Wait for homepage to load
        homeelement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Home"))
        )

        browser_logger.info("Browser found voter portal page")

        # Enter Last Name
        time.sleep(2)
        lastnamebox = driver.find_element(By.ID, "LastName")
        lastnamebox.clear()
        lastnamebox.click()
        lastnamebox.send_keys(lastname)
        time.sleep(1)

        # Enter First Name
        firstnamebox = driver.find_element(By.ID, "FirstName")
        firstnamebox.clear()
        firstnamebox.click()
        firstnamebox.send_keys(firstname)
        time.sleep(1)

        # Enter Birthday
        dob = driver.find_element(By.ID, "BirthDate")
        dob.clear()
        dob.click()
        dob.send_keys(birthdate)
        time.sleep(1)

        # Click submit button
        findme = driver.find_element(By.ID, "btFind")
        findme.click()
        browser_logger.info("Browser submitted data for search")

        # Wait for next page to load
        confirmelement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VoterTitle"))
        )

        browser_logger.info("Browser found results page")

        # Find voter name
        voter = driver.find_element(By.ID, "VoterTitle")
        votername = voter.text[7:]
        browser_logger.info(f"Browser found {votername}")

        # Find voter ID
        voterdata = driver.find_element(
            By.XPATH, "/html/body/div[3]/main/div[2]/div[2]/div[1]/div[1]"
        )
        voteridstring = voterdata.text.split("\n")
        voterid = voteridstring[1]
        precinct = voteridstring[3]
        affiliation = voteridstring[5]
        browser_logger.info(f"Browser found {voterid}, {precinct}, and {affiliation}")

        # Find Zipcode
        zipcodedata = driver.find_element(
            By.XPATH, "/html/body/div[3]/main/div[2]/div[2]/div[1]/div[2]"
        )
        zipcodestring = zipcodedata.text.split("\n")
        zipcode = zipcodestring[1]
        browser_logger.info(f"Browser found {zipcode}")
    
        # Find Voting location
        pollingplacedata = driver.find_element(
            By.XPATH, "//*[@id='Polling']/div[2]/div[1]/div[1]"
        )
        pollingstring = pollingplacedata.text.split("\n")
        pollingname = pollingstring[1]
        pollingaddr = pollingstring[3]
        pollingcity = pollingstring[4]
        fullpollingaddr = pollingaddr + pollingcity
        browser_logger.info(f"Browser found {pollingname} and {fullpollingaddr}")

        # Find election board info
        electionboarddata = driver.find_element(
            By.XPATH, "//*[@id='CEB']/div[2]/div/div[1]"
        )
        electionboardstring = electionboarddata.text.split("\n")
        electionboardname = electionboardstring[1]
        electionboardaddr = electionboardstring[3]
        electionboardcity = electionboardstring[4]
        fullelctionboardaddr = electionboardaddr + " " + electionboardcity
        electionboardmailbox = electionboardstring[6]
        electionboardmailcity = electionboardstring[7]
        fullelectionboardmailbox = electionboardmailbox + "  " + electionboardmailcity
        electionboardopen = electionboardstring[9]
        electionboardclose = electionboardstring[11]
        electionboardofficehours = electionboardopen + " - " + electionboardclose
        electionboardphone = electionboardstring[13]
        electionboardemail = electionboardstring[17]
        
        browser_logger.info(f"Browser found {electionboardname} and {fullelctionboardaddr}")
        data.append(
     f"""Name: {votername}
        Voter Id: {voterid}
        Precinct: {precinct}
        Affiliation: {affiliation}
        Polling Name: {pollingname}
        Address: {fullpollingaddr}
        Election Board Name: {electionboardname}
        Election Board Address: {fullelctionboardaddr}
        Election Board Mailbox: {electionboardmailbox}
        Election Board Offcie Hours: {electionboardofficehours}
        Election Board Phone: {electionboardphone}
        Election Board Email: {electionboardemail}""")

        success += 1
        total_transactions += 1
        driver.quit()
    
    except Exception as e:
        # Screenshot page to see if there was a issue.
        system_exception += 1
        total_transactions += 1
        error: Exception = e
        take_screenshot()
        browser_logger.info(f"Browser failed.")
        if driver.current_url == "about:blank":
            print("The browser is closed")
        else:
            close_app(browser)
            print("The browser is open")
        
        data.append(success)
        data.append(system_exception)
        data.append(business_exception)
        data.append(total_transactions)
        data.append(e)

    data.append(success)
    data.append(system_exception)
    data.append(business_exception)
    data.append(total_transactions)
    data.append("")
    
    

    return data
        