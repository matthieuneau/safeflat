from collections import Counter
import re
import pandas as pd


# Function for extracting numbers
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


# Exctracting floor level
def extract_after_etage(s):
    # Convert the input to a string if it isn't already
    s = str(s)
    
    # Check if the string is already in X/Y or X/- format
    already_formatted_match = re.match(r'^\d+[/\-]\d*$', s)
    if already_formatted_match:
        return s  # The string is already in the desired format, so we return it directly

    # Pattern regex to find and capture everything after "Étage"
    etage_match = re.search(r'étage\s*(.*)', s)
    if etage_match:
        return etage_match.group(1)  # Returns the match found after "Étage"
    
    # If none of the above conditions are met, returns None
    return None


#Extracting Surface
def extract_surface(text, surface_type):
    if pd.isnull(text):
        return None
    pattern = re.compile(rf'{surface_type} (\d+) m²', re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return int(match.group(1))  
    else:
        return None
    
#Extracting Exposure
def extract_exposition(text):
    if pd.isnull(text):
        return None
    # Search for a pattern where "Exposition" is followed by any characters up to a comma
    match = re.search(r'Exposition\s([^,]+),', text)
    if match:
        return match.group(1)  # Group 1 contains the part of the string between "Exposition" and the first comma.
    else:
        return None

#Checks if there is an elevator
def check_ascenseur(value):
    if pd.isnull(value):
        return None
    if 'Pas d\'ascenseur' in value:
        return 0
    if 'Ascenseur : non communiqué' in value or 'Ascenseur' not in value:
        return None
    if 'Ascenseur' in value:
        return 1
    
list_type = ["appartement", "appartement exécutif", "bateau", "bungalow", "cabane/hutte", "camping-car", "caravane", "chalet", "chambre / maison d'hôtes", "château", "cottage", "domaine", "ferme", "grange aménagée", "hôtel / auberge", "immeuble", "logement en copropriété", "maison", "maison de campagne", "maison de ville", "mas", "mobil home", "moulin", "pavillon", "péniche", "riad", "studio", "suites d'hôtel", "terrain de camping", "tour", "villa", "yacht", "villa vacances tout compris"]

def process_output(df : pd.DataFrame) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        df (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """
    df['type'] = df['title'].apply(lambda x: x.split()[0])
    df['meublé'] = df['title'].apply(lambda x: 1 if "meublé" in x else 0)
    df['price'] = df['price'].apply(lambda x : extract_number(x))
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df[['city', 'zipcode']] = df['city and zip code'].str.split('(', expand=True)
    df['city'] = df['city'].str.strip()
    df['zipcode'] = df['zipcode'].str.replace(')', '')
    df['nb_rooms'] = df['nb_rooms'].apply(lambda x : extract_number(x))
    df['nb_rooms'] = df['nb_rooms'].astype('Int64')
    df['nb_bedrooms'] = df['nb_bedrooms'].apply(lambda x : extract_number(x))
    df['nb_bedrooms'] = df['nb_bedrooms'].astype('Int64')
    df['surface'] = df['surface'].apply(lambda x : extract_number(x))
    df['numero_etage'] = df['numero_etage'].apply(extract_after_etage)
    df['balcon'] = df['Extérieur'].apply(lambda x: 1 if pd.notnull(x) and 'Balcon' in x else 0)
    df['terrasse'] = df['Extérieur'].apply(lambda x: 1 if pd.notnull(x) and 'Terrasse' in x else 0)
    df['jardin'] = df['Extérieur'].apply(lambda x: 1 if pd.notnull(x) and 'Jardin' in x else 0)
    df['surface_balcon'] = df['Extérieur'].apply(lambda x: extract_surface(x, "Balcon"))
    df['surface_terrasse'] = df['Extérieur'].apply(lambda x: extract_surface(x, "Terrasse"))
    df['surface_jardin'] = df['Extérieur'].apply(lambda x: extract_surface(x, "Jardin"))
    df['exposition'] = df['Cadre et situation'].apply(lambda x: extract_exposition(x))
    df['meublé'] = df['title'].apply(lambda x: 1 if "meublé" in x else 0)
    df['cave'] = df['Surfaces annexes'].apply(lambda x: 1 if pd.notnull(x) and 'Cave' in x else 0)
    df['parking'] = df['Surfaces annexes'].apply(lambda x: 1 if pd.notnull(x) and 'Parking' in x else 0)
    df['garage'] = df['Surfaces annexes'].apply(lambda x: 1 if pd.notnull(x) and 'Garage' in x else 0)
    df['box'] = df['Surfaces annexes'].apply(lambda x: 1 if pd.notnull(x) and 'Box' in x else 0)
    df['ascenseur'] = df['Services et accessibilité'].apply(check_ascenseur)
    df['ascenseur'] = df['ascenseur'].astype('Int64')
    df['interphone'] = df['Services et accessibilité'].apply(lambda x: 1 if pd.notnull(x) and 'Interphone' in x else 0)
    df['gardien'] = df['Services et accessibilité'].apply(lambda x: 1 if pd.notnull(x) and 'Gardien' in x else 0)
    df['salle de bain (Baignoire)'] = df['Hygiène'].apply(lambda x: 1 if pd.notnull(x) and 'baignoire' in x else 0)
    df['salle d\'eau (douche)'] = df['Hygiène'].apply(lambda x: 1 if pd.notnull(x) and 'douche' in x else 0)
    df['surface_salon'] = df['Pièces à vivre'].apply(lambda x: extract_surface(x, "Séjour / salon"))
    df['surface_salle_a_manger'] = df['Pièces à vivre'].apply(lambda x: extract_surface(x, "Salle à manger"))
    df['loyer_charges_comprises'] = df['loyer_charges_comprises'].apply(lambda x : extract_number(x))
    df['charges_forfaitaires'] = df['charges_forfaitaires'].apply(lambda x : extract_number(x))
    df['complement_loyer'] = df['complement_loyer'].apply(lambda x : extract_number(x))
    df['depot_garantie'] = df['depot_garantie'].apply(lambda x : extract_number(x))
    df['loyer_base'] = df['loyer_base'].apply(lambda x : extract_number(x))




    columns_to_keep = ['type','meublé', 'host_name', 'price', 'city', 'zipcode', 'neighbourhood','nb_rooms', 'nb_bedrooms', 'surface', 'numero_etage', 'description', 'balcon', 'terrasse', 'jardin', 'surface_balcon', 'surface_terrasse', 'surface_jardin', 'exposition', 'cave', 'parking', 'garage', 'box', 'ascenseur', 'interphone', 'gardien', 'salle de bain (Baignoire)', 'salle d\'eau (douche)', 'surface_salon', 'surface_salle_a_manger','Diagnostic de performance énergétique (DPE)', 'Indice d\'émission de gaz à effet de serre (GES)','loyer_charges_comprises', 'charges_forfaitaires', 'complement_loyer', 'depot_garantie' ]

    processed_data = df[columns_to_keep]

    return processed_data