"""
ASCII banner and color constants for terminal-ip-scanner.

The banner adapts to the terminal it's running in:
  - wide terminals get the full thin-outline ASCII art (plain ASCII only,
    so it renders identically everywhere, no Unicode box-drawing needed)
  - narrower terminals (e.g. a default 80-column Kali/tmux session) get a
    smaller boxed banner that is guaranteed to fit and stay aligned
  - terminals/locales that can't render Unicode box-drawing characters
    (rare, but happens over some SSH sessions with a non-UTF-8 LANG) get
    a plain ASCII fallback for that smaller box too

This avoids the classic "banner looks broken after git clone on a fresh
machine" problem, which is almost always a terminal-width or encoding
mismatch rather than a bug in the art itself.
"""

# Neon Green palette for the menu/prompts, with the banner itself in
# amber/orange (matching the classic terminal security-tool look where
# the title art is orange and everything below it is green). A few extra
# accents are mixed into the result panel only, so it reads as sectioned
# data rather than one flat color block, red reserved for errors only.
# Named semantically (not by literal color) so the palette can be swapped
# again later without renaming every call site.
PRIMARY = "bold bright_green"
DIM = "green"
ACCENT = "bold bright_green"
RED = "bold red"
BANNER_COLOR = "bold orange3"

# Result-panel-only accents (location vs network sections, value vs label).
INFO = "bold bright_cyan"       # location section header + values
WARN = "bold bright_yellow"     # network section header + values
MAGENTA = "bold bright_magenta"  # extra accent, used for one menu item
LABEL = "bright_black"          # dim field labels, left column

TITLE = "ScannerIP"

# Full banner: "ScannerIP" as one word, in a thin outline style (classic
# terminal security-tool look). Built entirely from plain ASCII (",",
# "-", ".", "|", "'", backtick), so, unlike a Unicode block-letter font,
# it renders identically on every terminal and encoding, no fallback
# needed for it. Widest line is 41 columns, comfortably inside even an
# 80-column default terminal, so this is shown far more often than the
# old wide block art.
BANNER_FULL = r"""
,---.                              |,---.
`---.,---.,---.,---.,---.,---.,---.||---'
    ||    ,---||   ||   ||---'|    ||    
`---'`---'`---^`   '`   '`---'`    ``    
"""
BANNER_FULL_WIDTH = 43  # widest line, plus a small safety margin

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
# Each entry is (number, label, color) so every bracketed number gets its
# own accent instead of one flat color block, "00" (exit) is red by
# convention to read as the "stop" action.
MENU_OPTIONS = [
    ("01", "Look up my own IP", PRIMARY),
    ("02", "Look up a specific IP", INFO),
    ("03", "Look up several IPs at once", WARN),
    ("04", "Save last result to JSON file", MAGENTA),
    ("00", "Exit", RED),
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
    Pick the right banner variant for the given terminal width (columns).
    BANNER_FULL is plain ASCII, so it only depends on width, not Unicode
    support; the compact boxed fallback (for narrower terminals) still
    respects use_unicode so its border characters never break either.
    """
    if width >= BANNER_FULL_WIDTH:
        return BANNER_FULL
    return _boxed_banner(min(width, 70), use_unicode=use_unicode)
