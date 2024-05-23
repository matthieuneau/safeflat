from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    #handler(None, None)

    #Download the hmtl of the web page:
    # html_page = fetch_html_with_oxylab("https://www.seloger.com/annonces/locations/appartement/croissy-sur-seine-78/centre-ville/210212077.htm")
    # with open("C:/Users/hennecol/Documents/safeflat/scraping/seloger-oxylab/annonces/annonce2.html", "w", encoding="utf-8") as file:
    #     file.write(html_page)

    # Find urls:
    # retrieve_urls("https://www.seloger.com/list.htm?projects=1&types=2,1&places=[{%22divisions%22:[2238]}]&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&m=search_refine-redirection-search_results")

    # Parse a page:
    data =scrape_ad('https://www.seloger.com/annonces/locations/appartement/livry-gargan-93/sully-vauban/212607781.htm')
    print(data)