from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import sys
import time

sys.path.append(
    r"C:\Users\mneau\OneDrive\Bureau\INFO\PYTHON\selenium\chromedriver_1.120.6099.129"
)

# Chrome options
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(
    r"C:\Users\mneau\OneDrive\Bureau\INFO\PYTHON\selenium\chromedriver_1.120.6099.129\chromedriver.exe"
)

# URL of the page
url = "https://www.abritel.fr/location-vacances/p5018652a?dateless=true&x_pwa=1&rfrr=HSR&pwa_ts=1703519688224&referrerUrl=aHR0cHM6Ly93d3cuYWJyaXRlbC5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=true&adults=2&regionId=59&destination=France&destType=MARKET&latLong=46.227638%2C2.213749&privacyTrackingState=CAN_NOT_TRACK&location_group=beach&searchId=a8edb45a-77f4-461c-9010-af09a5482ced&sort=RECOMMENDED&userIntent=&expediaPropertyId=48984559"

# Navigate to the page
driver.get(url)

# Wait for the element to be loaded
time.sleep(3)

try:
    driver.find_element_by_css_selector(
        ".onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon"
    ).click()

except:
    pass

time.sleep(3)

description = driver.find_element_by_css_selector("content-markup").text

# Write the text to a file
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(description)

# Close the browser
driver.quit()
