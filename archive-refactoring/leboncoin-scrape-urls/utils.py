def scrape_ad(ad_url: str) -> dict:
    """Scrape the data from the ad URL

    Args:
        url (str): URL of the ad

    Returns:
        dict: data scraped from the ad
    """
    # #for test purpose only, local html file:
    # file_path = "C:/Users/hennecol/Documents/safeflat/scraping/leboncoin-oxylab/annonces/annonce1.html"
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     soup = BeautifulSoup(file, 'lxml')

    html = fetch_html_with_oxylab(ad_url)
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # # Retrieving JSON data:
    try:
        json_data = {}  # Dictionary to store parsed JSON data

        # Find the specific script tag by ID
        script_tag = soup.find("script", id="__NEXT_DATA__")

        if script_tag and script_tag.string:
            # Parse the JSON content directly from the script tag
            json_object = json.loads(script_tag.string.strip())
            json_data = json_object  # Store it in the dictionary

        if json_data:
            ad = json_data["props"]["pageProps"]["ad"]

        # Retrieving url:
        try:
            data["url"] = ad_url
        except Exception as e:
            print("Error retrieving url:", e)
            data["url"] = "Not Available"

        # Retrieving title:
        try:
            data["titre"] = ad["subject"]
        except Exception as e:
            print("Error retrieving titre:", e)
            data["titre"] = "Not Available"

        # Retrieving first publication date:
        try:
            data["first_publication_date"] = ad["first_publication_date"]
        except Exception as e:
            print("Error retrieving first_publication_date:", e)
            data["first_publication_date"] = "Not Available"

        # Retrieving description:
        try:
            data["description"] = ad["body"]
        except Exception as e:
            print("Error retrieving description:", e)
            data["description"] = "Not Available"

        # Retrieving price:
        try:
            data["prix"] = ad["price"][0]
        except Exception as e:
            print("Error retrieving prix:", e)
            data["prix"] = "Not Available"

        # Retrieving property_type:
        try:
            data["type_de_bien"] = ad["attributes"][
                find_index(ad["attributes"], "real_estate_type")
            ]["value_label"]
        except Exception as e:
            print("Error retrieving type_de_bien:", e)
            data["type_de_bien"] = "Not Available"

        # Retrieving furnished or not: 1 if yes 0 if no
        try:
            data["meuble"] = ad["attributes"][
                find_index(ad["attributes"], "furnished")
            ]["value"]
        except Exception as e:
            print("Error retrieving meuble:", e)
            data["meuble"] = "Not Available"

        # Retrieving surface:
        try:
            data["surface"] = ad["attributes"][find_index(ad["attributes"], "square")][
                "value"
            ]
        except Exception as e:
            print("Error retrieving surface:", e)
            data["surface"] = "Not Available"

        # Retrieving nb of rooms:
        try:
            data["nb_rooms"] = ad["attributes"][find_index(ad["attributes"], "rooms")][
                "value"
            ]
        except Exception as e:
            print("Error retrieving nb_rooms:", e)
            data["nb_rooms"] = "Not Available"

        # Retrieving energy rate:
        try:
            data["DPE"] = ad["attributes"][find_index(ad["attributes"], "energy_rate")][
                "value"
            ]
        except Exception as e:
            print("Error retrieving DPE:", e)
            data["DPE"] = "Not Available"

        # Retrieving GES:
        try:
            data["GES"] = ad["attributes"][find_index(ad["attributes"], "ges")]["value"]
        except Exception as e:
            print("Error retrieving GES:", e)
            data["GES"] = "Not Available"

        # Retrieving elevator:
        try:
            data["ascenseur"] = ad["attributes"][
                find_index(ad["attributes"], "elevator")
            ]["value_label"]
        except Exception as e:
            print("Error retrieving ascenseur:", e)
            data["ascenseur"] = "Not Available"

        # Retrieving floor number:
        try:
            data["etage"] = ad["attributes"][
                find_index(ad["attributes"], "floor_number")
            ]["value"]
        except Exception as e:
            print("Error retrieving etage:", e)
            data["etage"] = "Not Available"

        # Retrieving nb of floors in the building:
        try:
            data["nb_etages"] = ad["attributes"][
                find_index(ad["attributes"], "nb_floors_building")
            ]["value"]
        except Exception as e:
            print("Error retrieving nb_etages:", e)
            data["nb_etages"] = "Not Available"

        # Retrieving monthly charges:
        try:
            data["charges"] = ad["attributes"][
                find_index(ad["attributes"], "monthly_charges")
            ]["value"]
        except Exception as e:
            print("Error retrieving charges:", e)
            data["charges"] = "Not Available"

        # Retrieving security deposit:
        try:
            data["caution"] = ad["attributes"][
                find_index(ad["attributes"], "security_deposit")
            ]["value"]
        except Exception as e:
            print("Error retrieving caution:", e)
            data["caution"] = "Not Available"

        # Retrieving region:
        try:
            data["region"] = ad["location"]["region_name"]
        except Exception as e:
            print("Error retrieving region:", e)
            data["region"] = "Not Available"

        # Retrieving department:
        try:
            data["departement"] = ad["location"]["department_name"]
        except Exception as e:
            print("Error retrieving departement:", e)
            data["departement"] = "Not Available"

        # Retrieving city:
        try:
            data["ville"] = ad["location"]["city"]
        except Exception as e:
            print("Error retrieving ville:", e)
            data["ville"] = "Not Available"

        # Retrieving zipcode:
        try:
            data["zipcode"] = ad["location"]["zipcode"]
        except Exception as e:
            print("Error retrieving zipcode:", e)
            data["zipcode"] = "Not Available"

        # Retrieving latitude:
        try:
            data["latitude"] = ad["location"]["lat"]
        except Exception as e:
            print("Error retrieving latitude:", e)
            data["latitude"] = "Not Available"

        # Retrieving longitude:
        try:
            data["longitude"] = ad["location"]["lng"]
        except Exception as e:
            print("Error retrieving longitude:", e)
            data["longitude"] = "Not Available"

        # Retrieving host_name:
        try:
            data["host_name"] = ad["owner"]["name"]
        except Exception as e:
            print("Error retrieving host_name:", e)
            data["host_name"] = "Not Available"

        # For test purpose only: store locally the json file
        # with open("/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/annonces/output.json", 'w') as json_file:
        #     json.dump(json_data, json_file, indent=4)

    except Exception as e:
        print("Error extracting JSON data:", e)

    data = pd.DataFrame([data])

    return data
