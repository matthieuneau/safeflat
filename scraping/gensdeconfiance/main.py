import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# import utils

# url = "https://gensdeconfiance.com/fr/annonce/a-louer-de-2019-d707ff8?origin=search&searchRanking=2"
url = "https://gensdeconfiance.com/fr/annonce/loue-boulogne-rives-de-seine-t4-104m-terrasse-8367bdc?origin=search&searchRanking=8"
# Setup Chrome options for headless browsing
options = Options()

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# utils.retrieve_data(url, driver, "output.csv")

driver.get(url)

time.sleep(3)

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
# try:
#     loyer_element = driver.find_element(
#         By.XPATH,
#         "//div[contains(@class, 'price-table')]//div[contains(@class, 'price-table__row')][1]//div[contains(@class, 'price-table__value')]",
#     )
#     loyer = loyer_element.text.strip()
#     print("Loyer:", loyer)
# except Exception as e:
#     print("Error:", e)

# Extracting description
try:
    description_element = driver.find_element(By.ID, "ad-description")
    description_element.screenshot("image.jpg")
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
#     characteristics_element = driver.find_element(
#         By.CSS_SELECTOR, r"#sfreact-reactRenderer65ad9e4b182194.59758836 > ul"
#     )
#     characteristics_element.screenshot("image.jpg")
# except Exception as e:
#     print(f"Error occurred: {e}")

print(result)

driver.quit()
