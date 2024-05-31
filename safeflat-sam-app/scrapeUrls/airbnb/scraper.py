from bs4 import BeautifulSoup
import json
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import *

def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    # for test purpose only, local html file:
    # file_path = "/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/airbnb-oxylab/annonces/annonce1.html"
    # with open(file_path, "r", encoding="utf-8") as file:
    #     soup = BeautifulSoup(file, "lxml")

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # # Retrieving JSON data:
    try:
        json_data = {}  # Dictionary to store parsed JSON data

        # Find the specific script tag by ID
        script_tag = soup.find("script", id="data-deferred-state-0")

        if script_tag and script_tag.string:
            # Parse the JSON content directly from the script tag
            json_object = json.loads(script_tag.string.strip())
            json_data = json_object  # Store it in the dictionary

        # #For test purpose only: store locally the json file
        # with open("C:/Users/hennecol/Documents/safeflat/scraping/airbnb-oxylab/annonces/output2.json", 'w') as json_file:
        #     json.dump(json_data, json_file, indent=4)

        # Retrieving url:
        try:
            data["url"] = ad_url
        except Exception as e:
            print("Error retrieving url:", e)
            data["url"] = "Not Available"

        # Retrieving title:
        try:
            data["title"] = json_data["niobeMinimalClientData"][0][1]["data"][
                "presentation"
            ]["stayProductDetailPage"]["sections"]["metadata"]["seoFeatures"]["title"]
        except Exception as e:
            print("Error retrieving title:", e)
            data["title"] = "Not Available"

        # Retrieving type:
        try:
            data["type"] = json_data["niobeMinimalClientData"][0][1]["data"][
                "presentation"
            ]["stayProductDetailPage"]["sections"]["metadata"]["sharingConfig"][
                "propertyType"
            ]
        except Exception as e:
            print("Error retrieving type:", e)
            data["type"] = "Not Available"

        # Retrieving location:
        try:
            data["ville"] = json_data["niobeMinimalClientData"][0][1]["data"][
                "presentation"
            ]["stayProductDetailPage"]["sections"]["metadata"]["sharingConfig"][
                "location"
            ]
        except Exception as e:
            print("Error retrieving ville:", e)
            data["ville"] = "Not Available"

        # Retrieving person_capacity:
        try:
            data["person_capacity"] = json_data["niobeMinimalClientData"][0][1]["data"][
                "presentation"
            ]["stayProductDetailPage"]["sections"]["metadata"]["sharingConfig"][
                "personCapacity"
            ]
        except Exception as e:
            print("Error retrieving person_capacity:", e)
            data["person_capacity"] = "Not Available"

        # Retrieving latitude:
        try:
            data["latitude"] = json_data["niobeMinimalClientData"][0][1]["data"][
                "presentation"
            ]["stayProductDetailPage"]["sections"]["metadata"]["loggingContext"][
                "eventDataLogging"
            ][
                "listingLat"
            ]
        except Exception as e:
            print("Error retrieving latitude:", e)
            data["latitude"] = "Not Available"

        # Retrieving longitude:
        try:
            data["longitude"] = json_data["niobeMinimalClientData"][0][1]["data"][
                "presentation"
            ]["stayProductDetailPage"]["sections"]["metadata"]["loggingContext"][
                "eventDataLogging"
            ][
                "listingLng"
            ]
        except Exception as e:
            print("Error retrieving longitude:", e)
            data["longitude"] = "Not Available"

        # Retrieving property infos list: 
        try:
            data["property_infos_list"] = "Not Available"
            section_data = find_property_list_infos(json_data)
            infos_list_of_dicts = section_data[0]["overviewItems"]
            infos_list = [element["title"] for element in infos_list_of_dicts]
            data["property_infos_list"] = infos_list
        except Exception as e:
            print("Error retrieving property_infos_list:", e)
            

        # Retrieving host name:
        try:
            data["host_name"] = "Not Available"
            section_data = find_host_name(json_data)
            data["host_name"] = section_data[0]["title"] 
        except Exception as e:
            print("Error retrieving host_name:", e)
            

        # Retrieving description:
        try:
            data["description"] = "Not Available"
            desc_dict_list = find_html_descriptions(json_data)
            if desc_dict_list:
                desc_list = [element["htmlText"] for element in desc_dict_list]
            data["description"] = ", ".join(desc_list)
        except Exception as e:
            print("Error retrieving description:", e)

        # Retrieving amenities:
        try:
            data["amenities"] = "Not Available"
            amenities_dict = find_amenities_sections(json_data)[0]
            amenities = []
            allAmenities = amenities_dict["seeAllAmenitiesGroups"]
            for amenities_group in allAmenities:
                for element in amenities_group["amenities"]:
                    amenities.append(element["title"])
            data["amenities"] = amenities
        except Exception as e:
            print("Error retrieving amenities:", e)

        
        # Retrieving bed_types:
        try:
            data["beds_type"] = "Not Available"
            beds_dict_list = find_room_arrangement_items(json_data)
            beds_type = [element["subtitle"] for element in beds_dict_list]
            data["beds_type"] = beds_type
        except Exception as e:
            print("Error retrieving bed_type:", e)

    except Exception as e:
        print("Error extracting JSON data:", e)

    return data


def find_html_descriptions(data, results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        if (
            "htmlDescription" in data
            and data["htmlDescription"].get("__typename") == "ReadMoreHtml"
        ):
            results.append(data["htmlDescription"])
        for key, value in data.items():
            find_html_descriptions(value, results)
    elif isinstance(data, list):
        for item in data:
            find_html_descriptions(item, results)

    return results


def find_amenities_sections(data, results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        if (
            "__typename" in data
            and "previewAmenitiesGroups" in data
            and "seeAllAmenitiesGroups" in data
            and data["__typename"] == "AmenitiesSection"
        ):
            results.append(data)
        for key, value in data.items():
            find_amenities_sections(value, results)
    elif isinstance(data, list):
        for item in data:
            find_amenities_sections(item, results)

    return results


def find_property_list_infos(data, results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        if (
            "__typename" in data
            and "title" in data
            and "overviewItems" in data
            and data["__typename"] == "PdpOverviewV2Section"
        ):
            results.append(data)
        for key, value in data.items():
            find_property_list_infos(value, results)
    elif isinstance(data, list):
        for item in data:
            find_property_list_infos(item, results)

    return results


def find_host_name(data, results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        if (
            "__typename" in data
            and "title" in data
            and "overviewItems" in data
            and "hostAvatar" in data
            and data["__typename"] == "PdpHostOverviewDefaultSection"
        ):
            results.append(data)
        for key, value in data.items():
            find_host_name(value, results)
    elif isinstance(data, list):
        for item in data:
            find_host_name(item, results)

    return results

def find_room_arrangement_items(data, results=None):
    if results is None:
        results = []

    if isinstance(data, dict):
        if (
            "__typename" in data
            and data["__typename"] == "RoomArrangementItem"
            and "title" in data
            and "subtitle" in data
            and "icons" in data
            and "images" in data
        ):
            results.append(data)
        for key, value in data.items():
            find_room_arrangement_items(value, results)
    elif isinstance(data, list):
        for item in data:
            find_room_arrangement_items(item, results)

    return results

