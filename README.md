# terminal-ip-scanner

A terminal-styled IP geolocation lookup tool. Green-on-black, ASCII banner,
fake "scan" animation — real data underneath.

```
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗          ██╗██████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║          ██║██╔══██╗
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║          ██║██████╔╝
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ██   ██║██╔═══╝
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗╚█████╔╝██║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝
                            S C A N N E R
```

## Install

```bash
git clone https://github.com/<your-username>/terminal-ip-scanner.git
cd terminal-ip-scanner
pip install -r requirements.txt
```

## Usage

**Interactive mode** : no flags to remember, just launch and type:

```bash
python main.py
```

```
scanner> 8.8.8.8
scanner> 1.1.1.1 8.8.8.8
scanner> q
```

**Scriptable mode** : pass IPs directly as arguments:

```bash
python main.py                 # your own public IP
python main.py 8.8.8.8         # a specific IP
python main.py 1.1.1.1 8.8.8.8 # multiple IPs in one run
```

## Project structure

```
terminal-ip-scanner/
├── main.py              # entry point
├── requirements.txt
└── scanner/
    ├── __init__.py
    ├── banner.py         # ASCII art, colors, copy/text constants
    ├── lookup.py         # API calls (ipwho.is) — data only, no printing
    ├── display.py         # all Rich terminal rendering
    └── cli.py            # orchestration: arg parsing + interactive menu
```

