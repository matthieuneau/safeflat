from utils import *
import scrapeUrls.pap.pap_postprocessing
import scrapeUrls.pap.pap_scraper


def handler(event, context):
    print("scraping urls for: ", event["website"])
    website = event["website"]
    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    scraper = eval(f"{website}.scraper.scrape_ad")
    postprocesser = eval(f"{website}.postprocessing.process_outputs")

    urls_to_scrape = event["sublist"]
    for url in urls_to_scrape:
        print("scraping url: ", url)
        data = scraper(url)
        print("data scraped: ", data)
        data_processed = postprocesser(data)
        print("data processed: ", data_processed)
        data_from_description = process_description(data["description"])
        print("data from description: ", data_from_description)
        merged_data = add_desc_content_to_df(data_from_description, data_processed)
        print("merged data: ", merged_data)
        save_to_database(merged_data, website)
        # Load the protected goods from db

    return "no error so far"
