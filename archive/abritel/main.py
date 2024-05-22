import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import os
import pandas as pd
from tqdm import tqdm
from utils import retrieve_data


url = "https://www.abritel.fr/search?adults=2&d1=2024-04-24&d2=2024-04-25&destination=Paris%20%28et%20environs%29%2C%20France&endDate=2024-04-25&flexibility=7_DAY&latLong=48.853564%2C2.348095&regionId=179898&semdtl=&sort=RECOMMENDED&startDate=2024-04-24&theme=&userIntent="
#url = "https://en.wikipedia.org/wiki/Madagascar"
urls = []
# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)

time.sleep(90)  # Ajustez ce temps selon la vitesse de chargement de votre page


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
        try:
                database = pd.read_csv(output_file)
        except pd.errors.EmptyDataError:
                print("Le fichier CSV est vide ou n'existe pas.")
                # Vous pouvez initialiser `database` à un DataFrame vide ou à une autre valeur par défaut
                database = pd.DataFrame()


page_nb = 1

for i in tqdm(range(1, page_nb + 1), desc="Scraping pages"):
    url = "https://www.abritel.fr/search?destination=Paris%20%28et%20environs%29%2C%20France&regionId=179898&latLong=48.853564%2C2.348095&flexibility=7_DAY&d1=2024-05-25&startDate=2024-05-25&d2=2024-05-26&endDate=2024-05-26&adults=2&theme=&userIntent=&semdtl=&sort=RECOMMENDED"
    driver.get(url)
    time.sleep(30)

    url_elems = driver.find_elements(
    By.CSS_SELECTOR, "a[data-stid='open-hotel-information']")

    print("len url_elems", len(url_elems))
    url_list = [
        element.get_attribute("href")
        for element in url_elems
        if element.get_attribute("href").startswith(
            "https://www.abritel.fr/"
        )  # avoids to retrieve the urls that redirect to ads
    ]
    #url_list = url_list[:5]  # For testing purpose
    url_list = list(set(url_list))
    print(f"url_list: {url_list}")
    driver.quit()

    # Implement tqdm progress bar for URL scraping
    with tqdm(total=len(url_list), leave=False, desc=f"Processing Page {i}") as pbar:
        for url in url_list:
            #driver.get(url)
            #time.sleep(6)
            print(f"url: {url}")
            data = retrieve_data(url)
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