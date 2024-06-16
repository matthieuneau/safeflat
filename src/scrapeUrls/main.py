from utils import *
from abritel_scraper import scrape_ad as abritel_scrape_ad
from abritel_postprocessing import process_outputs as abritel_process_outputs
from airbnb_scraper import scrape_ad as airbnb_scrape_ad
from airbnb_postprocessing import process_outputs as airbnb_process_outputs
from leboncoin_scraper import scrape_ad as leboncoin_scrape_ad
from leboncoin_postprocessing import process_outputs as leboncoin_process_outputs
from pap_scraper import scrape_ad as pap_scrape_ad
from pap_postprocessing import process_outputs as pap_process_outputs
from seloger_scraper import scrape_ad as seloger_scrape_ad
from seloger_postprocessing import process_outputs as seloger_process_outputs


def handler(event, _context):
    print("scraping urls for: ", event["website"])
    website = event["website"]
    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    SCRAPER_MAP = {
        "abritel": abritel_scrape_ad,
        "airbnb": airbnb_scrape_ad,
        "leboncoin": leboncoin_scrape_ad,
        "pap": pap_scrape_ad,
        "seloger": seloger_scrape_ad,
    }

    POSTPROCESSER_MAP = {
        "abritel": abritel_process_outputs,
        "airbnb": airbnb_process_outputs,
        "leboncoin": leboncoin_process_outputs,
        "pap": pap_process_outputs,
        "seloger": seloger_process_outputs,
    }

    scraper = SCRAPER_MAP[website]
    postprocesser = POSTPROCESSER_MAP[website]

    urls_to_scrape = event["sublist"]
    for url in urls_to_scrape:
        print("scraping url: ", url)
        data = scraper(url)
        print("data scraped: ", data)
        data_processed = postprocesser(data)
        print("data processed: ", data_processed)
        data_from_description = process_description(data.loc[0, "description"])
        print("data from description: ", data_from_description)
        merged_data = add_desc_content_to_df(data_from_description, data_processed)
        print("merged data: ", merged_data)
        save_to_database(merged_data, website)
        # Load the protected goods from db

    return "no error so far"
