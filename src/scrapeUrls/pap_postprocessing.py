import pandas as pd
from pap_scraper import scrape_ad


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


with open("tests/src/scrapeUrls/pap_ad_example_html.txt", "r") as file:
    data = file.read()

data = scrape_ad(data)
processed_data = process_outputs(data)
print(processed_data)
