"""
IP geolocation lookup logic.
Talks to the ipwho.is API and returns raw JSON data.
"""

import requests

API_BASE = "https://ipwho.is"
TIMEOUT_SECONDS = 8


def lookup_ip(ip: str = "") -> dict:
    """
    Look up geolocation data for an IP address.
    Pass an empty string to look up the caller's own public IP.

    Returns the parsed JSON response as a dict. On failure, the dict
    will contain "success": False and a "message" key.
    """
    url = f"{API_BASE}/{ip}" if ip else f"{API_BASE}/"
    response = requests.get(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()