from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://www.seloger.com/annonces/locations/appartement/strasbourg-67/neudorf-est-centre/214090983.htm?projects=1&types=2,1&places=[{%22inseeCodes%22:[670482]}]&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&m=search_to_detail&lv=S%27"
'''
page_nb = 2

url = f"https://www.seloger.com/list.htm?projects=1&types=2%2C1&places=%5B%7B%22divisions%22%3A%5B2238%5D%7D%5D&sort=d_dt_crea&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&LISTING-LISTpg={page_nb}"

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

driver.get(url)



url_elements = driver.find_elements(By.XPATH, '//a[@data-testid="sl.explore.coveringLink"]')
urls = [
    element.get_attribute("href")
    for element in url_elements
    if element.get_attribute("href").startswith(
        "https://www.seloger.com/"
    )  # avoids to retrieve the urls that redirect to ads
]'''
#print(urls)

# #Clicks on "Continuer sans accepter" if the cookie page shows up
# try:
#     # Utilisez une attente explicite pour attendre que la page accepter les cookies s'affiche
#     continuer_sans_accepter_button = WebDriverWait(driver, 30).until(
#         EC.presence_of_all_elements_located((By.XPATH, "//span[@class='didomi-continue-without-agreeing']"))
#     )

#     #Continue sans accepter les cookies
#     continuer_sans_accepter_button[0].click()

#     # Wait a bit for the text to fully load after clicking
#     time.sleep(2)
        
# except Exception as e:
#     print(f"Could not click 'Continuer sans accepter button: {e}")

#for url in urls:
'''for i in range(5,6):  
    utils.retrieve_data(urls[i], "output.csv")
    time.sleep(2)'''

utils.retrieve_data(url, "output.csv")
#driver.quit()