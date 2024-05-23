import pandas as pd

def filtrer_et_scorer_biens(data, critere_filtre):
    """
    Filtre les biens selon les critères spécifiés et calcule un score de correspondance pour les biens restants.
    
    Args:
    data (pd.DataFrame): DataFrame contenant les données des biens.
    critere_filtre (dict): Dictionnaire contenant les critères de filtrage (nb_sdb, nb_rooms, balcon, Baignoire).
    
    Returns:
    pd.DataFrame: DataFrame des biens filtrés avec un score de correspondance.
    """

    poids = {'host_name':10, 'nb_lits_doubles' : 2, 'nb_canapes_convertibles': 2, 'nb_lits_simples':2, 'nb_canapes':2, 'nb_lit_superposes':2, 'parking':2, 'Lave-linge':3, 'Sèche-linge':3,'climatisation':2}
    total = sum(poids.values())

    # Filtrage initial selon les critères
    input_file = pd.read_csv(data)
    filtered_data = input_file.copy()
    for feature, value in critere_filtre.items():
        if feature in ['balcon', 'Baignoire','nb_sdb','nb_bedrooms','piscine']:  # Pour ces caractéristiques, 1 signifie la présence souhaitée
            filtered_data = filtered_data[filtered_data[feature] == value]

    filtered_data['score_correspondance'] = 0

    # Pour les autres caractéristiques, ajouter 20 au score si elles correspondent
    scoring_features = ['host_name', 'nb_lits_doubles', 'nb_canapes_convertibles', 'nb_lits_simples', 'nb_canapes', 'nb_lit_superposes', 'parking', 'Lave-linge', 'Sèche-linge','climatisation']
    for feature in scoring_features:
        if feature in critere_filtre:
            filtered_data['score_correspondance'] += (filtered_data[feature] == critere_filtre[feature]) * poids[feature]/total
    
    
    return filtered_data

# Exemple d'utilisation de la fonction avec des critères hypothétiques
critere_filtre = {
    'nb_sdb': 2,
    'host_name' : 'Matthieu',
    'nb_bedrooms': 3,
    'nb_lits_double': 0,
    'nb_canapes_convertibles' : 2,
    'nb_lits_simples' : 0,
    'nb_canapes' : 0,
    'nb_lit_superposes' : 0,
    'piscine' : 0,
    'parking' : 1,
    'Lave-linge': 0
}

score_biens = filtrer_et_scorer_biens('output_preprocessed.csv', critere_filtre)
print(score_biens)