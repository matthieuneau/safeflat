from .abritel_retriever import retrieve_urls as abritel
from .airbnb_retriever import retrieve_urls as airbnb
from .leboncoin_retriever import retrieve_urls as leboncoin
from .pap_retriever import retrieve_urls as pap
from .seloger_retriever import retrieve_urls as seloger
import os


def handler(event):
    """Calls the appropriate function to retrieve the urls of the ads from the website given in the event

    Parameters
    ----------
    event : dict
        Contains the website to scrape

    Returns
    -------
    list
        The list of urls to scrape and to pass to the subsequent lambda function scrapeUrls

    Raises
    ------
    ValueError
        Provides an error message if the website is not part of those for which the scrapers have been implemented
    """
    print("website to scrape: ", event["website"])

    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    website = event["website"]
    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    urls_retriever = eval(f"{website}.retrieve_urls")
    data = urls_retriever()
    print("urls retrieved: ", data)

    return {"website": event["website"], "lists": data}
