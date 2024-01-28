from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
]
#print(urls)
driver.quit()

#for url in urls:
for i in range(6,12):  
    utils.retrieve_data(urls[i], "output.csv")
    time.sleep(2)

