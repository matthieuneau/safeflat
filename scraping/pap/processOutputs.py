import pandas as pd

data = pd.read_csv("scraping/pap/output.csv")
data = data.head(5)


def extract_rooms(details):
    """
    Extracts the number of rooms from the stringified list details.
    """
    for item in eval(details):
        if "pièces" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_bedrooms(details: str):
    """
    Extracts the number of bedrooms from the stringified list details.
    """
    for item in eval(details):
        if "chambres" in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_surface(details: str):
    """
    Extracts the surface from the stringified list details.
    """
    for item in eval(details):
        if "m²" in item and "Terrain" not in item:
            # Split the string on spaces and get the first element
            return item.split()[0]
    return "N/A"


def extract_terrain(details: str):
    """
    Extracts the surface from the stringified list details.
    """
    for item in eval(details):
        if "Terrain" in item:
            # Split the string on spaces and get the first element
            return item.split()[1]
    return "N/A"


def extract_rent_with_bills(details: str):
    """
    Extracts the rent with bills from the stringified list details.
    """
    for item in eval(details):
        if "charges comprises" in item:
            rent_with_bills = item.split("\n")[1].split()[0].replace(".", "")
            return rent_with_bills
    return "N/A"


def extract_bills(details: str):
    """
    Extracts the rent without bills from the stringified list details.
    """
    for item in eval(details):
        if "Dont charges" in item:
            bills = item.split("\n")[1].split()[0]
            return bills


data["title"] = data["title_and_price"].apply(lambda x: x.split("\n")[0])
data["price"] = data["title_and_price"].apply(
    lambda x: x.split("\n")[1].split("€")[0].replace(".", "")
)
data["nb_rooms"] = data["details"].apply(extract_rooms)
data["nb_bedrooms"] = data["details"].apply(extract_bedrooms)
data["surface"] = data["details"].apply(extract_surface)
data["terrain"] = data["details"].apply(extract_terrain)
data["rent_with_bills"] = data["conditions_financieres"].apply(extract_rent_with_bills)
data["bills"] = data["conditions_financieres"].apply(extract_bills)
data["date"] = data["ref_date"].apply(lambda x: x.split("/")[-1][1:])

# Dropping the unnecessary columns
data.drop(columns=["details", "conditions_financieres"], inplace=True)

print(data["title_and_price"])
print(data["price"])

data.to_csv("output_processed.csv", mode="w", header=True, index=False)
