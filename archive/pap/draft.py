import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from random import random
import pickle


options = uc.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--window-size=1920x1080")
options.add_argument(
    "--Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
)
driver = uc.Chrome(options=options)

driver.get("https://www.pap.fr")
time.sleep(2)

with open("cookies.pkl", "wb") as filehandler:
    pickle.dump(driver.get_cookies(), filehandler)

driver.quit()


options = uc.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--window-size=1920x1080")
options.add_argument(
    "--Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
)

driver = uc.Chrome(options=options)

driver.get("https://www.pap.fr/annonce/location-appartement-maison-1")
time.sleep(2)

with open("cookies.pkl", "rb") as cookiesfile:
    cookies = pickle.load(cookiesfile)
    for cookie in cookies:
        if "domain" in cookie:
            cookie["domain"] = "www.pap.fr"
        driver.add_cookie(cookie)

driver.refresh()

driver.save_screenshot("debug-screenshot.png")
url_list = driver.find_elements(By.CSS_SELECTOR, "a.item-thumb-link")
url_list = [item.get_attribute("href") for item in url_list]
# url_list = url_list[:2]
print(f"url_list: {url_list}")

driver.quit()
