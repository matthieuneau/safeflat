import random
import time
import yaml
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def get_random_user_agent():
    """
    Returns a random user agent from a predefined list of recent user agents.

    :return: A random user agent string
    :rtype: str
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
    ]
    return random.choice(user_agents)


def get_annonce_data(driver, annonce):
    """
    Retrieves data from a given annonce URL.
    """

    driver.get(annonce)
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

    # Retriving energy and GES
    try:
        energy = driver.find_element(
            By.CSS_SELECTOR, ".energy-indice ul li.active"
        ).text
        GES = driver.find_element(By.CSS_SELECTOR, ".ges-indice ul li.active").text
        data["energy_GES"] = {"energy": energy, "GES": GES}
    except Exception as e:
        print(f"Error retrieving energy and GES: {e}")
        data["energy_GES"] = {"energy": "Not Available", "GES": "Not Available"}

    # Retrieving ref and date
    try:
        ref_date = driver.find_element(By.CSS_SELECTOR, ".item-date").text
        data["ref_date"] = ref_date
    except Exception as e:
        print(f"Error retrieving reference and date: {e}")
        data["ref_date"] = "Not Available"

    print("data: ", data)
    return data
