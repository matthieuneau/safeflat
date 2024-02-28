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

    # Attendre que la page soit complètement chargée
    wait = WebDriverWait(driver, 120)  # Attendre jusqu'à 120 secondes maximum
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-section-id='AMENITIES_DEFAULT']")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "c1yo0219")))
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "lrl13de")))


    #Creates a BeautifulSoup object to get the source code
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    result["url"] = url



    # Extracting the title
    try:
        result["title"] = soup.find('h1').text.strip()
    except Exception as e:
        print("Error extracting title:", e)
        result["title"] = "Title Not Found"

    # Extracting the price
    try:
        price_tag = soup.find('span', class_='_tyxjp1')
        if not price_tag:
            price_tag_reduc = soup.find('span', class_='_1y74zjx') #different class if the price is in discounts
            price = price_tag_reduc.get_text(strip=True)

        else:   
            price = price_tag.get_text(strip=True)
        
        result["price"] = price.replace('\xa0', ' ')
    except Exception as e:
        print("Error extracting price:", e)
        result["price"] = "Price Not Found"


    # Extracting details
    
    try:
        div_tags_wrapper = soup.find('ol', class_='lgx66tx')
        caracteristiques = []
        for div_tag_container in div_tags_wrapper.find_all('li'):
            caractere = div_tag_container.get_text(strip=True)
            caractere = caractere.replace('\xa0', ' ')
            caracteristiques.append(caractere)

        result["nb_rooms"] = ""
        result["nb_bedrooms"] = ""
        result["surface"] = ""
        result["numero_etage"] = ""
        result["nb_voyageurs"] = ""
        result["nb_sdb"] = ""

        for text in caracteristiques:
            if 'pièce' in text:
                result["nb_rooms"] = text
            elif 'chambre' in text:
                result["nb_bedrooms"] = text
            elif 'm²' in text:
                result["surface"] = text
            elif 'Étage' in text:
                result["numero_etage"] = text
            elif 'voyageur' in text:
                result["nb_voyageurs"] = text
            elif 'bain' in text:
                result["nb_sdb"] = text

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
        if result["nb_voyageurs"] == "":
            result["nb_voyageurs"] = "Nb Voyageurs Not Found"
        if result["nb_sdb"] == "":
            result["nb_sdb"] = "Nb sdb Not Found"


    # Extracting the description
    try:
        div_tag_desc = soup.find_all('span', class_='lrl13de')
        liste_desc = []
        # Récupérez le texte de la balise
        for element in div_tag_desc:
            texte = element.get_text(strip=True)
            liste_desc.append(texte)
        try:
            result["description"] = liste_desc[1]
            #result["description_quartier"] = liste_desc[8]
        except Exception as e:
            result["description"] = "Description Not Found"
            #result["description_quartier"] = "Description Not Found"
            
    except Exception as e:
        print("Error extracting description:", e)
    

    #Exctracting equipments:
    try:
        liste_equipements = []
        div_tag_equip = soup.find_all('div', class_ = "_19xnuo97")
        for element in div_tag_equip:
            texte = element.get_text(strip = True)
            texte = texte.replace('\xa0', ' ')
            liste_equipements.append(texte)
        texte_equipements = ', '.join(liste_equipements)
        result["equipements"] = texte_equipements

    except Exception as e:
        print("Error extracting price:", e)
        result["equipements"] = "Equipements Not Found"

    #Extracting host name
    try: 
        texte_nom_hote = soup.find('div', class_='t1pxe1a4').get_text(strip=True)
        nom_hote = texte_nom_hote.split(': ')[-1]
        result["host_name"] = nom_hote

    except Exception as e:
        print("Error extracting nom_hote:", e)
        result["host_name"] = "Nom_hote Not Found"

    #Extracting number and type of beds:
    try:
        #Bed without pictures : different classes if there are pictures of the bed or not
        div_lit = soup.find_all('div', class_= '_qivhwv')
        if div_lit: 
            l_lit = []
            for element in div_lit:
                texte = element.get_text(strip = True)
                l_lit.append(texte)
            result["nb_beds"] = ', '.join(l_lit)
        else:
            div_lit_photo = soup.find_all('div', class_= '_19c0q1z')
            l_lit_photo = []
            for element in div_lit_photo:
                texte = element.get_text(strip = True)
                l_lit_photo.append(texte)
            result["nb_beds"] = ', '.join(l_lit_photo)

    except Exception as e:
        print("Error extracting Nb of beds:", e)
        result["host_name"] = "nb_beds Not Found"

    driver.quit()

    with open(output_file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames= result.keys(),
        )
        #writer.writeheader()
        writer.writerow(result)