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

def find_matching_items_host_name(data, key='__typename', value='PropertyContentItemText', results=None):
    if results is None:
        results = []
    
    if isinstance(data, dict):
        if key in data and data[key] == value:
            # Check further if the content structure matches
            if 'content' in data and isinstance(data['content'], dict):
                content = data['content']
                if (content.get('__typename') == 'PropertyContentText' and 
                    'primary' in content and isinstance(content['primary'], dict)):
                    primary = content['primary']
                    if (primary.get('__typename') == 'LodgingEnrichedMessage' and 
                        'value' in primary and primary.get('value') == "Tam"):
                        # Check all optional keys
                        if all(k in primary and primary[k] is None for k in ['icon', 'egdsMark', 'state', 'subtexts']):
                            if content.get('secondary') is None and data.get('expando') is None:
                                results.append(data)
        # Recurse into the dictionary
        for v in data.values():
            find_matching_items_host_name(v, key, value, results)
    elif isinstance(data, list):
        # Recurse into the list
        for item in data:
            find_matching_items_host_name(item, key, value, results)

    return results

def extract_text_host_name(data, key='value'):
    values = []
    for item in data:
        content = item.get('content', {})
        primary = content.get('primary', {})
        if key in primary:
            values.append(primary[key])
    return values

def find_location_with_coordinates(data, results=None):
    if results is None:
        results = []
    
    if isinstance(data, dict):
        if "location" in data and isinstance(data["location"], dict):
            # Check if "coordinates" is within "location"
            if "coordinates" in data["location"] and isinstance(data["location"]["coordinates"], dict):
                coords = data["location"]["coordinates"]
                # Validate the presence of expected keys within "coordinates"
                if coords.get('__typename') == 'Coordinates' and 'latitude' in coords and 'longitude' in coords:
                    results.append(coords)
        # Recursively process dictionary values
        for value in data.values():
            find_location_with_coordinates(value, results)
    elif isinstance(data, list):
        # Recursively process list elements
        for item in data:
            find_location_with_coordinates(item, results)

    return results

def find_type_host_type(data, results=None):
    if results is None:
        results = []
    
    if isinstance(data, dict):
        # Recursively process dictionary values
        for key, value in data.items():
            if key == "featuredMessages" and isinstance(value, list):
                # Check all items in the list to match the expected structure
                if all(isinstance(item, dict) and item.get('__typename') == 'EGDSPlainText' and 'text' in item for item in value):
                    results.extend(value)  # Using extend instead of append to flatten the list
            find_type_host_type(value, results)
    elif isinstance(data, list):
        # Recursively process list elements
        for item in data:
            find_type_host_type(item, results)

    return results

