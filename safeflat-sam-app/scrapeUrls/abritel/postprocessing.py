import pandas as pd
import re

def extract_surface(surface):
    match = re.search(r'(\d+)\s?m²', surface)
    return int(match.group(1)) if match else None

def extract_bedrooms(bedroom):
    match = re.search(r'(\d+)\s?chambre', bedroom)
    return int(match.group(1)) if match else None

def extract_bathrooms(bathroom):
    match = re.search(r'(\d+)\s?salle[s]?\s?de\s?bain[s]?', bathroom)
    return int(match.group(1)) if match else None

def count_beds(bed_description, bed_type):
    matches = re.findall(bed_type, bed_description)
    return len(matches) if matches else None


def process_output(data : dict) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        df (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """


    data['ville'] = data['location'].apply(lambda x: x.split(',')[0])
    data['surface'] = data['surface'].apply(extract_surface)
    data['nb_chambres'] = data['nb_bedrooms'].apply(extract_bedrooms)
    data['nb_bathrooms'] = data['nb_bathrooms'].apply(extract_bathrooms)
    data['baignoire'] = data['baignoire'].apply(lambda x: 'oui' if 'baignoire' in x.lower() else None)
    data['douche'] = data['douche'].apply(lambda x: 'oui' if 'douche' in x.lower() else None)
    data['lits_doubles'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'lit double|grand lit|futon \(double\)'))
    data['lits_simples'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'lit simple'))
    data['canapes_convertibles'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'canapé-lit'))
    data['lits_superposes'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'lit superposé'))






    # Sélectionner les colonnes nécessaires pour le fichier de sortie
    columns_to_keep = ['url','title', 'type', 'ville', 'person_capacity', 'latitude', 'longitude', 'nb_bedrooms', 'nb_beds', 'nb_bathrooms', 'host_name', 'lave-linge', 'sèche-linge', 'lave-vaisselle', 'balcon', 'terrasse', 'parking', 'ascenseur', 'climatisation', 'piscine', 'baignoire', 'lits_doubles', 'lits_simples', 'canapes_convertibles', 'lits_superposes']
    processed_data = data[columns_to_keep]

    return processed_data