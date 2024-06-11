from .utils import fetch_html_with_oxylab
from bs4 import BeautifulSoup


def retrieve_urls(page_url: str) -> list:
    """Retrives all the urls of the ads from a given page of airbnb

    Parameters
    ----------
    page_url : str
        page that contains the ads

    Returns
    -------
    list
        contains all the urls of the ads
    """

    html = fetch_html_with_oxylab(page_url)

    soup = BeautifulSoup(html, "html.parser")
    all_a_tags = soup.find_all("a")

    url_list = [
        item["href"]
        for item in all_a_tags
        if item.get("href", "").startswith("/rooms/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))

    # Add prefix and editing to have the correct URL
    url_list = [f"https://www.airbnb.fr{url}" for url in url_list]
    print("urls retrieved: ", url_list)
    return url_list
