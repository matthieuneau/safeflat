from selenium import webdriver
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

scraped_data = utils.retrieve_data(url, driver, "output.csv")

# Close the driver
driver.quit()
