import requests


def fetch_html_with_oxylab(page_url: str) -> str:
    """Uses oxylab as a wrapper to fetch the html of a page to avoid being blocked

    Parameters
    ----------
    page_url : str
        page for which the html is to be fetched

    Returns
    -------
    str
        the html of the page
    """
    proxies = {
        "http": "http://wrongusername:wrongpassword@unblock.oxylabs.io:60000",
        "https": "http://wrongusername:wrongpassword@unblock.oxylabs.io:60000",
    }

    response = requests.request(
        "GET",
        page_url,
        verify=False,  # Ignore the certificate
        proxies=proxies,
    )

    return response.text


print(type(fetch_html_with_oxylab("https://www.pap.fr")))
