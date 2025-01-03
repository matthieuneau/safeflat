import requests
import pandas as pd
from sqlalchemy import create_engine
import os
import dotenv

dotenv.load_dotenv()


def fetch_html_with_oxylab(page_url: str) -> str:
    """Uses oxylab as a wrapper to fetch the html of a page to avoid being blocked

    Parameters
    ----------
    page_url : str
        page for which the html is to be fetched

    Returns
    -------
    str
        the html of the page
    """
    proxies = {
        "http": f"http://{os.getenv('OXYLAB_USERNAME')}:{os.getenv('OXYLAB_PASSWORD')}@unblock.oxylabs.io:60000",
        "https": f"http://{os.getenv('OXYLAB_USERNAME')}:{os.getenv('OXYLAB_PASSWORD')}@unblock.oxylabs.io:60000",
    }

    response = requests.request(
        "GET",
        page_url,
        verify=False,  # Ignore the certificate
        proxies=proxies,
    )

    return response.text


def read_from_database(query: str) -> pd.DataFrame:
    """retrieves the

    Parameters
    ----------
    query : str
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """
    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": 3306,
        "user": "admin",
        "password": os.getenv("DB_PASSWORD"),
        "database": "scraping",
    }

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    df = pd.read_sql_query(query, con=engine)

    return df


def remove_already_scraped_urls(urls: list, website: str) -> list:
    query = f"select url from {website}"
    scraped_urls_df = read_from_database(query)["url"]
    print("scraped_urls_df: ", scraped_urls_df)
    scraped_urls_list = scraped_urls_df.to_list()
    print("scrapped_urls_list: ", scraped_urls_list)
    urls = [url for url in urls if url not in scraped_urls_list]

    return urls
