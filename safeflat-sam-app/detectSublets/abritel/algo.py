#from utils import *
from geopy.distance import geodesic
import pandas as pd


def score_calculation(row, property_infos, poids, poids_surface, poids_nom):
    total_poids = 0
    matching_poids = 0

    for key, value in property_infos.items():
        if value is not None:
            # Add surface weights
            if key in poids_surface:
                total_poids += poids_surface[key]
                if row[key] is not None and value - 1 <= row[key] <= value + 1:
                    matching_poids += poids_surface[key]
            
            # Add name weights
            elif key in poids_nom:
                total_poids += poids_nom[key]
                if row[key] is not None and isinstance(row[key], str) and isinstance(value, str) and (row[key] in value or value in row[key]):
                    matching_poids += poids_nom[key]
            
            # Add standard weights
            elif key in poids:
                total_poids += poids[key]
                if row[key] is not None and row[key] == value:
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
        "/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/abritel/output_processed.csv"
    )

    # Transform text into digital format:
    data_df["nb_bedrooms"] = pd.to_numeric(data_df["nb_bedrooms"], errors="coerce")
    data_df["surface"] = pd.to_numeric(data_df["surface"], errors="coerce")

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

    filter_surface = ["surface"]
    for filter in filter_surface:
        value = property_infos[filter]
        if value is not None:
            data_df = data_df[
                ((value * 0.75 <= data_df[filter]) & (data_df[filter] <= value * 1.25))
                | pd.isna(data_df[filter])
            ]

    # Defines the weight of each scoring feature (from 1 to 20)
    poids = {
        'nb_bedrooms' : 15,
        'nb_bathrooms': 15,
        'baignoire' : 10,
        'douche' :10,
        'lits_doubles': 8,
        'lits_simples': 8,
        'canapes_convertibles': 8, 
        'lits_superposes' : 8,
        'type': 5,
        "terrasse": 12,
        "balcon": 12,
        "jardin": 12,
        "cave": 6,
        "parking": 12,
        "garage": 10,
        "box": 5,
        "piscine": 15,
        "ascenseur": 6,
        "interphone": 6,
        "gardien": 10,
        "lave-linge": 10,
        "sèche-linge": 10,
        "climatisation":10
    }

    poids_surface = {'surface' : 20}
    poids_nom = {'host_name' : 20}

    # Cost calculation for each line
    data_df["cost"] = (
        data_df.apply(
            score_calculation, axis=1, property_infos=property_infos, poids=poids, poids_surface = poids_surface, poids_nom = poids_nom
        )
        * 100
    )

    print(data_df.columns)
    return data_df


