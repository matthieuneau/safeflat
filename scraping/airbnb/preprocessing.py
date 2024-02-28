from collections import Counter
import re
import pandas as pd

file_path = 'output.csv'
data = pd.read_csv(file_path)

# Fonction pour extraire les chiffres
def extract_number(text):
    if pd.isnull(text):
        return 0
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else 0

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

def preprocess_csv(input_file_path, output_file_path):
    # Charger le fichier CSV
    data = pd.read_csv(input_file_path)

    # Prétraitement des colonnes avec extraction des chiffres
    data['nb_voyageurs'] = data['nb_voyageurs'].apply(extract_number)
    data['nb_sdb'] = data['nb_sdb'].apply(lambda x: extract_number(x.split(' ')[0]))
    data['price'] = data['price'].apply(lambda x: extract_number(x.replace('€', '').replace('\xa0', '').replace(' ', '')))
    data['nb_bedrooms'] = data['nb_bedrooms'].apply(lambda x: extract_number(x.split(' ')[0]))

    # Gérer la colonne nb_rooms si elle existe
    if 'nb_rooms' in data.columns:
        data['nb_rooms'] = data['nb_rooms'].apply(extract_number)
    else:
        data['nb_rooms'] = 0  # Ajouter une colonne nb_rooms avec des zéros si elle n'existe pas

    # Compter les types de lits
    bed_types = data['nb_beds'].apply(count_beds)
    bed_columns = ['nb_lits_doubles', 'nb_canapes_convertibles', 'nb_lits_simples', 'nb_canapes', 'nb_lit_superposes']
    for idx, col in enumerate(bed_columns):
        data[col] = [beds[idx] for beds in bed_types]

    # Vérifier la présence des éléments dans la colonne equipements et créer de nouvelles colonnes
    equipement_features = ['piscine', 'parking', 'Lave-linge', 'climatisation', 'balcon', 'Sèche-linge', 'Baignoire']
    for feature in equipement_features:
        data[feature] = data['equipements'].apply(lambda x: 1 if feature.lower() in x.lower() else 0)

    # Sélectionner les colonnes nécessaires pour le fichier de sortie
    columns_to_keep = ['host_name', 'equipements', 'description', 'nb_rooms', 'numero_etage', 'surface', 'price', 'nb_bedrooms'] + bed_columns + equipement_features
    processed_data = data[columns_to_keep]

    # Sauvegarder dans un nouveau fichier CSV
    processed_data.to_csv(output_file_path, index=False)





