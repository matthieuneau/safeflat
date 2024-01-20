import time
import csv
from selenium.webdriver.common.by import By
from numpy import random


def retrieve_data(url, driver, output_file_path):
    """
    Navigates to a given URL and retrieves data using a Selenium WebDriver.

    This function navigates to the specified URL, waits for the page to load,
    and attempts to scrape data into a dictionary. It also tries to click a
    'Voir plus' button to reveal more information, if it exists.

    Parameters:
    url (str): The URL to navigate to.
    driver (selenium.webdriver): The WebDriver instance to use for navigation and data retrieval.
    """
    # Navigate to the page
    driver.get(url)

    # Allow some time for the page to load
    time.sleep(random.uniform(3, 5))

    # Create a dictionary to store the scraped data
    scraped_data = {"description": "", "price": "", "details": "", "title": ""}

    # Clicking the 'Voir plus' button to display the full description
    try:
        voir_plus_button = driver.find_element(
            By.CSS_SELECTOR, "button.mt-lg.text-body-1-link.font-semi-bold.underline"
        )
        voir_plus_button.click()

        # Wait a bit for the text to fully load after clicking
        time.sleep(2)
    except Exception as e:
        print(f"Could not click 'Voir plus' button: {e}")

    # Extract the description
    try:
        text_element = driver.find_element(
            By.CSS_SELECTOR, "p.whitespace-pre-line.text-body-1"
        )
        scraped_data["description"] = text_element.text
        print("description OK")

    except Exception as e:
        print(f"An error occurred while extracting text: {e}")

    # Extract the price
    try:
        price_element = driver.find_element(
            By.CSS_SELECTOR, 'div[data-qa-id="adview_price"] p.text-headline-2'
        )
        scraped_data["price"] = price_element.text
        print("price OK")

    except Exception as e:
        print(f"An error occurred while extracting price: {e}")

    # Retrieving the details(rooms, surface, city, postcode)
    try:
        details_element = driver.find_element(
            By.CSS_SELECTOR, "p.inline-flex.w-full.flex-wrap.mb-md"
        )
        scraped_data["details"] = details_element.text.split("\n")
        print("details OK")

    except Exception as e:
        print(f"An error occurred while extracting the details: {e}")

    # retrieve the title of the ad
    try:
        ad_title = driver.find_element(By.CSS_SELECTOR, 'h1[data-qa-id="adview_title"]')
        scraped_data["title"] = ad_title.text
        print("title OK")

    except Exception as e:
        print(f"An error occurred while extracting the title: {e}")

    # Now write the scraped data to a CSV file
    with open(output_file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["description", "price", "details", "title"]
        )
        writer.writeheader()
        writer.writerow(scraped_data)
