import json as j

class ApiResponse:
    """API response wrapper"""

    def __init__(self, response, response_time=None):
        self.response = response
        self.response_time = response_time

    def status_code(self):
        return self.response.status_code

    def headers(self):
        return self.response.headers

    def content(self):
        return self.response.text

    def json(self):
        """Returns JSON as dict"""
        try:
            if self.response.text:
                return self.response.json()
            return ""
        except ValueError as e:
            raise ValueError(
                f"Failed to parse JSON response: {e}\n"
                f"Actual response: {self.response.text}"
            ) from e

    def raise_error(self, message):
        try:
            body = f"\n{j.dumps(j.loads(self.content()), indent=4, sort_keys=True)}"
        except ValueError:
            body = self.content()
        raise ValueError(
            f"{message}\n"
            f"Response body: {body[:200]}...\n...\n(response body is truncated)"
        )
