import sys
import os
import pandas as pd
import importlib
import urllib3

urllib3.disable_warnings()

site_name = 'seloger'

# Ajout du chemin vers le dossier 'scrapeUrls'
scrapeUrls_path = os.path.join(os.path.dirname(__file__), 'scrapeUrls')
sys.path.append(scrapeUrls_path)

# Ajout du chemin vers le dossier 'retrieveUrls'
retrieveUrls_path = os.path.join(os.path.dirname(__file__), 'retrieveUrls')
sys.path.append(retrieveUrls_path)

# Ajouter le dossier `retrieveUrls/seloger` au sys.path
retrieve_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'retrieveUrls', site_name))
sys.path.append(retrieve_dir)

# Ajouter le dossier `scrapeUrls/seloger` au sys.path
scrape_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scrapeUrls', site_name))
sys.path.append(scrape_dir)

# Ajouter le dossier `detectSublets/seloger` au sys.path
scrape_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'detectSublets', site_name))
sys.path.append(scrape_dir)


from retriever import retrieve_urls # Remplacez par les noms des fonctions à importer
from scraper import scrape_ad  # Remplacez par les noms des fonctions à importer
from postprocessing import process_output  # Remplacez par les noms des fonctions à importer
from algo import filter_and_score
from generate_urls import generate_url

# Importation des modules utils avec des alias pour éviter les conflits de noms
scrape_utils = importlib.import_module('utils', 'scrapeUrls')
retrieve_utils = importlib.import_module('utils', 'retrieveUrls')

property_infos_same = {
    "type": "Appartement",
        "meuble": 'oui', 
        "host_name": "alain",
        "ville": "paris", 
        "zipcode": 75011,
        "quartier": None,
        "nb_rooms": 2,
        "nb_bedrooms": 1.0,
        "surface": 42.0,
        "balcon": 'oui',
        "terrasse": 'non',
        "jardin": 'non',
        "surface_balcon": None,
        "surface_terrasse": None,
        "surface_jardin": None,
        "exposition": None,
        "cave": "non",
        "parking": "oui",
        "garage": "non",
        "box": "non",
        "ascenseur": "oui",
        "interphone": "non",
        "gardien": "non",
        "numero_etage": 2.0,
        "nb_etages": None,
        "baignoire": "oui",
        "douche": "non",
        "surface_salon": None,
        "surface_salle_a_manger": None,
        "DPE": None,
        "GES": None
}

if __name__ == "__main__":
    url_cp = generate_url(75011)
    urls = retrieve_urls(url_cp)
    urls = urls[:1]
    for url in urls:
        scraped_data = scrape_ad(url)
        print('Scraped ad:', scraped_data)
        scraped_data = pd.DataFrame([scraped_data])
        processed_data = process_output(scraped_data)

        #To initialize csv file:
        #processed_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv') 
    
        data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')
        df_concatene = pd.concat([processed_data, data_bdd], ignore_index=True)
        colonnes_a_supprimer = [col for col in df_concatene.columns if 'Unnamed:' in col]
        df_concatene.drop(columns=colonnes_a_supprimer, inplace=True)
        df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')
        print("Data merged to database!")

    #     #save_to_database(merged_data)
    
    data_bdd2 = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')
    filtered_and_scored_data = filter_and_score(property_infos_same)
    filtered_and_scored_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_filter_score.csv')
    
