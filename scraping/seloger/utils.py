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
    and attempts to scrape data into a dictionary. It also tries to click a
    'Voir plus' button to reveal more information, if it exists.

    Parameters:
    url (str): The URL to navigate to.
    """


    # Navigate to the URL
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options) 
    driver.get(url)
    result = {}

    #Creates a BeautifulSoup object to get the source code
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')



    # Extracting the title
    try:
        result["title"] = soup.find('div', class_ = "Summarystyled__Title-sc-1u9xobv-4 dbveQQ").text.strip()
    except Exception as e:
        print("Error extracting title:", e)
        result["title"] = "Title Not Found"

    # Extracting the price
    try:
        result["price"] = soup.find('span', class_='global-styles__TextNoWrap-sc-1gbe8ip-6').text.strip()
    except Exception as e:
        print("Error extracting price:", e)
        result["price"] = "Price Not Found"

    # Extracting the City and zip code
    try:
        result["city and zip code"] = soup.find('span', class_='Localizationstyled__City-sc-gdkcr2-1 bgtLnh').text.strip()
    except Exception as e:
        print("Error extracting City and Zip Code:", e)
        result["city and zip code"] = "City and Zip Code Not Found"

    # Extracting the neighbourhood
    try:
        result["neighbourhood"] = span_element = soup.find('span', {'data-test': 'neighbourhood'}).text.strip()
    except Exception as e:
        print("Error extracting Neighbourhood:", e)
        result["neighbourhood"] = "Neighbourhood Not Found"

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
            result["nb_rooms"] = "Nb Rooms Not Found"
        if result["nb_bedrooms"] == "":
            result["nb_bedrooms"] = "Nb Bedrooms Not Found"
        if result["surface"] == "":
            result["surface"] = "Surface Not Found"
        if result["numero_etage"] == "":
            result["numero_etage"] = "Numero d'étage Not Found"

        # result["balcon"] = ""
        # result["terrasse"] = ""
        # result["exposition"] = ""
        # result["ascenceur"] = ""
        # result["gardien"] = ""
        # result["interphone"] = ""
        # result["kitchen_type"] = ""

    # Extracting the description
    try:
        result["description"] = soup.find('div', class_='ShowMoreText__UITextContainer-sc-1swit84-0').text.strip()
    except Exception as e:
        print("Error extracting description:", e)
        result["description"] = "Description Not Found"

    # Extraction of features
        try:
            elements = soup.find_all('div', class_='TitledDescription__TitledDescriptionContainer-sc-p0zomi-0 gtBcDa GeneralFeaturesstyled__GeneralListTitledDescription-sc-1ia09m5-5 jsTjoV')

            # Itérez sur chaque élément pour extraire le titre et le texte
            for element in elements:
                try:
                    titre = element.find('div', class_='feature-title').text.strip()
                    texte = element.find('div', class_='GeneralFeaturesstyled__TextWrapper-sc-1ia09m5-3').text.strip()
                    
                    # Ajoutez le titre et le texte au dictionnaire
                    result[titre] = texte

                except Exception as e:
                    print("Error extracting features:", e)
                    result[titre] = f"{titre} not found"
                
            
        except Exception as e:
            print("Error extracting features:", e)


    #Extracting Diagnostic de performance énergétique (DPE) and Indice d'émission de gaz à effet de serre (GES)
    try : 
        energy_elements = soup.find_all('div', {'data-test': 'diagnostics-content'})
        for element in energy_elements:
            try:
                titre = element.find('div', {'data-test' : 'diagnostics-preview-title'}).text.strip()
                letter = element.find('div', class_ = 'Previewstyled__Grade-sc-k3u73o-6 ehFYCZ').text.strip()

                #Add titre and lettre to the dictionnary
                result[titre] = letter
            except Exception as e:
                    print("Error extracting engergy elements:", e)
                    result[titre] = f"{titre} not found"
            

    except Exception as e:
        print("Error extracting Energy elements:", e)

    #Extracting loyer charges comprises
        
        










    driver.quit()

    with open(output_file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames= result.keys(),
        )
        writer.writeheader()
        writer.writerow(result)