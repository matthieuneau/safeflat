from utils import *
import urllib3

urllib3.disable_warnings()


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    #handler(None, None)

    #Download the hmtl of the web page:
    # html_page = fetch_html_with_oxylab("https://www.abritel.fr/location-vacances/p2162856?chkin=25%2F05%2F2024&chkout=29%2F05%2F2024&d1=2024-05-25&d2=2024-05-26&startDate=25%2F05%2F2024&endDate=29%2F05%2F2024&x_pwa=1&pwa_ts=1715131647160&referrerUrl=aHR0cHM6Ly93d3cuYWJyaXRlbC5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=true&adults=2&regionId=179898&destination=Paris%20%28et%20environs%29%2C%20France&destType=MARKET&neighborhoodId=553248635212958326&latLong=48.853564%2C2.348095&privacyTrackingState=CAN_NOT_TRACK&sort=RECOMMENDED&userIntent=&selectedRoomType=84082205&selectedRatePlan=000369e79bcc9a50478a8508ff1c0cb93f01&expediaPropertyId=84082205&propertyName=Appartement%20id%C3%A9al%20pour%20visite%20Paris&l10n=%5Bobject%20Object%5D&allowPreAppliedFilters=true&amenities=&chain=&daysInFuture=&origin=&group=&guestRating=&hotelName=&lodging=&paymentType=&bedType=&cleaningAndSafetyPractices=&poi=&price=&neighborhood=&roomIndex=&selected=&star=&stayLength=&theme=&travelerType=&bedroomFilter=&deals=&propertyStyle=&misId=&rewards=&pickUpTime=&dropOffTime=&commissionTiers=&agencyBusinessModels=&mealPlan=&cabinClass=&tripType=&airlineCode=&directFlights=&infantsInSeats=&driverAge=&partialStay=false&vacationRentalsOnly=false&mapBounds=&stayType=&house_rules_group=&highlightedPropertyId=&bed_type_group=&stay_options_group=&hotel_brand=&multi_neighborhood_group=&logger=%5Bobject%20Object%5D&petsIncluded=false&bedroom_count_gt=&us_bathroom_count_gt=&pricing_group=&rm1=a2")
    # with open("C:/Users/hennecol/Documents/safeflat/scraping/abritel-oxylab/annonces/annonce2.html", "w", encoding="utf-8") as file:
    #     file.write(html_page)

    # Find urls:
    #retrieve_urls("https://www.abritel.fr/search?destination=Paris%20%28et%20environs%29%2C%20France&regionId=179898&latLong=48.853564%2C2.348095&flexibility=0_DAY&d1=2024-05-25&startDate=2024-05-25&d2=2024-05-26&endDate=2024-05-26&adults=2&theme=&userIntent=&semdtl=&sort=RECOMMENDED")

    # Parse a page:
    scrape_ad(None)