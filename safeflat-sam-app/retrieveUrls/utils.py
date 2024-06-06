import requests
import pandas as pd
from sqlalchemy import create_engine


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat123_Uq0oI"
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


### TO BE EDITED ###
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


### TO BE EDITED ###
def remove_already_scraped_urls(urls: list) -> list:
    query = "select url from pap"
    scraped_urls_df = read_from_database(query)["url"]
    print("scraped_urls_df: ", scraped_urls_df)
    scraped_urls_list = scraped_urls_df.to_list()
    print("scrapped_urls_list: ", scraped_urls_list)
    urls = [url for url in urls if url not in scraped_urls_list]

    return urls

html_page = fetch_html_with_oxylab("https://www.abritel.fr/location-vacances/p2238650?dateless=true&x_pwa=1&rfrr=HSR&pwa_ts=1717660550034&referrerUrl=aHR0cHM6Ly93d3cuYWJyaXRlbC5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=true&adults=1&regionId=500409&destination=La%20Ciotat%2C%20Département%20des%20Bouches-du-Rhône%2C%20France&destType=BOUNDING_BOX&latLong=43.178517%2C5.609222&nightly_price=0%2C2000&bedroom_count_gt=1&privacyTrackingState=CAN_NOT_TRACK&searchId=34722838-47b6-4e7b-aa98-726f7be7b905&us_bathroom_count_gt=1&sort=PRICE_LOW_TO_HIGH&userIntent=&expediaPropertyId=92721726&propertyName=Calme%2C%20entre%20plages%20et%20centre%20historique%20de%20La%20Ciotat")
with open("/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/retrieveUrls/abritel/liste_annonces/annonce_name.html", "w", encoding="utf-8") as file:
    file.write(html_page)