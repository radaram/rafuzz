import pytest

from burp_request_parser import BurpRequestParser
from request_parser import RequestParser


@pytest.mark.asyncio
def test_parser_get_request():
    backend_parser = BurpRequestParser
    rp = RequestParser("tests/request_get.txt", backend_parser)
    request = rp.parse_text()
    data = request.get_data()
    assert data.get("method") == "GET"
    assert data.get("path") == "/get?test=FUZZ"
    assert data.get("http_version") == "HTTP/1.1"
    assert data.get("headers")
    assert len(data.get("headers")) == 6
    assert data.get("url") == "httpbin.org/get?test=FUZZ"



@pytest.mark.asyncio
def test_parser_post_request():
    backend_parser = BurpRequestParser
    rp = RequestParser("tests/request_post.txt", backend_parser)
    request = rp.parse_text()
    data = request.get_data()
    assert data.get("method") == "POST"
    assert data.get("path") == "/post"
    assert data.get("http_version") == "HTTP/1.1"
    assert data.get("headers")
    assert len(data.get("headers")) == 6
    assert data.get("url") == "httpbin.org/post"
    assert data.get("post_data") == '{"test": "FUZZ"}'


