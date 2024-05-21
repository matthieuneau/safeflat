from utils import *

def score_calculation(row, property_infos, poids):
    total_poids = 0
    matching_poids = 0
    
    for key, value in property_infos.items():
        if value is not None and key in poids:
            total_poids += poids[key]
            if row[key] == value:
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
    query = "SELECT * FROM pap"

    if property_infos['location'] is not None:
        query += f" WHERE location = '{property_infos['location']}'"  # Placeholder for location


    # Read data from the database and apply first filter (query):
    data_df = read_from_database(query)

    # Transform text into digital format:
    data_df['surface'] = pd.to_numeric(data_df['surface'], errors='coerce')
    data_df['terrain'] = pd.to_numeric(data_df['terrain'], errors='coerce')
    data_df['nb_rooms'] = pd.to_numeric(data_df['nb_rooms'], errors='coerce')
    data_df['nb_bedrooms'] = pd.to_numeric(data_df['nb_bedrooms'], errors='coerce')

    # First filter, only keeps matching data
    for feature, value in property_infos.items():
        if feature in ['nb_rooms', 'nb_bedrooms']:
            data_df = data_df[((max(0,value -1) <= data_df[feature]) & (data_df[feature] <= value + 1)) | pd.isna(data_df[feature])] #Only keeps the lines with the corresponding value +-1 or Nan value
        elif feature in ['surface']:
            if data_df[feature] is not None and value is not None:
                data_df = data_df[((value*0.75 <= data_df[feature]) & (data_df[feature] <= value*1.25))] 
        elif feature in ['terrain']:
            if data_df[feature] is not None and value is not None:
                data_df = data_df[((value*0.75 <= data_df[feature]) & (data_df[feature] <= value*1.25))] 
 

    # Defines the weight of each scoring feature (from 1 to 10)
    poids = {'nb_rooms': 10,'nb_bedrooms':10, 'surface': 10, 'terrain':10, 'energy':8, 'ges':8, 'bills': 10, 'piscine': 4, 'type_de_bien': 10, 'parking': 5, 'quartier': 10, 'meuble': 4, 'nombre_d\'etages' : 7, 'numero_d\'etage' : 10, 'ascenseur': 5, 'terrasse' : 7 }

    # Cost calculation for each line
    data_df['cost'] = data_df.apply(score_calculation, axis=1, property_infos=property_infos, poids=poids)*100

    
    return data_df

#Example of a property to protect:
property_infos_same = {

    'location': 'Paris 11e (75011)',
    'energy' : 'F', 
    'ges' : None, 
    'nb_rooms' : 3,
    'nb_bedrooms' : 2, 
    'surface' : 50, 
    'terrain' : None,
    'bills' : '50',
    'piscine' : 'Non',
    'type_de_bien' : 'appartement', 
    'parking' : 'oui',
    'quartier' : None, 
    'meuble' : None,
    'nombre_d\'etages' : None,
    'numero_d\'etage' : '1',
    'ascenseur' : 'oui',
    'cave' : None,
    'terrasse' : 'oui'

}

property_infos_1 = {

    'location': 'Strasbourg (67000)',
    'energy' : 'E', 
    'ges' : 'E', 
    'nb_rooms' : 3,
    'nb_bedrooms' : 1, 
    'surface' : 52.5, 
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

if __name__ == "__main__":
    filtered_data = filter_and_score(property_infos_same)
    print(filtered_data)

    # data = read_from_database("SELECT * FROM pap")
    # print(data)
    filtered_data.to_csv('C:/Users/hennecol/Documents/safeflat/scraping/pap-oxylab/csv_outputs/output_score.csv')