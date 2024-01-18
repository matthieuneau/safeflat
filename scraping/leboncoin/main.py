from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import time

sys.path.append(
    r"C:\Users\mneau\OneDrive\Bureau\INFO\PYTHON\selenium\chromedriver_1.120.6099.129"
)

# Chrome options
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(
    r"C:\Users\mneau\OneDrive\Bureau\INFO\PYTHON\selenium\chromedriver_1.120.6099.129\chromedriver.exe"
)

# URL of the page
url = "https://www.leboncoin.fr/offre/locations/2471706452"
# url = "https://www.leboncoin.fr/"

# Navigate to the page
driver.get(url)

# # Allow some time for the page to load
time.sleep(5)

try:
    voir_plus_button = driver.find_element(
        By.CSS_SELECTOR, "button.mt-lg.text-body-1-link.font-semi-bold.underline"
    )
    voir_plus_button.click()
    # Wait a bit for the text to fully load after clicking
    time.sleep(3)
except Exception as e:
    print(f"Could not click 'Voir plus' button: {e}")

# Extract the description and write to file
try:
    text_element = driver.find_element(
        By.CSS_SELECTOR, "p.whitespace-pre-line.text-body-1"
    )
    extracted_text = text_element.text

    # Open (or create) the file and write the extracted text
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(extracted_text)
    print("Description OK")

except Exception as e:
    print(f"An error occurred while extracting text: {e}")

try:
    # Extracting the price
    price_element = driver.find_element(
        By.CSS_SELECTOR, 'div[data-qa-id="adview_price"] p.text-headline-2'
    )
    price = price_element.text
    print("price OK")

except Exception as e:
    print(f"An error occurred while extracting price: {e}")

# Retrieving the details(rooms, surface, city, postcode)
try:
    details_element = driver.find_element(
        By.CSS_SELECTOR, "p.inline-flex.w-full.flex-wrap.mb-md"
    )
    file.write(details_element.text)
    print("details OK")

except Exception as e:
    print(f"An error occurred while extracting the details: {e}")

# retrieve the title of the ad
try:
    ad_title = driver.find_element(
        By.CSS_SELECTOR, "break-words text-headline-1-expanded undefined"
    )
    file.write(ad_title.text)

except Exception as e:
    print(f"An error occurred while extracting the title: {e}")

# Close the driver
driver.quit()
