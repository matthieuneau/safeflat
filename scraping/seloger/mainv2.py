import time
import undetected_chromedriver as uc
import utils
import os
import pandas as pd
from selenium.webdriver.common.by import By
from tqdm import tqdm

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("--headless")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

output_file = "output.csv"

# Initialize an empty DataFrame if the file doesn't exist or is empty
if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
    database = pd.DataFrame()
else:
    database = pd.read_csv(output_file)

page_nb = 2

for i in tqdm(range(1, page_nb + 1), desc="Scraping pages"):
    url = f"https://www.seloger.com/list.htm?projects=1&types=2%2C1&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&LISTING-LISTpg={i}"
    driver.get(url)
    time.sleep(4)

    url_elems = driver.find_elements(
        By.CSS_SELECTOR, "a[data-testid='sl.explore.coveringLink']"
    )
    print("len url_elems", len(url_elems))
    url_list = [
        element.get_attribute("href")
        for element in url_elems
        if element.get_attribute("href")
    ]
    url_list = url_list[:5]  # For testing purpose
    print(f"url_list: {url_list}")

    # Implement tqdm progress bar for URL scraping
    with tqdm(total=len(url_list), leave=False, desc=f"Processing Page {i}") as pbar:
        for url in url_list:
            driver.get(url)
            time.sleep(6)
            print(f"url: {url}")
            data = utils.retrieve_data(url, "output.csv")
            print(f"data: {data}")
            new_data_df = pd.DataFrame([data])

            if not new_data_df.isin(database.to_dict("records")).all(1).any():
                database = pd.concat([database, new_data_df], ignore_index=True)
            else:
                print("Duplicate data, not appending.")

            pbar.update(
                1
            )  # Manually update the progress bar after each URL is processed

database.to_csv(output_file, mode="w", header=True, index=False)
driver.quit()