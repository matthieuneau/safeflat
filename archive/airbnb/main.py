from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import preprocessing




# urls = []
# url = "https://www.airbnb.fr/s/Tourcoing--France/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-03-01&monthly_length=3&monthly_end_date=2024-06-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-04-11&checkout=2024-04-12&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=1&query=Tourcoing%2C%20France&place_id=ChIJXScKvtQow0cRj4WtfX0xLiU&adults=8"
# # Setup Chrome options for undetected_chromedriver
# options = uc.ChromeOptions()

# # Initialize the WebDriver with the specified options
# driver = uc.Chrome(options=options)

# driver.get(url)

# try:
#     while True:  # Boucle jusqu'à ce qu'on ne trouve plus de lien "Suivant"
#         # Attendre que le lien "Suivant" soit chargé et cliquable
#         wait = WebDriverWait(driver, 40)
#         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[rel="noopener noreferrer nofollow"]')))

#         url_elements = driver.find_elements(By.CSS_SELECTOR, '[rel="noopener noreferrer nofollow"]')
#         urls_temp = [
#             element.get_attribute("href")
#             for element in url_elements
#             if element.get_attribute("href").startswith(
#                 "https://www.airbnb.fr/rooms/"
#             )  # avoids to retrieve the urls that redirect to ads
#         ]

#         urls_temp = list(set(urls_temp))
#         urls+= urls_temp
#         next_link = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Suivant"]'))
#         )
        
#          # Cliquer sur le lien "Suivant"
#         link_element= driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Suivant"]')
#         link_url = link_element.get_attribute('href')

#         driver.get(link_url)


        
# except Exception as e:
#     # Si le lien "Suivant" n'est pas trouvé, on suppose qu'on est à la dernière page
#     print("Dernière page atteinte.")

# finally:
#     driver.quit() 


# #for url in urls:
# for i in range(20):  
utils.retrieve_data("https://www.airbnb.fr/rooms/15435153?adults=1&category_tag=Tag%3A670&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=221575830&check_in=2024-03-02&check_out=2024-03-07&source_impression_id=p3_1709118849_jXpRWpu389xiedpy&previous_page_section_name=1000&federated_search_id=02e5416b-aa13-431a-8fb6-ea45f3d00e35", "output.csv")
#     time.sleep(2)


#Preprocess the csv file:
#preprocessing.preprocess_csv('output.csv', 'output_preprocessed.csv')

