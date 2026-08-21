"""
Terminal rendering for terminal-ip-scanner.
All Rich-based output (banner, scan animation, result panels) lives here.
"""

from __future__ import annotations

import time
import random
import shutil
import sys
import json as json_module

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import HEAVY

from .banner import banner_for, TAGLINE, CREDIT, SCAN_STEPS, HELP_LINES, GREEN, DIM_GREEN, RED
from .errors import ScannerError

console = Console()


def _terminal_supports_unicode() -> bool:
    """Best-effort check that stdout can render Unicode box-drawing chars.
    True on virtually every modern Linux/Kali/macOS terminal; only false
    on the rare non-UTF-8 locale (e.g. some minimal SSH/container setups)."""
    encoding = getattr(sys.stdout, "encoding", None) or ""
    try:
        "─│┌┐└┘".encode(encoding)
        return True
    except (LookupError, UnicodeEncodeError, TypeError):
        return False


def print_banner():
    """
    Print a banner sized and encoded to match the current terminal, so it
    never wraps or renders as garbled characters -- the two ways an ASCII
    banner typically "breaks" after a fresh `git clone` on a new machine
    (e.g. an 80-column default terminal on Kali, or a non-UTF-8 SSH session).
    """
    width = shutil.get_terminal_size(fallback=(80, 24)).columns
    use_unicode = _terminal_supports_unicode()
    banner = banner_for(width, use_unicode=use_unicode)

    try:
        console.print(f"[{GREEN}]{banner}[/{GREEN}]")
    except UnicodeEncodeError:
        # Last-resort fallback: strip to plain ASCII no matter what.
        console.print(banner_for(width, use_unicode=False).encode("ascii", "replace").decode())

    console.print(Text(TAGLINE, style=DIM_GREEN))
    console.print()
    console.print(Text(CREDIT, style=DIM_GREEN))
    console.print()


def print_help():
    console.print(f"[{DIM_GREEN}]commands:[/{DIM_GREEN}]")
    for cmd, desc in HELP_LINES:
        console.print(f"  [{GREEN}]{cmd:<16}[/{GREEN}] {desc}")
    console.print()


def fake_scan_lines(target: str, animate: bool = True):
    """Print a few fake 'hacking' status lines for flavor before the real lookup."""
    for step in SCAN_STEPS:
        console.print(f"[{DIM_GREEN}]>[/{DIM_GREEN}] {step.format(target=target)}", style=DIM_GREEN)
        if animate:
            time.sleep(random.uniform(0.08, 0.18))


def render_result(data: dict):
    ip = data.get("ip", "?")
    city = data.get("city") or "UNKNOWN"
    region = data.get("region") or "-"
    country = data.get("country") or "UNKNOWN"
    cc = data.get("country_code") or "--"
    postal = data.get("postal") or "-"
    lat = data.get("latitude")
    lon = data.get("longitude")
    tz = (data.get("timezone") or {}).get("id", "-")
    conn = data.get("connection") or {}
    isp = conn.get("isp") or "-"
    org = conn.get("org") or "-"
    asn = conn.get("asn") or "-"

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style=DIM_GREEN, justify="right")
    table.add_column(style=GREEN)

    table.add_row("TARGET IP", ip)
    table.add_row("CITY", city)
    table.add_row("REGION", region)
    table.add_row("COUNTRY", f"{country} [{cc}]")
    table.add_row("POSTAL", str(postal))
    table.add_row("COORDS", f"{lat:.4f}, {lon:.4f}" if lat and lon else "-")
    table.add_row("TIMEZONE", tz)
    table.add_row("ISP", isp)
    table.add_row("ORG", org)
    table.add_row("ASN", str(asn))

    console.print(
        Panel(
            table,
            title=f"[{GREEN}]TARGET ACQUIRED[/{GREEN}]",
            subtitle=f"[{DIM_GREEN}]accuracy: city/ISP-level, not exact address[/{DIM_GREEN}]",
            border_style="green",
            box=HEAVY,
        )
    )

    if lat and lon:
        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        console.print(f"[{DIM_GREEN}]  map ->[/{DIM_GREEN}] {maps_url}\n")


def print_json(data: dict):
    """Print raw JSON — used with --json flag, no styling, script-friendly."""
    console.print_json(json_module.dumps(data))


def print_error(err: ScannerError):
    console.print(f"[{RED}]ERROR:[/{RED}] {err}\n")


def print_session_closed():
    console.print(f"[{DIM_GREEN}]session closed.[/{DIM_GREEN}]")


def print_aborted():
    console.print(f"\n[{RED}]aborted by user[/{RED}]")


def print_saved(path: str):
    console.print(f"[{DIM_GREEN}]saved ->[/{DIM_GREEN}] {path}\n")


def rule(label: str):
    console.print()
    console.rule(f"[{GREEN}]{label}[/{GREEN}]", style="green")


def prompt(text: str) -> str:
    return console.input(f"[{GREEN}]{text}[/{GREEN}] ").strip()
