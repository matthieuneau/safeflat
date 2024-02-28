import pandas as pd
import os
import time
import utils
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from tqdm import tqdm


# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--incognito")

driver = uc.Chrome(options=options)

output_file = "/Users/mneau/Desktop/safeflat/scraping/pap/output.csv"

# Initialize an empty DataFrame if the file doesn't exist or is empty
if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
    database = pd.DataFrame()
else:
    database = pd.read_csv(output_file)

pages_to_scrape = [1, 2, 3]

for page_num in tqdm(pages_to_scrape, desc="Scraping page"):

    url = f"https://www.pap.fr/annonce/location-appartement-maison-{page_num}"
    # url = "file:///Users/mneau/Desktop/safeflat/scraping/pap/listing_page.html"

    driver.get(url)

    # Wait for the element to be loaded
    time.sleep(3)

    url_list = driver.find_elements(By.CSS_SELECTOR, "a.item-thumb-link")
    url_list = [item.get_attribute("href") for item in url_list]
    url_list = url_list[:5]
    print(f"url_list: {url_list}")

    # Create a manual tqdm progress bar for the inner loop
    pbar = tqdm(
        total=len(url_list), leave=False
    )  # leave=False to clean up on completion
    pbar.set_description(f"page {page_num}")

    with tqdm(total=len(url_list), leave=False, desc=f"Page {page_num}") as pbar:
        for i, annonce in enumerate(url_list, start=1):
            pbar.set_postfix_str(f"annonce {i}/{len(url_list)}")
            data = utils.get_annonce_data(driver, annonce)
            new_data_df = pd.DataFrame([data])

            if not new_data_df.isin(database.to_dict("records")).all(1).any():
                database = pd.concat([database, new_data_df], ignore_index=True)
            else:
                print("Duplicate data, not appending.")

            pbar.update(1)  # Manually update the progress bar

database.to_csv(output_file, mode="w", header=True, index=False)

driver.quit()
