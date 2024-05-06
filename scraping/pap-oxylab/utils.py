import requests
from bs4 import BeautifulSoup


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat"
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
    print(len(url_list))
    print(f"url_list: {url_list}")


def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Retrieving title and price
    try:
        title_and_price = soup.select_one("h1.item-title")
        data["title_and_price"] = (
            title_and_price.text.strip() if title_and_price else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving title and price: {e}")
        data["title_and_price"] = "Not Available"

    # Retrieving location
    try:
        location = soup.select_one("div.location-selector > h2")
        data["location"] = location.text.strip() if location else "Not Available"
    except Exception as e:
        print(f"Error retrieving location: {e}")
        data["location"] = "Not Available"

    # Retrieving nb of rooms, surface and nb of bedrooms when available
    try:
        list_items = soup.select("ul.item-tags.margin-bottom-20 > li")
        details = [
            item.find("strong").text.strip()
            for item in list_items
            if item.find("strong")
        ]
        data["details"] = details
    except Exception as e:
        print(f"Error retrieving details: {e}")
        data["details"] = []

    # Retrieving description
    try:
        description = soup.select_one("div.description-container")
        data["description"] = (
            description.text.strip() if description else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving description: {e}")
        data["description"] = "Not Available"

    # Retrieving metro stations closeby
    try:
        metro = soup.select(".item-transports")
        metro_stations = [item.text.strip() for item in metro]
        data["metro_stations"] = metro_stations
    except Exception as e:
        print(f"Error retrieving metro stations: {e}")
        data["metro_stations"] = []

    # Retrieving conditions financieres
    try:
        conditions_financieres = soup.select(".row > .col-1-3")
        conditions_financieres = [item.text.strip() for item in conditions_financieres]
        data["conditions_financieres"] = conditions_financieres
    except Exception as e:
        print(f"Error retrieving financial conditions: {e}")
        data["conditions_financieres"] = []

    # Retrieving energy and ges
    try:
        energy = soup.select_one(".energy-indice ul li.active")
        data["energy"] = energy.text.strip() if energy else "Not Available"
    except Exception as e:
        print(f"Error retrieving energy: {e}")
        data["energy"] = "Not Available"

    # Retrieving ges
    try:
        ges = soup.select_one(".ges-indice ul li.active")
        data["ges"] = ges.text.strip() if ges else "Not Available"
    except Exception as e:
        print(f"Error retrieving ges: {e}")
        data["ges"] = "Not Available"

    # Retrieving ref and date
    try:
        ref_date = soup.select_one(".item-date")
        data["ref_date"] = ref_date.text.strip() if ref_date else "Not Available"
    except Exception as e:
        print(f"Error retrieving reference and date: {e}")
        data["ref_date"] = "Not Available"
    print(data)
    return data


if __name__ == "__main__":
    scrape_ad("https://www.pap.fr/annonces/maison-la-celle-saint-cloud-r448201718")
