from sqlalchemy import create_engine
import ast
import pandas as pd
import os
from langchain_openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat3"
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
    
    # Add prefix and editing to have the correct URL
    url_list = [f"https://www.leboncoin.fr{url}" for url in url_list]
    print("urls retrieved: ", url_list)
    return url_list



def find_index(dictionaries, search_key):
    """ Recherche l'indice du dictionnaire dont la valeur pour la clé 'key' est égale à `search_key`. """
    for index, dictionary in enumerate(dictionaries):
        if dictionary.get('key') == search_key:
            return index
    return None


def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    # #for test purpose only, local html file:
    # file_path = "C:/Users/hennecol/Documents/safeflat/scraping/leboncoin-oxylab/annonces/annonce1.html"
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file, 'lxml')

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # # Retrieving JSON data:
    try:
        json_data = {}  # Dictionary to store parsed JSON data

        # Find the specific script tag by ID
        script_tag = soup.find('script', id="__NEXT_DATA__")

        if script_tag and script_tag.string:
            # Parse the JSON content directly from the script tag
            json_object = json.loads(script_tag.string.strip())
            json_data = json_object  # Store it in the dictionary
        
        if json_data:
            ad = json_data['props']['pageProps']['ad']


        # Retrieving url:
        try:
            data["url"] = ad_url
        except Exception as e:
            print("Error retrieving url:", e)
            data["url"] = "Not Available"

        # Retrieving title: 
        try:
            data["titre"] = ad["subject"]
        except Exception as e:
            print("Error retrieving titre:", e)
            data["titre"] = "Not Available"
        
        # Retrieving first publication date:
        try:
            data["first_publication_date"] = ad["first_publication_date"]
        except Exception as e:
            print("Error retrieving first_publication_date:", e)
            data["first_publication_date"] = "Not Available"

        # Retrieving description:
        try:
            data["description"] = ad["body"]
        except Exception as e:
            print("Error retrieving description:", e)
            data["description"] = "Not Available"

        # Retrieving price:
        try:
            data["prix"] = ad["price"][0]
        except Exception as e:
            print("Error retrieving prix:", e)
            data["prix"] = "Not Available"

        # Retrieving property_type:
        try:
            data["type_de_bien"] = ad["attributes"][find_index(ad["attributes"],"real_estate_type")]["value_label"]
        except Exception as e:
            print("Error retrieving type_de_bien:", e)
            data["type_de_bien"] = "Not Available"
        
        # Retrieving furnished or not: 1 if yes 0 if no
        try:
            data["meuble"] = ad["attributes"][find_index(ad["attributes"],"furnished")]["value"]
        except Exception as e:
            print("Error retrieving meuble:", e)
            data["meuble"] = "Not Available"

        # Retrieving surface:
        try:
            data["surface"] = ad["attributes"][find_index(ad["attributes"],"square")]["value"]
        except Exception as e:
            print("Error retrieving surface:", e)
            data["surface"] = "Not Available"

        # Retrieving nb of rooms:
        try:
            data["nb_rooms"] = ad["attributes"][find_index(ad["attributes"],"rooms")]["value"]
        except Exception as e:
            print("Error retrieving nb_rooms:", e)
            data["nb_rooms"] = "Not Available"
        
        # Retrieving energy rate:
        try:
            data["DPE"] = ad["attributes"][find_index(ad["attributes"],"energy_rate")]["value"]
        except Exception as e:
            print("Error retrieving DPE:", e)
            data["DPE"] = "Not Available"

        # Retrieving GES:
        try:
            data["GES"] = ad["attributes"][find_index(ad["attributes"],"ges")]["value"]
        except Exception as e:
            print("Error retrieving GES:", e)
            data["GES"] = "Not Available"

        # Retrieving elevator:
        try:
            data["ascenseur"] = ad["attributes"][find_index(ad["attributes"],"elevator")]["value_label"]
        except Exception as e:
            print("Error retrieving ascenseur:", e)
            data["ascenseur"] = "Not Available"

        # Retrieving floor number:
        try:
            data["etage"] = ad["attributes"][find_index(ad["attributes"],"floor_number")]["value"]
        except Exception as e:
            print("Error retrieving etage:", e)
            data["etage"] = "Not Available"

        # Retrieving nb of floors in the building:
        try:
            data["nb_etages"] = ad["attributes"][find_index(ad["attributes"],"nb_floors_building")]["value"]
        except Exception as e:
            print("Error retrieving nb_etages:", e)
            data["nb_etages"] = "Not Available"

        # Retrieving monthly charges:
        try:
            data["charges"] = ad["attributes"][find_index(ad["attributes"],"monthly_charges")]["value"]
        except Exception as e:
            print("Error retrieving charges:", e)
            data["charges"] = "Not Available"

        # Retrieving security deposit:
        try:
            data["caution"] = ad["attributes"][find_index(ad["attributes"],"security_deposit")]["value"] 
        except Exception as e:
            print("Error retrieving caution:", e)
            data["caution"] = "Not Available"

        # Retrieving region:
        try:
            data["region"] = ad["location"]["region_name"]
        except Exception as e:
            print("Error retrieving region:", e)
            data["region"] = "Not Available"

        # Retrieving department:
        try:
            data["departement"] = ad["location"]["department_name"]
        except Exception as e:
            print("Error retrieving departement:", e)
            data["departement"] = "Not Available"

        # Retrieving city:
        try:
            data["ville"] = ad["location"]["city"]
        except Exception as e:
            print("Error retrieving ville:", e)
            data["ville"] = "Not Available"

        # Retrieving zipcode:
        try:
            data["zipcode"] = ad["location"]["zipcode"]
        except Exception as e:
            print("Error retrieving zipcode:", e)
            data["zipcode"] = "Not Available"

        # Retrieving latitude:
        try:
            data["latitude"] = ad["location"]["lat"]
        except Exception as e:
            print("Error retrieving latitude:", e)
            data["latitude"] = "Not Available"

        # Retrieving longitude:
        try:
            data["longitude"] = ad["location"]["lng"]
        except Exception as e:
            print("Error retrieving longitude:", e)
            data["longitude"] = "Not Available"
        
        # Retrieving host_name:
        try:
            data["host_name"] = ad["owner"]["name"]
        except Exception as e:
            print("Error retrieving host_name:", e)
            data["host_name"] = "Not Available"
        
        
        # For test purpose only: store locally the json file
        # with open("/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/annonces/output.json", 'w') as json_file:
        #     json.dump(json_data, json_file, indent=4)


    except Exception as e:
        print("Error extracting JSON data:", e)

    data = pd.DataFrame([data])

    return data


