def pap_scraper(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    data["url"] = ad_url

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
        location = soup.select_one(".item-description.margin-bottom-30 > h2")
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
        description = soup.select_one("div.margin-bottom-30 > p")
        data["description"] = (
            description.text.strip() if description else "Not Available"
        )
    except Exception as e:
        print(f"Error retrieving description: {e}")
        data["description"] = "Not Available"

    # # Retrieving metro stations closeby
    # try:
    #     metro = soup.select(".item-transports")
    #     metro_stations = [item.text.strip() for item in metro]
    #     data["metro_stations"] = metro_stations
    # except Exception as e:
    #     print(f"Error retrieving metro stations: {e}")
    #     data["metro_stations"] = []

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
    data = pd.DataFrame([data])
    return data


def extract_rooms(details):
    for item in details:
        if "pièce" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_bedrooms(details: str):
    for item in details:
        if "chambre" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_surface(details: str):
    for item in details:
        if "m²" in item and "Terrain" not in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_terrain(details: str):
    for item in details:
        if "Terrain" in item:
            # Split the string on spaces and get the first element
            return item.split()[1]
    return "N/A"


def extract_rent_with_bills(conditions_financieres: str):
    for item in conditions_financieres:
        if "charges comprises" in item:
            rent_with_bills = item.split("\n")[1].split()[0].replace(".", "")
            return rent_with_bills
    return "N/A"


def extract_bills(conditions_financieres: str):
    for item in conditions_financieres:
        if "Dont charges" in item:
            bills = item.split("\n")[1].split()[0]
            return bills


def process_outputs(data: pd.DataFrame) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        data (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """
    data["title"] = data["title_and_price"].apply(lambda x: x.split("\t")[0])
    data["price"] = data["title_and_price"].apply(
        lambda x: x.split("\t")[1:][-1]
        .replace("€", "")
        .replace(" ", "")
        .replace(".", "")
    )
    data["nb_rooms"] = data["details"].apply(extract_rooms)
    data["nb_bedrooms"] = data["details"].apply(extract_bedrooms)
    data["surface"] = data["details"].apply(extract_surface)
    data["terrain"] = data["details"].apply(extract_terrain)
    data["rent_with_bills"] = data["conditions_financieres"].apply(
        extract_rent_with_bills
    )
    data["bills"] = data["conditions_financieres"].apply(extract_bills)

    data.drop(
        ["title_and_price", "details", "conditions_financieres"], axis=1, inplace=True
    )

    return data


def add_desc_content_to_df(
    processed_desc: pd.DataFrame, processed_ad: pd.DataFrame
) -> pd.DataFrame:
    """Merges all the information from the processed description and the processed ad with one simple rule:
    Consider that the data from the ad is more reliable than the data from the description. So if there is
    a conflict between the two, keep the data from the description.

    Args:
        processed_desc (pd.DataFrame): processed description data
        processed_ad (pd.DataFrame): processed ad data

    Returns:
        pd.DataFrame: merged data
    """
    for col in processed_desc.columns:
        if col not in processed_ad.columns:
            processed_ad[col] = processed_desc[col]

    return processed_ad
