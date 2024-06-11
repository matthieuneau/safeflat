from .utils import fetch_html_with_oxylab
from bs4 import BeautifulSoup


def retrieve_urls(page_url: str) -> list:
    """Retrives all the urls of the ads from a given page of abritel

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
        if item.get("href", "").startswith("/location-vacances/")
    ]

    # Remove duplicates
    url_list = list(set(url_list))
    print(len(url_list))
    print(f"url_list: {url_list}")
    return url_list
