"""
Terminal rendering for terminal-ip-scanner.
All Rich-based output (banner, scan animation, result panels, menu) lives here.
"""

from __future__ import annotations

import time
import random
import shutil
import sys
import json as json_module

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import HEAVY

from .banner import (
    banner_for,
    SCAN_STEPS,
    HELP_LINES,
    MENU_OPTIONS,
    PRIMARY,
    DIM,
    ACCENT,
    RED,
    INFO,
    WARN,
    LABEL,
)
from .errors import ScannerError

# Cap the console width so panels, rules, and separators stay a readable
# size even inside a very wide IDE terminal (e.g. VS Code), instead of
# stretching edge-to-edge with mostly empty space.
_TERM_WIDTH = shutil.get_terminal_size(fallback=(80, 24)).columns
console = Console(width=min(_TERM_WIDTH, 78))


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
        console.print(f"[{PRIMARY}]{banner}[/{PRIMARY}]")
    except UnicodeEncodeError:
        # Last-resort fallback: strip to plain ASCII no matter what.
        console.print(banner_for(width, use_unicode=False).encode("ascii", "replace").decode())

    console.print()


def print_help():
    console.print(f"[{ACCENT}]commands:[/{ACCENT}]")
    for cmd, desc in HELP_LINES:
        console.print(f"  [{PRIMARY}]{cmd:<16}[/{PRIMARY}] {desc}")
    console.print()


def print_menu():
    """Bordered, numbered option menu in the style of classic terminal
    security tools: '[01] Label' entries, each number colored with its
    own accent (hacker-style per-section coloring) rather than one flat
    color for the whole list."""
    console.print(f"[{DIM}][::][/{DIM}] [{ACCENT}]Select an option[/{ACCENT}] [{DIM}][::][/{DIM}]")
    console.print()
    for number, label, color in MENU_OPTIONS:
        console.print(f"[{DIM}][[/{DIM}][{color}]{number}[/{color}][{DIM}]][/{DIM}] {label}")
    console.print()


def fake_scan_lines(target: str, animate: bool = True):
    """Print a few fake 'hacking' status lines for flavor before the real lookup."""
    for step in SCAN_STEPS:
        console.print(f"[{DIM}]>[/{DIM}] {step.format(target=target)}", style=DIM)
        if animate:
            time.sleep(random.uniform(0.08, 0.18))


def render_result(data: dict):
    """
    Render a lookup result as a compact, sectioned panel: a LOCATION block
    (cyan) and a NETWORK block (yellow), inside a green-bordered box sized
    to its content rather than stretched to the terminal's full width.
    """
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

    def section_table(accent: str) -> Table:
        t = Table(show_header=False, box=None, padding=(0, 1))
        t.add_column(style=LABEL, justify="right")
        t.add_column(style=accent)
        return t

    location = section_table(INFO)
    location.add_row("TARGET IP", ip)
    location.add_row("CITY", city)
    location.add_row("REGION", region)
    location.add_row("COUNTRY", f"{country} [{cc}]")
    location.add_row("POSTAL", str(postal))
    location.add_row("COORDS", f"{lat:.4f}, {lon:.4f}" if lat and lon else "-")
    location.add_row("TIMEZONE", tz)

    network = section_table(WARN)
    network.add_row("ISP", isp)
    network.add_row("ORG", org)
    network.add_row("ASN", str(asn))

    body = Group(
        Text(" LOCATION", style=INFO),
        location,
        Text(""),
        Text(" NETWORK", style=WARN),
        network,
    )

    console.print(
        Panel(
            body,
            title=f"[{ACCENT}]TARGET ACQUIRED[/{ACCENT}]",
            subtitle=f"[{DIM}]city/ISP-level accuracy[/{DIM}]",
            border_style="bright_green",
            box=HEAVY,
            expand=False,
        )
    )

    if lat and lon:
        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        console.print(f"[{DIM}]  map ->[/{DIM}] {maps_url}\n")


def print_json(data: dict):
    """Print raw JSON, used with --json flag, no styling, script-friendly."""
    console.print_json(json_module.dumps(data))


def print_error(err: ScannerError):
    console.print(f"[{RED}]ERROR:[/{RED}] {err}\n")


def print_session_closed():
    console.print(f"[{DIM}]session closed.[/{DIM}]")


def print_aborted():
    console.print(f"\n[{RED}]aborted by user[/{RED}]")


def print_saved(path: str):
    console.print(f"[{DIM}]saved ->[/{DIM}] {path}\n")


def print_invalid_choice(choice: str):
    console.print(f"[{RED}]ERROR:[/{RED}] '{choice}' is not a valid option\n")


def rule(label: str):
    console.print()
    console.rule(f"[{ACCENT}]{label}[/{ACCENT}]", style="bright_green")


def prompt(text: str) -> str:
    return console.input(f"[{DIM}][-][/{DIM}] [{ACCENT}]{text}[/{ACCENT}] : ").strip()
