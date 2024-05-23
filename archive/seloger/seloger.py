import undetected_chromedriver as uc
import os
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

""" Test avec Seloger"""
pages = []


## Set Chrome Options
options = uc.ChromeOptions()
# options.headless=True
# options.add_argument('--headless')
# options.add_argument(f'--proxy-server={PROXY}')
# options.add_argument(f"user-agent={my_user_agent}")

## Create Undetected Chromedriver with Proxy
driver = uc.Chrome(options=options)

nb_pages = 2

for num_page in range(1, nb_pages + 1):
    url = "https://www.seloger.com/list.htm?projects=1&types=2%2C1&places=%5B%7B%22inseeCodes%22%3A%5B750056%5D%7D%5D&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&LISTING-LISTpg=1"
    driver.get(url)
    annonces = driver.find_elements(
        By.XPATH, '//a[@data-testid="sl.explore.coveringLink"]'
    )
    liste_liens = []
    for lien in annonces:
        lien_annonce = lien.get_attribute("href")
        liste_liens.append(lien_annonce)
    for url in lien_annonce:
        data = utils.retrieve_data(driver, url)

driver.quit()


url_annonce = liste_liens[7]
driver.get(url_annonce)


try:
    # Utilisez une attente explicite pour attendre que la page accepter les cookies s'affiche
    continuer_sans_accepter_button = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//span[@class='didomi-continue-without-agreeing']")
        )
    )

    # Continue sans accepter les cookies
    continuer_sans_accepter_button[0].click()

    # Wait a bit for the text to fully load after clicking
    time.sleep(2)

except Exception as e:
    print(f"Could not click 'Continuer sans accepter button: {e}")


try:
    voir_tout_button = driver.find_element(
        By.XPATH, "//button[@data-test='show-detail-feature-button-desktop']"
    )
    voir_tout_button.click()
    time.sleep(1)

except Exception as e:
    print(f"Could not click 'Voir toutes les caractéristiques' button: {e}")

# Titre de l'annonce:
titre_annonce = driver.find_elements(
    By.XPATH, '//div[@class="Summarystyled__Title-sc-1u9xobv-4 dbveQQ"]'
)[0].text


# Prix:
prix = driver.find_elements(
    By.XPATH, '//span[@class="global-styles__TextNoWrap-sc-1gbe8ip-6 gxurQr"]'
)[
    1
].text  # à voir si c'est toujours la 2e span


# Autres infos:
# Ordre: Nb pièces, (Nb chambres), Surface, Nb etages, Balcon, Terasse, Jardin, Garage, Ascenceur, Piscine  ?Parking?
autres_infos_WebElement = driver.find_elements(
    By.XPATH, '//div[@class="Tags__TagContainer-sc-edpl7u-0 EPxew"]'
)
autres_infos = [element.text for element in autres_infos_WebElement]

# Quartier:
quartier = driver.find_elements(By.XPATH, '//span[@data-test="neighbourhood"]')[0].text

# Ville + code postal:
ville_cp = driver.find_elements(
    By.XPATH, '//span[@class="Localizationstyled__City-sc-gdkcr2-1 bgtLnh"]'
)[0].text


# Description:
description = driver.find_elements(
    By.XPATH, "//div[@class='ShowMoreText__UITextContainer-sc-1swit84-0 fDeZMv']"
)[0].text

data_dict = {
    "Titre de l'annonce": [titre_annonce],
    "Prix": [prix],
    "Autres Infos": [", ".join(autres_infos)],
    "Quartier": [quartier],
    "Ville et CP": [ville_cp],
    "Description": [description],
}


# Caractéristiques:
# Récupère les blocs de caractéristiques (ex: Extérieur, Cadre et situation...)
blocs_caract = driver.find_elements(
    By.CSS_SELECTOR, "div.TitledDescription__TitledDescriptionContainer-sc-p0zomi-0"
)


for bloc in blocs_caract:
    titre_caract_l = bloc.find_elements(By.CSS_SELECTOR, "div.feature-title")
    if not titre_caract_l:  # Vérifie si titre_caract est vide
        continue
    titre_caract = titre_caract_l[0].text  # Récupère le titre des caractéristiques
    caract_list = bloc.find_elements(
        By.CSS_SELECTOR, "div.GeneralFeaturesstyled__TextWrapper-sc-1ia09m5-3"
    )
    data_dict[titre_caract] = [", ".join([caract.text for caract in caract_list])]


driver.quit()
