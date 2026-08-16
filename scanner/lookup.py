"""
IP geolocation lookup logic.
Talks to the ipwho.is API and returns parsed data. Pure data layer —
no printing, no Rich, so it can be unit tested and reused on its own.
"""

from __future__ import annotations

import ipaddress

import requests

from .errors import InvalidIPError, LookupError

API_BASE = "https://ipwho.is"
DEFAULT_TIMEOUT_SECONDS = 8


def validate_ip(ip: str) -> None:
    """Raise InvalidIPError if `ip` is not empty and not a valid IPv4/IPv6 address."""
    if not ip:
        return  # empty string == "look up my own IP", always valid
    try:
        ipaddress.ip_address(ip)
    except ValueError as exc:
        raise InvalidIPError(f"'{ip}' is not a valid IP address") from exc


def lookup_ip(ip: str = "", timeout: float = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """
    Look up geolocation data for an IP address.
    Pass an empty string to look up the caller's own public IP.

    Returns the parsed JSON response as a dict on success.

    Raises:
        InvalidIPError: if `ip` is not empty and not a syntactically valid IP.
        LookupError: if the request fails (network error, timeout, bad status,
            or the API itself reports success=False).
    """
    validate_ip(ip)

    url = f"{API_BASE}/{ip}" if ip else f"{API_BASE}/"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.Timeout as exc:
        raise LookupError(f"request timed out after {timeout}s") from exc
    except requests.ConnectionError as exc:
        raise LookupError("could not connect — check your internet connection") from exc
    except requests.HTTPError as exc:
        raise LookupError(f"API returned an error status: {exc}") from exc
    except requests.RequestException as exc:
        raise LookupError(str(exc)) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise LookupError("API returned invalid JSON") from exc

    if not data.get("success", True):
        raise LookupError(data.get("message", "unknown API error"))

    return data
