import sys
import os
import pandas as pd
import importlib
import urllib3

urllib3.disable_warnings()

site_name = 'airbnb'

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

from generate_urls import generate_airbnb_url  # Remplacez par les noms des fonctions à importer
from retriever import retrieve_urls # Remplacez par les noms des fonctions à importer
from scraper import scrape_ad  # Remplacez par les noms des fonctions à importer
from postprocessing import process_output  # Remplacez par les noms des fonctions à importer

# Importation des modules utils avec des alias pour éviter les conflits de noms
scrape_utils = importlib.import_module('utils', 'scrapeUrls')
retrieve_utils = importlib.import_module('utils', 'retrieveUrls')


if __name__ == "__main__":
    url_listing = generate_airbnb_url("67000", 15, "03/10/2024", "04/10/2024")
    urls = retrieve_urls(url_listing)
    #for url in urls:
    url = urls[1]
    # try:
    #     scraped_data = scrape_ad(url)
    #     print('Scraped ad:', scraped_data)
    #     scraped_data = pd.DataFrame(scraped_data)

    #     desc_data = scrape_utils.process_description(scraped_data["description"])

    #     merged_data = scrape_utils.add_desc_content_to_df(desc_data, scraped_data)
    #     processed_data = process_output(merged_data)
    #     #merged_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/airbnb/output.csv')

    #     #data_bdd = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output_processed.csv')

    #     #df_concatene = pd.concat([merged_data, data_bdd], ignore_index=True)
    #     #df_concatene.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/csv_ouptus/output_processed.csv')

    #     #save_to_database(merged_data)
    # except Exception as e:
    #     print(f"An error occrued while processing the ad: {url}", "\n", e)

    scraped_data = scrape_ad(url)
    print('Scraped ad:', scraped_data)
    scraped_data = pd.DataFrame([scraped_data])

    desc_data = scrape_utils.process_description(scraped_data["description"])

    merged_data = scrape_utils.add_desc_content_to_df(desc_data, scraped_data)
    merged_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/airbnb/output_before_preproc.csv')
    #processed_data = process_output(merged_data)

    

    