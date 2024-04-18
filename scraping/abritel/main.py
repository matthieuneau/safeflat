import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https://www.abritel.fr/search?adults=2&d1=2024-04-24&d2=2024-04-25&destination=Paris%20%28et%20environs%29%2C%20France&endDate=2024-04-25&flexibility=7_DAY&latLong=48.853564%2C2.348095&regionId=179898&semdtl=&sort=RECOMMENDED&startDate=2024-04-24&theme=&userIntent="
urls = []
# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)

time.sleep(300)  # Ajustez ce temps selon la vitesse de chargement de votre page


# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     # Faire défiler la page vers le bas
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Attendez que la page charge
#     time.sleep(2)  # Ajustez ce temps si nécessaire

#     # Calculez la nouvelle hauteur de défilement et comparez-la à la dernière hauteur de défilement
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# # Attendez un moment pour que le scroll soit complet ou pour que le contenu dynamique se charge
# time.sleep(10)

# try:
#     while True:
        # Récupérez les URLs après avoir défilé
        # url_elements = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-stid="open-hotel-information"]'))
        # )
        # urls_temp = [
        #     element.get_attribute("href")
        #     for element in url_elements
        #     if "https://www.abritel.fr/" in element.get_attribute("href")
        # ]

        # urls_temp = list(set(urls_temp))
        # urls+= urls_temp
        # print(len(urls))

        # Scroller jusqu'en bas de la page
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)

        # next_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-stid="next-button"]'))
        # )

        # # Cliquez sur le bouton
        # next_button.click()

# except Exception as e:
#     Si le lien "Suivant" n'est pas trouvé, on suppose qu'on est à la dernière page
#     print("Dernière page atteinte.")


# finally:
#     driver.quit() 