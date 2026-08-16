"""
Unit tests for scanner.lookup — the API is mocked, no real network calls.
Run with: pytest
"""

import pytest
import requests

from scanner.errors import InvalidIPError, LookupError
from scanner.lookup import lookup_ip, validate_ip


class TestValidateIP:
    def test_empty_string_is_valid(self):
        validate_ip("")  # should not raise

    def test_valid_ipv4(self):
        validate_ip("8.8.8.8")  # should not raise

    def test_valid_ipv6(self):
        validate_ip("2001:4860:4860::8888")  # should not raise

    def test_invalid_ip_raises(self):
        with pytest.raises(InvalidIPError):
            validate_ip("not-an-ip")

    def test_out_of_range_octet_raises(self):
        with pytest.raises(InvalidIPError):
            validate_ip("999.999.999.999")


class TestLookupIP:
    def test_invalid_ip_raises_before_request(self, mocker):
        mock_get = mocker.patch("requests.get")
        with pytest.raises(InvalidIPError):
            lookup_ip("garbage")
        mock_get.assert_not_called()

    def test_successful_lookup_returns_data(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "success": True,
            "ip": "8.8.8.8",
            "city": "Mountain View",
            "country": "United States",
        }
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.get", return_value=mock_response)

        data = lookup_ip("8.8.8.8")
        assert data["ip"] == "8.8.8.8"
        assert data["city"] == "Mountain View"

    def test_api_reports_failure_raises_lookup_error(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "success": False,
            "message": "invalid IP address",
        }
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.get", return_value=mock_response)

        with pytest.raises(LookupError, match="invalid IP address"):
            lookup_ip("1.2.3.4")

    def test_timeout_raises_lookup_error(self, mocker):
        mocker.patch("requests.get", side_effect=requests.Timeout())
        with pytest.raises(LookupError, match="timed out"):
            lookup_ip("8.8.8.8")

    def test_connection_error_raises_lookup_error(self, mocker):
        mocker.patch("requests.get", side_effect=requests.ConnectionError())
        with pytest.raises(LookupError, match="connect"):
            lookup_ip("8.8.8.8")

    def test_empty_ip_queries_self_endpoint(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"success": True, "ip": "1.2.3.4"}
        mock_response.raise_for_status.return_value = None
        mock_get = mocker.patch("requests.get", return_value=mock_response)

        lookup_ip("")
        called_url = mock_get.call_args[0][0]
        assert called_url == "https://ipwho.is/"
