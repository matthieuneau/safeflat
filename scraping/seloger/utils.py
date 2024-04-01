import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from numpy import random
from bs4 import BeautifulSoup



def retrieve_data(url, output_file_path):
    """
    TO BE UPDATED
    Navigates to a given URL and retrieves data using a Selenium WebDriver.

    This function navigates to the specified URL, waits for the page to load,
    and attempts to scrape data into a dictionary.

    Parameters:
    url (str): The URL to navigate to.
    output_file_path : path to the csv where the data is stored
    """


    # Navigate to the URL
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options) 
    driver.get(url)
    result = {}

    #Creates a BeautifulSoup object to get the source code
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    result["url"] = url

    # Extracting the title
    try:
        result["title"] = soup.find('div', class_ = "Summarystyled__Title-sc-1u9xobv-4 dbveQQ").text.strip()
    except Exception as e:
        print("Error extracting title:", e)
        result["title"] = None

    # Extracting the price
    try:
        result["price"] = soup.find('span', class_='global-styles__TextNoWrap-sc-1gbe8ip-6').text.strip()
    except Exception as e:
        print("Error extracting price:", e)
        result["price"] = None

    # Extracting the City and zip code
    try:
        result["city and zip code"] = soup.find('span', class_='Localizationstyled__City-sc-gdkcr2-1 bgtLnh').text.strip()
    except Exception as e:
        print("Error extracting City and Zip Code:", e)
        result["city and zip code"] = None

    # Extracting the neighbourhood
    try:
        result["neighbourhood"] = soup.find('span', {'data-test': 'neighbourhood'}).text.strip()
    except Exception as e:
        print("Error extracting Neighbourhood:", e)
        result["neighbourhood"] = None

    # Extracting details
    
    try:
        div_tags_wrapper = soup.find('div', class_='Summarystyled__TagsWrapper-sc-1u9xobv-14')
        caracteristiques = []
        for div_tag_container in div_tags_wrapper.find_all('div', class_='Tags__TagContainer-sc-edpl7u-0'):
            caractere = div_tag_container.text.strip()
            caracteristiques.append(caractere)

        result["nb_rooms"] = ""
        result["nb_bedrooms"] = ""
        result["surface"] = ""
        result["numero_etage"] = ""

        for text in caracteristiques:
            if 'pièce' in text:
                result["nb_rooms"] = text
            elif 'chambre' in text:
                result["nb_bedrooms"] = text
            elif 'm²' in text:
                result["surface"] = text
            elif 'Étage' in text:
                result["numero_etage"] = text

    except Exception as e:
        print("Error extracting details:", e)
        if result["nb_rooms"] == "":
            result["nb_rooms"] = None
        if result["nb_bedrooms"] == "":
            result["nb_bedrooms"] = None
        if result["surface"] == "":
            result["surface"] = None
        if result["numero_etage"] == "":
            result["numero_etage"] = None

    # Extracting the description
    try:
        result["description"] = soup.find('div', class_='ShowMoreText__UITextContainer-sc-1swit84-0').text.strip()
    except Exception as e:
        print("Error extracting description:", e)
        result["description"] = None

    # Extraction of features
    try:
        result["Extérieur"] = ""
        result["Cadre et situation"] = ""
        result["Surfaces annexes"] = ""
        result["Services et accessibilité"] = ""
        result["Cuisine"] = ""
        result["Hygiène"] = ""
        result["Pièces à vivre"] = ""

        feature_elements = soup.find_all('div', class_='TitledDescription__TitledDescriptionContainer-sc-p0zomi-0 gtBcDa GeneralFeaturesstyled__GeneralListTitledDescription-sc-1ia09m5-5 jsTjoV')
        
        # Itérez sur chaque élément pour extraire le titre et le texte
        for element in feature_elements:
            texte=[]
            titre = element.find('div', class_='feature-title').text.strip()
            texte_liste = element.find_all('div', class_='GeneralFeaturesstyled__TextWrapper-sc-1ia09m5-3')
            for texte_element in texte_liste:
                texte.append(texte_element.text.strip())

            # Ajoutez le titre et le texte au dictionnaire
            if titre in result:
                result[titre] = ", ".join(texte)
            else :
                print(f"La colonne {titre} n'est pas dans result")
            
    except Exception as e:
        print("Error extracting features:", e)


    #Extracting Diagnostic de performance énergétique (DPE) and Indice d'émission de gaz à effet de serre (GES)
    try : 
        result["Diagnostic de performance énergétique (DPE)"] = ""
        result["Indice d'émission de gaz à effet de serre (GES)"] = ""
        energy_elements = soup.find_all('div', {'data-test': 'diagnostics-content'})
        for element in energy_elements:
            try:
                titre = element.find('div', {'data-test' : 'diagnostics-preview-title'}).text.strip()
                letter = element.find('div', class_ = 'Previewstyled__Grade-sc-k3u73o-6 ehFYCZ').text.strip()
                if titre == "Diagnostic de performance énergétique (DPE)":
                    result["Diagnostic de performance énergétique (DPE)"] = letter
                elif titre == "Indice d'émission de gaz à effet de serre (GES)":
                    result["Indice d'émission de gaz à effet de serre (GES)"] = letter
                    
            except Exception as e:
                    print("Error extracting energy elements:", e)
                    result[titre] = None
    except Exception as e:
        print("Error extracting Energy elements:", e)

    #Extracting charges, loyer de base, loyer charges comprises : 
        
    try:
        result["loyer_base"] = ""
        result["charges_forfaitaires"] = ""
        result["complement_loyer"] = ""
        result["depot_garantie"] = ""
        result["loyer_charges_comprises"] = ""

        price_details = soup.find('span', {'data-test': 'price-detail-content'})
        try:
            result["loyer_base"] = soup.find(text="Loyer de base (hors charge)").find_next(class_="value").text.strip()
        except Exception as e:
            print("Error extracting loyer_base:", e)
        
        try:
            result["charges_forfaitaires"] = soup.find(text="Charges forfaitaires").find_next(class_="value").text.strip()
        except Exception as e:
            print("Error extracting charges_forfaitaires:", e)
        
        try:
            result["complement_loyer"] = soup.find(text="Complément de loyer").find_next(class_="value").text.strip()
        except Exception as e:
            print("Error extracting complément_loyer:", e)
        
        try:
            result["depot_garantie"] = soup.find(text="Dépôt de garantie").find_next(class_="value").text.strip()
        except Exception as e:
            print("Error extracting depot_garantie:", e)
        
        try:
            result["loyer_charges_comprises"] = soup.find(text="Loyer charges comprises").find_next(class_="big").text.strip()
        except Exception as e:
            print("Error extracting :", e)
        
        
    except Exception as e:
        print("Error extracting price_details:", e)

    driver.quit()

    return result

    # with open(output_file_path, "a", newline="", encoding="utf-8") as file:
    #     writer = csv.DictWriter(
    #         file,
    #         fieldnames= result.keys(),
    #     )
    #     #writer.writeheader()
    #     writer.writerow(result)