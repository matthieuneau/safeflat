from bs4 import BeautifulSoup
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
        if item.get("href", "").startswith("/location-vacances/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))

    # Add prefix and editing to have the correct URL
    url_list = [f"https://www.abritel.fr{url}" for url in url_list]
    print("urls retrieved: ", url_list)
    return url_list
