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
        if item.get("href", "").startswith("/ad/locations/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))
    print(len(url_list))
    print(f"url_list: {url_list}")


def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    #for test purpose only, local html file:
    file_path = "/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/annonces/annonce1.html"
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # html = fetch_html_with_oxylab(ad_url)
    # soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Retrieving title 
    try:
        data["title"] = soup.select_one("#grid > article > div:nth-child(2) > div > h1").text.strip()
    except Exception as e:
        print("Error retrieving title:", e)
        data["title"] = "Not Available"

    #Retrieving specs: nb rooms, surface, localisation
    try:
        data["nb_rooms"] = "Not Available"
        data["surface"] = "Not Available"
        data["city_zipcode"] = "Not Available"
        spans_specs = soup.select('p.inline-flex > *')
        specs_list = [span.get_text(strip=True).lower() for span in spans_specs]
        for element in specs_list:
            if 'pièce' in element:
                data["nb_rooms"] = element
            elif 'm²' in element:
                data['surface'] = element
            elif any(char.isdigit() for char in element):  # Checks if there's any digit, assuming zipcode includes numbers
                data["city_zipcode"] = element
    except Exception as e:
        print("Error retrieving title:", e)

    # Retrieving price : Price isn't in the html file
    try:
        data["price"] = soup.select_one("#grid > article > div:nth-child(2) > div > div.flex.flex-wrap > div.mr-md.flex.flex-wrap.items-center.justify-between > div > p").text.strip()
    except Exception as e:
        print("Error extracting price:", e)
        data["price"] = "Not Available"


    # # Extracting description
    try:
        data["description"] = soup.select_one("#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-1 > div > p").text.strip()
    except Exception as e:
        print("Error extracting description:", e)
        data["description"] = "Not Available"


    # # Retrieving JSON data:
    try:
        json_data = {}  # Dictionary to store parsed JSON data

        # Find the specific script tag by ID
        script_tag = soup.find('script', id="__NEXT_DATA__")

        if script_tag and script_tag.string:
            # Parse the JSON content directly from the script tag
            json_object = json.loads(script_tag.string.strip())
            json_data = json_object  # Store it in the dictionary
        
        # For test purpose only: store locally the json file
        # with open("/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/annonces/output.json", 'w') as json_file:
        #     json.dump(json_data, json_file, indent=4)


    except Exception as e:
        print("Error extracting JSON data:", e)

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
