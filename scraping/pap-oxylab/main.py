from utils import *


def handler(event, context):
    res = retrieve_urls("https://www.pap.fr/annonce/location-appartement-maison")
    print(res)


if __name__ == "__main__":
    handler(None, None)