def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    # #for test purpose only, local html file:
    # file_path = "C:/Users/hennecol/Documents/safeflat/scraping/abritel-oxylab/annonces/annonce1.html"
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file, 'lxml')

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Retrieving title 
    data["title"] = "Not Available"
    try:
        title = soup.select_one('h1.uitk-heading.uitk-heading-3[aria-hidden="true"]')
        data["title"] = (
            title.text.strip() if title else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving title: {e}")

    # Retrieving price : Price isn't in the html file

    # Retrieving location
    data["location"] = "Not Available"
    try:
        location = soup.select_one('div.uitk-text.uitk-type-start.uitk-type-300.uitk-text-default-theme[data-stid="content-hotel-address"]')
        data["location"] = location.text.strip() if location else "Not Available"
    except Exception as e:
        print(f"Error retrieving location: {e}")


    # Retrieving local interests
    data["local_interests"] = "Not Available"
    try:
        local_interests = soup.select('ul.uitk-typelist li')
        local_interests_list = []
        for li in local_interests:
            span_texts = [span.text.strip() for span in li.select('span.uitk-layout-flex-item')]
            local_interests_list.append(span_texts)
        data["local_interests"] = local_interests_list
    except Exception as e:
        print(f"Error retrieving local interests: {e}")
        

    # Retrieving surface
    data["surface"] = "Not Available"
    try:
        span_tags = soup.find_all('span', class_="uitk-text uitk-text-spacing-three uitk-type-300 uitk-text-standard-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-half_width uitk-layout-flex-item-flex-grow-1")
        for span_tag in span_tags:
            full_text = span_tag.text.strip()
            if 'm²' in full_text.lower():
                data["surface"] = full_text
                break  # Once we find the surface, break the loop to avoid overwriting with "Not Available"
    except Exception as e:
        print(f"Error retrieving surface: {e}")


    # Retrieiving number of bedrooms
    try:
        rooms_tags = soup.find_all('h3', class_="uitk-heading uitk-heading-5")
        extracted_rooms = []   
        for rooms_tag in rooms_tags:
            full_text = rooms_tag.text.strip()
            if "chambre" in full_text.lower():
                extracted_rooms.append(full_text)
        data["nb_bedrooms"] = ", ".join(extracted_rooms) if extracted_rooms else "Not Available"
    except Exception as e:
        print(f"Error retrieving bedrooms: {e}")
        data["nb_bedrooms"] = "Not Available"

    # Retrieving number of bathrooms
    try:
        bathrooms_tags = soup.find_all('h3', class_="uitk-heading uitk-heading-5")
        extracted_bathrooms = []   
        for bathroom_tag in bathrooms_tags:
            # Use .text to directly access all text content inside the tag, including nested tags
            full_text = bathroom_tag.text.strip()
            if "salle de bain" in full_text.lower():
                extracted_bathrooms.append(full_text)
        # Set "nb_bathrooms" to the concatenated string of bathroom descriptions or "Not Available" if none found
        data["nb_bathrooms"] = ", ".join(extracted_bathrooms) if extracted_bathrooms else "Not Available"
    except Exception as e:
        print("Error extracting nb_bathrooms:", e)
        data["nb_bathrooms"] = "Not Available"

    # Retrieving type of bathroom : with a "baignoire" or a "douche"
    try:
        div_tags = soup.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
        extracted_baignoire = []
        extracted_douche = []

        for div_tag in div_tags:
            # Directly use .text to get all text inside the tag, properly handling nested elements
            full_text = div_tag.text.strip()
            if "baignoire" in full_text.lower():
                extracted_baignoire.append(full_text)
            if "douche" in full_text.lower():
                extracted_douche.append(full_text)

        # Set values in data dictionary, checking if any results were found
        data["baignoire"] = ", ".join(extracted_baignoire) if extracted_baignoire else "Not Available"
        data["douche"] = ", ".join(extracted_douche) if extracted_douche else "Not Available"

    except Exception as e:
        print("Error extracting bathroom type:", e)
        data["baignoire"] = "Not Available"
        data["douche"] = "Not Available"

    # Retrieving type and number of beds
    try:
        div_tags = soup.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
        extracted_texts = []

        for div_tag in div_tags:
            # Directly use .text to get all text inside the tag, including nested elements
            full_text = div_tag.text.strip()
            full_text_lower = full_text.lower()
            if "lit" in full_text_lower or "futon" in full_text_lower:
                extracted_texts.append(full_text)

        data["beds"] = ", ".join(extracted_texts) if extracted_texts else "Not Available"

    except Exception as e:
        print("Error extracting beds:", e)
        data["beds"] = "Not Available"

    # Retrieving other spaces
    try:
        extracted_spaces = []
        # Find the first 'h3' tag with text "Espaces"
        h3_tag = soup.find('h3', string="Espaces")
        
        if h3_tag:  # Ensure the 'h3' tag was found
            # Find the next 'div' with class "uitk-layout-grid" following the 'h3' tag
            grid_div = h3_tag.find_next('div', class_="uitk-layout-grid")
            
            if grid_div:  # Ensure the grid 'div' was found
                # Find all 'div' tags with specific classes within the grid
                items = grid_div.find_all('div', class_="uitk-text uitk-type-300 uitk-type-regular uitk-text-standard-theme uitk-layout-flex-item")
                
                for item in items:
                    # Extract and strip text from each item and add it to the list
                    extracted_spaces.append(item.text.strip())
            
            else:
                print("Grid 'div' not found after 'h3'")
        else:
            print("'h3' tag with string 'Espaces' not found")

        # Join all extracted spaces into a string, or use "Not Available" if no spaces were found
        data["other_spaces"] = ", ".join(extracted_spaces) if extracted_spaces else "Not Available"

    except Exception as e:
        print("Error extracting other spaces:", e)
        data["other_spaces"] = "Not Available"

    # Retrieving JSON data:description, host name, coordinates, host type, type
    try:
        json_data = {}
        scripts = soup.find_all('script')
        for idx, script in enumerate(scripts):
            results = re.findall(r'JSON\.parse\((.*?)\);', script.string if script.string else '')
            for result in results:
                # Clean the string for proper transformation to JSON
                cleaned_string = json.loads(result)
                json_object = json.loads(cleaned_string)
                
                # Use an index to avoid overwriting in the dictionary
                json_data[f'script_{idx}'] = json_object

        # Extract description
        try:
            matching_desc = find_matching_items_desc(json_data)
            extracted_desc = extract_texts_desc(matching_desc)
            data["description"] = extracted_desc
        except Exception as e:
            print("Error extracting description:", e)
            data["description"] = "Not Available"
        
        # Extract host name
        try:
            matching_host_name = find_matching_items_host_name(json_data)
            extracted_host_name = extract_text_host_name(matching_host_name)[0]
            data["host_name"] = extracted_host_name
        except Exception as e:
            print("Error extracting host_name:", e)
            data["host_name"] = "Not Available"

        # Extract coordinates
        try:
            matching_coordinates = find_location_with_coordinates(json_data)
            data["latitude"] = matching_coordinates[0]['latitude']
            data["longitude"] = matching_coordinates[0]['longitude']
        except Exception as e:
            print("Error extracting coordinates:", e)
            data["latitude"] = "Not Available"
            data["longitude"] = "Not Available"

        # Extract type and host_type
        try:
            matching_type = find_type_host_type(json_data)
            data["type"] = matching_type[0]['text']
            data["host_type"] = matching_type[1]['text']
        except Exception as e:
            print("Error extracting coordinates:", e)
            data["type"] = "Not Available"
            data["host_type"] = "Not Available"
        
    except Exception as e:
        print("Error extracting JSON:", e)

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
