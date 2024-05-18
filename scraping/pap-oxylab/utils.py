from sqlalchemy import create_engine
import ast
import pandas as pd
import os
from langchain_openai import OpenAI
import requests
from bs4 import BeautifulSoup


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat2"
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
        if item.get("href", "").startswith("/annonces/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))
    # Add prefix and editing to have the correct URL
    url_list = [f"https://www.pap.fr{url}" for url in url_list]
    print("urls retrieved: ", url_list)
    return url_list


def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    data["url"] = ad_url

    # Retrieving title and price
    try:
        title_and_price = soup.select_one("h1.item-title")
        data["title_and_price"] = (
            title_and_price.text.strip() if title_and_price else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving title and price: {e}")
        data["title_and_price"] = "Not Available"

    # Retrieving location
    try:
        location = soup.select_one(".item-description.margin-bottom-30 > h2")
        data["location"] = location.text.strip() if location else "Not Available"
    except Exception as e:
        print(f"Error retrieving location: {e}")
        data["location"] = "Not Available"

    # Retrieving nb of rooms, surface and nb of bedrooms when available
    try:
        list_items = soup.select("ul.item-tags.margin-bottom-20 > li")
        details = [
            item.find("strong").text.strip()
            for item in list_items
            if item.find("strong")
        ]
        data["details"] = details
    except Exception as e:
        print(f"Error retrieving details: {e}")
        data["details"] = []

    # Retrieving description
    try:
        description = soup.select_one("div.margin-bottom-30 > p")
        data["description"] = (
            description.text.strip() if description else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving description: {e}")
        data["description"] = "Not Available"

    # # Retrieving metro stations closeby
    # try:
    #     metro = soup.select(".item-transports")
    #     metro_stations = [item.text.strip() for item in metro]
    #     data["metro_stations"] = metro_stations
    # except Exception as e:
    #     print(f"Error retrieving metro stations: {e}")
    #     data["metro_stations"] = []

    # Retrieving conditions financieres
    try:
        conditions_financieres = soup.select(".row > .col-1-3")
        conditions_financieres = [item.text.strip() for item in conditions_financieres]
        data["conditions_financieres"] = conditions_financieres
    except Exception as e:
        print(f"Error retrieving financial conditions: {e}")
        data["conditions_financieres"] = []

    # Retrieving energy and ges
    try:
        energy = soup.select_one(".energy-indice ul li.active")
        data["energy"] = energy.text.strip() if energy else "Not Available"
    except Exception as e:
        print(f"Error retrieving energy: {e}")
        data["energy"] = "Not Available"

    # Retrieving ges
    try:
        ges = soup.select_one(".ges-indice ul li.active")
        data["ges"] = ges.text.strip() if ges else "Not Available"
    except Exception as e:
        print(f"Error retrieving ges: {e}")
        data["ges"] = "Not Available"

    # Retrieving ref and date
    try:
        ref_date = soup.select_one(".item-date")
        data["ref_date"] = ref_date.text.strip() if ref_date else "Not Available"
    except Exception as e:
        print(f"Error retrieving reference and date: {e}")
        data["ref_date"] = "Not Available"
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
    - nombre_d'etages: Le nombre d'étages du bien
    - numero_d'etage: À quel étage se situe le bien s'il s'agit d'un appartement
    - ascenseur: La présence ou non d'un ascenseur qui permet d'accéder à l'appartement s'il s'agit d'un appartement en immeuble. Renvoie oui s'il y a un ascenseur, non sinon
    - cave: La présence ou non d'une cave. Renvoie oui s'il y a une cave, non sinon
    - terrasse: La présence ou non d'une terrasse. Renvoie oui s'il y en a une, non sinon


    Renvoie un simple dictionnaire qui les contient. N'essaie pas d'inventer ou de deviner des informations. À chaque fois que tu ne trouves pas une information, associe la valeur 'N/A' à la clé. Par exemple, si tu n'es pas en mesure de déterminer si le bien est meublé ou non, inclus 'meuble': 'N/A' dans le dictionnaire.
    Voici quelques exemples pour t'aider:

    Exemple 1:
    F3 Bien situé dans les hauts de Sainte-Suzanne deux rives proche de toutes commodités. Une cuisine ouverte et deux chambres plus 2 salles de bains et wc en bas et en haut.l'entrée donne directement sur une terrasse sécurisée à l'arrière une autre terrasse donnait directement sur une courette. Cette location meublée d'un montant 1150€mois tout charge inclus de plus il n'y a pas tout à l'égout. L'axé via un portail électrique donnant dans une cour privée idéal pour seniors cherchant la tranquillité

    Réponse 1:
    {{"surface": "N/A", "nb_rooms": 3, "piscine": "Non", "type_de_bien": "N/A", "nb_bedrooms": "N/A", "parking": "N/A", "quartier": "N/A", "meuble": "N/A", "nombre_d'etages": "N/A", "numero_d'etage": "N/A", "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}}

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
    {{"surface": "N/A", "nb_rooms": "N/A", "piscine": "Non", "type_de_bien": "appartement", "nb_bedrooms": "N/A", "parking": "oui", "quartier": "N/A", "meuble": "N/A", "nombre_d'etages": "N/A", "numero_d'etage": 1, "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}} 

    Répond en renvoyant un dictionnaire sans aucun autres commentaires.

    Voici la description de l'annonce en question: 

    {{ {description} }}
"""

    response = llm.invoke(prompt)

    refining_prompt = f"""This is a python string that is meant to be converted to a dictionary. Make sure that it has the right 
    syntax and can be converted to a dictionary. Here is the string:
    {response}
    Also, make sure that the output has the same keys as this example and if there are any typos in the keys, correct them.
    {{"surface": "N/A", "nb_rooms": "N/A", "piscine": "Non", "type_de_bien": "appartement", "nb_bedrooms": "N/A", "parking": "oui", "quartier": "N/A", "meuble": "N/A", "nombre_d'etages": "N/A", "numero_d'etage": 1, "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}} 
    Answer only with the corrected output without adding any comments.
    """
    response = llm.invoke(refining_prompt)
    response = ast.literal_eval(response)
    response = pd.DataFrame([response])

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

    data.drop(
        ["title_and_price", "details", "conditions_financieres"], axis=1, inplace=True
    )

    return data


<<<<<<< HEAD
if __name__ == "__main__":
    # dict_data = scrape_ad(
    #     "https://www.pap.fr/annonces/appartement-bures-sur-yvette-91440-r432200988"
    # )
    data_csv = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/pap-oxylab/csv_outputs/output.csv')
    df_data = pd.DataFrame(data_csv)
    result = process_outputs(df_data)
    print(result)
=======
def add_desc_content_to_df(
    processed_desc: pd.DataFrame, processed_ad: pd.DataFrame
) -> pd.DataFrame:
    """Merges all the information from the processed description and the processed ad with one simple rule:
    Consider that the data from the ad is more reliable than the data from the description. So if there is
    a conflict between the two, keep the data from the description.

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


def save_to_database(data_collected: pd.DataFrame):
    # Convert all columns to string to avoid errors when writing to database
    data_collected = data_collected.map(str)

    db_config = {
        "host": "safeflat-scraping-data.cls8g8ie67qg.us-east-1.rds.amazonaws.com",
        "port": 3306,
        "user": "admin",
        "password": "SBerWIyVxBu229rGer6Z",
        "database": "scraping",
    }

    table_name = "pap"

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    data_collected.to_sql(name="pap", con=engine, if_exists="append", index=False)


def read_from_database(query: str) -> pd.DataFrame:
    db_config = {
        "host": "safeflat-scraping-data.cls8g8ie67qg.us-east-1.rds.amazonaws.com",
        "port": 3306,
        "user": "admin",
        "password": "SBerWIyVxBu229rGer6Z",
        "database": "scraping",
    }

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    df = pd.read_sql_query(query, con=engine)

    return df


def remove_already_scraped_urls(urls: list) -> list:
    query = "select url from pap"
    scraped_urls_df = read_from_database(query)["url"]
    print("scraped_urls_df: ", scraped_urls_df)
    scraped_urls_list = scraped_urls_df.to_list()
    print("scrapped_urls_list: ", scraped_urls_list)
    urls = [url for url in urls if url not in scraped_urls_list]

    return urls
>>>>>>> b1fda924e9288603a822e807c8f53e1dc2152841
