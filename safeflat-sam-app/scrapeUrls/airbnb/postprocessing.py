from collections import Counter
import re
import pandas as pd


# Fonction pour extraire le nombre de lits doubles
def extract_lits_doubles(liste_types_lits):
    match = re.search(r'(\d+)\s*lits?\s*doubles?', liste_types_lits)
    if match:
        return int(match.group(1))
    return 0

# Fonction pour extraire le nombre de lits simples
def extract_lits_simples(liste_types_lits):
    match = re.search(r'(\d+)\s*lits?\s*simples?', liste_types_lits)
    if match:
        return int(match.group(1))
    return 0

# Fonction pour extraire le nombre de canapés convertibles
def extract_canapes_convertibles(liste_types_lits):
    match = re.search(r'(\d+)\s*canapés?\s*convertibles?', liste_types_lits)
    if match:
        return int(match.group(1))
    return 0

# Fonction pour extraire le nombre de lits superposés
def extract_lits_superposes(liste_types_lits):
    match = re.search(r'(\d+)\s*lits?\s*superposés?', liste_types_lits)
    if match:
        return int(match.group(1))
    return 0


def extract_number_of_bedrooms(details_list):
    for detail in details_list:
        if "chambre" in detail:
            return int(detail.split()[0])
    return None  # Valeur par défaut si non trouvée

def extract_number_of_beds(details_list):
    for detail in details_list:
        if "lit" in detail:
            return int(detail.split()[0])
    return None  # Valeur par défaut si non trouvée

def extract_number_of_bathrooms(details_list):
    for detail in details_list:
        if "salle de bain" in detail:
            return int(detail.split()[0].replace("\xa0", ""))
    return None  # Valeur par défaut si non trouvée

def process_output(data : dict) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        df (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """
    #Extract type:
    data['type'] = data['type'].str.lower()
    data['type'] = data['type'].apply(lambda x: 'appartement' if 'appartement' in x else ('maison' if 'maison' in x else ('studio' if 'studio' in x else x)))


    # Extract data from property_infos_list:
    data['nb_bedrooms'] = data['property_infos_list'].apply(extract_number_of_bedrooms)
    data['nb_beds'] = data['property_infos_list'].apply(extract_number_of_beds)
    data['nb_bathrooms'] = data['property_infos_list'].apply(extract_number_of_bathrooms)

    #Extract host name:
    data['host_name'] = data['host_name'].apply(lambda x: x.split(":")[1].strip() if isinstance(x, str) and "Hôte" in x else x)

    def convert_to_str_list(amenities_list):
        if isinstance(amenities_list, list):
            return [str(item).lower() for item in amenities_list if isinstance(item, str)]
        return []

    data['amenities'] = data['amenities'].apply(convert_to_str_list)
    
    # Function to check for an amenity in property_infos_list
    def has_amenity(amenities_list, amenity):
        return 'oui' if any(amenity in item for item in amenities_list) else 'non'



    # Apply the function to each row in the DataFrame
    data['lave-linge'] = data['amenities'].apply(lambda x: has_amenity(x, 'lave-linge'))
    data['sèche-linge'] = data['amenities'].apply(lambda x: has_amenity(x, 'sèche-linge'))
    data['lave-vaisselle'] = data['amenities'].apply(lambda x: has_amenity(x, 'lave-vaisselle'))
    data['balcon'] = data['amenities'].apply(lambda x: has_amenity(x, 'balcon'))
    data['terrasse'] = data['amenities'].apply(lambda x: has_amenity(x, 'terrasse'))
    data['parking'] = data['amenities'].apply(lambda x: has_amenity(x, 'parking'))
    data['ascenseur'] = data['amenities'].apply(lambda x: has_amenity(x, 'ascenseur'))
    data['climatisation'] = data['amenities'].apply(lambda x: has_amenity(x, 'climatisation'))
    data['piscine'] = data['amenities'].apply(lambda x: has_amenity(x, 'piscine'))
    data['baignoire'] = data['amenities'].apply(lambda x: has_amenity(x, 'baignoire'))

    # Convert lists in beds_type to strings
    data['beds_type'] = data['beds_type'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    #Extract data from beds_type:
    data['lits_doubles'] = data['beds_type'].apply(extract_lits_doubles)
    data['lits_simples'] = data['beds_type'].apply(extract_lits_simples)
    data['canapes_convertibles'] = data['beds_type'].apply(extract_canapes_convertibles)
    data['lits_superposes'] = data['beds_type'].apply(extract_lits_superposes)

    # Sélectionner les colonnes nécessaires pour le fichier de sortie
    columns_to_keep = ['url','title', 'type', 'ville', 'person_capacity', 'latitude', 'longitude', 'nb_bedrooms', 'nb_beds', 'nb_bathrooms', 'host_name', 'lave-linge', 'sèche-linge', 'lave-vaisselle', 'balcon', 'terrasse', 'parking', 'ascenseur', 'climatisation', 'piscine', 'baignoire', 'lits_doubles', 'lits_simples', 'canapes_convertibles', 'lits_superposes']
    processed_data = data[columns_to_keep]

    return processed_data





