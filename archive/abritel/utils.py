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
import pandas as pd


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

    # for test purpose only, local html file
    #file_path = "/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/abritel/Logement pour 4 pers proche des Buttes Chaumont (12_04_2024 12_29_04).html"
    with open(url, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml') 


    # # Navigate to the URL
    # options = uc.ChromeOptions()
    # driver = uc.Chrome(options=options) 
    # options.add_argument("--incognito")
    # # driver.get(url)
    # # time.sleep(20)
    result = {}

    # # #Creates a BeautifulSoup object to get the source code
    # page_source = driver.page_source
    # soup = BeautifulSoup(page_source, 'html.parser')

    result["url"] = url

    #Extracting the title ok
    try:
        result["title"] = soup.find('h1', class_="uitk-heading uitk-heading-3", attrs={"aria-hidden": "true"}).text.strip()
    except Exception as e:
        print("Error extracting title:", e)
        result["title"] = None

    # Extracting the type of property
    try:
        result["type"] = soup.find_all('span', class_="uitk-text uitk-type-300 uitk-text-default-theme uitk-spacing uitk-spacing-padding-blockstart-two")[0].text.strip()
    except Exception as e:
        print("Error extracting type", e)
        result["type"] = None

    # Extracting the host type
    try:
        result["host_type"] = soup.find_all('span', class_="uitk-text uitk-type-300 uitk-text-standard-theme")[1].text.strip()
    except Exception as e:
        print("Error extracting host type", e)
        result["host_type"] = None

    # Extracting the price ok
    try:
        result["price"] = soup.find('span', attrs={"data-stid": "price-lockup-text"}).text.strip()
    except Exception as e:
        print("Error extracting price:", e)
        result["price"] = None

    # Extracting the City ok
    try:
        result["city"] = soup.find('div', class_="uitk-text uitk-type-300 uitk-text-default-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width", attrs={"data-stid": "content-hotel-address"}).text.strip()
    except Exception as e:
        print("Error extracting City:", e)
        result["city"] = None

    # Extracting the surface ok
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

    # Extracting the number of rooms ok
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


    # Extracting the number of bathrooms ok
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


    # Extracting the type of bathroom : with a "baignoire" or a "douche" ok
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


    # Extracting the type and number of beds ok
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

    # Extracting other spaces ok
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
        

    # Extracting the description ok 
    try:
        desc_tag = soup.find('div', {"data-stid": "content-markup"})
        if desc_tag:
            for br in desc_tag.find_all("br"):
                br.decompose()  # Supprime chaque balise <br> du document
        result["description"] = desc_tag.text.strip()
    except Exception as e:
        print("Error extracting description:", e)
        result["description"] = None

    #Extracting host_name ok:
    try:
        h3_tag = soup.find('h3', string="Responsable de l’hébergement")
        grid_div = h3_tag.find_next('div', class_="uitk-layout-grid")
        name_div = grid_div.find('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item").text.strip()
        result["host_name"] = name_div
    except Exception as e:
        print("Error extracting host_name:", e)
        result["host_name"] = None

    #Extracting gps coordinates ok:
    #h3_tag = soup.find('h3', string="Découvrez la région")

    # driver.quit()

    return result

    
    
    #print(result)
    
