import time
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def get_annonce_data(driver, url):
    """
    Retrieve the data of an annonce from the given url.

    Args:
        driver (_type_): _description_
        url (_type_): _description_

    Returns:
        dict: A dictionary containing the data of the annonce.
    """

    # Navigate to the page
    driver.get(url)

    time.sleep(2)

    data = {}
    # Retrieve the title
    try:
        title = driver.find_element(
            By.CSS_SELECTOR, ".break-words.text-headline-1-expanded.undefined"
        ).text
        data["title"] = title
    except Exception as e:
        print(f"Error retrieving the title: {e}")
        data["title"] = "N/A"

    # Retrieve the specs
    try:
        specs = driver.find_elements(
            By.CSS_SELECTOR, ".inline-flex.w-full.flex-wrap.mb-md span"
        )
        specs = [spec.text for spec in specs]
        data["specs"] = specs
    except Exception as e:
        print(f"Error retrieving the specs: {e}")
        data["specs"] = "N/A"

    # Retrieving price
    try:
        price = driver.find_element(
            By.XPATH, '//*[@id="grid"]/article/div[1]/div/div[1]/div[2]/div/p'
        ).text
        data["price"] = price
    except Exception as e:
        print(f"Error retrieving the price: {e}")
        data["price"] = "N/A"

    # Retrieving post date
    try:
        post_date = driver.find_element(
            By.XPATH,
            '//*[@id="grid"]/article/div[1]/div/div[2]/p',
        ).text
        data["post_date"] = post_date
    except Exception as e:
        print(f"Error retrieving the post date: {e}")
        data["post_date"] = "N/A"

    # Retrieving the authors's name
    try:
        author = driver.find_element(
            By.CSS_SELECTOR,
            "#aside > section > div.sc-6af05cec-0.dCvEUZ > div.pr-md.\[grid-area\:profile\].custom\:pt-none > a",
        ).text
        data["author"] = author
    except Exception as e:
        print(f"Error retrieving the author's name: {e}")
        data["author"] = "N/A"

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
    try:
        description = driver.find_element(
            By.XPATH,
            '//*[@id="grid"]/article/div[4]/div[2]/div/p',
        ).text
        data["description"] = description
    except Exception as e:
        print(f"Error retrieving the description: {e}")
        data["description"] = "N/A"

    # Retrieving the criteres titles and values
    # First we need to click on the "Voir tous les criteres button"
    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "#grid > article > div.grid-flow-rows.grid > div.mx-lg.grid.gap-lg.py-xl.border-b-sm.border-b-neutral\/dim-4.lg\:mx-md.row-start-4 > button",
        ).click()
    except Exception as e:
        print(f"Voir tous les criteres' button not found: {e}")

    try:
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
        titles = [
            item.find_element(By.CSS_SELECTOR, "div>div>p")
            for item in titles_and_values
        ]
        # Retrieving the criteres values
        values = [
            item.find_element(By.CSS_SELECTOR, "div>div>span")
            for item in titles_and_values
        ]
        # Zipping the titles and values together
        criteres = dict(
            zip([title.text for title in titles], [value.text for value in values])
        )
        data["criteres"] = criteres

    except Exception as e:
        print(f"Error retrieving the criteres: {e}")
        data["criteres"] = "N/A"

    # Retrieving the energy class and GES
    try:
        classe_energie = driver.find_element(
            By.XPATH,
            "//div[@data-qa-id='criteria_item_energy_rate']//div[contains(@class,'styles_active__')]",
        ).text
        data["classe_energie"] = classe_energie
    except Exception as e:
        print(f"Error retrieving the energy class: {e}")
        data["classe_energie"] = "N/A"

    try:
        ges = driver.find_element(
            By.XPATH,
            "//div[@data-qa-id='criteria_item_ges']//div[contains(@class,'styles_active__')]",
        ).text
        data["ges"] = ges
    except Exception as e:
        print(f"Error retrieving the GES: {e}")
        data["ges"] = "N/A"

    print(data)
    return data
