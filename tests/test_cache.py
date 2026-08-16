"""
Unit tests for scanner.cache.
"""

from scanner import cache


def setup_function():
    cache.clear()


def test_get_missing_key_returns_none():
    assert cache.get("8.8.8.8") is None


def test_set_then_get_returns_value():
    cache.set("8.8.8.8", {"ip": "8.8.8.8"})
    assert cache.get("8.8.8.8") == {"ip": "8.8.8.8"}


def test_size_tracks_entries():
    assert cache.size() == 0
    cache.set("8.8.8.8", {})
    cache.set("1.1.1.1", {})
    assert cache.size() == 2


def test_clear_empties_cache():
    cache.set("8.8.8.8", {})
    cache.clear()
    assert cache.size() == 0
