<div align="center">

# Terminal-Ip-Scanner : Hacker-Style Tool

</div>

## 🛠️ Tech Stack

**ភាសាសរសេរកូដ និង ឧបករណ៍**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-4B8BBE?style=flat&logo=windowsterminal&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP-green?style=flat)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)

---

## ✨ Features

- **IP Geolocation Lookup**: ប្រើ ipwho.is API (ឥតគិតថ្លៃ, គ្មាន API key) ស្វែងរកទីតាំង**ប្រហាក់ប្រហែល** តាមកម្រិត city/ISP (មិនមែនទីតាំងជាក់លាក់ GPS ទេ)
- **Interactive Numbered Menu**: ម៉ឺនុយបែបលេខ `[01]` `[02]` `[03]` `[00]` ជ្រើសរើសមុខងារជាមុន បន្ទាប់មកទើបបញ្ចូល IP
- **Scriptable Mode**: ដាក់ IP ជា argument លើ command-line ដោយផ្ទាល់ សម្រាប់ភ្ជាប់ជាមួយ script ផ្សេង
- **Multiple IP Lookup**: ស្វែងរកបានច្រើន IP ក្នុងលើកតែមួយ
- **Session History**: កត់ត្រារាល់ IP ដែលបាន lookup ក្នុងវគ្គនោះ ហើយអាចឆែកមើលឡើងវិញបាន
- **Hacker-Style Terminal UI**: ASCII banner (thin outline style, ពណ៌ក្រហម), ម៉ឺនុយពណ៌ Neon Green/Yellow, fake scan animation
- **Sectioned Result Panel**: លទ្ធផលបែងចែកជា LOCATION (cyan) និង NETWORK (yellow) ដាច់ដោយឡែក
- **JSON Export**: `--json` flag សម្រាប់ output script-friendly, `--output FILE` សម្រាប់ save ទៅ JSON file
- **Error Handling**: IP validation, timeout, no-internet ទាំងអស់មាន error message ច្បាស់លាស់
- **In-Memory Cache**: មិន query API ដដែលៗសម្រាប់ IP ដូចគ្នាក្នុងវគ្គតែមួយ
- **Terminal-Adaptive Banner**: Detect terminal width/encoding ដោយស្វ័យប្រវត្តិ មិនខូច/wrap ខុសទាល់តែសោះ (សាកល្បងលើ Kali)
- **Unit Tests ពេញលេញ**: ប្រើ pytest + pytest-mock, mock API calls ទាំងអស់ (គ្មានហៅ network ពិតពេល test)

---

## 🖥️ Terminal Compatibility (Kali-tested)

Banner detect terminal width និង encoding ដោយស្វ័យប្រវត្តិ ដើម្បីកុំឲ្យខូចពេល clone លើម៉ាស៊ីនថ្មី :

| លក្ខខណ្ឌ terminal | អ្វីដែលបង្ហាញ |
|---|---|
| ធំ (≥73 columns) + UTF-8 | Full block-letter ASCII art "ScannerIP" |
| ធម្មតា (Kali default 80 columns) + UTF-8 | Full ASCII art (សមដោយស្វ័យប្រវត្តិ) |
| តូចជាង 73 columns ឬ Non-UTF-8 locale | Boxed banner តូច / ASCII box ធម្មតា (`+`, `-`, `|`) |

មិនចាំបាច់ setup អ្វីទេ : វា detect ដោយស្វ័យប្រវត្តិរាល់ដង run។

---

## 📋 Menu Options

| លេខ | ពណ៌ bracket | មុខងារ |
|---|---|---|
| `01` | លឿង | Look up an IP address |
| `02` | លឿង | Look up multiple IP addresses |
| `03` | លឿង | Check history (IP ទាំងអស់ដែលបាន lookup ក្នុងវគ្គនេះ) |
| `00` | លឿង | Exit |

អាចវាយ `0`, `00`, `000` ។ល។ ឲ្យ Exit បានដូចគ្នា (normalize ដោយស្វ័យប្រវត្តិ)។

---

## 📁 Project Structure

```
terminal-ip-scanner/
├── scanner/
│   ├── __init__.py
│   ├── banner.py         → ASCII art, ពណ៌, menu options, text constants
│   ├── errors.py         → custom exceptions
│   ├── cache.py          → in-memory lookup cache
│   ├── lookup.py         → API calls (ipwho.is) : data ត្រឹមតែប៉ុណ្ណោះ
│   ├── display.py        → terminal rendering ទាំងអស់ (Rich)
│   └── cli.py            → arg parsing + interactive menu
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

1. Clone Repository :

   ```bash
   git clone <url-repo> terminal-ip-scanner
   cd terminal-ip-scanner
   ```

2. Install Dependencies :

   ```bash
   pip install -r requirements.txt
   ```

3. Run Interactive Mode :

   ```bash
   python main.py
   ```

   ម៉ឺនុយបែបលេខនឹងបង្ហាញឡើង ជ្រើសរើសលេខ (`01`-`03`, `00` ដើម្បីចេញ) រួចបញ្ចូលព័ត៌មានតាមសំណើ (ឧ. IP address)

4. ឬ Run Scriptable Mode ដោយផ្ទាល់ :

   ```bash
   python main.py 8.8.8.8
   python main.py 8.8.8.8 1.1.1.1 --json
   python main.py 8.8.8.8 --output results.json
   ```

5. ដើម្បី Run Tests :

   ```bash
   pip install -r requirements-dev.txt
   pytest -v
   ```

---

## 📄 License

**Modified MIT License :** អ្នកអាចប្រើ ចម្លង កែប្រែ និងចែកចាយកូដនេះដោយសេរីសម្រាប់គោលបំណងអប់រំ ស្រាវជ្រាវ និងការធ្វើតេស្តដែលមានការអនុញ្ញាតត្រឹមត្រូវ ឲ្យតែរក្សាទុកសេចក្តីជូនដំណឹង Copyright។ ហាមយកទៅប្រើលើផ្លូវខុសច្បាប់ ឬព្យាបាទ។ មើលព័ត៌មានលម្អិតក្នុងឯកសារ [LICENSE](LICENSE)។

---

## 👤 Author

**Built with ❤️ and code by Mr. Siev E**
