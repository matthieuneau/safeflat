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

url = "https://www.seloger.com/list.htm?projects=1&types=2,1&places=[{%22inseeCodes%22:[750101]}]&sort=d_dt_crea&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&m=search_refine-redirection-search_results"
urls = []

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)

# #Cliquer sur l'element pour refuser les cookies
# wait = WebDriverWait(driver, 30)
# # Attendre que l'élément soit cliquable
# element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".didomi-continue-without-agreeing")))
# # Cliquer sur l'élément
# element.click()



try:
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

    # # Attendre que le bouton "Suivant" soit cliquable
    #next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='gsl.uilib.Paging.nextButton']")))

    # # Obtenez la hauteur totale de la page
    # total_height = driver.execute_script("return document.body.scrollHeight")

    # # Calculez les 2/3 de la hauteur
    # scroll_height = 4/5 * total_height

    # # Faites défiler la page jusqu'à la position calculée
    # driver.execute_script(f"window.scrollTo(0, {scroll_height});")
    
    # Cliquer sur le bouton "Suivant"
    #next_button.click()

    
    
except TimeoutException:
    # Si le bouton "Suivant" n'est pas trouvé, sortir de la boucle
    print("Fin de la pagination, le bouton 'Suivant' n'est plus présent.")


driver.quit()

for url_ in urls:
    utils.retrieve_data(url_, "output.csv")
time.sleep(2)

