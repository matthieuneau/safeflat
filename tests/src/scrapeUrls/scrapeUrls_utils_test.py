import pandas as pd
import pytest
from src.scrapeUrls.utils import process_description, save_to_database


@pytest.mark.parametrize(
    "data_saved, should_succeed",
    [
        (
            pd.DataFrame(
                {
                    "url": "http://example.com/property/123",
                    "location": "123 Main St, Anytown, AN 12345",
                    "description": "A beautiful property with modern amenities and a spacious layout.",
                    "energy": "B",
                    "ges": "C",
                    "ref_date": "2024-06-13",
                    "title": "Stunning 4-bedroom House with Pool",
                    "price": "350,000",
                    "nb_rooms": 6,
                    "nb_bedrooms": 4,
                    "surface": "200 sqm",
                    "terrain": "500 sqm",
                    "rent_with_bills": "No",
                    "bills": "Approximately 200/month",
                    "piscine": "Yes",
                    "type_de_bien": "House",
                    "parking": "Garage for 2 cars",
                    "quartier": "Downtown",
                    "meuble": "No",
                    "nombre_d'etages": 2,
                    "numero_d'etage": 1,
                    "ascenseur": "No",
                    "cave": "Yes",
                    "terrasse": "Yes",
                },
                index=[0],
            ),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "key_does_not_exist": "http://example.com/property/123",
                },
                index=[0],
            ),
            False,
        ),
    ],
)
def test_save_to_database(data_saved, should_succeed):
    if should_succeed:
        try:
            save_to_database(data_saved, "pap")
            no_error = True
        except Exception as e:
            no_error = False
            print(f"Error occurred: {e}")
        assert no_error, "save_to_database raised an error unexpectedly"
    else:
        with pytest.raises(Exception):
            save_to_database(data_saved, "pap")


def test_process_description():
    desc = """
    Construite en 1890, cette belle maison de famille d'une surface de 190 m2 et rénovée en 2023 se situe dans le quartier recherché Le Parc de Saint Maur.

    Sa localisation est idéale, notamment pour les familles, puisqu’elle se trouve à 4 min à pied du RER A (station Champigny), à 6 min à pied des bords de marne, à 3 min à pied des écoles primaire et maternelle Le Parc-Tilleuls, et du collège Le Parc (sectorisation).
    Elle est proche des commerces et de la place des marronniers.

    La maison se compose d'une belle entrée desservant un séjour double traversant donnant sur le jardin, une salle à manger ainsi qu’une cuisine mêlant charme d'antan et modernité.
    La salle à manger dessert un vestibule, des toilettes, une pièce pouvant faire office de bureau ou de chambre, ainsi que l’accès par un couloir jardin d hiver à l’espace buanderie.

    Au premier étage : trois chambres, deux salles de bain, des toilettes, ainsi qu’un grand espace dressing.
    Au second : une pièce pouvant faire office de bureau ou de chambre, ainsi qu’un grand espace sous combles isolés pouvant également servir de chambre ou d espace de jeu
    Le sous-sol accueille la chaudière et comprend un espace de rangement.

    Son orientation, idéale plein sud permet de bénéficier d’un ensoleillement tout au long de la journée et de rendre les espaces de vie très lumineux.
    Devant la maison plein sud un jardin clos, arboré et sans vis-à-vis
    Une petite serre attenante à la maison vous permettra de vous initier au jardinage.
    Une pièce « débarras » se situe à l’arrière de la maison.

    Elle dispose d'un garage double pouvant être aménager en dépendance (accès à l'eau et l'électricité).

    Nb : le montant des charges restent à parfaire."""
    try:
        process_description(desc)
        no_error = True
    except Exception as e:
        no_error = False
        print(f"Error occurred: {e}")
    assert no_error, "process_description raised an error unexpectedly"
