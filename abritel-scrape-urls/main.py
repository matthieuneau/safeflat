from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    #handler(None, None)

    #Download the hmtl of the web page:
    # html_page = fetch_html_with_oxylab("https://www.abritel.fr/location-vacances/p2104945?chkin=2024-05-25&chkout=2024-05-26&d1=2024-05-25&d2=2024-05-26&startDate=2024-05-25&endDate=2024-05-26&x_pwa=1&rfrr=HSR&pwa_ts=1715166053627&referrerUrl=aHR0cHM6Ly93d3cuYWJyaXRlbC5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=true&adults=2&regionId=6217179&destination=Strasbourg%2C+Bas-Rhin+%28d%C3%A9partement%29%2C+France&destType=MARKET&neighborhoodId=553248635976398536&latLong=48.5835%2C7.74588&searchId=27ca03ba-c6c9-4426-a096-2d4a2d1209ac&privacyTrackingState=CAN_NOT_TRACK&sort=RECOMMENDED&top_dp=85&top_cur=EUR&userIntent=&selectedRoomType=77095833&selectedRatePlan=0003b27547198ca343bdb16233c0588ed9f4&expediaPropertyId=77095833&propertyName=Un+appartement+refait+%C3%A0+neuf")
    # with open("C:/Users/hennecol/Documents/safeflat/scraping/abritel-oxylab/annonces/annonce3.html", "w", encoding="utf-8") as file:
    #     file.write(html_page)

    # Find urls:
    #retrieve_urls("https://www.abritel.fr/search?destination=Paris%20%28et%20environs%29%2C%20France&regionId=179898&latLong=48.853564%2C2.348095&flexibility=0_DAY&d1=2024-05-25&startDate=2024-05-25&d2=2024-05-26&endDate=2024-05-26&adults=2&theme=&userIntent=&semdtl=&sort=RECOMMENDED")

    # Parse a page:
    data =scrape_ad('https://www.abritel.fr/location-vacances/p2104945?chkin=2024-05-25&chkout=2024-05-26&d1=2024-05-25&d2=2024-05-26&startDate=2024-05-25&endDate=2024-05-26&x_pwa=1&rfrr=HSR&pwa_ts=1715166053627&referrerUrl=aHR0cHM6Ly93d3cuYWJyaXRlbC5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=true&adults=2&regionId=6217179&destination=Strasbourg%2C+Bas-Rhin+%28d%C3%A9partement%29%2C+France&destType=MARKET&neighborhoodId=553248635976398536&latLong=48.5835%2C7.74588&searchId=27ca03ba-c6c9-4426-a096-2d4a2d1209ac&privacyTrackingState=CAN_NOT_TRACK&sort=RECOMMENDED&top_dp=85&top_cur=EUR&userIntent=&selectedRoomType=77095833&selectedRatePlan=0003b27547198ca343bdb16233c0588ed9f4&expediaPropertyId=77095833&propertyName=Un+appartement+refait+%C3%A0+neuf')
    print(data)