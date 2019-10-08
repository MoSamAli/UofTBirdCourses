# This scraper requires a valid UTOR login. You will be prompted for your UTORID and password
# when running this scraper because the website being scraped is behind an Acorn login screen

from getpass import getpass
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import json

with open('config.json') as scraper_config_file:
    scraper_config = json.load(scraper_config_file)

quercus_url = "https://q.utoronto.ca/courses/48756/external_tools/291"
evals_url = "https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=hjeZ7JJWJupVgjPoyu&userid=tO4GQugFiFULB0AXgInh7idHCU-AnN3pNhvC&lng=en"

#TODO: Create configurable driver

# if scraper_config["driver"] is "chrome":
#     driver = webdriver.Chrome()
# elif scraper_config["driver"] is "firefox":
#     driver = webdriver.Firefox()

driver = webdriver.Firefox()

driver.implicitly_wait(5)
driver.get(quercus_url)

# Elements from the acorn login page
utorid_input: WebElement = driver.find_element_by_id("username")
password_input: WebElement = driver.find_element_by_id("password")
login_button: WebElement = driver.find_element_by_name("_eventId_proceed")

# Prompts user for UTORID and password and logs into acorn with those details
utorid = input("UTORID: ")
utorid_input.send_keys()
password = getpass()
password_input.send_keys(password)
login_button.click()

# Once you're loggin in, navigate to the course evals URL
driver.get(evals_url)


# Elements from the course evals data page
hundred_button: WebElement = driver.find_element_by_css_selector("#fbvGridPageSizeSelectBlock > select:nth-child(1) > option:nth-child(7)")
next_button: WebElement = driver.find_element_by_css_selector(".gPaging > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > input:nth-child(1)")
print(next_button)
# Fetch 100 evals at a time. 
hundred_button.click()

# This is the html we get from the page
html: property = driver.page_source
soup = BeautifulSoup(html, 'html')


find_result = soup.find(id="fbvGrid")
print(find_result)
#Turn this result into a list of dictionaries check https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-the-tree

# For now, all we do with the beautiful soup data model of our page is write it to an index.html
# file. #TODO: Parse this data and get the course eval info we're looking for
#index = open("index.html", "w")
#index.write(str(soup))
