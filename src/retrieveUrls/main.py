from abritel_retriever import retrieve_urls as abritel_retrieve_urls
from airbnb_retriever import retrieve_urls as airbnb_retrieve_urls
from leboncoin_retriever import retrieve_urls as leboncoin_retrieve_urls
from gensdeconfiance_retriever import retrieve_urls as gensdeconfiance_retrieve_urls
from pap_retriever import retrieve_urls as pap_retrieve_urls
from seloger_retriever import retrieve_urls as seloger_retrieve_urls
from utils import remove_already_scraped_urls


def handler(event, _context):
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

    FUNCTIONS_MAP = {
        "abritel": abritel_retrieve_urls,
        "airbnb": airbnb_retrieve_urls,
        "leboncoin": leboncoin_retrieve_urls,
        "gensdeconfiance": gensdeconfiance_retrieve_urls,
        "pap": pap_retrieve_urls,
        "seloger": seloger_retrieve_urls,
    }

    allowed_websites = {"abritel", "airbnb", "leboncoin", "pap", "seloger"}

    website = event["website"]
    if website not in allowed_websites:
        raise ValueError(f"No scraper implemented for this website: {website}")

    url_retriever = FUNCTIONS_MAP[website]
    data = url_retriever()
    # filter out urls already in database to avoid useless scraping
    data = remove_already_scraped_urls(data, website)
    print("urls retrieved: ", data)

    return {"website": event["website"], "lists": data}
