from config import settings
from core.api.api_response import ApiResponse
from core.api.clients.base_client import BaseClient
from core.logconfig import get_logger

logger = get_logger(__name__)


class HackerNewsClient(BaseClient):
    def __init__(self, url=None, **kwargs):
        super().__init__(url or settings.url, **kwargs)

    def get_top_stories(self, validate: bool = True) -> ApiResponse:
        return self.get(
            f"{self.url}/v0/topstories.json",
            code=200,
            message="get top stories",
            validate=validate,
        )

    def get_item(self, item_id: int, validate: bool = True) -> ApiResponse:
        return self.get(
            f"{self.url}/v0/item/{item_id}.json",
            code=200,
            message="get item",
            validate=validate,
        )
