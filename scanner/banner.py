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

# Neon Green palette for the menu/prompts, with the banner itself in
# alert red (classic hacker/security-tool look: red title art, green
# menu below). bright_red is a basic 16-color ANSI code, so it renders
# consistently on virtually every Linux terminal (Kali, GNOME Terminal,
# Konsole, plain xterm included) -- unlike a 256-color name such as
# orange3, which some basic terminals/SSH sessions render inconsistently
# or fall back on. A few extra accents are mixed into the result panel
# only, so it reads as sectioned data rather than one flat color block.
# Named semantically (not by literal color) so the palette can be
# swapped again later without renaming every call site.
PRIMARY = "bold bright_green"
DIM = "green"
ACCENT = "bold bright_green"
RED = "bold red"
BANNER_COLOR = "bold bright_red"

# Result-panel-only accents (location vs network sections, value vs label).
INFO = "bold bright_cyan"       # location section header + values
WARN = "bold bright_yellow"     # network section header + values
MAGENTA = "bold bright_magenta"  # spare accent, currently unused
LABEL = "bright_black"          # dim field labels, left column

TITLE = "ScannerIP"
MENU_PROMPT_LABEL = "Select an option"

# Full block-letter banner: "ScannerIP" as one word. Widest line is 71
# columns, so this should only be shown when the terminal is comfortably
# wider than that and supports Unicode (see banner_for below), otherwise
# most terminals will wrap it and the box-drawing characters will look
# broken.
BANNER_FULL = r"""
███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ██╗██████╗ 
██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗██║██╔══██╗
███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝██║██████╔╝
╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗██║██╔═══╝ 
███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║██║██║     
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     
"""
BANNER_FULL_WIDTH = 73  # widest line, plus a small safety margin

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
]

# Numbered menu, styled after the bordered "[01] Label" hacker-tool look.
# Each entry is (number, label, color); every bracketed number uses the
# same bright-yellow accent (bracket characters included), matching the
# "[::] ... [::]" header above it, for one consistent, legible color
# instead of a different color per option. Labels say "an IP" / "multiple
# IPs" rather than "a specific IP" -- the lookup only ever returns an
# approximate city/ISP-level area, never an exact or precise location,
# and "specific" risks setting the wrong expectation.
MENU_OPTIONS = [
    ("01", "Look up an IP address", WARN),
    ("02", "Look up multiple IP addresses", WARN),
    ("03", "Check history", WARN),
    ("00", "Exit", WARN),
]


def _boxed_banner(width: int, use_unicode: bool) -> str:
    """
    Build a centered, bordered banner at the given width. Generated
    programmatically (not hand-typed) so it is always correctly aligned
    regardless of width, nothing to accidentally break.
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
