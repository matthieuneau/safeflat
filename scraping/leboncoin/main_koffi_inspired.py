import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from numpy import random
from utils import retrieve_data

# Set Chrome Options
options = uc.ChromeOptions()
# options.headless=True
# options.add_argument('--headless')
# options.add_argument(f'--proxy-server={PROXY}')
# options.add_argument(f"user-agent={my_user_agent}")

# Create Undetected Chromedriver with Proxy
driver = uc.Chrome(options=options)

url = "https://www.leboncoin.fr/f/locations/real_estate_type--2"
# Send Request
driver.get(url)

time.sleep(4)

posts = driver.find_elements(By.XPATH, "//a[@data-test-id='ad' and @data-qa-id='aditem_container']")

webpages = []
# Récupérez les liens des annonces
for post in posts:
    url = post.get_attribute('href')
    webpages.append(url)

print(webpages)

for webpage in webpages:
    retrieve_data(webpage, driver, "output.csv")
    time.sleep(random.uniform(3, 5))

driver.quit()
