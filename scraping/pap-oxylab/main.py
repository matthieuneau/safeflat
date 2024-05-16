from utils import *


def handler(event, context):
    res = scrape_ad("https://www.pap.fr/annonces/appartement-angers-r451801512")


if __name__ == "__main__":
    handler(None, None)