def process_description(description: str) -> pd.DataFrame:
    os.environ["OPENAI_API_KEY"] = "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"
    llm = OpenAI(model="gpt-3.5-turbo-instruct")

    prompt = f"""Tu es un expert en location immobilière et tu maîtrises tout le vocabulaire associé. Tu dois m'aider à extraire des informations pertinentes parmi de longues descriptions de biens immobiliers que je vais te donner.

    Voici la description d'une annonce d'un bien immobilier qui est mis en location sur un site d'annonces. Essaie de relever les informations suivantes dans le texte de cette description:

    - surface: La surface indiquée en m2
    - nb_rooms: Le nombre de pièces
    - piscine: La présence ou non d'une piscine. Renvoie oui si elle est présente, non sinon. Une piscine sera toujours indiquée explicitement dans la description donc si elle n’est pas indiquée, renvoie non
    - type_de_bien: Le type de bien dont il s'agit. Il peut uniquement s'agir d'un appartement ou d'une maison
    - nb_bedrooms: Le nombre de chambres
    - parking: La présence ou non d'une place de parking privée. Renvoie oui si elle est présente, non sinon
    - quartier: Le nom du quartier où est situé le bien immobilier
    - meuble: Si le bien est meublé renvoie oui, sinon renvoie non
    - nb_etages: Le nombre d'étages du bien
    - etage: À quel étage se situe le bien s'il s'agit d'un appartement
    - ascenseur: La présence ou non d'un ascenseur qui permet d'accéder à l'appartement s'il s'agit d'un appartement en immeuble. Renvoie oui s'il y a un ascenseur, non sinon
    - cave: La présence ou non d'une cave. Renvoie oui s'il y a une cave, non sinon
    - terrasse: La présence ou non d'une terrasse. Renvoie oui s'il y en a une, non sinon


    Renvoie un simple dictionnaire qui les contient. N'essaie pas d'inventer ou de deviner des informations. À chaque fois que tu ne trouves pas une information, associe la valeur 'N/A' à la clé. Par exemple, si tu n'es pas en mesure de déterminer si le bien est meublé ou non, inclus 'meuble': 'N/A' dans le dictionnaire.
    Voici quelques exemples pour t'aider:

    Exemple 1:
    F3 Bien situé dans les hauts de Sainte-Suzanne deux rives proche de toutes commodités. Une cuisine ouverte et deux chambres plus 2 salles de bains et wc en bas et en haut.l'entrée donne directement sur une terrasse sécurisée à l'arrière une autre terrasse donnait directement sur une courette. Cette location meublée d'un montant 1150€mois tout charge inclus de plus il n'y a pas tout à l'égout. L'axé via un portail électrique donnant dans une cour privée idéal pour seniors cherchant la tranquillité

    Réponse 1:
    {{"surface": "N/A", "nb_rooms": 3, "piscine": "Non", "type_de_bien": "N/A", "nb_bedrooms": "N/A", "parking": "N/A", "quartier": "N/A", "meuble": "N/A", "nb_etages": "N/A", "etage": "N/A", "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}}

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
    - Seule charge : taxe d'ordure ménagère.

    Réponse 2:
    {{"surface": "N/A", "nb_rooms": "N/A", "piscine": "Non", "type_de_bien": "appartement", "nb_bedrooms": "N/A", "parking": "oui", "quartier": "N/A", "meuble": "N/A", "nb_etages": "N/A", "etage": 1, "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}} 

    Répond en renvoyant un dictionnaire sans aucun autres commentaires.

    Voici la description de l'annonce en question: 

    {{ {description} }}
"""

    response = llm.invoke(prompt)

    refining_prompt = f"""This is a python string that is meant to be converted to a dictionary. Make sure that it has the right 
    syntax and can be converted to a dictionary. Here is the string:
    {response}
    Also, make sure that the output has the same keys as this example and if there are any typos in the keys, correct them.
    {{"surface": "N/A", "nb_rooms": "N/A", "piscine": "Non", "type_de_bien": "appartement", "nb_bedrooms": "N/A", "parking": "oui", "quartier": "N/A", "meuble": "N/A", "nb_etages": "N/A", "etage": 1, "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}} 
    Answer only with the corrected output without adding any comments.
    """
    response = llm.invoke(refining_prompt)
    response = ast.literal_eval(response)
    response = pd.DataFrame([response])

    return response


def add_desc_content_to_df(
    processed_desc: pd.DataFrame, processed_ad: pd.DataFrame
) -> pd.DataFrame:
    """Merges all the information from the processed description and the processed ad with one simple rule:
    Consider that the data from the ad is more reliable than the data from the description. So if there is
    a conflict between the two, keep the data from the ad.

    Args:
        processed_desc (pd.DataFrame): processed description data
        processed_ad (pd.DataFrame): processed ad data

    Returns:
        pd.DataFrame: merged data
    """
    for col in processed_desc.columns:
        if col not in processed_ad.columns:
            processed_ad[col] = processed_desc[col]

    return processed_ad



if __name__ == "__main__":
    dict_data = scrape_ad(
        "https://www.leboncoin.fr/ad/locations/2490728497"
    )
    df_data = pd.DataFrame([dict_data])
    df_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output.csv')