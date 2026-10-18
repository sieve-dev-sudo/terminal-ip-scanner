<div align="center">

# Demo : Terminal IP Scanner

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI-4B8BBE?style=for-the-badge&logo=windowsterminal&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-API-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

**developed by Mr. Siev E**

</div>

---

## ✨ Features

- IP Geolocation Lookup តាមរយៈ ipwho.is API (ឥតគិតថ្លៃ, គ្មាន API key)
- Interactive numbered menu (`[01]` `[02]` ...) : ជ្រើសរើសមុខងារជាមុន បន្ទាប់មកទើបបញ្ចូល IP
- Scriptable mode : ដាក់ IP ជា argument លើ command-line
- Hacker-style terminal UI (ASCII banner, ពណ៌ Neon Green, fake scan animation)
- លេខម៉ឺនុយនីមួយៗមានពណ៌ផ្ទាល់ខ្លួន (green/cyan/yellow/magenta/red)
- លទ្ធផល lookup បែងចែកជា LOCATION (cyan) និង NETWORK (yellow) sections
- ស្វែងរកបានច្រើន IP ក្នុងលើកតែមួយ
- `--json` flag : output JSON សម្រាប់ភ្ជាប់ជាមួយ script ផ្សេង
- `--output FILE` : save លទ្ធផលទៅ JSON file
- `--no-animation` : skip fake scan delay
- IP validation + error handling (invalid IP, timeout, no internet)
- In-memory cache : មិន query API ដដែលៗសម្រាប់ IP ដូចគ្នា
- Unit tests ពេញលេញ (pytest, mock API)
- Banner ស្វ័យប្រវត្តិកែតាមទំហំ terminal : មិនខូច/wrap ខុសនៅលើ Kali ឬ terminal ណាមួយ
- Console width កំណត់កំរិតអតិបរមា : កុំឲ្យ box/divider វែងហួសហេតុនៅលើ terminal ធំ (ឧ. VS Code)

---

## 🖥️ Terminal Compatibility (Kali-tested)

Banner detect terminal width និង encoding ដោយស្វ័យប្រវត្តិ ដើម្បីកុំឲ្យខូចពេល clone លើម៉ាស៊ីនថ្មី :

| លក្ខខណ្ឌ terminal | អ្វីដែលបង្ហាញ |
|---|---|
| ធំ (≥76 columns) + UTF-8 | Full block-letter ASCII art "SCANNER \| IP" |
| ធម្មតា (Kali default 80 columns) + UTF-8 | Boxed banner តូច តម្រូវទំហំពិត |
| Non-UTF-8 locale / SSH minimal | ASCII box ធម្មតា (`+`, `-`, `\|`) គ្មាន Unicode |

មិនចាំបាច់ setup អ្វីទេ : វា detect ដោយស្វ័យប្រវត្តិរាល់ដង run។

---

## 📋 Menu Options

| លេខ | ពណ៌ | មុខងារ |
|---|---|---|
| `01` | បៃតង | Look up my own IP |
| `02` | Cyan | Look up a specific IP |
| `03` | លឿង | Look up several IPs at once |
| `04` | ស្វាយ | Save last result to JSON file |
| `00` | ក្រហម | Exit |

---

## 📁 Project Structure

```
terminal-ip-scanner/
├── scanner/
│   ├── __init__.py
│   ├── banner.py        → ASCII art, ពណ៌, text constants
│   ├── errors.py         → custom exceptions
│   ├── cache.py           → in-memory lookup cache
│   ├── lookup.py          → API calls (ipwho.is) : data ត្រឹមតែប៉ុណ្ណោះ
│   ├── display.py         → terminal rendering ទាំងអស់ (Rich)
│   └── cli.py             → arg parsing + interactive menu
├── tests/
│   ├── test_lookup.py
│   ├── test_cache.py
│   ├── test_cli.py
│   └── test_banner.py
├── main.py               → entry point
├── pyproject.toml        → packaging (pip install .)
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
   ម៉ឺនុយបែបលេខនឹងបង្ហាញឡើង ជ្រើសរើសលេខ (`01`-`04`, `00` ដើម្បីចេញ) រួចបញ្ចូលព័ត៌មានតាមសំណើ (ឧ. IP address)
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

## Author

**Mr. Siev E**

---

## License

MIT : see [LICENSE](LICENSE).
