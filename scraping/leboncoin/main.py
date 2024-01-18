from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import sys
import time

sys.path.append(
    r"C:\Users\mneau\OneDrive\Bureau\INFO\PYTHON\selenium\\"
    r"chromedriver_1.120.6099.129"
)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(
    r"C:\Users\mneau\OneDrive\Bureau\INFO\PYTHON\selenium\\"
    r"chromedriver_1.120.6099.129"
    r"\chromedriver.exe"
)

# URL of the page
url = "https://www.leboncoin.fr/offre/locations/2471706452"
# url = "https://www.leboncoin.fr/"

# Navigate to the page
driver.get(url)

# # Allow some time for the page to load
time.sleep(5)

# Create a dictionary to store the scraped data
scraped_data = {"description": "", "price": "", "details": "", "title": ""}

# Clicking the 'Voir plus' button to display the full description
try:
    voir_plus_button = driver.find_element(
        By.CSS_SELECTOR, "button.mt-lg.text-body-1-link.font-semi-bold.underline"
    )
    voir_plus_button.click()
    # Wait a bit for the text to fully load after clicking
    time.sleep(3)
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
with open("output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file, fieldnames=["description", "price", "details", "title"]
    )
    writer.writeheader()
    writer.writerow(scraped_data)

# Close the driver
driver.quit()

with open("output.txt", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    for row in reader:
        # Extract each field into a variable
        description = row["description"]
        price = row["price"]
        details = row["details"]
        title = row["title"]

        # Print the variables to the terminal
        print(f"Description: {description}")
        print(f"Price: {price}")
        print(f"Details: {details}")
        print(f"Title: {title}\n")
