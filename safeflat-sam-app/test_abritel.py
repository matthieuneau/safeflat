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
#from postprocessing import process_output  # Remplacez par les noms des fonctions à importer
#from algo import filter_and_score

# Importation des modules utils avec des alias pour éviter les conflits de noms
scrape_utils = importlib.import_module('utils', 'scrapeUrls')
retrieve_utils = importlib.import_module('utils', 'retrieveUrls')

lat = 43.178517
lon = 5.609222
nb_chambres = 1
nb_salles_de_bains = 1
prix_min = 0
prix_max = 2000
sort_order = 'asc' 

if __name__ == "__main__":
    url_coord = generate_abritel_url(lat, lon, nb_chambres, nb_salles_de_bains, prix_min, prix_max, sort_order)
    urls = retrieve_urls(url_coord)
    
    #urls = [urls[2]]
    for url in urls:
        try:
            scraped_data = abritel_scraper(url)
            print('Scraped ad:', scraped_data)
            scraped_data = pd.DataFrame([scraped_data])

    #         processed_data = process_output(scraped_data)

    #         desc_data = scrape_utils.process_description(scraped_data["description"])

    #         merged_data = scrape_utils.add_desc_content_to_df(desc_data, processed_data)
            
            #data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')
            data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_before_process.csv')

    #         merged_data.reset_index(drop=True, inplace=True)
            data_bdd.reset_index(drop=True, inplace=True)
            df_concatene = pd.concat([scraped_data, data_bdd], ignore_index=True)
    #         df_concatene = pd.concat([merged_data, data_bdd], ignore_index=True)
            colonnes_a_supprimer = [col for col in df_concatene.columns if 'Unnamed:' in col]
            df_concatene.drop(columns=colonnes_a_supprimer, inplace=True)
            df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_before_process.csv')

    #         df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')
    #         print("Data merged to database!")

    #         # data_bdd2 = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/airbnb/outpu_processed.csv')
    #         # filtered_and_scored_data = filter_and_score(property_infos_same)
    #         # filtered_and_scored_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/airbnb/output_filtered_score.csv')

    #         #save_to_database(merged_data)
        except Exception as e:
            print(f"An error occrued while processing the ad: {url}", "\n", e)
        

        # scraped_data = scrape_ad(url)
        # print('Scraped ad:', scraped_data)
        # scraped_data = pd.DataFrame([scraped_data])
        # processed_data = process_output(scraped_data)

        # desc_data = scrape_utils.process_description(scraped_data["description"])

        # merged_data = scrape_utils.add_desc_content_to_df(desc_data, processed_data)

        # data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')

        # merged_data.reset_index(drop=True, inplace=True)
        # data_bdd.reset_index(drop=True, inplace=True)
        # df_concatene = pd.concat([merged_data, data_bdd], ignore_index=True)
        # colonnes_a_supprimer = [col for col in df_concatene.columns if 'Unnamed:' in col]
        # df_concatene.drop(columns=colonnes_a_supprimer, inplace=True)
        # print("Colonnes :", df_concatene.columns)
        # df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv')

 

    

    

    