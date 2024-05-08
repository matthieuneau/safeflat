import pandas as pd
import os
from langchain_openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json
import re


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat"
    password = "saaj098KLN++"

    proxies = {
        "http": f"http://{username}:{password}@unblock.oxylabs.io:60000",
        "https": f"http://{username}:{password}@unblock.oxylabs.io:60000",
    }

    response = requests.request(
        "GET",
        page_url,
        verify=False,  # Ignore the certificate
        proxies=proxies,
    )

    return response.text


def retrieve_urls(page_url: str) -> list:
    """Retrieve the URLs of the ads from the page

    Args:
        page (str): url of the page listing the ads

    Returns:
        list: list of the URLs of the ads on the page
    """

    html = fetch_html_with_oxylab(page_url)

    soup = BeautifulSoup(html, "html.parser")
    all_a_tags = soup.find_all("a")

    url_list = [
        item["href"]
        for item in all_a_tags
        if item.get("href", "").startswith("/location-vacances/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))
    print(len(url_list))
    print(f"url_list: {url_list}")

def find_matching_items_desc(data, key='__typename', value='PropertyContentItemMarkup', results=None):
    if results is None:
        results = []
    
    if isinstance(data, dict):
        if key in data and data[key] == value:
            # Check further if the content structure matches
            if 'content' in data and isinstance(data['content'], dict):
                content = data['content']
                if content.get('__typename') == 'MarkupText' and 'text' in content and 'markupType' in content:
                    if content['markupType'] == 'HTML':
                        results.append(data)
        # Recurse into the dictionary
        for v in data.values():
            find_matching_items_desc(v, key, value, results)
    elif isinstance(data, list):
        # Recurse into the list
        for item in data:
            find_matching_items_desc(item, key, value, results)

    return results

def extract_texts_desc(data):
    texts = []
    for item in data:
        content = item.get('content', {})
        if 'text' in content:
            texts.append(content['text'])
    return texts


def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    #for test purpose only, local html file:
    file_path = "C:/Users/hennecol/Documents/safeflat/scraping/abritel-oxylab/annonces/annonce2.html"
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # html = fetch_html_with_oxylab(ad_url)
    # soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Retrieving title 
    try:
        title = soup.select_one('h1.uitk-heading.uitk-heading-3[aria-hidden="true"]')
        data["title"] = (
            title.text.strip() if title else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving title: {e}")
        data["title"] = "Not Available"

    # Retrieving price : Price isn't in the html file
    # try:
    #     title = soup.select('.uitk-text.uitk-type-500.uitk-type-medium.uitk-text-emphasis-theme')
    #     data["price"] = (
    #         title.text.strip() if title else "Not Available"
    #     )
    # except Exception as e:
    #     print(f"Error retrieving title: {e}")
    #     data["price"] = "Not Available"
    

    # Retrieving location
    try:
        location = soup.select_one('div.uitk-text.uitk-type-start.uitk-type-300.uitk-text-default-theme[data-stid="content-hotel-address"]')
        data["location"] = location.text.strip() if location else "Not Available"
    except Exception as e:
        print(f"Error retrieving location: {e}")
        data["location"] = "Not Available"

    # Retrieving surface
    try:
        span_tags = soup.find_all('span', class_="uitk-text uitk-text-spacing-three uitk-type-300 uitk-text-standard-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-half_width uitk-layout-flex-item-flex-grow-1")
        # Loop over each tag found to extract relevant text
        for span_tag in span_tags:
            # Text extraction, including all text elements at tag and child level, then deletion of SVG elements
            text_parts = [element for element in span_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if 'm²' in full_text.lower():
                data["surface"] = full_text
            else:
                data["surface"] = None

    except Exception as e:
        print(f"Error retrieving title: {e}")
        data["surface"] = "Not Available"


    # Retrieiving number of bedrooms
    try:
        rooms_tags = soup.find_all('h3', class_="uitk-heading uitk-heading-5")
        extracted_rooms = []   
        for rooms_tag in rooms_tags:
            text_parts = [element for element in rooms_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if "chambre" in full_text.lower():
                extracted_rooms.append(full_text)
        data["nb_bedrooms"] = ", ".join(extracted_rooms)
    except Exception as e:
        print(f"Error retrieving title: {e}")
        data["nb_bedrooms"] = "Not Available"

    # Retrieving number of bathrooms
    try:
        bathrooms_tags = soup.find_all('h3', class_="uitk-heading uitk-heading-5")
        extracted_bathrooms = []   
        for rooms_tag in bathrooms_tags:
            text_parts = [element for element in rooms_tag if isinstance(element, str)]
            full_text = "".join(text_parts).strip()
            if "salle de bain" in full_text.lower():
                extracted_bathrooms.append(full_text)
        data["nb_bathrooms"] = ", ".join(extracted_bathrooms)
    except Exception as e:
        print("Error extracting nb_bathrooms:", e)
        data["nb_bathrooms"] = "Not Available"

    # Retrieving type of bathroom : with a "baignoire" or a "douche"
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
            if "douche" in full_text.lower():
                extracted_douche.append(full_text)
        data["baignoire"] = ", ".join(extracted_baignoire)
        data["douche"] = ", ".join(extracted_douche)
    except Exception as e:
        print("Error extracting bathroom type:", e)
        data["baignoire"] = "Not Available"
        data["douche"] = "Not Available"

    # Retrieving type and number of beds
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
        data["beds"] = ", ".join(extracted_texts)
    except Exception as e:
        print("Error extracting beds:", e)
        data["beds"] = "Not Available"

    # Retrieving other spaces
    try:
        extracted_spaces = []
        h3_tag = soup.find('h3', string="Espaces")
        grid_div = h3_tag.find_next('div', class_="uitk-layout-grid")
        items = grid_div.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
        for item in items:
            extracted_spaces.append(item.text.strip())
        data["other_spaces"] = ", ".join(extracted_spaces)
    except Exception as e:
        print("Error extracting other spaces:", e)
        data["other_spaces"] = "Not Available"

    # Retrieving JSON data:description
    try:
        json_data = {}
        scripts = soup.find_all('script')
        for idx, script in enumerate(scripts):
            results = re.findall(r'JSON\.parse\((.*?)\);', script.string if script.string else '')
            for result in results:
                # Nettoyer la chaîne pour une bonne transformation en JSON
                cleaned_string = json.loads(result)
                json_object = json.loads(cleaned_string)
                
                # Utiliser un index pour éviter les écrasements dans le dictionnaire
                json_data[f'script_{idx}'] = json_object
        try:
            matching_items = find_matching_items_desc(json_data)
            extracted_texts = extract_texts_desc(matching_items)
            data["description"] = extracted_texts
        except Exception as e:
            print("Error extracting description:", e)
            data["description"] = "Not Available"


        # # # Extract data un a JSON file:
        # with open("output.json", 'w', encoding='utf-8') as file:
        #     json.dump(json_data, file, ensure_ascii=False, indent=4)
        
    except Exception as e:
        print("Error extracting JSON:", e)


    # # Retrieving metro stations closeby
    # try:
    #     metro = soup.select(".item-transports")
    #     metro_stations = [item.text.strip() for item in metro]
    #     data["metro_stations"] = metro_stations
    # except Exception as e:
    #     print(f"Error retrieving metro stations: {e}")
    #     data["metro_stations"] = []

    # # Retrieving conditions financieres
    # try:
    #     conditions_financieres = soup.select(".row > .col-1-3")
    #     conditions_financieres = [item.text.strip() for item in conditions_financieres]
    #     data["conditions_financieres"] = conditions_financieres
    # except Exception as e:
    #     print(f"Error retrieving financial conditions: {e}")
    #     data["conditions_financieres"] = []

    # # Retrieving energy and ges
    # try:
    #     energy = soup.select_one(".energy-indice ul li.active")
    #     data["energy"] = energy.text.strip() if energy else "Not Available"
    # except Exception as e:
    #     print(f"Error retrieving energy: {e}")
    #     data["energy"] = "Not Available"

    # # Retrieving ges
    # try:
    #     ges = soup.select_one(".ges-indice ul li.active")
    #     data["ges"] = ges.text.strip() if ges else "Not Available"
    # except Exception as e:
    #     print(f"Error retrieving ges: {e}")
    #     data["ges"] = "Not Available"

    # # Retrieving ref and date
    # try:
    #     ref_date = soup.select_one(".item-date")
    #     data["ref_date"] = ref_date.text.strip() if ref_date else "Not Available"
    # except Exception as e:
    #     print(f"Error retrieving reference and date: {e}")
    #     data["ref_date"] = "Not Available"
    print(data)

    return data


def process_description(description: str) -> dict:
    os.environ["OPENAI_API_KEY"] = "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"
    llm = OpenAI()

    question = f"""Tu es un expert en location immobilière et tu maitrises tout le vocabulaire associe. Tu dois m’aider a extraire des informations pertinentes parmi de longues descriptions de biens immobiliers que je vais te donner.

    Voici la description d'une annonce d'un bien immobilier qui est mis en location sur un site d'annonces. Essaie de relever les informations suivantes dans le texte de cette description:

    - surface: La surface indiquée en m2
    - nb_rooms: Le nombre de pièces
    - piscine: La presence ou non d’une piscine. Renvoie oui si elle est présente, non sinon. Une piscine sera toujours indiquée explicitement dans la description donc si elle n’est pas indiquée, renvoie non
    - type de bien: Le type de bien dont il s’agit. Il peut uniquement s’agir d’un appartement ou d’une maison
    - nb_bedrooms: Le nombre de chambres
    - parking: La presence ou non d’une place de parking privée. Renvoie oui si elle est présente, non sinon
    - quartier: Le nom du quartier ou est situe le bien immobilier
    - meuble: Si le bien est meuble renvoie oui, sinon renvoie non
    - nombre d’etages: Le nombre d’etages du bien
    - numero d’etage: A quel étage se situe le bien s’il s’agit d’un appartement 
    - ascenseur:La presence ou non d’un ascenseur qui permet d’acceder a l’appartement s’il s’agit d’un appartement en immeuble. Renvoie oui s’il y a un ascenseur, non sinon
    - cave: La presence ou non d’une cave. Renvoie oui s’il y a une cave, non sinon
    - terrasse: La presence ou non d’une terrasse. Renvoie oui s’il y en a une, non sinon


    Renvoie un simple dictionnaire qui les contient. N’essaie pas d’inventer ou de deviner des informations. A chaque fois que tu ne trouves pas une information, associe la valeur “N/A” a la clé. Par exemple, si tu n’es pas en mesure de determiner si le bien est meuble ou non, inclu “meuble”: N/A dans le dictionnaire.
    Voici quelques exemples pour t’aider:

    Exemple 1:
    F3 Bien situé dans les hauts de Sainte-Suzanne deux rives proche de toutes commodités. Une cuisine ouverte et deux chambres plus 2 salles de bains et wc en bas et en haut.l’entrée donne directement sur une terrasse sécurisée à l’arrière une autre terrasse donnait directement sur une courette. Cette location meublée d'un montant 1150€mois tout charge inclus de plus il n’y a pas tout à l’égout. L’ axé via un portail électrique donnant dans une cour privée idéal pour seniors cherchant la tranquillité

    Reponse 1:
    {{"surface": "N/A”, "nb_rooms": 3, "piscine": "Non", "type de bien": "N/A", "nb_bedrooms": "N/A", "parking": "N/A", "quartier": "N/A", "meuble": "N/A", "nombre d’etages": "N/A", "numero d’etage": "N/A", "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}}

    Exemple 2:
    - Quartier calme et résidentiel.
    - Portail et entrée individuelle, cuisine semi-équipée, salle de bain avec baignoire et toilettes séparées avec lave-mains.
    - Suite parentale (chambre avec salle d'eau).
    - Appartement au premier étage dans une grande maison.
    - Deux terrasses dans un appartement traversant : possibilité de manger à l'extérieur.
    - Parking individuel.
    - Placards de rangements dans deux chambres et à l'entrée.                                                                                                                                                                               
    - Proximité des écoles : maternelle, élémentaire, collège et lycée.
    - Proximité des transports en commun : lignes de bus 2, 4 et 5 au bout de la rue, RER A gare Sucy-Bonneuil accessible en 10min de bus ou 25min à pied.
    - Commerces et équipements sportifs à proximité.
    - Parc Municipal des Sports de Sucy à moins d'un kilomètre : club de tennis, football, athlétisme, rugby, stade, etc.
    - Conservatoire de musique à proximité.
    - Seule charge : taxe d'ordure ménagère.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              "['Sucy - Bonneuil', 'Boissy-Saint-Léger', 'La Varenne - Chennevières']"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

    Reponse 2:
    {{"surface": "N/A", "nb_rooms": "N/A", "piscine": "Non", "type de bien": "appartement", "nb_bedrooms": "N/A", "parking": "oui", "quartier": "N/A", "meuble": "N/A", "nombre d’etages": "N/A", "numero d’etage": 1, "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}} 


    Repond en renvoyant un dictionnaire sans aucun autres commentaires.

    Voici la description de l'annonce en question: 

    {{ {description} }}
    """

    response = llm.invoke(question)

    return response


def extract_rooms(details):
    for item in details:
        if "pièce" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_bedrooms(details: str):
    for item in details:
        if "chambre" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_surface(details: str):
    for item in details:
        if "m²" in item and "Terrain" not in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_terrain(details: str):
    for item in details:
        if "Terrain" in item:
            # Split the string on spaces and get the first element
            return item.split()[1]
    return "N/A"


def extract_rent_with_bills(conditions_financieres: str):
    for item in conditions_financieres:
        if "charges comprises" in item:
            rent_with_bills = item.split("\n")[1].split()[0].replace(".", "")
            return rent_with_bills
    return "N/A"


def extract_bills(conditions_financieres: str):
    for item in conditions_financieres:
        if "Dont charges" in item:
            bills = item.split("\n")[1].split()[0]
            return bills


def process_outputs(data: pd.DataFrame) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        data (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """
    data["title"] = data["title_and_price"].apply(lambda x: x.split("\t")[0])
    data["price"] = data["title_and_price"].apply(
        lambda x: x.split("\t")[1:][-1]
        .replace("€", "")
        .replace(" ", "")
        .replace(".", "")
    )
    data["nb_rooms"] = data["details"].apply(extract_rooms)
    data["nb_bedrooms"] = data["details"].apply(extract_bedrooms)
    data["surface"] = data["details"].apply(extract_surface)
    data["terrain"] = data["details"].apply(extract_terrain)
    data["rent_with_bills"] = data["conditions_financieres"].apply(
        extract_rent_with_bills
    )
    data["bills"] = data["conditions_financieres"].apply(extract_bills)

    return data


if __name__ == "__main__":
    dict_data = scrape_ad(
        "https://www.pap.fr/annonces/appartement-bures-sur-yvette-91440-r432200988"
    )
    df_data = pd.DataFrame([dict_data])
    result = process_outputs(df_data)
    print(result["energy"])
    print(result["ges"])
