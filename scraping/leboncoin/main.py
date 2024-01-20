from selenium import webdriver
import sys
import utils
import time
from numpy import random
from selenium.webdriver.common.by import By

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
# url = "https://www.leboncoin.fr/offre/locations/2466675077"

# scraped_data = utils.retrieve_data(url, driver, "output.csv")

main_url = "https://www.leboncoin.fr/f/locations/real_estate_type--2"

# Open the main page
driver.get(main_url)

time.sleep(random.uniform(6, 8))

# List to store the URLs
urls = []

try:
    # Open the main page
    driver.get(main_url)

    # Random sleep to mimic human behavior and avoid getting blocked
    time.sleep(random.uniform(6, 8))

    # Find all anchor elements on the page
    anchors = driver.find_elements(By.TAG_NAME, 'a')

    # Filter and store the URLs that start with '/offre/locations'
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if href and '/offre/locations' in href:
            urls.append(href)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()

# Print the URLs
print(urls)