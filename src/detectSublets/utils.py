import os
from sqlalchemy import create_engine
import requests
import pandas as pd


def get_client_data():
    headers = {
        "Authorization": "Token untokenrandom",
        "Content-Type": "application/json",
    }

    response = requests.get("http://13.60.104.49/app/api/biens", headers=headers)
    # df = pd.DataFrame(response.json()
    return response


def send_detection_event(
    data_with_scores: pd.DataFrame,
    property_to_protect_id: int,
    threshold_score: float,
    website: str,
):
    sublet_detected = []

    for _, row in data_with_scores.iterrows():
        if row["score"] > threshold_score:
            sublet_detected.append(
                {
                    "property_to_protect_id": property_to_protect_id,
                    "sublet_url": row["url"],
                    "website": website,
                }
            )

    headers = {
        "Authorization": f"Token untokenrandom",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "http://13.60.104.49/app/api/biens", headers=headers, data=sublet_detected
    )
    df = pd.DataFrame(response.json())
    print(df)


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


def read_from_database(query: str) -> pd.DataFrame:
    """retrieves the

    Parameters
    ----------
    query : str
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """
    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": 3306,
        "user": "admin",
        "password": os.getenv("DB_PASSWORD"),
        "database": "scraping",
    }

    # Creating a connection string for SQLAlchemy
    connection_string = f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'

    engine = create_engine(connection_string)

    df = pd.read_sql_query(query, con=engine)

    return df


# FOR TESTING PURPOSE ONLY
def add_client_data(data):
    # csrf_token = get_csrf_token()
    # if not csrf_token:
    #     print("CSRF token not found. Cannot proceed.")
    #     return

    csrf_token = "kn4y8iNDa2QOoTOVmlsl48jenLvquRFV"
    session_id = "0c0r7e4ejfnjnlia4az6ariifqf70d40"

    headers = {
        "Authorization": "Token untokenrandom",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
    }

    cookies = {
        "csrftoken": csrf_token,
        "sessionid": session_id,
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.post(
        "http://13.60.104.49/app/api/biens", headers=headers, cookies=cookies, json=data
    )

    if response.status_code == 200:
        print("Data added successfully!")
    else:
        print(f"Failed to add data. Status code: {response.status_code}")
        print(f"Response: {response.text}")


# def get_csrf_token():
#     headers = {
#         "Authorization": "Token untokenrandom",
#         "Content-Type": "application/json",
#     }

#     # Assuming there's an endpoint to fetch the CSRF token
#     response = requests.get("http://16.171.35.18/app/api/biens", headers=headers)

#     if response.status_code == 200:
#         # Extract CSRF token from cookies
#         print("response cookies", response.cookies)
#         csrf_token = response.cookies["csrftoken"]
#         return csrf_token
#     else:
#         print(f"Failed to get CSRF token. Status code: {response.status_code}")
#         return None


if __name__ == "__main__":
    add_client_data(
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
        }
    )
    get_client_data()
