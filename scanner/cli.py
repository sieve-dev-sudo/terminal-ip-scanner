"""
CLI orchestration for terminal-ip-scanner.
Wires together lookup.py (data), cache.py (dedup), and display.py (rendering).
"""

from __future__ import annotations

import argparse
import json
import sys

from . import cache, display
from .errors import ScannerError
from .lookup import DEFAULT_TIMEOUT_SECONDS, lookup_ip


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="terminal-ip-scanner",
        description="Terminal-styled IP geolocation lookup tool.",
    )
    parser.add_argument(
        "ips",
        nargs="*",
        help="one or more IP addresses to look up (omit to look up your own IP, "
        "or omit entirely to enter interactive mode)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print raw JSON instead of the styled panel (script-friendly)",
    )
    parser.add_argument(
        "--no-animation",
        action="store_true",
        help="skip the fake scan-line animation delay",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"request timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="save all results as JSON to FILE",
    )
    return parser


def run_targets(
    targets: list[str],
    *,
    as_json: bool = False,
    animate: bool = True,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    output_path: str | None = None,
) -> list[dict]:
    """Look up and render a batch of IPs (empty string == caller's own IP).
    Returns the list of successfully-fetched result dicts."""
    results = []

    for target in targets:
        label = target if target else "SELF"
        if not as_json:
            display.rule(label)
            display.fake_scan_lines(label, animate=animate)

        cached = cache.get(target)
        if cached is not None:
            data = cached
        else:
            try:
                data = lookup_ip(target, timeout=timeout)
                cache.set(target, data)
            except ScannerError as e:
                display.print_error(e)
                continue

        if as_json:
            display.print_json(data)
        else:
            display.render_result(data)

        results.append(data)

    if output_path and results:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        display.print_saved(output_path)

    return results


def interactive_menu(*, timeout: float = DEFAULT_TIMEOUT_SECONDS):
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
        run_targets(targets, timeout=timeout)


def main(argv: list[str] | None = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # IPs passed as CLI args -> run once and exit (scriptable mode).
    # No args at all -> interactive menu (easy mode).
    if args.ips:
        if not args.json:
            display.print_banner()
        run_targets(
            args.ips,
            as_json=args.json,
            animate=not args.no_animation,
            timeout=args.timeout,
            output_path=args.output,
        )
    else:
        interactive_menu(timeout=args.timeout)


def entrypoint():
    try:
        main()
    except KeyboardInterrupt:
        display.print_aborted()
        sys.exit(130)


if __name__ == "__main__":
    entrypoint()
