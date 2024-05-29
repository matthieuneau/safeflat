from bs4 import BeautifulSoup
import json
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import *

def retrieve_urls(page_url: str) -> list:
    """Retrieve the URLs of the ads from the page

    Args:
        page (str): url of the page listing the ads

    Returns:
        list: list of the URLs of the ads on the page
    """

    html = fetch_html_with_oxylab(page_url)
    soup = BeautifulSoup(html, "html.parser")

    # #for test purpose only, local html file:
    # file_path = "/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/retrieveUrls/airbnb/listing_annonces.html"
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file, 'lxml')

    id_list = []
    # # Retrieving JSON data:
    try:
        json_data = {}  # Dictionary to store parsed JSON data

        # Find the specific script tag by ID
        script_tag = soup.find("script", id="data-deferred-state-0")

        if script_tag and script_tag.string:
            # Parse the JSON content directly from the script tag
            json_object = json.loads(script_tag.string.strip())
            json_data = json_object  # Store it in the dictionary

        # # For test purpose only: store locally the json file
        # with open("/Users/lucashennecon/Documents/Mission JE/safeflat/safeflat-sam-app/retrieveUrls/airbnb/output.json", 'w') as json_file:
        #     json.dump(json_data, json_file, indent=4)

        id_dict = json_data['niobeMinimalClientData'][0][1]['data']['presentation']['staysSearch']['mapResults']['staysInViewport']
        id_list = [element['listingId'] for element in id_dict]

    except Exception as e:
        print("Error extracting JSON data:", e)

    # Remove duplicates
    id_list = list(set(id_list))

    # Add prefix and editing to have the correct URL
    url_list = [f"https://www.airbnb.fr/rooms/{id}" for id in id_list]
    print("urls retrieved: ", url_list)
    return url_list
