from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

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

# Navigate to the page
url = "https://www.leboncoin.fr/f/locations/real_estate_type--2"
driver.get(url)

# Allow some time for the page to load
time.sleep(4)

# Find all anchor tags
all_links_elements = driver.find_elements(By.TAG_NAME, "a")

# List to store all post URLs
post_urls = []

# Traverse and extract URLs
for link in all_links_elements:
    href = link.get_attribute("href")
    if href and "condition_to_identify_post_links" in href:
        post_urls.append(href)

# Close the driver
driver.quit()

# Print the extracted URLs
for url in post_urls:
    print(url)
