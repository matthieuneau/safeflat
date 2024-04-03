import pandas as pd

def filtrer_et_scorer_biens(data_path, critere_filtre):
    """
    Filtre les biens selon les critères spécifiés et calcule un score de correspondance pour les biens restants.
    
    Args:
    data_path (csv): Path to the raw csv file
    critere_filtre (dict): Dictionary containing the characteristics of the property to be searched
    
    Returns:
    pd.DataFrame: DataFrame of filtered propreties with a match score.
    """

    input_file = pd.read_csv(data_path)
    filtered_data = input_file.copy()

    
    # First filter, only keeps matching data
    for feature, value in critere_filtre.items():
        if feature in ['type', 'city','zipcode','nb_rooms', 'nb_bedrooms', 'numero_etage','balcon','terrasse', 'jardin', 'salle de bain (Baignoire)', 'salle d\'eau (douche)', 'ascenseur']:
            filtered_data = filtered_data[(filtered_data[feature] == value) | pd.isna(filtered_data[feature])] #Only keeps the lines with the corresponding value or Nan value
        elif feature in ['surface', 'surface_jardin','surface_salon', 'surface_salle_a_manger']:
            filtered_data = filtered_data[((value -1.5 <= filtered_data[feature]) & (filtered_data[feature] <= value + 1.5)) | pd.isna(filtered_data[feature])] 
        elif feature in ['surface_balcon', 'surface_terrasse']:
            filtered_data = filtered_data[((value -0.5 <= filtered_data[feature]) & (filtered_data[feature] <= value + 0.5)) | pd.isna(filtered_data[feature])]
 

    # Defines the weight of each scoring feature
    poids = {'neighbourhood':10, 'exposition' : 10, 'cave': 2, 'parking':2, 'garage':2, 'box':2, 'interphone':3, 'gardien':2, 'Diagnostic de performance énergétique (DPE)':10,'Indice d\'émission de gaz à effet de serre (GES)':10}
    total = sum(poids.values())

    # Sets the score to 0:
    filtered_data['score_correspondance'] = 0

    # For the other features, add their weight to the score if there is a match 
    for feature in poids.keys():
        if feature in critere_filtre:
            filtered_data['score_correspondance'] += (filtered_data[feature] == critere_filtre[feature]) * poids[feature]/total
    
    
    return filtered_data

# Exemple d'utilisation de la fonction avec des critères hypothétiques
critere_filtre = {
    'type': 'Appartement',  # Choisi en se basant sur les types disponibles dans le fichier
    'meublé': 1,  # Exemple de critère binaire (0 ou 1)
    'city': 'Paris',  # Utilisation d'une ville présente dans le fichier
    'zipcode': 75010,  # Code postal correspondant à la ville
    'nb_rooms': 2,  # Spécifié arbitrairement
    'nb_bedrooms': 1,  # Extrait d'une des lignes du fichier
    'surface': 45,  # Moyenne basée sur les surfaces disponibles dans le fichier
    'numero_etage': '0/0',  # Extrait d'une ligne, supposant une structure 'étage/total'
    'ascenseur': 1,  # Supposé pour le critère d'ascenseur
    'interphone': 1,  # Choisi arbitrairement
    'gardien': 0,  # Choisi arbitrairement
    'salle de bain (Baignoire)': 0,  # Basé sur les options disponibles
    'salle d\'eau (douche)': 1,  # Choisi en fonction des données du fichier
    'loyer_charges_comprises': 900,  # Défini arbitrairement dans une fourchette plausible
    'Diagnostic de performance énergétique (DPE)' : 'D',
    'garage' : 0,
    'interphone' : 0,
    'gardien' : 0

}


score_biens = filtrer_et_scorer_biens('output_preprocessed.csv', critere_filtre)
print(score_biens)