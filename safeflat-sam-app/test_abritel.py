import sys
import os
import pandas as pd
import importlib
import urllib3

urllib3.disable_warnings()

site_name = 'abritel'

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
from scraper import abritel_scraper  # Remplacez par les noms des fonctions à importer
from generate_urls import generate_abritel_url
from postprocessing import process_output  # Remplacez par les noms des fonctions à importer
from algo import filter_and_score

# Importation des modules utils avec des alias pour éviter les conflits de noms
scrape_utils = importlib.import_module('utils', 'scrapeUrls')
retrieve_utils = importlib.import_module('utils', 'retrieveUrls')

#For test purpose:
lat = 43.208037
lon = 6.557318
nb_chambres = 1
nb_salles_de_bains = 1
prix_min = 0
prix_max = 2000
sort_order = 'asc' 

property_infos = {
        'ville' : 'la croix-valmer',
        'surface' : 32.0,
        'nb_bedrooms' : 1,
        'nb_bathrooms': 1.0,
        'baignoire' : None,
        'douche' : 'oui',
        'lits_doubles': 1.0,
        'lits_simples': None,
        'canapes_convertibles': 2.0, 
        'lits_superposes' : None,
        'host_name' : 'mann',
        'type': 'appartement',
        "terrasse": 'oui',
        "balcon": None,
        "jardin": None,
        "cave": None,
        "parking": None,
        "garage": None,
        "box": None,
        "piscine": 'oui',
        "ascenseur": None,
        "interphone": None,
        "gardien": None,
        "lave-linge": 'oui',
        "sèche-linge": None,
        "climatisation": 'oui'
}

if __name__ == "__main__":
    # url_coord = generate_abritel_url(lat, lon, nb_chambres, nb_salles_de_bains, prix_min, prix_max, sort_order)
    # urls = retrieve_urls(url_coord)
    
    # urls = urls[1:]
    # for url in urls:
    #     scraped_data = abritel_scraper(url)
    #     print('Scraped ad:', scraped_data)
    #     scraped_data = pd.DataFrame([scraped_data])
        
    #     processed_data = process_output(scraped_data)
    #     #processed_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_processed.csv') #To initialize the csv file

    #     data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_processed.csv')
    #     data_bdd.reset_index(drop=True, inplace=True)
    #     df_concatene = pd.concat([processed_data, data_bdd], ignore_index=True)
    #     colonnes_a_supprimer = [col for col in df_concatene.columns if 'Unnamed:' in col]
    #     df_concatene.drop(columns=colonnes_a_supprimer, inplace=True)

    #     df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_processed.csv')
    #     print("Data merged to database!")

    #Try of the scoring function
    data_bdd2 = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_processed.csv')
    filtered_and_scored_data = filter_and_score(property_infos)
    filtered_and_scored_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_filtered_score.csv')




 

    

    

    