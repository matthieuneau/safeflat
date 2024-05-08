import json

def print_json_structure(data, indent=0):
    """Imprime la structure de l'objet JSON avec les clés."""
    if isinstance(data, dict):
        for key in data:
            print('  ' * indent + str(key))
            print_json_structure(data[key], indent + 1)
    elif isinstance(data, list):
        if data:
            print('  ' * indent + 'List of {} items'.format(len(data)))
            print_json_structure(data[0], indent + 1)
        else:
            print('  ' * indent + 'Empty List')
    else:
        print('  ' * indent + 'Value of type ' + str(type(data)))

# Chemin vers le fichier JSON
file_path = 'C:/Users/hennecol/Documents/safeflat/scraping/abritel-oxylab/annonces/output.json'

# Charger le fichier JSON
with open(file_path, 'r') as file:
    data = json.load(file)

# Afficher la structure du JSON
print_json_structure(data)