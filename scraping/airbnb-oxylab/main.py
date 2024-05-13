from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    #handler(None, None)

    #Download the hmtl of the web page:
    # html_page = fetch_html_with_oxylab("https://www.airbnb.fr/rooms/922476662199202586?adults=1&children=0&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-05-31&check_out=2024-06-01&source_impression_id=p3_1715505742_wbYa3wj70S4PVvCl&previous_page_section_name=1000&federated_search_id=3b0fa2ee-5ad9-435c-84ab-4cd649301685")
    # with open("C:/Users/hennecol/Documents/safeflat/scraping/airbnb-oxylab/annonces/annonce2.html", "w", encoding="utf-8") as file:
    #     file.write(html_page)

    # Find urls:
    # retrieve_urls("https://www.leboncoin.fr/recherche?category=10&owner_type=private")

    # Parse a page:
    data =scrape_ad('https://www.airbnb.fr/rooms/1109220943409848089?adults=1&children=0&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-05-31&check_out=2024-06-01&source_impression_id=p3_1715505742_bzLFl1UsEdblBnmL&previous_page_section_name=1000&federated_search_id=3b0fa2ee-5ad9-435c-84ab-4cd649301685')
    print(data)