from utils import *

data_df = read_from_database("SELECT * FROM pap")
data_df['surface'] = pd.to_numeric(data_df['surface'], errors='coerce')
data_df['terrain'] = pd.to_numeric(data_df['terrain'], errors='coerce')

def filter_and_score(data, property_infos):
    """
    Filters goods according to specified criteria and calculates a match score for the remaining goods.
    
    Args:
    data (pd.DataFrame): Data from the database
    property_infos (dict): Dictionary containing the characteristics of the property to be searched
    
    Returns:
    pd.DataFrame: DataFrame of filtered propreties with a match score.
    """
    
    # First filter, only keeps matching data
    for feature, value in property_infos.items():
        if feature in ['location', 'nb_rooms', 'nb_bedrooms']:
            data = data[(data[feature] == value) | pd.isna(data[feature])] #Only keeps the lines with the corresponding value or Nan value
        elif feature in ['surface']:
            data = data[((value -1.5 <= data[feature]) & (data[feature] <= value + 1.5)) | pd.isna(data[feature])] 
        elif feature in ['terrain']:
            data = data[((value -5 <= data[feature]) & (data[feature] <= value + 5)) | pd.isna(data[feature])]
 

    # Defines the weight of each scoring feature (from 1 to 10)
    poids = {'energy':10, 'ges':10, 'bills': 10, 'piscine': 4, 'type_de_bien': 10, 'parking': 5, 'quartier': 10, 'meuble': 4, 'nombre_d\'etages' : 7, 'numero_d\'etage' : 10, 'ascenceur': 5, 'terrasse' : 7 }
    total = sum(poids.values())

    # Sets the score to 0:
    data['score_correspondance'] = 0

    # For the other features, add their weight to the score if there is a match 
    for feature in poids.keys():
        if feature in property_infos:
            data['score_correspondance'] += (data[feature] == property_infos[feature]) * poids[feature]/total
    
    return data

#Example of a property to protect:
property_infos_same = {

    'location': 'Strasbourg (67000)',
    'energy' : 'E', 
    'ges' : 'E', 
    'nb_rooms' : '2',
    'nb_bedrooms' : '1', 
    'surface' : 52, 
    #'terrain' : '',
    'bills' : '150',
    'piscine' : 'Non',
    'type_de_bien' : 'appartement', 
    'parking' : 'oui',
    'quartier' : 'Hyper Centre', 
    #'meuble' : '',
    #'nombre_d\'etages' : '',
    'numero_d\'etage' : '1',
    #'ascenceur' : '',
    #'cave' : '',
    'terrasse' : 'oui'

}

filtered_data = filter_and_score(data_df, property_infos_same)
print(filtered_data)
filtered_data.to_csv('/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/pap-oxylab/csv_outputs/output_score.csv')