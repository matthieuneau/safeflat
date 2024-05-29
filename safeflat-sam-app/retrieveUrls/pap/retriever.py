from utils import *
from bs4 import BeautifulSoup


### STILL NEED TO ADD THE PAGE NAVIGATION
def retrieve_urls() -> list:
    """Retrieve the URLs of the ads from the page

    Args:
        page (str): url of the page listing the ads

    Returns:
        list: list of the URLs of the ads on the page
    """
    urls_to_scrape = []

    for i in range(1, 3):

        page_url = f"https://www.pap.fr/annonce/location-appartements-{i}"

        html = fetch_html_with_oxylab(page_url)

        soup = BeautifulSoup(html, "html.parser")
        all_a_tags = soup.find_all("a")

        url_list = [
            item["href"]
            for item in all_a_tags
            if item.get("href", "").startswith("/annonces/")
        ]

        #### FOR TESTING PURPOSE, SHORTEN THE LIST FOR NOW
        url_list = url_list[:2]

        # Remove duplicates
        url_list = list(set(url_list))
        # Add prefix and editing to have the correct URL
        url_list = [f"https://www.pap.fr{url}" for url in url_list]
        urls_to_scrape = urls_to_scrape + [url_list]

    return urls_to_scrape
