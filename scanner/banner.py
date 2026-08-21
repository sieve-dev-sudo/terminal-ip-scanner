"""
ASCII banner and color constants for terminal-ip-scanner.

The banner adapts to the terminal it's running in:
  - wide, UTF-8 terminals get the full block-letter ASCII art
  - narrower terminals (e.g. a default 80-column Kali/tmux session) get a
    smaller boxed banner that is guaranteed to fit and stay aligned
  - terminals/locales that can't render Unicode box-drawing characters
    (rare, but happens over some SSH sessions with a non-UTF-8 LANG) get
    a plain ASCII fallback with no special characters at all

This avoids the classic "banner looks broken after git clone on a fresh
machine" problem, which is almost always a terminal-width or encoding
mismatch rather than a bug in the art itself.
"""

GREEN = "bold green"
DIM_GREEN = "green"
RED = "bold red"

TITLE = "TERMINAL-IP-SCANNER"
TAGLINE = "network geolocation utility // ctrl+c to quit"
CREDIT = "developed by Mr. Siev E"

# Full block-letter banner. Widest line is 79 columns, so this should only
# be shown when the terminal is comfortably wider than that (see
# banner_for below) — otherwise most terminals will wrap it and the
# box-drawing characters will look broken. Uses a full-height "║" bar
# between TERMINAL and IP (instead of a small mid-height hyphen) so the
# separator is unambiguous at a glance.
BANNER_FULL = r"""
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗      ║ ██╗██████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║      ║ ██║██╔══██╗
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║      ║ ██║██████╔╝
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║      ║ ██║██╔═══╝
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗ ║ ██║██║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ║ ╚═╝╚═╝
                                 S C A N N E R
"""
BANNER_FULL_WIDTH = 80  # widest line, plus a small safety margin

SCAN_STEPS = [
    "initializing trace on {target}...",
    "resolving nameservers...",
    "pinging edge nodes...",
    "triangulating geo-coordinates...",
    "querying registry (RIR) records...",
    "cross-referencing ASN database...",
]

HELP_LINES = [
    ("<enter>", "look up your own public IP"),
    ("<ip>", "look up one IP  (e.g. 8.8.8.8)"),
    ("<ip1> <ip2> ...", "look up several at once"),
    ("q", "quit"),
]


def _boxed_banner(width: int, use_unicode: bool) -> str:
    """
    Build a centered, bordered banner at the given width. Generated
    programmatically (not hand-typed) so it is always correctly aligned
    regardless of width — nothing to accidentally break.
    """
    inner_width = max(width - 2, len(TITLE) + 2)

    if use_unicode:
        tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"
    else:
        tl, tr, bl, br, h, v = "+", "+", "+", "+", "-", "|"

    top = f"{tl}{h * inner_width}{tr}"
    bottom = f"{bl}{h * inner_width}{br}"
    title_line = f"{v}{TITLE.center(inner_width)}{v}"

    return "\n".join([top, title_line, bottom])


def banner_for(width: int, use_unicode: bool = True) -> str:
    """
    Pick the right banner variant for the given terminal width (columns)
    and Unicode support. Falls back gracefully rather than ever printing
    something wider than the terminal or something the terminal can't
    render.
    """
    if use_unicode and width >= BANNER_FULL_WIDTH:
        return BANNER_FULL
    return _boxed_banner(min(width, 70), use_unicode=use_unicode)
