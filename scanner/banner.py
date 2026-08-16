"""
ASCII banner and color constants for terminal-ip-scanner.
"""

GREEN = "bold green"
DIM_GREEN = "green"
RED = "bold red"

BANNER = r"""
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗          ██╗██████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║          ██║██╔══██╗
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║          ██║██████╔╝
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ██   ██║██╔═══╝
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗╚█████╔╝██║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝
                            S C A N N E R
"""

TAGLINE = "network geolocation utility // ctrl+c to quit"

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