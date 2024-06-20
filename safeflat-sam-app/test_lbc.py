import sys
import os
import pandas as pd
import importlib
import urllib3

urllib3.disable_warnings()

site_name = 'leboncoin'

# Ajout du chemin vers le dossier 'scrapeUrls'
scrapeUrls_path = os.path.join(os.path.dirname(__file__), 'scrapeUrls')
sys.path.append(scrapeUrls_path)

# Ajout du chemin vers le dossier 'retrieveUrls'
retrieveUrls_path = os.path.join(os.path.dirname(__file__), 'retrieveUrls')
sys.path.append(retrieveUrls_path)

# Ajouter le dossier `retrieveUrls/airbnb` au sys.path
retrieve_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'retrieveUrls', site_name))
sys.path.append(retrieve_dir)

# Ajouter le dossier `scrapeUrls/airbnb` au sys.path
scrape_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scrapeUrls', site_name))
sys.path.append(scrape_dir)

# Ajouter le dossier `detectSublets/airbnb` au sys.path
scrape_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'detectSublets', site_name))
sys.path.append(scrape_dir)



from retriever import retrieve_urls # Remplacez par les noms des fonctions à importer
from scraper import scrape_ad  # Remplacez par les noms des fonctions à importer
from postprocessing import process_output  # Remplacez par les noms des fonctions à importer
from algo import filter_and_score

# Importation des modules utils avec des alias pour éviter les conflits de noms
scrape_utils = importlib.import_module('utils', 'scrapeUrls')
retrieve_utils = importlib.import_module('utils', 'retrieveUrls')


#Airbnb:
property_infos_same = {
    "ville": "Strasbourg",
    "type": "appartement",
    "latitude": 48.5825846,
    "longitude": 7.7389715,
    "nb_bedrooms" : 1,
    "nb_bathrooms": 1,
    "host_name" : 'Emma',
    "lave-linge": 'oui',
    "sèche-linge": 'oui',
    "balcon": 'non',
    "terrasse": 'non',
    "parking": 'non',
    "ascenseur": 'non',
    "climatisation": 'non',
    "piscine": 'non',
    "baignoire": 'non',
    "lits_doubles": 1,
    "lits_simples": 0,
    "canapes_convertibles": 1,
    "lits_superposes": 0,
    "surface": None,
    "nb_rooms": None,
    "quartier": None,
    "meuble": None,
    "nombre_d'etages": None,
    "numero_d'etage": 1,
    "cave": None,
}

if __name__ == "__main__":
    urls = retrieve_urls('https://www.leboncoin.fr/recherche?category=10&locations=Strasbourg_67000__48.58504_7.73642_5000_1000&real_estate_type=2')
    urls = urls[1:]
    # for url in urls:
    #     scraped_data = scrape_ad(url)
    #     print('Scraped ad:', scraped_data)
    #     scraped_data = pd.DataFrame(scraped_data)
    #     processed_data = process_output(scraped_data)

    #     desc_data = scrape_utils.process_description(scraped_data["description"])

    #     merged_data = scrape_utils.add_desc_content_to_df(desc_data, processed_data)
    #     #merged_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output.csv')

    #     data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output.csv')
    #     df_concatene = pd.concat([merged_data, data_bdd], ignore_index=True)
    #     colonnes_a_supprimer = [col for col in df_concatene.columns if 'Unnamed:' in col]
    #     df_concatene.drop(columns=colonnes_a_supprimer, inplace=True)
    #     df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output.csv')
    #     print("Data merged with database!")
        
    data_bdd2 = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output.csv')
    filtered_and_scored_data = filter_and_score(property_infos_same)
    filtered_and_scored_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output_filtered_score.csv')

    #     #save_to_database(merged_data)

    #Test postprocessing
    # data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output.csv')
    # data_processed = process_output(data_bdd)
    # data_processed.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output_processed.csv')


 

    

    

    