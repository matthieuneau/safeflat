#from utils import *
from geopy.distance import geodesic
import pandas as pd


def score_calculation(row, property_infos, poids):
    total_poids = 0
    matching_poids = 0

    for key, value in property_infos.items():
        if value is not None and key in poids:
            total_poids += poids[key]
            if row[key] == value:
                matching_poids += poids[key]

    if total_poids == 0:
        return 0
    return matching_poids / total_poids


def filter_and_score(property_infos):
    """
    Filters goods according to specified criteria and calculates a match score for the remaining goods.

    Args:
    property_infos (dict): Dictionary containing the characteristics of the property to be searched

    Returns:
    pd.DataFrame: DataFrame of filtered propreties with a match score.
    """

    # Dynamic construction of SQL query based on property_infos values
    # query = "SELECT * FROM pap"

    # if property_infos['ville'] is not None:
    #     query += f" WHERE ville = '{property_infos['ville']}'"  # Placeholder for location

    # Read data from the database and apply first filter (query):
    # data_df = read_from_database(query)
    data_df = pd.read_csv(
        "/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/airbnb/outpu_processed.csv"
    )

    # Transform text into digital format:
    data_df["surface"] = pd.to_numeric(data_df["surface"], errors="coerce")
    data_df["nb_bedrooms"] = pd.to_numeric(data_df["nb_bedrooms"], errors="coerce")
    data_df["latitude"] = pd.to_numeric(data_df["latitude"], errors="coerce")
    data_df["longitude"] = pd.to_numeric(data_df["longitude"], errors="coerce")
    data_df["nb_bathrooms"] = pd.to_numeric(data_df["nb_bathrooms"], errors="coerce")
    data_df["lits_doubles"] = pd.to_numeric(data_df["lits_doubles"], errors="coerce")
    data_df["lits_simples"] = pd.to_numeric(data_df["lits_simples"], errors="coerce")
    data_df["canapes_convertibles"] = pd.to_numeric(data_df["canapes_convertibles"], errors="coerce")
    data_df["lits_superposes"] = pd.to_numeric(data_df["lits_superposes"], errors="coerce")
    data_df["numero_d'etage"] = pd.to_numeric(data_df["numero_d'etage"], errors="coerce")
    data_df["nombre_d'etages"] = pd.to_numeric(data_df["nombre_d'etages"], errors="coerce")


    # To be replaced with the SQL query:
    filter_place = ["ville"]
    for filter in filter_place:
        if property_infos[filter] is not None:
            data_df = data_df[data_df[filter] == property_infos[filter]]

    # # First filter, only keeps matching data
    filter_rooms = ["nb_bedrooms"]
    for filter in filter_rooms:
        value = property_infos[filter]
        if value is not None:
            data_df = data_df[
                (
                    (max(0, value - 1) <= data_df[filter])
                    & (data_df[filter] <= value + 1)
                )
                | pd.isna(data_df[filter])
            ]

    # filter_surface = ["surface"]
    # for filter in filter_surface:
    #     value = property_infos[filter]
    #     if value is not None:
    #         data_df = data_df[
    #             ((value * 0.75 <= data_df[filter]) & (data_df[filter] <= value * 1.25))
    #             | pd.isna(data_df[filter])
    #         ]

    def is_within_distance(row, point_ref, max_distance_km):
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            return True
        point = (row["latitude"], row["longitude"])
        return geodesic(point, point_ref).kilometers <= max_distance_km

    lat = property_infos["latitude"]
    lng = property_infos["longitude"]
    if lat is not None and lng is not None:
        data_df = data_df[
            data_df.apply(
                is_within_distance, axis=1, point_ref=(lat, lng), max_distance_km=5
            )
        ]

    # Defines the weight of each scoring feature (from 1 to 20)
    poids = {
        "type": 5,
        "nb_bedrooms" : 7,
        "nb_bathrooms": 8,
        "host_name" : 20,
        "lave-linge": 7,
        "sèche-linge": 7,
        "balcon": 10,
        "terrasse": 10,
        "parking": 6,
        "ascenseur": 8,
        "climatisation": 5,
        "piscine": 10,
        "baignoire": 10,
        "lits_doubles": 6,
        "lits_simples": 6,
        "canapes_convertibles": 6,
        "lits_superposes": 6,
        "surface": 8,
        "nb_rooms": 7,
        "quartier": 7,
        "meuble": 5,
        "nombre_d'etages": 6,
        "numero_d'etage": 6,
        "cave": 4,
    }

    # Cost calculation for each line
    data_df["cost"] = (
        data_df.apply(
            score_calculation, axis=1, property_infos=property_infos, poids=poids
        )
        * 100
    )

    print(data_df.columns)
    return data_df


# Example of a property to protect:
property_infos_same = {
    "ville": "Strasbourg",
    "type": "appartement",
    "latitude": 48.5825846,
    "longitude": 7.7389715,
    "nb_bedrooms" : 1,
    "nb_bathrooms": 1,
    "host_name" : 'Emma',
    "lave-linge": 'oui',
    "sèche-linge": 'oui',
    "balcon": 'non',
    "terrasse": 'non',
    "parking": 'non',
    "ascenseur": 'non',
    "climatisation": 'non',
    "piscine": 'non',
    "baignoire": 'non',
    "lits_doubles": 1,
    "lits_simples": 0,
    "canapes_convertibles": 1,
    "lits_superposes": 0,
    "surface": None,
    "nb_rooms": None,
    "quartier": None,
    "meuble": None,
    "nombre_d'etages": None,
    "numero_d'etage": 1,
    "cave": None,
}

if __name__ == "__main__":
    filtered_data = filter_and_score(property_infos_same)
    print(filtered_data)

    # data = read_from_database("SELECT * FROM pap")
    # print(data)
    # filtered_data.to_csv('C:/Users/hennecol/Documents/safeflat/scraping/pap-oxylab/csv_outputs/output_score.csv')
