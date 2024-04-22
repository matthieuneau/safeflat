import random
import time
import yaml
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def scrape_ad(driver, ad):
    """
    Retrieves data from a given annonce URL.
    """

    driver.get(ad)
    time.sleep(2)
    data = {}

    # Retrieving title and price
    try:
        title_and_price = driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div[1]/h1[@class='item-title']"
        )
        data["title_and_price"] = title_and_price.text
    except Exception as e:
        print(f"Error retrieving title and price: {e}")
        data["title_and_price"] = "Not Available"

    # Retrieving location
    try:
        location = driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div[1]/div[5]/h2"
        )
        data["location"] = location.text
    except Exception as e:
        print(f"Error retrieving location: {e}")
        data["location"] = "Not Available"

    # Retrieving nb of rooms, surface and nb of bedrooms when available
    try:
        list_items = driver.find_elements(
            By.CSS_SELECTOR, "ul.item-tags.margin-bottom-20 > li"
        )
        details = [item.find_element(By.TAG_NAME, "strong").text for item in list_items]
        data["details"] = details
    except Exception as e:
        print(f"Error retrieving details: {e}")
        data["details"] = []

    # Retrieving description
    try:
        description = driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div[1]/div[5]/div[1]"
        )
        data["description"] = description.text
    except Exception as e:
        print(f"Error retrieving description: {e}")
        data["description"] = "Not Available"

    # Retrieving metro stations closeby
    try:
        metro = driver.find_elements(By.CSS_SELECTOR, ".item-transports")
        metro_stations = [item.text for item in metro]
        data["metro_stations"] = metro_stations
    except Exception as e:
        print(f"Error retrieving metro stations: {e}")
        data["metro_stations"] = []

    # Retrieving conditions financieres
    try:
        conditions_financieres = driver.find_elements(
            By.CSS_SELECTOR, ".row > .col-1-3"
        )
        conditions_financieres = [item.text for item in conditions_financieres]
        data["conditions_financieres"] = conditions_financieres
    except Exception as e:
        print(f"Error retrieving financial conditions: {e}")
        data["conditions_financieres"] = []

    # Retriving energy and ges
    try:
        energy = driver.find_element(
            By.CSS_SELECTOR, ".energy-indice ul li.active"
        ).text
        data["energy"] = energy
    except Exception as e:
        print(f"Error retrieving energy: {e}")
        data["energy"] = "Not Available"

    # Retrieving ges
    try:
        ges = driver.find_element(By.CSS_SELECTOR, ".ges-indice ul li.active").text
        data["ges"] = ges
    except Exception as e:
        print(f"Error retrieving ges: {e}")
        data["ges"] = "Not Available"

    # Retrieving ref and date
    try:
        ref_date = driver.find_element(By.CSS_SELECTOR, ".item-date").text
        data["ref_date"] = ref_date
    except Exception as e:
        print(f"Error retrieving reference and date: {e}")
        data["ref_date"] = "Not Available"

    print("data: ", data)
    return data
