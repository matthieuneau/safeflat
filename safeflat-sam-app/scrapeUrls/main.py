from abritel import scraper as abritel
from airbnb import scraper as airbnb
from leboncoin import scraper as leboncoin
from gensdeconfiance import scraper as gensdeconfiance
from pap import scraper as pap
from seloger import scraper as seloger


def handler(event, context):
    print("scraping urls for: ", event["website"])
    urls_to_scrape = event["sublist"]
    for url in urls_to_scrape:
        print("scraping url: ", url)

    return "no error so far"
