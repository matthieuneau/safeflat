import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# import utils

# Setup Chrome options for headless browsing
options = Options()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# url = r"C:\Users\mneau\OneDrive\Bureau\SafeFlat\scraping\abritel\example_annonce.html"
url = r"C:\Users\mneau\OneDrive\Bureau\SafeFlat\scraping\abritel\example_annonce2.html"
# url = r"C:\Users\mneau\OneDrive\Bureau\SafeFlat\scraping\abritel\example_annonce3.html"

driver.get(url)

time.sleep(2)

elements = driver.find_elements(By.CLASS_NAME, "uitk-text")
features = [element.text.lower() for element in elements]
print(features)

driver.close()
driver.quit()

# New code to filter the features list
keywords = [
    "m²",
    "chambre",
    "salle de bain",
    "personne",
    "salles de bain",
    "lit",
    "balcon",
]
filtered_features = list(
    filter(lambda feature: any(keyword in feature for keyword in keywords), features)
)
print(filtered_features)
