from src.retrieveUrls.utils import fetch_html_with_oxylab


def fetch_html_with_oxylab_test():
    res = fetch_html_with_oxylab("https://www.pap.fr")
    assert res != '["Client not found"]'
