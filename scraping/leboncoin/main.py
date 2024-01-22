import undetected_chromedriver as uc
import time
import yaml
from selenium.webdriver.common.by import By
from numpy import random
from utils import retrieve_data

# Define multiple user agents to avoid detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.0; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Edg/104.0.0.0",
]

# Define a custom user agent
user_agent = random.choice(user_agents)

# Set Chrome Options
options = uc.ChromeOptions()
# options.headless=True
# options.add_argument('--headless')
# options.add_argument(f'--proxy-server={PROXY}')
options.add_argument(f"user-agent={user_agent}")


# Load the configuration file
with open("../../Config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

nb_pages_to_scrape = config["nb_pages_to_scrape"]

# Create Undetected Chromedriver with Proxy
driver = uc.Chrome(options=options)

for page_nb in range(1, nb_pages_to_scrape + 1):
    url = f"https://www.leboncoin.fr/f/locations/real_estate_type--2/p-{page_nb}"
    # Send Request
    driver.get(url)

    time.sleep(4)

    posts = driver.find_elements(
        By.XPATH, "//a[@data-test-id='ad' and @data-qa-id='aditem_container']"
    )

    webpages = []
    # Récupérez les liens des annonces
    for post in posts:
        url = post.get_attribute("href")
        webpages.append(url)

    print(webpages)

    for webpage in webpages:
        retrieve_data(webpage, driver, "output.csv")
        time.sleep(random.uniform(3, 5))

driver.quit()
