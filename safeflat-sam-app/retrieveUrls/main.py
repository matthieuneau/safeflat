from abritel import retriever as abritel
from airbnb import retriever as airbnb
from leboncoin import retriever as leboncoin
from gensdeconfiance import retriever as gensdeconfiance
from pap import retriever as pap
from seloger import retriever as seloger
import os


def handler(event, context):
    print("website to scrape: ", event["website"])

    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    website = event["website"]
    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    urls_retriever = eval(f"{website}.retrieve_urls")
    data = urls_retriever()
    print("urls retrieved: ", data)

    return {"website": event["website"], "lists": data}
