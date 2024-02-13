from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
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
# options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

nb_pages = 2

# for page_num in range(1, nb_pages + 1):

# url = f"https://www.pap.fr/annonce/location-appartement-maison-{page_num}"
url = "file:///Users/mneau/Desktop/safeflat/scraping/pap/listing_page.html"

driver.get(url)

# Wait for the element to be loaded
time.sleep(2)

url_list = driver.find_elements(By.CSS_SELECTOR, "a.item-thumb-link")
url_list = [item.get_attribute("href") for item in url_list]
# print(f"url_list: {url_list}")

output_file = "output.csv"

# Initialize an empty DataFrame if the file doesn't exist or is empty
if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
    database = pd.DataFrame()
else:
    database = pd.read_csv(output_file)

for annonce in url_list:
    data = utils.get_annonce_data(driver, annonce)
    new_data_df = pd.DataFrame([data])

    # Check if the new data is already present in the in-memory DataFrame
    if not new_data_df.isin(database.to_dict("records")).all(1).any():
        # If the data is not present, append it to the in-memory DataFrame
        database = pd.concat([database, new_data_df], ignore_index=True)
    else:
        print("Duplicate data, not appending.")

# After processing all annonces, write the consolidated DataFrame to the CSV file
database.to_csv(output_file, mode="w", header=True, index=False)

driver.quit()
