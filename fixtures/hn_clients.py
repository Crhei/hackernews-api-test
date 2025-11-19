import pytest

from core.api.clients.hackernews_client import HackerNewsClient

@pytest.fixture
def hn_client():
    yield HackerNewsClient()
