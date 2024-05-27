import requests
import os
import ast
import pandas as pd
from langchain_openai import OpenAI


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
