from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import utils

url = "https://www.pap.fr/annonce/location-appartement-maison"

# Setup Chrome options for headless browsing
options = Options()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)

time.sleep(3)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content to load
    time.sleep(2)  # Adjust the sleep time as necessary

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(3)

url_elements = driver.find_elements(By.CSS_SELECTOR, ".item-title")
urls = [
    element.get_attribute("href")
    for element in url_elements
    if element.get_attribute("href").startswith(
        "https://www.pap.fr/annonces"
    )  # avoids to retrieve the urls that redirect to ads
]
# print(urls)

for url in urls:
    utils.retrieve_data(url, driver, "output.csv")
    time.sleep(2)

driver.quit()
