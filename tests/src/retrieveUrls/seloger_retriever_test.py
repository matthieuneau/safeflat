from src.retrieveUrls.seloger_retriever import retrieve_urls


def test_retrieve_urls():
    urls = retrieve_urls()
    assert len(urls) > 0
