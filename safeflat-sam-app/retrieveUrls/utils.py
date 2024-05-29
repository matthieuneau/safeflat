import requests
import pandas as pd
from sqlalchemy import create_engine


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat4"
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
