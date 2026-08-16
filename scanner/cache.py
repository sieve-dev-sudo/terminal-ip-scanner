"""
Lightweight in-memory cache for lookup results within a single run.
Not persisted to disk — each new process starts with an empty cache.
Keeps repeated lookups of the same IP (e.g. re-running the same target
in interactive mode) from hitting the API again.
"""

from __future__ import annotations

_cache: dict[str, dict] = {}


def get(ip: str) -> dict | None:
    return _cache.get(ip)


def set(ip: str, data: dict) -> None:
    _cache[ip] = data


def clear() -> None:
    _cache.clear()


def size() -> int:
    return len(_cache)
