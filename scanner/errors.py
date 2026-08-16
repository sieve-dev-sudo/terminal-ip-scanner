"""
Custom exceptions for terminal-ip-scanner.
Keeping these separate from lookup.py makes them easy to import
from tests or other consumers without pulling in the requests dependency.
"""


class ScannerError(Exception):
    """Base class for all terminal-ip-scanner errors."""


class InvalidIPError(ScannerError):
    """Raised when the given string is not a valid IPv4/IPv6 address."""


class LookupError(ScannerError):
    """Raised when the geolocation API call fails or returns an error."""
