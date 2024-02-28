import os
from tqdm import tqdm
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

# Need to login first...
driver.get("https://accounts.gensdeconfiance.com/login")
email = "m.neau10@gmail.com"
password = "Safeflat123"

time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="identifier"]').send_keys(email)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div/form/button').click()

time.sleep(2)
output_file = "output.csv"

# Initialize an empty DataFrame if the file doesn't exist or is empty
if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
    database = pd.DataFrame()
else:
    database = pd.read_csv(output_file)

# Browsing the pages
pages_to_scrape = list(range(1, 3))

with tqdm(
    total=len(pages_to_scrape), desc="Pages Progress", leave=False, colour="green"
) as pages_progress:
    for page_num in pages_to_scrape:
        url = f"https://gensdeconfiance.com/ui/search?radius=10&rootLocales=fr%2Cen&orderColumn=pertinence&orderDirection=ASC&type=offering&ownerTypes=INDIVIDUAL%2CPRO%2CASSO&propertyTypes=apartment%2Chome&category=realestate__rent&page={page_num}"
        driver.get(url)
        time.sleep(2)

        # Get the list of URLs
        page_urls = driver.find_elements(
            By.XPATH,
            "//*[@id='__next']/div[2]/main/div/main/div[1]/form/section[2]/div[3]/a",
        )
        url_list = [item.get_attribute("href") for item in page_urls]
        url_list = url_list[:5]  # For testing purpose
        print(f"url_list: {url_list}")

        # Initialize the second progress bar for annonce progression on the current page
        with tqdm(
            total=len(url_list),
            desc=f"Page {page_num} Annonces",
            leave=False,
            colour="#00ff00",
        ) as annonces_progress:
            for url in url_list:
                data = utils.get_annonce_data(driver, url)
                new_data_df = pd.DataFrame([data])

                # Check if the new data is already present in the in-memory DataFrame
                if not new_data_df.isin(database.to_dict("records")).all(1).any():
                    # If the data is not present, append it to the in-memory DataFrame
                    database = pd.concat([database, new_data_df], ignore_index=True)
                else:
                    print("Duplicate data, not appending.")
                time.sleep(2)

                # Update the second progress bar after processing each annonce
                annonces_progress.update(1)

        # Update the first progress bar after completing all annonces on the current page
        pages_progress.update(1)


database.to_csv(output_file, index=False, mode="w")

# Close the browser
driver.quit()
