from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import yaml
import utils
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


with open("../../config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--headless")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# URL of the page
url = "file:///Users/mneau/Desktop/safeflat/scraping/pap/pap_example.html"

driver.get(url)

# Wait for the element to be loaded
time.sleep(2)

# Create a dictionary to store the data we scrape
data = {"title": [], "price": [], "description": []}

# Find the paragraph element using CSS Selector
title_and_price = driver.find_element(
    By.XPATH, "/html/body/div[2]/div/div[1]/h1[@class='item-title']"
)
title_and_price = title_and_price.text
print(f"title_and_price: {title_and_price}")

# Retrieving location
location = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[5]/h2")
location = location.text
print(f"location: {location}")

# Retrieving nb of rooms, surface and nb of bedrooms when available
list_items = driver.find_elements(
    By.CSS_SELECTOR,
    "body > div.sidebar-layout.margin-top-header.details-annonce-container > div > div.main-content.details-item.padding-top-30.padding-bottom-60.margin-bottom-60.sm-padding-bottom-40.sm-margin-bottom-30 > div.item-description.margin-bottom-30 > ul.item-tags.margin-bottom-20 > li",
)
details = [item.find_element(By.TAG_NAME, "strong").text for item in list_items]
print(f"details: {details}")

# Retrieving description
description = driver.find_element(
    By.XPATH, "/html/body/div[2]/div/div[1]/div[5]/div[1]"
)
description = description.text
print(f"description: {description}")

# Retrieving metro stations closeby
metro = driver.find_elements(
    By.CSS_SELECTOR,
    ".item-transports",
)
metro_stations = []
metro_stations = [item.text for item in transport]
print(f"metro_stations: {metro_stations}")

conditions_financieres = driver.find_elements(By.CSS_SELECTOR, ".row > .col-1-3")
conditions_financieres = [item.text for item in conditions_financieres]

driver.quit()
