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

    # if property_infos['zipcode'] is not None:
    #     query += f" WHERE ville = '{property_infos['zipcode']}'"  # Placeholder for location

    # Read data from the database and apply first filter (query):
    # data_df = read_from_database(query)
    data_df = pd.read_csv(
        "/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/seloger/output_processed.csv"
    )

    # Transform text into digital format:
    data_df["nb_rooms"] = pd.to_numeric(data_df["nb_rooms"], errors="coerce")
    data_df["nb_bedrooms"] = pd.to_numeric(data_df["nb_bedrooms"], errors="coerce")
    data_df["surface"] = pd.to_numeric(data_df["surface"], errors="coerce")
    data_df["surface_balcon"] = pd.to_numeric(data_df["surface_balcon"], errors="coerce")
    data_df["surface_terrasse"] = pd.to_numeric(data_df["surface_terrasse"], errors="coerce")
    data_df["surface_jardin"] = pd.to_numeric(data_df["surface_jardin"], errors="coerce")

    # To be replaced with the SQL query:
    filter_place = ["ville", "zipcode"] 
    for filter in filter_place:
        if property_infos[filter] is not None:
            data_df = data_df[data_df[filter] == property_infos[filter]]

    # # First filter, only keeps matching data
    filter_rooms = ["nb_rooms", "nb_bedrooms"]
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
        "type": 10,
        "meuble": 15, # à changer en meuble
        "quartier": 15,
        "nb_rooms": 15,
        "nb_bedrooms": 15,
        "balcon": 10,
        "terrasse": 10,
        "jardin": 10,
        "exposition": 7,
        "cave": 7,
        "parking": 5,
        "garage": 10,
        "box": 10,
        "ascenseur": 10,
        "interphone": 5,
        "gardien": 10,
        "numero_etage": 12,
        "nb_etages": 8,
        "baignoire": 13,
        "douche": 13,
        "DPE": 5,
        "GES": 5
        
    }

    poids_surface = {
        "surface": 15,
        "surface_balcon": 12,
        "surface_terrasse": 12,
        "surface_jardin": 10,
        "surface_salon": 15,
        "surface_salle_a_manger": 15
    }

    poids_nom = {
        "host_name": 20,

    }

    # Cost calculation for each line
    data_df["cost"] = (
        data_df.apply(
            score_calculation, axis=1, property_infos=property_infos, poids=poids, poids_surface = poids_surface, poids_nom = poids_nom
        )
        * 100
    )

    print(data_df.columns)
    return data_df


# Example of a property to protect:
property_infos_same = {
    "type": "Appartement",
        "meuble": 1, 
        "host_name": "Kevin",
        "ville": "Paris", 
        "zipcode": 75011,
        "quartier": "Quartier Léon-Blum Folie-Regnault",
        "nb_rooms": 4,
        "nb_bedrooms": 3.0,
        "surface": 33.0,
        "balcon": 0,
        "terrasse": 0,
        "jardin": 0,
        "surface_balcon": None,
        "surface_terrasse": None,
        "surface_jardin": None,
        "exposition": None,
        "cave": 1,
        "parking": 0,
        "garage": 0,
        "box": 1,
        "ascenseur": 1.0,
        "interphone": 0,
        "gardien": 0,
        "numero_etage": 4.0,
        "nb_etages": 6.0,
        "baignoire": 1,
        "douche": 1,
        "surface_salon": None,
        "surface_salle_a_manger": None,
        "DPE": "D",
        "GES": "D"
}

if __name__ == "__main__":
    filtered_data = filter_and_score(property_infos_same)
    print(filtered_data)

    # data = read_from_database("SELECT * FROM pap")
    # print(data)
    # filtered_data.to_csv('C:/Users/hennecol/Documents/safeflat/scraping/pap-oxylab/csv_outputs/output_score.csv')
