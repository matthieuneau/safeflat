from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    #handler(None, None)

    #Download the hmtl of the web page:
    # html_page = fetch_html_with_oxylab("https://www.airbnb.fr/rooms/45859399?category_tag=Tag%3A8678&enable_m3_private_room=true&photo_id=1264383530&search_mode=regular_search&check_in=2024-05-26&check_out=2024-05-27&source_impression_id=p3_1715734328_n9aBmunrWRgPTGsr&previous_page_section_name=1000&federated_search_id=b80d3f0d-b5a6-4512-8c44-bb18523f866d")
    # with open("C:/Users/hennecol/Documents/safeflat/scraping/airbnb-oxylab/annonces/annonce3.html", "w", encoding="utf-8") as file:
    #     file.write(html_page)

    # Find urls:
    # retrieve_urls("https://www.leboncoin.fr/recherche?category=10&owner_type=private")

    # Parse a page:
    data =scrape_ad('https://www.airbnb.fr/rooms/45859399?category_tag=Tag%3A8678&enable_m3_private_room=true&photo_id=1264383530&search_mode=regular_search&check_in=2024-05-26&check_out=2024-05-27&source_impression_id=p3_1715734328_n9aBmunrWRgPTGsr&previous_page_section_name=1000&federated_search_id=b80d3f0d-b5a6-4512-8c44-bb18523f866d')
    print(data)