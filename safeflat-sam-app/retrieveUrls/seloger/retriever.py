from bs4 import BeautifulSoup
import json
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import *

def retrieve_urls(page_url: str) -> list:
    """Retrieve the URLs of the ads from the page

    Args:
        page (str): url of the page listing the ads

    Returns:
        list: list of the URLs of the ads on the page
    """

    html = fetch_html_with_oxylab(page_url)

    soup = BeautifulSoup(html, "html.parser")
    all_a_tags = soup.find_all("a")

    url_list = [
        item["href"]
        for item in all_a_tags
        if item.get("href", "").startswith("/annonces/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))
    
    # Add prefix and editing to have the correct URL
    url_list = [f"https://www.seloger.com{url}" for url in url_list]
    print("urls retrieved: ", url_list)
    return url_list

if __name__ == "__main__":
    #Download the hmtl of the web page:
    html_page = fetch_html_with_oxylab('https://www.seloger.com/list.htm?projects=1&types=2%2C1&places=%5B%7B%22subDivisions%22%3A%5B%2275%22%5D%7D%5D&sort=d_dt_crea&mandatorycommodities=0&enterprise=0&qsVersion=1.0')
    with open("/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/retrieveUrls/seloger/page_annonces/liste_annonces.html", "w", encoding="utf-8") as file:
        file.write(html_page)