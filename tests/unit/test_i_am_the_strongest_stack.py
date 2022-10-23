from __future__ import annotations

import json
from http import HTTPStatus
from typing import Any

from aws_lambda_powertools.event_handler import content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from strongest_function import index as app


class Response:
    def __init__(self, response: dict[str, Any]) -> None:
        self._status_code: int = response.get("statusCode", 0)
        self._headers: dict[str, Any] = response.get("headers", {"", ""})
        self._content_type: str = self._headers.get("Content-Type", "")
        self._is_base64_encoded: bool = response.get("isBase64Encoded", False)
        self._multi_value_headers: dict[str, Any] = response.get(
            "multiValueHeaders", {"", ""}
        )
        self._body: str | bytes = response.get("body", "")

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def headers(self) -> dict[str, Any]:
        return self._headers

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def is_base64_encoded(self) -> bool:
        return self._is_base64_encoded

    @property
    def multi_value_headers(self) -> dict[str, Any]:
        return self._multi_value_headers

    @property
    def body(self) -> Any:
        if self._content_type == content_types.APPLICATION_JSON:
            res: dict[str, Any] = json.loads(self._body)
            return res
        return self.body


def apigw_event(path: str, body: dict[str, Any] | str, method: str) -> dict[str, Any]:
    """Generates API GW Event"""

    if isinstance(body, dict):
        body = json.dumps(body)

    return {
        "body": body,
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": method,
        "stageVariables": {"baz": "qux"},
        "path": path,
    }


def test_get_status() -> None:
    body: dict[str, Any] = {}
    path: str = "/status"
    method: str = "GET"
    event = apigw_event(path, body, method)
    context = LambdaContext()

    res = Response(app.handler(event, context))
    data: str = res.body.get("status", "")

    assert data == "ok"


def test_post_new_genesis() -> None:
    body: dict[str, Any] = {"test": "abc"}
    path: str = "/new-genesis"
    method: str = "POST"
    event = apigw_event(path, body, method)
    context = LambdaContext()

    res = Response(app.handler(event, context))
    data: str = res.body.get("test", "")

    assert res.status_code == HTTPStatus.OK.value
    assert "uuid4" in res.headers
    assert data == "abc"
    assert res.content_type == content_types.APPLICATION_JSON


def test_put_i_am_invincible() -> None:
    body: dict[str, Any] = {}
    path: str = "/new-genesis/i-am-invincible"
    method: str = "PUT"
    event = apigw_event(path, body, method)
    context = LambdaContext()

    res = Response(app.handler(event, context))
    data: str = res.body.get("message", "")

    assert res.status_code == HTTPStatus.BAD_REQUEST.value
    assert data == "未実装"
