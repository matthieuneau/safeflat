import pytest
import os
from src.scrapeUrls.pap_scraper import scrape_ad
from unittest.mock import patch


@pytest.fixture
def mock_fetch_html_with_oxylab(mocker):
    mock = mocker.patch("src.scrapeUrls.pap_scraper.fetch_html_with_oxylab")
    return mock


def test_scrape_ad(mock_fetch_html_with_oxylab):
    # Open the example HTML file
    html_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../scrapeUrls/pap_ad_example_html.txt",
    )
    with open(html_file_path, "r") as file:
        html = file.read()

    # Set the return value of the mock
    mock_fetch_html_with_oxylab.return_value = html

    # Call the function under test
    result = scrape_ad("https://some_url_for_testing.com")

    print(result)

    # Assertions (you need to add your actual expected output and assertions here)
    assert result is not None
