import pandas as pd
import time
from scraper import scrape_ad
from processOutputs import *
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from tqdm import tqdm
from saveToDatabase import save_to_database


# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--incognito")

driver = uc.Chrome(options=options)

output_file = "/Users/mneau/Desktop/safeflat/scraping/pap/output.csv"

data_collected = pd.DataFrame()

pages_to_scrape = list(range(1, 2))

### SCRAPING LOOP

for page_num in tqdm(pages_to_scrape, desc="Scraping page"):
    ad_data = pd.DataFrame()

    url = f"https://www.pap.fr/annonce/location-appartement-maison-{page_num}"

    driver.get(url)
    time.sleep(2)

    url_list = driver.find_elements(By.CSS_SELECTOR, "a.item-thumb-link")
    url_list = [item.get_attribute("href") for item in url_list]
    url_list = url_list[:1]
    # print(f"url_list: {url_list}")

    # Create a manual tqdm progress bar for the inner loop
    pbar = tqdm(
        total=len(url_list), leave=False
    )  # leave=False to clean up on completion
    pbar.set_description(f"page {page_num}")

    with tqdm(total=len(url_list), leave=False, desc=f"Page {page_num}") as pbar:
        for i, annonce in enumerate(url_list, start=1):
            pbar.set_postfix_str(f"annonce {i}/{len(url_list)}")
            data = scrape_ad(driver, annonce)
            new_data_df = pd.DataFrame([data])
            ad_data = pd.concat([ad_data, new_data_df], ignore_index=True)
            pbar.update(1)
    pbar.close()

    ### POST PROCESSING THE DATA

    ad_data = process_outputs(ad_data)
    llm_data = process_description(ad_data["description"])
    final_data = add_chatgpt_info_to_data(llm_data, ad_data)
    data_collected = pd.concat([data_collected, final_data], ignore_index=True)

    ### SAVE THE DATA TO DATABASE
    save_to_database(data_collected)

driver.quit()
