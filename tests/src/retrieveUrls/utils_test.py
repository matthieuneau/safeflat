import pandas as pd
from src.retrieveUrls.utils import fetch_html_with_oxylab, read_from_database
import pytest


def test_fetch_html_with_oxylab():
    res = fetch_html_with_oxylab("https://www.pap.fr")
    assert res != '["Client not found"]'


@pytest.mark.parametrize(
    "query, expected_output",
    [
        ("SELECT * FROM pap", pd.DataFrame),
        ("SELECT * FROM someTableThatDoesNotExist", Exception),
    ],
)
def test_read_from_database(query, expected_output):
    if issubclass(expected_output, Exception):
        with pytest.raises(expected_output):
            read_from_database(query)
    else:
        result = read_from_database(query)
        assert isinstance(result, expected_output)
