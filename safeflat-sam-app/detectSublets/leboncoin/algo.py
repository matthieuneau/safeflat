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
    #     query += f" AND WHERE zipcode = '{property_infos['zipcode']}'"  # Placeholder for location



    # Read data from the database and apply first filter (query):
    # data_df = read_from_database(query)
    data_df = pd.read_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/csv_outputs/leboncoin/output.csv')

    # Transform text into digital format:
    data_df['surface'] = pd.to_numeric(data_df['surface'], errors='coerce')
    data_df['nb_rooms'] = pd.to_numeric(data_df['nb_rooms'], errors='coerce')
    data_df['nb_bedrooms'] = pd.to_numeric(data_df['nb_bedrooms'], errors='coerce')
    data_df['latitude'] = pd.to_numeric(data_df['latitude'], errors='coerce')
    data_df['longitude'] = pd.to_numeric(data_df['longitude'], errors='coerce')

    #To be replaced with the SQL query:
    filter_place = ['ville', 'zipcode']
    for filter in filter_place:
        if property_infos[filter] is not None:
            data_df = data_df[data_df[filter]== property_infos[filter]]

    # # First filter, only keeps matching data
    filter_rooms = ['nb_rooms']
    for filter in filter_rooms:
        value = property_infos[filter]
        if value is not None:
            data_df = data_df[((max(0,value -1) <= data_df[filter]) & (data_df[filter] <= value + 1)) | pd.isna(data_df[filter])]

    filter_surface = ['surface']
    for filter in filter_surface:
        value = property_infos[filter]
        if value is not None:
            data_df = data_df[((value*0.75 <= data_df[filter]) & (data_df[filter] <= value*1.25)) | pd.isna(data_df[filter])]


    def is_within_distance(row, point_ref, max_distance_km):
        if pd.isna(row['latitude']) or pd.isna(row['longitude']):
            return True
        point = (row['latitude'], row['longitude'])
        return geodesic(point, point_ref).kilometers <= max_distance_km


    lat= property_infos['latitude']
    lng = property_infos['longitude']
    if lat is not None and lng is not None:
        data_df = data_df[data_df.apply(is_within_distance, axis=1, point_ref=(lat, lng), max_distance_km= 5)]





    # Defines the weight of each scoring feature (from 1 to 10)
    poids = {'type' : 8, 'meuble' :3, 'nb_rooms' : 10 ,'DPE' : 10, 'GES' : 10, 'ascenseur' : 5, 'numero_etage' : 7, 'nb_etages' : 7, 'charges' : 10, 'caution' : 5, 'piscine' : 5, 'nb_bedrooms' : 5, 'parking' : 3, 'quartier' : 5, 'cave' : 3,'terrasse' : 4}
    poids_surface = {'surface' : 10}
    poids_nom = {'host_name' : 10}
    
    # Cost calculation for each line
    data_df["cost"] = (
        data_df.apply(
            score_calculation, axis=1, property_infos=property_infos, poids=poids, poids_surface = poids_surface, poids_nom = poids_nom
        )
        * 100
    )

    return data_df


