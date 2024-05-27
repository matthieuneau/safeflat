from utils import *

urls = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison-1")
urls = urls[:3] + [
    "https://www.pap.fr/annonces/appartement-alfortville-94140-r452702533"
]

urls = remove_already_scraped_urls(urls)

print(urls)
