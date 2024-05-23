from collections import Counter
import re
import pandas as pd

# Fonction pour extraire les chiffres
def extract_number(s):
    """
    Extracts a floating number from a string containing a formatted number, or returns the value if it is already a number.

    Args:
        s (str, int, float): The string containing the number or the number directly.

    Returns:
        float: The floating number extracted from the string, or the input value if already a number. Returns None if no number is found.  
    """
    # Vérifier si l'entrée est déjà un entier ou un flottant
    if isinstance(s, (int, float)):
        return float(s)
    
    # Utiliser une regex pour extraire les parties numériques
    match = re.search(r'(\d{1,3}(?:\s?\d{3})*)(?:[.,]\d+)?', str(s))
    if match:
        # Nettoyer la chaîne correspondante
        number_str = match.group(0).replace(' ', '').replace(',', '.')
        return float(number_str)
    
    return None

# Fonction pour compter les lits
def count_beds(bed_str):
    if pd.isna(bed_str):
        return [0, 0, 0, 0, 0]
    
    # Normaliser les pluriels en singuliers pour comptage
    normalized_str = bed_str.replace('lits doubles', 'lit double')\
                             .replace('canapés convertibles', 'canapé convertible')\
                             .replace('lits simples', 'lit simple')\
                             .replace('canapés', 'canapé')\
                             .replace('lits superposés', 'lit superposé')
    
    # Trouver tous les lits et leurs quantités
    beds = re.findall(r'(\d+) (lit double|canapé convertible|lit simple|canapé|lit superposé)', normalized_str)
    
    # Compter les lits par type
    bed_counts = Counter({key: 0 for key in ['lit double', 'canapé convertible', 'lit simple', 'canapé', 'lit superposé']})
    for count, bed_type in beds:
        bed_counts[bed_type] += int(count)
    
    return [bed_counts['lit double'], bed_counts['canapé convertible'], bed_counts['lit simple'], bed_counts['canapé'], bed_counts['lit superposé']]

def process_output(data : pd.DataFrame) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        df (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """
    # Column pre-processing with number extraction
    data['nb_voyageurs'] = data['nb_voyageurs'].apply(extract_number)
    data['nb_sdb'] = data['nb_sdb'].apply(lambda x: extract_number(x.split(' ')[0]))
    data['price'] = data['price'].apply(lambda x: extract_number(x.replace('€', '').replace('\xa0', '').replace(' ', '')))
    data['nb_bedrooms'] = data['nb_bedrooms'].apply(lambda x: extract_number(x.split(' ')[0]))
    data['nb_rooms'] = data['nb_rooms'].apply(extract_number)


    # Counting bed types
    bed_types = data['nb_beds'].apply(count_beds)
    bed_columns = ['nb_lits_doubles', 'nb_canapes_convertibles', 'nb_lits_simples', 'nb_canapes', 'nb_lit_superposes']
    for idx, col in enumerate(bed_columns):
        data[col] = [beds[idx] for beds in bed_types]

    # Check the presence of items in the equipment column and create new columns
    equipement_features = ['piscine', 'parking', 'Lave-linge', 'climatisation', 'balcon', 'Sèche-linge', 'Baignoire']
    for feature in equipement_features:
        data[feature] = data['equipements'].apply(lambda x: 1 if feature.lower() in x.lower() else 0)

    # Sélectionner les colonnes nécessaires pour le fichier de sortie
    columns_to_keep = ['url','title','nb_voyageurs', 'nb_sdb', 'host_name', 'equipements', 'description', 'nb_rooms', 'numero_etage', 'surface', 'price', 'nb_bedrooms'] + bed_columns + equipement_features
    processed_data = data[columns_to_keep]

    return processed_data





