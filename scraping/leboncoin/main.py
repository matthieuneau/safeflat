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
# url = "https://www.leboncoin.fr/offre/locations/2467639678"
url = "https://www.leboncoin.fr/"


# Navigate to the page
driver.get(url)

# Wait to bluff the captcha mechanism
time.sleep(5)

# Find the paragraph element
paragraph = driver.find_element_by_css_selector("p.whitespace-pre-line")

# Retrieve the text
text = paragraph.text

# Write the text to a file
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(text)

# Close the browser
driver.quit()
