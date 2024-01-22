import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yaml

# import utils

with open("../../Config.yaml", "r") as file:
    config = yaml.safe_load(file)

url = "https://gensdeconfiance.com/fr/annonce/a-louer-de-2019-d707ff8?origin=search&searchRanking=2"
# url = "https://gensdeconfiance.com/fr/annonce/loue-boulogne-rives-de-seine-t4-104m-terrasse-8367bdc?origin=search&searchRanking=8"
# Setup Chrome options for headless browsing
options = Options()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# utils.retrieve_data(url, driver, "output.csv")

driver.get(url)

time.sleep(3)

# # Sign in
# driver.find_element(
#     By.CSS_SELECTOR, "a.Link__Wrapper-sc-1cyaaqe-0-a[href='/fr/connexion']"
# ).click()

# time.sleep(2)

# # Entering email
# email_input = driver.find_element(By.ID, "identifier")
# email_input.send_keys("m.neau10@gmail.com")

# # Entering password
# password_input = driver.find_element(By.ID, "password")
# password_input.send_keys("Safeflat")

# # Clicking on "Se connecter"
# connect_button = driver.find_element(
#     By.XPATH, "//button[span[contains(text(), 'Se connecter')]]"
# )
# connect_button.click()

# time.sleep(2)

result = {}

# Clicking on "Lire la suite" to display the full description if needed
# try:
#     driver.find_element(By.ID, "ad-description__more").click()
# except Exception as e:
#     print("No Lire la suite button", e)

# Extracting title
try:
    title_element = driver.find_element(By.ID, "post-title")
    result["title"] = title_element.text
except Exception as e:
    print("Error extracting title:", e)
    result["title"] = "Title Not Found"

# Extracting location
try:
    location_element = driver.find_element(By.ID, "post-title-breadcrumb")
    location_text = location_element.text.split("\n")[-1].strip()
    result["location"] = location_text
except Exception as e:
    print("Error extracting location:", e)
    location_text = "Location Not Found"

# Extracting rent and bills
try:
    loyer_element = driver.find_element(
        By.CSS_SELECTOR, ".price-table__row .price-table__value"
    )
    loyer_value = loyer_element.text.strip()
    print(loyer_value)
except Exception as e:
    print("Error:", e)

# Extracting description
try:
    description_element = driver.find_element(By.ID, "ad-description")
    # description_element.screenshot("image.jpg")
    description_text = description_element.text.strip()
    result["description"] = description_text
except Exception as e:
    print("Error extracting description:", e)

# Extracting characteristics
# try:
#     li_elements = driver.find_elements(
#         By.CSS_SELECTOR, ".indexclient__GridList-dYErZy.XvGJg > li"
#     )

#     # Iterate over each <li> element to retrieve the value from the <span> tag
#     for li in li_elements:
#         value = li.find_element(By.CSS_SELECTOR, "span.Value__ValueWrapper-dqBrCn").text
#         print(value)

# try:
#     element = driver.find_element(By.ID, "ad-description")
#     driver.execute_script("arguments[0].scrollIntoView();", element)
#     driver.execute_script("window.scrollBy(0, -450);")
#     driver.get_screenshot_as_file("screenshot.png")
# except Exception as e:
#     print(f"Error occurred: {e}")

# time.sleep(4)

# print(result)

driver.quit()
