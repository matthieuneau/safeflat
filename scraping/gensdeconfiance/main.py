from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import yaml
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import utils

with open("../../config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# Need to login first...
driver.get("https://accounts.gensdeconfiance.com/login")
email = "m.neau10@gmail.com"
password = "Safeflat123"

time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="identifier"]').send_keys(email)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div/form/button').click()

# Browsing the pages
nb_pages = 2
for page_num in range(1, nb_pages + 1):
    url = "https://gensdeconfiance.com/ui/search?radius=10&rootLocales=fr%2Cen&orderColumn=pertinence&orderDirection=ASC&type=offering&ownerTypes=INDIVIDUAL%2CPRO%2CASSO&propertyTypes=apartment%2Chome&category=realestate__rent&page={page_num}"
    # Navigate to the page
    driver.get(url)
    time.sleep(2)

    # Get the list of URLs
    urls = driver.find_elements(
        By.XPATH,
        "//*[@id='__next']/div[2]/main/div/main/div[1]/form/section[2]/div[3]/a",
    )
    url_list = [item.get_attribute("href") for item in urls]
    print(f"url_list: {url_list}")

    for url in url_list:
        data = utils.get_annonce_data(driver, url)
        print(f"data: {data}")

# Close the browser
driver.quit()
