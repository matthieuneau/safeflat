import os
import random
import time
import yaml
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAI


def get_annonce_data(driver, annonce):
    """
    Retrieves data from a given annonce URL.
    """

    driver.get(annonce)
    time.sleep(2)
    data = {}

    # Try retrieving title
    try:
        data["title"] = driver.find_element(By.CSS_SELECTOR, "h1#post-title").text
    except Exception as e:
        print(f"Error retrieving title: {e}")
        data["title"] = "Not Available"

    # Try retrieving subtitle
    try:
        data["subtitle"] = driver.find_element(
            By.CSS_SELECTOR, "h2#post-title-breadcrumb"
        ).text
    except Exception as e:
        print(f"Error retrieving subtitle: {e}")
        data["subtitle"] = "Not Available"

    # Try retrieving author's name
    try:
        data["author"] = driver.find_element(By.CSS_SELECTOR, "#owner-name > a").text
    except Exception as e:
        print(f"Error retrieving author: {e}")
        data["author"] = "Not Available"

    # Try retrieving price titles and values
    try:
        titles = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "div.price-table > div.price-table__row > div.price-table__cell",
            )
        ]
        values = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "div.price-table > div.price-table__row > div.price-table__value",
            )
        ]
        data["prices"] = dict(zip(titles, values))
    except Exception as e:
        print(f"Error retrieving prices: {e}")
        data["prices"] = "Not Available"

    # Try retrieving characteristics titles and values
    try:
        characteristics_titles = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "ul.indexclient__GridList-dYErZy.XvGJg > li > p",
            )
        ]
        characteristics_values = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "ul.indexclient__GridList-dYErZy.XvGJg > li > ul > li",
            )
        ]
        data["characteristics"] = dict(
            zip(characteristics_titles, characteristics_values)
        )
    except Exception as e:
        print(f"Error retrieving characteristics: {e}")
        data["characteristics"] = "Not Available"

    # Try retrieving description
    # First click on the "Lire la suite" button if it exists to make sure the full description is displayed
    try:
        driver.find_element(By.CSS_SELECTOR, "#ad-description__more").click()
    except Exception as e:
        print(f'Error when trying to click on "Lire la suite" button: {e}')
    # Then retrieve the description
    try:
        data["description"] = driver.find_element(
            By.CSS_SELECTOR, "div#ad-description"
        ).text
    except Exception as e:
        # print(f"Error retrieving description: {e}")
        data["description"] = "Not Available"

    print("===================================")
    print("          NEW POST DISPLAY          ")
    print("===================================")
    print(data)
    return data


def process_description(description):
    """
    Processes the description of an annonce.
    """
    os.environ["OPENAI_API_KEY"] = "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"
    llm = OpenAI()

    question = f"""Tu es un expert en location immobilière et tu maitrises tout le vocabulaire associe. Tu dois m’aider a extraire des informations pertinentes parmi de longues descriptions de biens immobiliers que je vais te donner.

    Voici la description d'une annonce d'un bien immobilier qui est mis en location sur un site d'annonces. Essaie de relever les informations suivantes dans le texte de cette description:

    - surface: La surface indiquée en m2
    - nombre de pieces: Le nombre de pieces 
    - piscine: La presence ou non d’une piscine. Renvoie oui si elle est présente, non sinon. Une piscine sera toujours indiquée explicitement dans la description donc si elle n’est pas indiquée, renvoie non
    - type de bien: Le type de bien dont il s’agit. Il peut uniquement s’agir d’un appartement ou d’une maison
    - nombre de chambres: Le nombre de chambres
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
    {{"surface": "N/A”, "nombre de pieces": 3, "piscine": "Non", "type de bien": "N/A", "nombre de chambres": "N/A", "parking": "N/A", "quartier": "N/A", "meuble": "N/A", "nombre d’etages": "N/A", "numero d’etage": "N/A", "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}}

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
    {{"surface": "N/A", "nombre de pieces": "N/A", "piscine": "Non", "type de bien": "appartement", "nombre de chambres": "N/A", "parking": "oui", "quartier": "N/A", "meuble": "N/A", "nombre d’etages": "N/A", "numero d’etage": 1, "ascenseur": "N/A", "cave": "N/A", "terrasse": "oui"}} 


    Repond en renvoyant un dictionnaire sans aucun autres commentaires.

    Voici la description de l'annonce en question: 

    {{ {description} }}
    """

    response = llm.invoke(question)

    return response
