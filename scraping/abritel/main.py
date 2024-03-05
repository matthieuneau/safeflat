import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.abritel.fr/search?adults=2&d1=&d2=&destination=Paris%20%28et%20environs%29%2C%20France&endDate=&regionId=179898&semdtl=&sort=RECOMMENDED&startDate=&theme=&userIntent="
urls = []
# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)


try:
    while True:
        # Récupérez les URLs après avoir défilé
        url_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-stid="open-hotel-information"]'))
        )
        urls_temp = [
            element.get_attribute("href")
            for element in url_elements
            if "https://www.abritel.fr/" in element.get_attribute("href")
        ]

        urls_temp = list(set(urls_temp))
        urls+= urls_temp
        print(len(urls))

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-stid="next-button"]'))
        )

        # Cliquez sur le bouton
        next_button.click()

# Votre code suivant...
except Exception as e:
    # Si le lien "Suivant" n'est pas trouvé, on suppose qu'on est à la dernière page
    print("Dernière page atteinte.")


finally:
    driver.quit() 