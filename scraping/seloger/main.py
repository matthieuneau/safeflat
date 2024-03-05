from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains





page_nb = 2

url = f"https://www.seloger.com/list.htm?projects=1&types=2%2C1&natures=1&places=%5B%7B%22inseeCodes%22%3A%5B670482%5D%7D%5D&enterprise=0&qsVersion=1.0"
urls = []

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)

# wait = WebDriverWait(driver, 30)
# # Attendre que l'élément soit cliquable
# element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".didomi-continue-without-agreeing")))
# # Cliquer sur l'élément
# element.click()

wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes pour les conditions

url_elements = driver.find_elements(By.XPATH, '//a[@data-testid="sl.explore.coveringLink"]')
urls_temp = [
    element.get_attribute("href")
    for element in url_elements
    if element.get_attribute("href").startswith(
        "https://www.seloger.com/"
    )  # avoids to retrieve the urls that redirect to ads
]
urls_temp = list(set(urls_temp))
urls+= urls_temp
print(len(urls))

# while True:
#     try:
#         url_elements = driver.find_elements(By.XPATH, '//a[@data-testid="sl.explore.coveringLink"]')
#         urls_temp = [
#             element.get_attribute("href")
#             for element in url_elements
#             if element.get_attribute("href").startswith(
#                 "https://www.seloger.com/"
#             )  # avoids to retrieve the urls that redirect to ads
#         ]
#         urls_temp = list(set(urls_temp))
#         urls+= urls_temp
#         print(len(urls))
#         # # Attendre que le bouton "Suivant" soit cliquable
#         # next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='gsl.uilib.Paging.nextButton']")))

#         # # Obtenez la hauteur totale de la page
#         # total_height = driver.execute_script("return document.body.scrollHeight")

#         # # Calculez les 2/3 de la hauteur
#         # scroll_height = 4/5 * total_height

#         # # Faites défiler la page jusqu'à la position calculée
#         # driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        
#         # # Cliquer sur le bouton "Suivant"
#         # next_button.click()

#         element = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.XPATH, "//a[@data-testid='gsl.uilib.Paging.nextButton']"))
#         )

#         # Scroller jusqu'à l'élément (optionnel si vous utilisez move_to_element plus tard)
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

#         # Placer la souris sur l'élément et cliquer (deux méthodes possibles)
#         actions = ActionChains(driver)
#         actions.move_to_element(element).click().perform()
        
        
#     except TimeoutException:
#         # Si le bouton "Suivant" n'est pas trouvé, sortir de la boucle
#         print("Fin de la pagination, le bouton 'Suivant' n'est plus présent.")
#         break






driver.quit()

for url_ in urls:
    utils.retrieve_data(url_, "output.csv")
time.sleep(2)

