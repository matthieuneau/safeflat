from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
url = "https://www.airbnb.fr/rooms/13903824?adults=1&category_tag=Tag%3A8678&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1620494697&search_mode=flex_destinations_search&check_in=2024-01-02&check_out=2024-01-07&source_impression_id=p3_1703518192_ivuPMgKq3jSUwhF9&previous_page_section_name=1000&federated_search_id=032d40d9-9d58-464f-aeba-f5374dad8567"

# Navigate to the page
driver.get(url)

# Wait for the element to be loaded
time.sleep(5)

# Find the paragraph element using CSS Selector
paragraph = driver.find_element_by_css_selector(
    ".ll4r2nl.atm_kd_pg2kvz_1bqn0at.dir.dir-ltr"
)

# Retrieve the text
text = paragraph.text

# Write the text to a file
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(text)

# Close the browser
driver.quit()
