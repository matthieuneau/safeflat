from abritel import retriever as abritel
from airbnb import retriever as airbnb
from leboncoin import retriever as leboncoin
from pap import retriever as pap
from seloger import retriever as seloger


def handler(event, context):
    print("website to scrape: ", event["website"])

    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    website = event["website"]
    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    urls_retriever = eval(f"{website}.retrieve_urls")
    data = urls_retriever()

    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return {"website": event["website"], "lists": data}
