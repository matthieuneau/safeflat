from utils import *
import pap.algo


def handler(event, context):
    print("detecting sublets for: ", event["website"])
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

    algo = eval(f"{website}.algo.filter_and_score")

    # FETCH THE GOODS TO PROTECT FROM THE DATABASE
    # goods_to_protect = read_from_database("SELECT * FROM protected_goods")

    for good in goods_to_protect:

