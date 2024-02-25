import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import yaml
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import utils

# with open("../../config.yaml", "r") as file:
#     config = yaml.safe_load(file)

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)
url = "file:///Users/mneau/Desktop/safeflat/scraping/gensdeconfiance/example.html"

driver.get(url)

time.sleep(2)

print(utils.get_annonce_data(driver, url))
