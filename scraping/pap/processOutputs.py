from langchain_openai import OpenAI
import pandas as pd
import os

data = pd.read_csv("scraping/pap/output.csv")
data = data.head(5)


def extract_rooms(details):
    for item in details:
        if "pièces" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_bedrooms(details: str):
    for item in details:
        if "chambres" in item:
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
    data["title"] = data["title_and_price"].apply(lambda x: x.split("\n")[0])
    data["price"] = data["title_and_price"].apply(
        lambda x: x.split("\n")[1].split("€")[0].replace(".", "")
    )
    data["nb_rooms"] = data["details"].apply(extract_rooms)
    data["nb_bedrooms"] = data["details"].apply(extract_bedrooms)
    data["surface"] = data["details"].apply(extract_surface)
    data["terrain"] = data["details"].apply(extract_terrain)
    data["rent_with_bills"] = data["conditions_financieres"].apply(
        extract_rent_with_bills
    )
    data["bills"] = data["conditions_financieres"].apply(extract_bills)
    data["date"] = data["ref_date"].apply(lambda x: x.split("/")[-1][1:])

    # Dropping the unnecessary columns
    data.drop(
        columns=["details", "conditions_financieres", "title_and_price"], inplace=True
    )

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


def add_chatgpt_info_to_data(llm_response: str, data_collected) -> dict:
    llm_response = eval(llm_response)
    for key, value in llm_response.items():
        if key not in data_collected.columns:
            data_collected[key] = value
        else:  # Do nothing because we consider that data collected directly is more reliable
            pass
    return data_collected
