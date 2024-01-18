from selenium import webdriver
import csv
import sys
import utils

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

scraped_data = utils.retrieve_data(url, driver)

# Now write the scraped data to a CSV file
with open("output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file, fieldnames=["description", "price", "details", "title"]
    )
    writer.writeheader()
    writer.writerow(scraped_data)

# Close the driver
driver.quit()
