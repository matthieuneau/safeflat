from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    #handler(None, None)

    #Download the hmtl of the web page:
    # html_page = fetch_html_with_oxylab("https://www.leboncoin.fr/ad/locations/2689785455")
    # with open("/Users/lucashennecon/Documents/Mission JE/safeflat/scraping/leboncoin-oxylab/annonces/annonce2.html", "w", encoding="utf-8") as file:
    #     file.write(html_page)

    # Find urls:
    # retrieve_urls("https://www.leboncoin.fr/recherche?category=10&owner_type=private")

    # Parse a page:
    data =scrape_ad('https://www.leboncoin.fr/ad/locations/2681655531')
    print(data)