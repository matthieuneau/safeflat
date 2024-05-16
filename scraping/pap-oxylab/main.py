from utils import *
import json


def handler(event, context):

    num_pages = 4
    for i in range(num_pages):
        urls = retrieve_urls(
            f"https://www.pap.fr/annonce/location-appartement-maison-{i}"
        )
        for url in urls:
            try:
                scraped_data = scrape_ad(url)
                scraped_data = process_outputs(scraped_data)

                desc_data = process_description(scraped_data["description"])

                merged_data = add_desc_content_to_df(desc_data, scraped_data)
                save_to_database(merged_data)
            except Exception as e:
                print(f"An error occrued while processing the ad: {url}", "\n", e)

    return {"statusCode": 200, "body": json.dumps("Lambda executed successfully!")}


if __name__ == "__main__":
    handler(None, None)
