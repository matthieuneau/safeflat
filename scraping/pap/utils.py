import time
import csv
from selenium.webdriver.common.by import By
from numpy import random


def retrieve_data(url, driver, output_file_path):
    """
    TO BE UPDATED
    Navigates to a given URL and retrieves data using a Selenium WebDriver.

    This function navigates to the specified URL, waits for the page to load,
    and attempts to scrape data into a dictionary. It also tries to click a
    'Voir plus' button to reveal more information, if it exists.

    Parameters:
    url (str): The URL to navigate to.
    driver (selenium.webdriver): The WebDriver instance to use for navigation and data retrieval.
    """

    result = {}

    # Navigate to the URL
    driver.get(url)

    time.sleep(3)

    # Extracting the title
    try:
        result["title"] = driver.find_element(By.CSS_SELECTOR, "h1.item-title").text
    except Exception as e:
        print("Error extracting title:", e)
        result["title"] = "Title Not Found"

    # Extracting the price
    try:
        result["price"] = driver.find_element(
            By.XPATH, "//span[@class='item-price']"
        ).text
    except Exception as e:
        print("Error extracting price:", e)
        result["price"] = "Price Not Found"

    # Extracting the location
    try:
        result["location"] = driver.find_element(
            By.CSS_SELECTOR, "div.item-description h2"
        ).text
    except Exception as e:
        print("Error extracting location:", e)
        result["location"] = "Location Not Found"

    # Extracting details
    try:
        result["nb_rooms"] = ""
        result["nb_bedrooms"] = ""
        result["surface"] = ""
        result["nb_rooms"] = driver.find_element(
            By.CSS_SELECTOR, "div.item-description ul li:nth-child(1) strong"
        ).text
        result["nb_bedrooms"] = driver.find_element(
            By.CSS_SELECTOR, "div.item-description ul li:nth-child(2) strong"
        ).text
        result["surface"] = driver.find_element(
            By.CSS_SELECTOR, "div.item-description ul li:nth-child(3) strong"
        ).text
    except Exception as e:
        print("Error extracting details:", e)
        if result["nb_rooms"] == "":
            result["nb_rooms"] = "Nb Rooms Not Found"
        if result["nb_bedrooms"] == "":
            result["nb_bedrooms"] = "Nb Bedrooms Not Found"
        if result["surface"] == "":
            result["surface"] = "Surface Not Found"

    # Extracting the description
    try:
        description = driver.find_element(
            By.CSS_SELECTOR, "div.margin-bottom-30 > p"
        ).text
        result["description"] = description
    except Exception as e:
        print("Error extracting description:", e)
        result["description"] = "Description Not Found"

    # This contains the Conditions Financières, Classe Energie and GES
    html_content = driver.find_elements(By.XPATH, "//div[@class='row']")

    # Extracting the Conditions Financières
    try:
        conditions_financieres = html_content[1]

        loyer_charges_comprises = conditions_financieres.find_element(
            By.XPATH, ".//div[1]"
        ).text
        result[loyer_charges_comprises.split("\n")[0]] = loyer_charges_comprises.split(
            "\n"
        )[1]

        dont_charges = conditions_financieres.find_element(By.XPATH, ".//div[2]").text
        result[dont_charges.split("\n")[0]] = dont_charges.split("\n")[1]

        depot_de_garantie = conditions_financieres.find_element(
            By.XPATH, ".//div[3]"
        ).text
        result[depot_de_garantie.split("\n")[0]] = depot_de_garantie.split("\n")[1]
    except Exception as e:
        print("Error extracting Conditions Financières:", e)
        # if result["loyer_charges_comprises"] == "":
        # result["loyer_charges_comprises"] = "Loyer Charges Comprises Not Found"
        # if result["dont_charges"] == "":
        # result["dont_charges"] = "Dont Charges Not Found"
        # if result["depot_de_garantie"] == "":
        # result["depot_de_garantie"] = "Depot De Garantie Not Found"

    # Extracting the Classe Energie and GES
    try:
        classe_energie_GES = html_content[2]

        # Extracting "Classe énergie"
        classe_energie_element = classe_energie_GES.find_element(
            By.CSS_SELECTOR, ".energy-indice .active"
        )
        classe_energie = (
            classe_energie_element.text.strip()
            if classe_energie_element
            else "Not Found"
        )

        # Extracting "GES"
        ges_element = classe_energie_GES.find_element(
            By.CSS_SELECTOR, ".ges-indice .active"
        )
        ges = ges_element.text.strip() if ges_element else "Not Found"
    except Exception as e:
        print("Error extracting Classe Energie and GES:", e)
        result["classe_energie"] = "Classe Energie Not Found"
        result["ges"] = "GES Not Found"

    # Extracting transports connections
    try:
        transport_labels_elements = driver.find_elements(
            By.CSS_SELECTOR, "ul.item-transports li span.label"
        )
        transport_labels = [element.text for element in transport_labels_elements]
        result["transports"] = transport_labels
    except Exception as e:
        print("Error extracting transport labels:", e)
        result["transports"] = "Transport Labels Not Found"

    driver.quit()

    with open(output_file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "title",
                "price",
                "location",
                "nb_rooms",
                "nb_bedrooms",
                "surface",
                "description",
                "Loyer charges comprises",
                "Dont charges",
                "Dépôt de garantie",
                "classe_energie",
                "ges",
                "transports",
            ],
        )
        writer.writeheader()
        writer.writerow(result)
