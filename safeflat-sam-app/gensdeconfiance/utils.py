import random
import time
import yaml
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def get_annonce_data(driver, annonce):
    """
    Retrieves data from a given annonce URL.
    """

    driver.get(annonce)
    time.sleep(2)
    data = {}

    # Try retrieving title
    try:
        data["title"] = driver.find_element(By.CSS_SELECTOR, "h1#post-title").text
    except Exception as e:
        print(f"Error retrieving title: {e}")
        data["title"] = "Not Available"

    # Try retrieving subtitle
    try:
        data["subtitle"] = driver.find_element(
            By.CSS_SELECTOR, "h2#post-title-breadcrumb"
        ).text
    except Exception as e:
        print(f"Error retrieving subtitle: {e}")
        data["subtitle"] = "Not Available"

    # Try retrieving author's name
    try:
        data["author"] = driver.find_element(By.CSS_SELECTOR, "#owner-name > a").text
    except Exception as e:
        print(f"Error retrieving author: {e}")
        data["author"] = "Not Available"

    # Try retrieving price titles and values
    try:
        titles = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "div.price-table > div.price-table__row > div.price-table__cell",
            )
        ]
        values = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "div.price-table > div.price-table__row > div.price-table__value",
            )
        ]
        data["prices"] = dict(zip(titles, values))
    except Exception as e:
        print(f"Error retrieving prices: {e}")
        data["prices"] = "Not Available"

    # Try retrieving characteristics titles and values
    try:
        characteristics_titles = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "ul.indexclient__GridList-dYErZy.XvGJg > li > p",
            )
        ]
        characteristics_values = [
            item.text
            for item in driver.find_elements(
                By.CSS_SELECTOR,
                "ul.indexclient__GridList-dYErZy.XvGJg > li > ul > li",
            )
        ]
        data["characteristics"] = dict(
            zip(characteristics_titles, characteristics_values)
        )
    except Exception as e:
        print(f"Error retrieving characteristics: {e}")
        data["characteristics"] = "Not Available"

    # Try retrieving description
    # First click on the "Lire la suite" button if it exists to make sure the full description is displayed
    try:
        driver.find_element(By.CSS_SELECTOR, "#ad-description__more").click()
    except Exception as e:
        print(f'Error when trying to click on "Lire la suite" button: {e}')
    # Then retrieve the description
    try:
        data["description"] = driver.find_element(
            By.CSS_SELECTOR, "div#ad-description"
        ).text
    except Exception as e:
        # print(f"Error retrieving description: {e}")
        data["description"] = "Not Available"

    print("===================================")
    print("          NEW POST DISPLAY          ")
    print("===================================")
    print(data)
    return data
