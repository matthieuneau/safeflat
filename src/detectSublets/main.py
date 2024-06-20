from utils import *
import pandas as pd
from pap_algo import filter_and_score as pap_filter_and_score


def handler(event, _context):
    print("detecting sublets for ads coming from: ", event["website"])
    print("scraped_data", event["scraped_data"])

    # Convert the serialized data back to a DataFrame
    scraped_properties = pd.DataFrame(event["scraped_data"])
    print("scraped_properties as df: ", scraped_properties.shape)

    website = event["website"]
    allowed_websites = {
        "leboncoin",
        "airbnb",
        "pap",
        "seloger",
        "abritel",
        "gensdeconfiance",
    }

    if website not in allowed_websites:
        raise ValueError(f"No algorithm implemented for this website: {website}")

    ALGO_MAP = {"pap": pap_filter_and_score}

    detection_algo = ALGO_MAP[website]

    # NEED TO FETCH THE ACTUAL DATA FROM THE CLIENT
    print("properties to protect fetched from DB: ", scraped_properties)

    for scraped_property in scraped_properties:
        data_with_scores = detection_algo(scraped_property)
        print(data_with_scores)
        send_detection_event(
            website=event["website"],
            threshold_score=0.2,
            data_with_scores=data_with_scores,
            property_to_protect_id=scraped_property["id"],
        )

    scraped_properties = [
        {
            "location": "Paris 11e (75011)",
            "energy": "F",
            "ges": None,
            "nb_rooms": 3,
            "nb_bedrooms": 2,
            "surface": 50,
            "terrain": None,
            "bills": "50",
            "piscine": "Non",
            "type_de_bien": "appartement",
            "parking": "oui",
            "quartier": None,
            "meuble": None,
            "nombre_d'etages": None,
            "numero_d'etage": "1",
            "ascenseur": "oui",
            "cave": None,
            "terrasse": "oui",
        },
        # {
        #     "location": "Strasbourg (67000)",
        #     "energy": "E",
        #     "ges": "E",
        #     "nb_rooms": 3,
        #     "nb_bedrooms": 1,
        #     "surface": 52.5,
        #     #'terrain' : '',
        #     "bills": "150",
        #     "piscine": "Non",
        #     "type_de_bien": "appartement",
        #     "parking": "oui",
        #     "quartier": "Hyper Centre",
        #     #'meuble' : '',
        #     #'nombre_d\'etages' : '',
        #     "numero_d'etage": "1",
        #     #'ascenceur' : '',
        #     #'cave' : '',
        #     "terrasse": "oui",
        # },
    ]

    # NEED TO ADD FILTERING ON LOCATION
    for property_to_protect in scraped_properties:
        data_with_scores = scoring_algorithm(property_to_protect, event["scraped_data"])
        print(data_with_scores)
