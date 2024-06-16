from utils import *
from pap_algo import filter_and_score as pap_filter_and_score


def handler(event, _context):
    print("detecting sublets for ads coming from: ", event["website"])
    print("scraped_data", event["scraped_data"])
    website = event["website"]
    allowed_websites = {
        "leboncoin",
        "airbnb",
        "pap",
        "seloger",
        "abritel",
        "gensdeconfiance",
    }

    if website not in allowed_websites:
        raise ValueError(f"No algorithm implemented for this website: {website}")

    ALGO_MAP = {"pap": pap_filter_and_score}

    # NEED TO FETCH THE ACTUAL DATA FROM THE CLIENT
    properties_to_protect = get_client_data()
    print("properties to protect fetched from DB: ", properties_to_protect)


if __name__ == "__main__":
    handler({"website": "pap", "scraped_data": "data"}, None)
