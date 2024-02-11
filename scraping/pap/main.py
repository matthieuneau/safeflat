from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import yaml
import utils
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

with open("../../config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# URL of the page
url = "file:///Users/mneau/Desktop/safeflat/scraping/pap/pap_example.html"

driver.get(url)

# Wait for the element to be loaded
time.sleep(2)

# Find the paragraph element using CSS Selector
paragraph = driver.find_element_by_css_selector(
    ".ll4r2nl.atm_kd_pg2kvz_1bqn0at.dir.dir-ltr"
)

# Retrieve the text
text = paragraph.text

# Write the text to a file
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(text)

# Close the browser
driver.quit()
