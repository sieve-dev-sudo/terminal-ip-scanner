#!/usr/bin/env python3
"""
terminal-ip-scanner
Run this file to launch the scanner.

    python main.py                 # interactive menu, looks up your own IP
    python main.py 8.8.8.8         # look up a specific IP
    python main.py 1.1.1.1 8.8.8.8 # look up multiple IPs at once
"""

from scanner.cli import entrypoint

if __name__ == "__main__":
    entrypoint()
