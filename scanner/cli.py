"""
CLI orchestration for terminal-ip-scanner.
Wires together lookup.py (data) and display.py (rendering).
"""

import sys

import requests

from . import display
from .lookup import lookup_ip


def run_targets(targets: list[str]):
    """Look up and render a batch of IPs (empty string == caller's own IP)."""
    for target in targets:
        label = target if target else "SELF"
        display.rule(label)
        display.fake_scan_lines(label)
        try:
            data = lookup_ip(target)
            display.render_result(data)
        except requests.RequestException as e:
            display.print_connection_error(e)


def interactive_menu():
    """Menu loop for easy, no-flags-required usage."""
    display.print_banner()
    display.print_help()

    while True:
        try:
            raw = display.prompt("scanner>")
        except EOFError:
            break

        if raw.lower() in ("q", "quit", "exit"):
            display.print_session_closed()
            break

        targets = raw.split() if raw else [""]
        run_targets(targets)


def main():
    # IPs passed as CLI args -> run once and exit (scriptable mode).
    # No args -> interactive menu (easy mode).
    if len(sys.argv) > 1:
        display.print_banner()
        run_targets(sys.argv[1:])
    else:
        interactive_menu()


def entrypoint():
    try:
        main()
    except KeyboardInterrupt:
        display.print_aborted()


if __name__ == "__main__":
    entrypoint()