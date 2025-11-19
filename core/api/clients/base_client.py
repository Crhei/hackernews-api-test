import json as json_lib
from typing import List
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from config import settings
from core.api.api_response import ApiResponse
from core.logconfig import get_logger

logger = get_logger(__name__)

class BaseClient:
    """Base class for API clients for GET requests only"""

    def __init__(
        self,
        url: str,
        retry_codes: List = None,
    ):
        """Initialize the base client"""
        self.url = url
        self.retry_codes = [429] if not retry_codes else retry_codes
        self._session = None

    def update_headers(self, headers):
        """Update request headers with data provided from the test/client"""
        if headers:
            self._session.headers.update(headers)

    def send(
        self,
        verb,
        url,
        headers=None,
        params=None,
        follow_redirects=True,
        code=None,
        message=None,
        validate=True,
    ):
        """Send a GET request (only GET is supported)"""
        self._session = requests.Session()

        retries = Retry(
            total=4,
            backoff_factor=1,
            status_forcelist=self.retry_codes,
            allowed_methods=frozenset(["GET"]),
        )
        self._session.mount("http://", HTTPAdapter(max_retries=retries))
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self.update_headers(headers)

        params = (
            {k: v for k, v in params.items() if v is not None} if params else None
        )  # remove empty query params
        self._session.params = params

        if message:
            logger.info(message[:1].upper() + message[1:])
        else:
            logger.warning(f"Please add log message for `{verb} {url}`")
        
        if settings.detailed_logs:  # for tracing logs
            processed_request_txt = self.request_as_text(
                url, verb, params
            )
            log_request(processed_request_txt)
        
        try:
            response = self._session.request(
                verb,
                url,
                verify=True,
                allow_redirects=follow_redirects,
            )
        except Exception as e:
            raise ConnectionError("Failed to get response\n" + str(e)) from None
        
        if settings.detailed_logs:
            log_response(response)

        if validate and code and response.status_code != code:
            ApiResponse(response).raise_error(
                f"Failed to {message}\n"
                f"Status code: {response.status_code} ({code} expected)"
            )
        return ApiResponse(response, response.elapsed)

    def get(
        self,
        url,
        headers=None,
        params=None,
        follow_redirects=True,
        code=None,
        message=None,
        validate=True,
    ):
        """Send a GET request"""
        return self.send(
            "get",
            url,
            headers=headers,
            params=params,
            follow_redirects=follow_redirects,
            code=code,
            message=message,
            validate=validate,
        )

    def request_as_text(self, url, verb, params):
        """Format request as text for logging"""
        host = urlparse(url).netloc
        query = (
            ("?" + "&".join("%s=%s" % (k, v) for k, v in list(params.items())))
            if params
            else ""
        )
        path = f"{urlparse(url).path}{query}"
        headers = "\n".join(
            [": ".join([k, v]) for k, v in list(self._session.headers.items())]
        )
        return f"{verb.upper()} {path} HTTP/1.1\nHost: {host}\n{headers}\n"


def log_request(request_txt):
    logger.debug(f"Request\n{request_txt}\n{'-' * 25} End of request {'-' * 25}")


def log_response(response):
    content_type = (
        response.headers["Content-Type"]
        if "Content-Type" in response.headers
        else "undefined"
    )
    if response.text and "json" in content_type:
        try:
            response_body = json_lib.dumps(
                response.json(), indent=4, sort_keys=True
            )
        except ValueError as e:
            logger.warning(f"Failed to parse response JSON body. {e}")
            response_body = response.text
    else:
        response_body = response.text

    response_headers = "\n".join(
        [": ".join([k, v]) for k, v in list(response.headers.items())]
    )
    logger.debug(
        f"Response ({response.elapsed})\nHTTP/1.1 {response.status_code} {response.reason}\n"
        f"{response_headers}\n\n{response_body}\n{'-' * 25} End of response {'-' * 25}"
    )
