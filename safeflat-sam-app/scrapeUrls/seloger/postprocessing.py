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

def extract_id(url):
    # Utiliser une expression régulière pour extraire l'ID
    pattern = r'/(\d+)\.htm'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
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

def split_etage_column(df):
    numero_etage = []
    nb_etages = []

    for etage in df['etage']:
        try:
            etage_split = etage.split('/')
            if len(etage_split) == 2:
                numero_etage.append(int(etage_split[0]) if etage_split[0].isdigit() else None)
                nb_etages.append(int(etage_split[1]) if etage_split[1].isdigit() else None)
            else:
                numero_etage.append(None)
                nb_etages.append(None)
        except Exception as e:
            numero_etage.append(None)
            nb_etages.append(None)

    df['numero_etage'] = numero_etage
    df['nb_etages'] = nb_etages

    return df


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
        return 'non'
    if 'Ascenseur : non communiqué' in value or 'Ascenseur' not in value:
        return None
    if 'Ascenseur' in value:
        return 'oui'
    
def extract_quartier(text):
    prefix = "Quartier "
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
    
list_type = ["appartement", "appartement exécutif", "bateau", "bungalow", "cabane/hutte", "camping-car", "caravane", "chalet", "chambre / maison d'hôtes", "château", "cottage", "domaine", "ferme", "grange aménagée", "hôtel / auberge", "immeuble", "logement en copropriété", "maison", "maison de campagne", "maison de ville", "mas", "mobil home", "moulin", "pavillon", "péniche", "riad", "studio", "suites d'hôtel", "terrain de camping", "tour", "villa", "yacht", "villa vacances tout compris"]

def process_output(df : pd.DataFrame) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        df (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """

    df['id'] = df['url'].apply(lambda x: extract_id(x))
    df['type'] = df['title'].apply(lambda x: x.split()[0])
    df['meuble'] = df['title'].apply(lambda x: 'oui' if "meublé" in x else 'non')
    df['price'] = df['price'].apply(lambda x : extract_number(x))
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df[['ville', 'zipcode']] = df['city and zip code'].str.split('(', expand=True)
    df['ville'] = df['ville'].str.strip()
    df['zipcode'] = df['zipcode'].str.replace(')', '')
    df['nb_rooms'] = df['nb_rooms'].apply(lambda x : extract_number(x))
    df['nb_rooms'] = df['nb_rooms'].astype('Int64')
    df['nb_bedrooms'] = df['nb_bedrooms'].apply(lambda x : extract_number(x))
    df['nb_bedrooms'] = df['nb_bedrooms'].astype('Int64')
    df['surface'] = df['surface'].apply(lambda x : extract_number(x))
    df['etage'] = df['etage'].apply(extract_after_etage)
    df['balcon'] = df['Extérieur'].apply(lambda x: 'oui' if pd.notnull(x) and 'Balcon' in x else 'non')
    df['terrasse'] = df['Extérieur'].apply(lambda x: 'oui' if pd.notnull(x) and 'Terrasse' in x else 'non')
    df['jardin'] = df['Extérieur'].apply(lambda x: 'oui' if pd.notnull(x) and 'Jardin' in x else 'non')
    df['surface_balcon'] = df['Extérieur'].apply(lambda x: extract_surface(x, "Balcon"))
    df['surface_terrasse'] = df['Extérieur'].apply(lambda x: extract_surface(x, "Terrasse"))
    df['surface_jardin'] = df['Extérieur'].apply(lambda x: extract_surface(x, "Jardin"))
    df['exposition'] = df['Cadre et situation'].apply(lambda x: extract_exposition(x))
    df['cave'] = df['Surfaces annexes'].apply(lambda x: 'oui' if pd.notnull(x) and 'Cave' in x else 'non')
    df['parking'] = df['Surfaces annexes'].apply(lambda x: 'oui' if pd.notnull(x) and 'Parking' in x else 'non')
    df['garage'] = df['Surfaces annexes'].apply(lambda x: 'oui' if pd.notnull(x) and 'Garage' in x else 'non')
    df['box'] = df['Surfaces annexes'].apply(lambda x: 'oui' if pd.notnull(x) and 'Box' in x else 'non')
    df['ascenseur'] = df['Services et accessibilité'].apply(check_ascenseur)
    df['interphone'] = df['Services et accessibilité'].apply(lambda x: 'oui' if pd.notnull(x) and 'Interphone' in x else 'non')
    df['gardien'] = df['Services et accessibilité'].apply(lambda x: 'oui' if pd.notnull(x) and 'Gardien' in x else 'non')
    df['baignoire'] = df['Hygiène'].apply(lambda x: 'oui' if pd.notnull(x) and 'baignoire' in x else 'non')
    df['douche'] = df['Hygiène'].apply(lambda x: 'oui' if pd.notnull(x) and 'douche' in x else 'non')
    df['surface_salon'] = df['Pièces à vivre'].apply(lambda x: extract_surface(x, "Séjour / salon"))
    df['surface_salle_a_manger'] = df['Pièces à vivre'].apply(lambda x: extract_surface(x, "Salle à manger"))
    df['loyer_charges_comprises'] = df['loyer_charges_comprises'].apply(lambda x : extract_number(x))
    df['charges_forfaitaires'] = df['charges_forfaitaires'].apply(lambda x : extract_number(x))
    df['complement_loyer'] = df['complement_loyer'].apply(lambda x : extract_number(x))
    df['depot_garantie'] = df['depot_garantie'].apply(lambda x : extract_number(x))
    df['loyer_base'] = df['loyer_base'].apply(lambda x : extract_number(x))
    df['quartier'] = df['quartier'].apply(extract_quartier)

    df = split_etage_column(df)
    df.replace('Not Available', None, inplace=True)
    # Convert all string objects in the DataFrame to lowercase
    df = df.map(lambda s: s.lower() if type(s) == str else s)




    columns_to_keep = ['url', 'id', 'type','meuble', 'host_name', 'price', 'ville', 'zipcode', 'quartier','nb_rooms', 'nb_bedrooms', 'surface', 'description', 'balcon', 'terrasse', 'jardin', 'surface_balcon', 'surface_terrasse', 'surface_jardin', 'exposition', 'cave', 'parking', 'garage', 'box', 'ascenseur', 'interphone', 'gardien', 'numero_etage', 'nb_etages', 'baignoire', 'douche', 'surface_salon', 'surface_salle_a_manger','DPE', 'GES','loyer_charges_comprises', 'charges_forfaitaires', 'complement_loyer', 'depot_garantie' ]

    processed_data = df[columns_to_keep]

    return processed_data