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
# options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# URL of the page
url = "file:///Users/mneau/Desktop/safeflat/scraping/leboncoin/leboncoin_example.html"

# Navigate to the page
driver.get(url)

# Wait to bluff the captcha mechanism
time.sleep(2)

title = driver.find_element(
    By.CSS_SELECTOR, ".break-words.text-headline-1-expanded.undefined"
).text
print(f"title: {title}")

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

# Retrieving criteres
criteres = driver.find_elements(
    By.CSS_SELECTOR, "div.styles_criteria__U5Ul8.flex.flex-wrap > div > div"
)

print(criteres[0].find_element(By.CSS_SELECTOR, "span").text)


criteres = {
    c.find_element(By.CSS_SELECTOR, "p")
    .text: c.find_element(By.CSS_SELECTOR, "span")
    .text
    for c in criteres
}
print(f"criteres: {criteres}")

# Close the browser
driver.quit()

# grid > article > div:nth-child(2) > div > div.sc-12a6ec0d-0.gJGwBE > div.mr-md.flex.flex-wrap.items-center.justify-between > div > p
