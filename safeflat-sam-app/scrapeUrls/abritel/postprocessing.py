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
    data['nb_bedrooms'] = data['nb_bedrooms'].apply(extract_bedrooms)
    data['nb_bathrooms'] = data['nb_bathrooms'].apply(extract_bathrooms)
    data['baignoire'] = data['baignoire'].apply(lambda x: 'oui' if 'baignoire' in x.lower() else None)
    data['douche'] = data['douche'].apply(lambda x: 'oui' if 'douche' in x.lower() else None)
    data['lits_doubles'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'lit double|grand lit|futon \(double\)'))
    data['lits_simples'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'lit simple'))
    data['canapes_convertibles'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'canapé-lit'))
    data['lits_superposes'] = data['beds'].apply(lambda x: count_beds(x.lower(), r'lit superposé'))

    spaces = ["terrasse", "balcon", "jardin", "cave", "parking", "garage", "box"]
    for space in spaces:
        data[space] = data['other_spaces'].apply(lambda x: 'oui' if space in x.lower() else None)

    data['host_type'] = data['host_type'].apply(lambda x: x.split()[1] if x and len(x.split()) > 1 else None)

    amenities_list = ["piscine", "ascenseur", "interphone", "gardien", "lave-linge", "sèche-linge", "climatisation"]
    for amenity in amenities_list:
        data[amenity] = data['amenities'].apply(lambda x: 'oui' if any(amenity in item.lower() for item in x) else None)

    # Sélectionner les colonnes nécessaires pour le fichier de sortie
    columns_to_keep = ['url','ville','surface', 'nb_bedrooms', 'nb_bathrooms', 'baignoire', 'douche', 'lits_doubles', 'lits_simples', 'canapes_convertibles', 'lits_superposes', 'host_name', 'latitude', 'longitude', 'type', 'host_type',"terrasse", "balcon", "jardin", "cave", "parking", "garage", "box", "piscine", "ascenseur", "interphone", "gardien", "lave-linge", "sèche-linge", "climatisation"]
    processed_data = data[columns_to_keep]

    processed_data.replace('Not Available', None, inplace=True)

    return processed_data

#For test purpose only:
# data_bdd = pd.read_csv('C:/Users/hennecol/Documents/safeflat/safeflat-sam-app/csv_outputs/abritel/output_before_process.csv')
# data_processed = process_output(data_bdd)
# data_processed.to_csv('C:/Users/hennecol/Documents/safeflat/safeflat-sam-app/csv_outputs/abritel/output_processed.csv')