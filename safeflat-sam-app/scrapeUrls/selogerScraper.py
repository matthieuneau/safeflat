from bs4 import BeautifulSoup
from utils import fetch_html_with_oxylab


def seloger_scraper(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    # for test purpose only, local html file:
    file_path = "/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/seloger-oxylab/annonces/annonce2.html"
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

    # html = fetch_html_with_oxylab(ad_url)
    # soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Retrieving title
    try:
        data["title"] = soup.find(
            "div", class_="Summarystyled__Title-sc-1u9xobv-4 dbveQQ"
        ).text.strip()
    except Exception as e:
        print("Error retrieving title:", e)
        data["title"] = "Not Available"

    # Retrieving price : Price isn't in the html file
    try:
        data["price"] = soup.find(
            "span", class_="global-styles__TextNoWrap-sc-1gbe8ip-6"
        ).text.strip()
    except Exception as e:
        print("Error extracting price:", e)
        data["price"] = "Not Available"

    # # Retrieving City and Zip code
    try:
        data["city and zip code"] = soup.find(
            "span", class_="Localizationstyled__City-sc-gdkcr2-1 bgtLnh"
        ).text.strip()
    except Exception as e:
        print("Error extracting City and Zip Code:", e)
        data["city and zip code"] = "Not Available"

    # Retrieving the neighbourhood
    try:
        data["neighbourhood"] = soup.find(
            "span", {"data-test": "neighbourhood"}
        ).text.strip()
    except Exception as e:
        print("Error extracting Neighbourhood:", e)
        data["neighbourhood"] = "Not Available"

    # Retrieving details : nb_rooms, nb_bedrooms, surface, numero_etage
    try:
        # Initialize the result dictionary with default values
        data["nb_rooms"] = "Not Available"
        data["nb_bedrooms"] = "Not Available"
        data["surface"] = "Not Available"
        data["numero_etage"] = "Not Available"

        # Attempt to find the outer div wrapper
        div_tags_wrapper = soup.find(
            "div", class_="Summarystyled__TagsWrapper-sc-1u9xobv-14"
        )
        if div_tags_wrapper is not None:
            caracteristiques = []
            # Iterate over each tag container found within the wrapper
            for div_tag_container in div_tags_wrapper.find_all(
                "div", class_="Tags__TagContainer-sc-edpl7u-0"
            ):
                caractere = (
                    div_tag_container.text.strip().lower()
                )  # Convert text to lowercase
                caracteristiques.append(caractere)

            # Assign values based on the content of each tag container
            for text in caracteristiques:
                if "pièce" in text:
                    data["nb_rooms"] = text
                elif "chambre" in text:
                    data["nb_bedrooms"] = text
                elif "m²" in text:
                    data["surface"] = text
                elif "étage" in text:  # Ensuring the keyword is also in lowercase
                    data["numero_etage"] = text
        else:
            print("No div tags wrapper found for details.")

    except Exception as e:
        print("Error extracting details:", e)

    # Extracting description
    try:
        data["description"] = soup.find(
            "div", class_="ShowMoreText__UITextContainer-sc-1swit84-0"
        ).text.strip()
    except Exception as e:
        print("Error extracting description:", e)
        data["description"] = "Not Available"

    # Retrieving features: exterieur, cadre et situation, surfaces annexes, service et accessibilite, cuisine, hygiene, piece a vivre
    try:
        data["Extérieur"] = "Not Available"
        data["Cadre et situation"] = "Not Available"
        data["Surfaces annexes"] = "Not Available"
        data["Services et accessibilité"] = "Not Available"
        data["Cuisine"] = "Not Available"
        data["Hygiène"] = "Not Available"
        data["Pièces à vivre"] = "Not Available"

        feature_elements = soup.find_all(
            "div",
            class_="TitledDescription__TitledDescriptionContainer-sc-p0zomi-0 gtBcDa GeneralFeaturesstyled__GeneralListTitledDescription-sc-1ia09m5-5 jsTjoV",
        )

        for element in feature_elements:
            texte = []
            titre_element = element.find("div", class_="feature-title")
            if titre_element:
                titre = titre_element.text.strip()
                texte_liste = element.find_all(
                    "div", class_="GeneralFeaturesstyled__TextWrapper-sc-1ia09m5-3"
                )
                if texte_liste:
                    for texte_element in texte_liste:
                        texte.append(texte_element.text.strip())

                    if titre in data:
                        data[titre] = ", ".join(texte)
                    else:
                        print(f"The column '{titre}' isn't in data")
            else:
                print("Feature title element not found.")

    except Exception as e:
        print(
            "Error extracting features (exterieur, cadre et situation, surfaces annexes, service et accessibilite, cuisine, hygiene, piece a vivre):",
            e,
        )

    # Retrieving DPE and GES:
    try:
        # Initialize with default values assuming 'result' dictionary already exists
        data["Diagnostic de performance énergétique (DPE)"] = "Not Available"
        data["Indice d'émission de gaz à effet de serre (GES)"] = "Not Available"

        energy_elements = soup.find_all("div", {"data-test": "diagnostics-content"})
        for element in energy_elements:
            try:
                titre_element = element.find(
                    "div", {"data-test": "diagnostics-preview-title"}
                )
                letter_element = element.find(
                    "div", class_="Previewstyled__Grade-sc-k3u73o-6 ehFYCZ"
                )

                # Check if both elements are found to avoid NoneType errors
                if titre_element and letter_element:
                    titre = titre_element.text.strip()
                    letter = letter_element.text.strip()
                    if titre == "Diagnostic de performance énergétique (DPE)":
                        data["Diagnostic de performance énergétique (DPE)"] = letter
                    elif titre == "Indice d'émission de gaz à effet de serre (GES)":
                        data["Indice d'émission de gaz à effet de serre (GES)"] = letter
                else:
                    if not titre_element:
                        print("Diagnostic title element not found.")
                    if not letter_element:
                        print("Diagnostic letter element not found.")

            except Exception as e:
                print(f"Error processing an individual energy element: {e}")

    except Exception as e:
        print("Error extracting Energy elements:", e)

    # Retrieving price details:
    try:
        # Initialize all price-related fields with a default value
        data["loyer_base"] = "Not Available"
        data["charges_forfaitaires"] = "Not Available"
        data["complement_loyer"] = "Not Available"
        data["depot_garantie"] = "Not Available"
        data["loyer_charges_comprises"] = "Not Available"

        price_details = soup.select('div[data-test="price-detail-content"] > div')

        title_map = {
            "Loyer de base (hors charge)": "loyer_base",
            "Charges forfaitaires": "charges_forfaitaires",
            "Complément de loyer": "complement_loyer",
            "Dépôt de garantie": "depot_garantie",
            "Loyer charges comprises": "loyer_charges_comprises",
        }

        # Iterate through each div and extract the necessary information
        for detail in price_details:
            spans = detail.find_all("span")
            if (
                len(spans) == 2
            ):  # Ensure there are exactly two spans as expected for title and value
                title = spans[0].text.strip()
                value = spans[1].text.strip()
                if title in title_map:  # Check if the title matches any in the map
                    data[title_map[title]] = value
    except Exception as e:
        print("Error extracting price details:", e)

    # Retrieving host name:
    try:
        data["host_name"] = soup.select_one(
            ".LightSummarystyled__IndividualName-sc-112ffju-12.iqzZxZ"
        ).text.strip()
    except Exception as e:
        print("Error extracting host name:", e)
        data["host_name"] = "Not Available"

    return data
