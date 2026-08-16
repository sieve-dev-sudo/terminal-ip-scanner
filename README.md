<div align="center">

# Demo : Terminal IP Scanner

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI-4B8BBE?style=for-the-badge&logo=windowsterminal&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-API-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

</div>

---

## ✨ Features

- IP Geolocation Lookup តាមរយៈ ipwho.is API (ឥតគិតថ្លៃ, គ្មាន API key)
- Interactive menu mode : វាយ IP ចូលផ្ទាល់ដោយមិនចាំបាច់ចាំ command
- Scriptable mode : ដាក់ IP ជា argument លើ command-line
- Hacker-style terminal UI (ASCII banner, ពណ៌បៃតង, fake scan animation)
- ស្វែងរកបានច្រើន IP ក្នុងលើកតែមួយ
- `--json` flag : output JSON សម្រាប់ភ្ជាប់ជាមួយ script ផ្សេង
- `--output FILE` : save លទ្ធផលទៅ JSON file
- `--no-animation` : skip fake scan delay
- IP validation + error handling (invalid IP, timeout, no internet)
- In-memory cache : មិន query API ដដែលៗសម្រាប់ IP ដូចគ្នា
- Unit tests ពេញលេញ (pytest, mock API)

---

## 📁 Project Structure

```
terminal-ip-scanner/
├── scanner/
│   ├── __init__.py
│   ├── banner.py          → ASCII art, ពណ៌, text constants
│   ├── errors.py          → custom exceptions
│   ├── cache.py           → in-memory lookup cache
│   ├── lookup.py          → API calls (ipwho.is) : data ត្រឹមតែប៉ុណ្ណោះ
│   ├── display.py         → terminal rendering ទាំងអស់ (Rich)
│   └── cli.py             → arg parsing + interactive menu
├── tests/
│   ├── test_lookup.py
│   ├── test_cache.py
│   └── test_cli.py
├── main.py                → entry point
├── pyproject.toml         → packaging (pip install .)
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

---

## 🚀 How to Run

1. Clone ឬ download repository នេះ
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run interactive mode:
   ```bash
   python main.py
   ```
   រួចវាយ IP ចូល (ឧ. `8.8.8.8`) ឬចុច Enter ទទេដើម្បីមើល IP ខ្លួនឯង
4. ឬ run scriptable mode ដោយផ្ទាល់:
   ```bash
   python main.py 8.8.8.8
   python main.py 8.8.8.8 1.1.1.1 --json
   python main.py 8.8.8.8 --output results.json
   ```

### Development

```bash
pip install -r requirements-dev.txt
pytest -v
```

---

## License

MIT : see [LICENSE](LICENSE).
