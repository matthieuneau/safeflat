from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import yaml
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

with open("../../config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# URL of the page
url = "file:///Users/mneau/Desktop/safeflat/scraping/leboncoin/leboncoin_example.html"

# Navigate to the page
driver.get(url)

# Wait to bluff the captcha mechanism
time.sleep(2)

# Retrieve the title
title = driver.find_element(
    By.CSS_SELECTOR, ".break-words.text-headline-1-expanded.undefined"
).text
print(f"title: {title}")

# Retrieve the specs
specs = driver.find_elements(
    By.CSS_SELECTOR, ".inline-flex.w-full.flex-wrap.mb-md span"
)
specs = [spec.text for spec in specs]
print(f"specs: {specs}")

# Retrieving price
price = driver.find_element(
    By.XPATH, '//*[@id="grid"]/article/div[1]/div/div[1]/div[2]/div/p'
).text
print(f"price: {price}")

# Retrieving post date
post_date = driver.find_element(
    By.XPATH,
    '//*[@id="grid"]/article/div[1]/div/div[2]/p',
).text
print(f"post_date: {post_date}")

# Retrieving description
description = driver.find_element(
    By.XPATH,
    '//*[@id="grid"]/article/div[4]/div[2]/div/p',
).text
print(f"description: {description}")

# Retrieving the criteres titles and values
titles_and_values = driver.find_elements(
    By.CSS_SELECTOR, "div.styles_criteria__U5Ul8.flex.flex-wrap > div"
)
# Filter out energy class and GES because we need to treat them separately
titles_and_values = [
    item
    for item in titles_and_values
    if (
        "criteria_item_energy_rate" not in item.get_attribute("class")
        and "criteria_item_ges" not in item.get_attribute("class")
    )
]

# Retrieving the criteres titles
titles = [item.find_element(By.CSS_SELECTOR, "div>div>p") for item in titles_and_values]
print([value.text for value in titles])

# Retrieving the criteres values
values = [
    item.find_element(By.CSS_SELECTOR, "div>div>span") for item in titles_and_values
]
print([value.text for value in values])

# Close the browser
driver.quit()

# grid > article > div:nth-child(2) > div > div.sc-12a6ec0d-0.gJGwBE > div.mr-md.flex.flex-wrap.items-center.justify-between > div > p
