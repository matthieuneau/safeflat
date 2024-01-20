import undetected_chromedriver as uc
import os
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

# Set Chrome Options
options = uc.ChromeOptions()
# options.headless=True
# options.add_argument('--headless')
# options.add_argument(f'--proxy-server={PROXY}')
# options.add_argument(f"user-agent={my_user_agent}")

# Create Undetected Chromedriver with Proxy
driver = uc.Chrome(options=options)

url = "https://www.leboncoin.fr/f/locations/real_estate_type--2"
# Send Request
driver.get(url)

time.sleep(4)

annonces = driver.find_elements(By.XPATH, "//a[@data-test-id='ad' and @data-qa-id='aditem_container']")

liste_liens = []
# Récupérez les liens des annonces
for lien in annonces:
    lien_annonce = lien.get_attribute('href')
    liste_liens.append(lien_annonce)
    print(lien_annonce)

driver.quit()
