import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from numpy import random
from bs4 import BeautifulSoup
import re



def retrieve_data(url):
    """
    TO BE UPDATED
    Navigates to a given URL and retrieves data using a Selenium WebDriver.

    This function navigates to the specified URL, waits for the page to load,
    and attempts to scrape data into a dictionary.

    Parameters:
    url (str): The URL to navigate to.
    output_file_path : path to the csv where the data is stored
    """

    #for test purpose only, local html file
    # file_path = "/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/abritel/Logement pour 4 pers proche des Buttes Chaumont (12_04_2024 12_29_04).html"
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file, 'lxml') 


    # Navigate to the URL
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options) 
    options.add_argument("--incognito")
    driver.get(url)
    result = {}

    # #Creates a BeautifulSoup object to get the source code
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    result["url"] = url

    #Extracting the title
    try:
        result["title"] = soup.find('h1', class_="uitk-heading uitk-heading-3", attrs={"aria-hidden": "true"}).text.strip()
    except Exception as e:
        print("Error extracting title:", e)
        result["title"] = None

    # Extracting the type of property
    try:
        result["type"] = soup.find_all('span', class_="uitk-text uitk-type-300 uitk-text-standard-theme")[0].text.strip()
    except Exception as e:
        print("Error extracting type", e)
        result["type"] = None

    # Extracting the host type
    try:
        result["host_type"] = soup.find_all('span', class_="uitk-text uitk-type-300 uitk-text-standard-theme")[1].text.strip()
    except Exception as e:
        print("Error extracting host type", e)
        result["host_type"] = None

    # Extracting the price
    try:
        result["price"] = soup.find('span', attrs={"data-stid": "price-lockup-text"}).text.strip()
    except Exception as e:
        print("Error extracting price:", e)
        result["price"] = None

    # Extracting the City
    try:
        result["city"] = soup.find('div', class_="uitk-text uitk-type-300 uitk-text-default-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width", attrs={"data-stid": "content-hotel-address"}).text.strip()
    except Exception as e:
        print("Error extracting City:", e)
        result["city"] = None

    # Extracting the surface
    try:
        span_tags = soup.find_all('span', class_="uitk-text uitk-text-spacing-three uitk-type-300 uitk-text-standard-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-half_width uitk-layout-flex-item-flex-grow-1")
        # Loop over each tag found to extract relevant text
        for span_tag in span_tags:
            # Text extraction, including all text elements at tag and child level, then deletion of SVG elements
            text_parts = [element for element in span_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if 'm²' in full_text.lower():
                result["surface"] = full_text
            else:
                result["surface"] = None

    except Exception as e:
        print("Error extracting surface:", e)
        result["surface"] = None

    # Extracting the number of rooms
    try:
        rooms_tags = soup.find_all('h3', class_="uitk-heading uitk-heading-5")
        extracted_rooms = []   
        for rooms_tag in rooms_tags:
            text_parts = [element for element in rooms_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if "chambre" in full_text.lower():
                extracted_rooms.append(full_text)
        result["nb_rooms"] = ", ".join(extracted_rooms)
    except Exception as e:
        print("Error extracting nb_rooms:", e)
        result["nb_rooms"] = None


    # Extracting the number of bathrooms
    try:
        bathrooms_tags = soup.find_all('h3', class_="uitk-heading uitk-heading-5")
        extracted_bathrooms = []   
        for rooms_tag in bathrooms_tags:
            text_parts = [element for element in rooms_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if "salle de bain" in full_text.lower():
                extracted_bathrooms.append(full_text)
        result["nb_bathrooms"] = ", ".join(extracted_bathrooms)
    except Exception as e:
        print("Error extracting nb_bathrooms:", e)
        result["nb_bathrooms"] = None


    # Extracting the type of bathroom : with a "baignoire" or a "douche"
    try:
        span_tags = soup.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
        # Loop over each tag found to extract relevant text
        extracted_baignoire = []
        extracted_douche = []
        for span_tag in span_tags:
            # Text extraction, including all text elements at tag and child level, then deletion of SVG elements
            text_parts = [element for element in span_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if "baignoire" in full_text.lower():
                extracted_baignoire.append(full_text)
            elif "douche" in full_text.lower():
                extracted_douche.append(full_text)
        result["baignoire"] = ", ".join(extracted_baignoire)
        result["douche"] = ", ".join(extracted_douche)
    except Exception as e:
        print("Error extracting bathroom type:", e)
        result["baignoire"] = None
        result["douche"] = None


    # Extracting the type and number of beds
    try:
        span_tags = soup.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
        # Loop over each tag found to extract relevant text
        extracted_texts = []
        for span_tag in span_tags:
            # Text extraction, including all text elements at tag and child level, then deletion of SVG elements
            text_parts = [element for element in span_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            full_text_lower = full_text.lower()
            if "lit" in full_text_lower or "futon" in full_text_lower:
                extracted_texts.append(full_text)
        result["beds"] = ", ".join(extracted_texts)
    except Exception as e:
        print("Error extracting beds:", e)
        result["beds"] = None

    # Extracting other spaces
    try:
        extracted_spaces = []
        h3_tag = soup.find('h3', string="Espaces")
        grid_div = h3_tag.find_next('div', class_="uitk-layout-grid")
        items = grid_div.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
        for item in items:
            extracted_spaces.append(item.text.strip())
        result["other_spaces"] = ", ".join(extracted_spaces)
    except Exception as e:
        print("Error extracting other spaces:", e)
        result["other_spaces"] = None
        

    # Extracting the description
    try:
        desc_tag = soup.find('div', {"data-stid": "content-markup"})
        if desc_tag:
            for br in desc_tag.find_all("br"):
                br.decompose()  # Supprime chaque balise <br> du document
        result["description"] = desc_tag.text.strip()
    except Exception as e:
        print("Error extracting description:", e)
        result["description"] = None

    #Extracting host_name:
    try:
        h3_tag = soup.find('h3', string="Responsable de l’hébergement")
        grid_div = h3_tag.find_next('div', class_="uitk-layout-grid")
        name_div = grid_div.find('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item").text.strip()
        result["host_name"] = name_div
    except Exception as e:
        print("Error extracting host_name:", e)
        result["host_name"] = None

    #Extracting gps coordinates:
    #h3_tag = soup.find('h3', string="Découvrez la région")

    
    #print(result)

retrieve_data("https://www.abritel.fr/location-vacances/p2222172?dateless=true&x_pwa=1&rfrr=HSR&pwa_ts=1712826156970&referrerUrl=aHR0cHM6Ly93d3cuYWJyaXRlbC5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=true&adults=2&regionId=179898&destination=Paris+%28et+environs%29%2C+France&destType=BOUNDING_BOX&latLong=48.853564%2C2.348095&searchId=ffd95704-a260-4a18-9087-d724cae9e556&privacyTrackingState=CAN_NOT_TRACK&sort=RECOMMENDED&userIntent=&expediaPropertyId=91650429&propertyName=Charmant+chalet+d%27%C3%A9poque+-+1936")