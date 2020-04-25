import pytest
import sys

sys.path.append('../lib')
import config
from fetch_more import fetch_more

def test_fetch_more_exists():
    assert fetch_more(config.url_more)

pytest.main()
