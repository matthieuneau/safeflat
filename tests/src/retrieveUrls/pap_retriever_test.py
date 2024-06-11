from src.retrieveUrls.pap_retriever import retrieve_urls


def test_retrieve_urls():
    """Check that the lists of urls returns are not empty and that they start with the correct prefix"""
    urls = retrieve_urls()
    for i in range(len(urls)):
        assert len(urls[i]) > 0
        for url in urls[i]:
            assert url.startswith("https://www.pap.fr")
