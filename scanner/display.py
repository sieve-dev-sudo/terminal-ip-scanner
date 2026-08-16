"""
Terminal rendering for terminal-ip-scanner.
All Rich-based output (banner, scan animation, result panels) lives here.
"""

import time
import random

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import HEAVY

from .banner import BANNER, TAGLINE, SCAN_STEPS, HELP_LINES, GREEN, DIM_GREEN, RED

console = Console()


def print_banner():
    console.print(f"[{GREEN}]{BANNER}[/{GREEN}]")
    console.print(Align.center(Text(TAGLINE, style=DIM_GREEN)))
    console.print()


def print_help():
    console.print(f"[{DIM_GREEN}]commands:[/{DIM_GREEN}]")
    for cmd, desc in HELP_LINES:
        console.print(f"  [{GREEN}]{cmd:<16}[/{GREEN}] {desc}")
    console.print()


def fake_scan_lines(target: str):
    """Print a few fake 'hacking' status lines for flavor before the real lookup."""
    for step in SCAN_STEPS:
        console.print(f"[{DIM_GREEN}]>[/{DIM_GREEN}] {step.format(target=target)}", style=DIM_GREEN)
        time.sleep(random.uniform(0.08, 0.18))


def render_result(data: dict):
    if not data.get("success", True):
        console.print(
            Panel(
                f"[{RED}]LOOKUP FAILED[/{RED}]\n{data.get('message', 'unknown error')}",
                border_style="red",
                box=HEAVY,
            )
        )
        return

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


def print_connection_error(err: Exception):
    console.print(f"[{RED}]CONNECTION ERROR:[/{RED}] {err}\n")


def print_session_closed():
    console.print(f"[{DIM_GREEN}]session closed.[/{DIM_GREEN}]")


def print_aborted():
    console.print(f"\n[{RED}]aborted by user[/{RED}]")


def rule(label: str):
    console.print()
    console.rule(f"[{GREEN}]{label}[/{GREEN}]", style="green")


def prompt(text: str) -> str:
    return console.input(f"[{GREEN}]{text}[/{GREEN}] ").strip()