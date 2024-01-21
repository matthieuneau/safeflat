from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import utils

# URL of the flat
url = "https://www.pap.fr/annonces/appartement-alfortville-94140-r441800902"

# Setup Chrome options for headless browsing
options = Options()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

utils.retrieve_data(url, driver, "output.csv")
