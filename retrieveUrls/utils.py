import requests


def fetch_html_with_oxylab(page_url: str) -> str:
    username = "safeflat"
    password = "saaj098KLN++"

    proxies = {
        "http": f"http://{username}:{password}@unblock.oxylabs.io:60000",
        "https": f"http://{username}:{password}@unblock.oxylabs.io:60000",
    }

    response = requests.request(
        "GET",
        page_url,
        verify=False,  # Ignore the certificate
        proxies=proxies,
    )

    return response.text
