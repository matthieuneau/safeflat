import os
import utils
import pandas as pd
from numpy import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

output_file = "/Users/mneau/Desktop/safeflat/scraping/leboncoin/output.csv"

# Initialize an empty DataFrame if the file doesn't exist or is empty
if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
    database = pd.DataFrame()
else:
    database = pd.read_csv(output_file)

nb_pages = 2

for page_num in range(1, nb_pages + 1):
    url = f"https://www.leboncoin.fr/recherche?category=10&owner_type=private&real_estate_type=1%2C2&page={page_num}"
    # url = "file:///Users/mneau/Desktop/safeflat/scraping/leboncoin/search_result.html"
    # url = "file:///Users/mneau/Desktop/safeflat/scraping/leboncoin/example.html"

    driver.get(url)
    time.sleep(random.uniform(6, 8))

    urls = [
        element.get_attribute("href")
        for element in driver.find_elements(
            By.CSS_SELECTOR, 'a[data-qa-id="aditem_container"]'
        )
    ]
    print(urls)

    for url in urls:
        data = utils.get_annonce_data(driver, url)
        print(data)
        new_data_df = pd.DataFrame([data])
        # Check if the new data is already present in the in-memory DataFrame
        if not new_data_df.isin(database.to_dict("records")).all(1).any():
            # If the data is not present, append it to the in-memory DataFrame
            database = pd.concat([database, new_data_df], ignore_index=True)
        else:
            print("Duplicate data, not appending.")
        time.sleep(2)

database.to_csv(output_file, index=False, mode="w")

# Close the browser
driver.quit()
