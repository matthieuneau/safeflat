import pap.postprocessing

pap.postprocessing.process_outputs()


def handler(event, context):
    print("scraping urls for: ", event["website"])
    website = event["website"]
    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    scraper = eval(f"{website}.scraper.scrape_ad")
    postprocesser = eval(f"{website}.postprocessing.process_outputs")
    descriptionprocesser = 

    urls_to_scrape = event["sublist"]
    for url in urls_to_scrape:
        print("scraping url: ", url)
        data = scraper(url)
        print("data scraped: ", data)
        data_processed = postprocesser(data)
        print("data processed: ", data_processed)

    return "no error so far"
