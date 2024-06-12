import pandas as pd

def process_output(data : dict) -> pd.DataFrame:
    """Taking care of all the processing of the scraped data, EXCEPT PROCESSING THE DESCRIPTION, which is done by calling ChatGPT

    Args:
        df (pd.DataFrame): contains the raw scraped data

    Returns:
        pd.DataFrame: contains the processed data
    """
    # Convert all string objects in the DataFrame to lowercase
    data = data.map(lambda s: s.lower() if type(s) == str else s)

    #Convert 1 = oui, 2 = non
    data['meuble'] = data['meuble'].replace({'1': 'oui', '2': 'non'})

    # Replace "Not Available" and "N/A" with None in the DataFrame
    data.replace("not available", None, inplace=True)
    data.replace("N/A", None, inplace=True)

    columns_to_keep = ['url', 'id', 'titre', 'first_publication_date', 'prix', 'type', 'meuble', 'surface', 'nb_rooms', 'DPE', 'GES', 'ascenseur', 'numero_etage', 'nb_etages', 'charges', 'caution', 'region', 'departement', 'ville', 'zipcode', 'latitude', 'longitude', 'host_name', 'piscine', 'nb_bedrooms', 'parking', 'quartier', 'cave', 'terrasse']
    processed_data = data[columns_to_keep]

    return processed_data