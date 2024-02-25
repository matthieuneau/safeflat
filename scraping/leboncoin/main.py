from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import yaml
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# with open("../../config.yaml", "r") as file:
#     config = yaml.safe_load(file)

# Setup Chrome options for undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--incognito")

# Initialize the WebDriver with the specified options
driver = uc.Chrome(options=options)

# URL of the page
url = "file:///Users/mneau/Desktop/safeflat/scraping/leboncoin/example.html"

# Navigate to the page
driver.get(url)

time.sleep(2)

# Retrieve the title
title = driver.find_element(
    By.CSS_SELECTOR, ".break-words.text-headline-1-expanded.undefined"
).text
print(f"title: {title}")

# Retrieve the specs
specs = driver.find_elements(
    By.CSS_SELECTOR, ".inline-flex.w-full.flex-wrap.mb-md span"
)
specs = [spec.text for spec in specs]
print(f"specs: {specs}")

# Retrieving price
price = driver.find_element(
    By.XPATH, '//*[@id="grid"]/article/div[1]/div/div[1]/div[2]/div/p'
).text
print(f"price: {price}")

# Retrieving post date
post_date = driver.find_element(
    By.XPATH,
    '//*[@id="grid"]/article/div[1]/div/div[2]/p',
).text
print(f"post_date: {post_date}")

# Retrieving the authors's name
try:
    author = driver.find_element(
        By.CSS_SELECTOR,
        "#aside > section > div.sc-6af05cec-0.dCvEUZ > div.pr-md.\[grid-area\:profile\].custom\:pt-none > a",
    ).text
    print(f"author: {author}")
except Exception as e:
    print(f"Error retrieving the author's name: {e}")

# Retrieving description
# Clicking on the "Voir plus" button to display the full description
try:
    driver.find_element(
        By.CSS_SELECTOR,
        "#grid > article > div.grid-flow-rows.grid > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-1 > div > button",
    ).click()
except Exception as e:
    print(f"Error clicking on the 'Voir plus' button: {e}")
# Now we can actually retrieve the description
description = driver.find_element(
    By.XPATH,
    '//*[@id="grid"]/article/div[4]/div[2]/div/p',
).text
print(f"description: {description}")

# Retrieving the criteres titles and values
# First we need to click on the "Voir tous les criteres button"
try:
    driver.find_element(
        By.CSS_SELECTOR,
        "#grid > article > div.grid-flow-rows.grid > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > button",
    ).click()
except Exception as e:
    print(f"Voir tous les criteres' button not found: {e}")
titles_and_values = driver.find_elements(
    By.CSS_SELECTOR, "div.styles_criteria__U5Ul8.flex.flex-wrap > div"
)
# Filter out energy class and GES because we need to treat them separately
titles_and_values = [
    item
    for item in titles_and_values
    if (
        item.find_element(By.CSS_SELECTOR, "div > div > p").text
        not in ["Classe énergie", "GES"]
    )
]

# Retrieving the criteres titles
titles = [item.find_element(By.CSS_SELECTOR, "div>div>p") for item in titles_and_values]
print("titles: ", [value.text for value in titles])

# Retrieving the criteres values
values = [
    item.find_element(By.CSS_SELECTOR, "div>div>span") for item in titles_and_values
]
print("values: ", [value.text for value in values])

# Zipping the titles and values together
criteres = dict(zip([title.text for title in titles], [value.text for value in values]))
print("criteres: ", criteres)

# Retrieving the energy class and GES
class_energie = driver.find_element(
    By.CSS_SELECTOR,
    "#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > div > div:nth-child(5) > div > div > div.styles_active__6vnrC",
).text
print(f"class_energie: {class_energie}")

# ges = driver.find_element(
#     By.CSS_SELECTOR,
#     "#grid > article > div.grid.grid-flow-row > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > div > div:nth-child(6) > div > div > div.styles_item__YzUPI.styles_active__6vnrC",
# ).text
# print(f"ges: {ges}")


# Close the browser
driver.quit()

# grid > article > div:nth-child(2) > div > div.sc-12a6ec0d-0.gJGwBE > div.mr-md.flex.flex-wrap.items-center.justify-between > div > p
