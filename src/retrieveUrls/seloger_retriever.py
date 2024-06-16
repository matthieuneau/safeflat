from bs4 import BeautifulSoup
from utils import fetch_html_with_oxylab


def retrieve_urls(page_url: str) -> list:
    """
    The retrieve_urls function retrieves all the urls of the ads from a given page of seloger

    Parameters
    ----------
        page_url: str
            Specify the page that contains the ads

    Returns
    -------

        A list of urls
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
    print(len(url_list))
    print(f"url_list: {url_list}")
    return url_list
