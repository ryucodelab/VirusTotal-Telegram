<div align="center">

# 🛡️ VirusTotal Telegram Bot

**An automatic Telegram security bot that scans files and URLs in real-time using VirusTotal.**

Drop a file or paste a link — VTBot scans it instantly and reports back with a clean, multi-language security verdict.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-21.10-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://python-telegram-bot.org/)
[![VirusTotal](https://img.shields.io/badge/Powered%20by-VirusTotal-394EFF?style=for-the-badge&logo=virustotal&logoColor=white)](https://www.virustotal.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#-license)
[![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen?style=for-the-badge)](https://github.com/ryucodelab)

</div>

---

## ✨ Overview

**VTBot** is a lightweight Telegram bot that automatically detects when a user sends a **file** or **URL**, submits it to the [VirusTotal](https://www.virustotal.com/) engine, and returns a formatted security report — no commands needed, it just works passively in the background.

## 🚀 Features

- 📁 **Auto File Scanning** — Detects any document sent to the bot and scans it via VirusTotal
- 🔗 **Auto URL Scanning** — Detects links in messages/captions and scans them automatically
- 🌍 **Multi-language Support** — Built-in locales for `English`, `Bahasa Indonesia`, `Português`, and `العربية`
- ⚡ **Real-time Status Updates** — Live "scanning..." feedback while the report is being generated
- 🧹 **Auto Cleanup** — Temporary downloaded files are wiped after each scan
- 🚧 **File Size Guard** — Configurable max file size to prevent abuse
- 🧩 **Modular Architecture** — Clean separation between detection, downloading, scanning, formatting, and cleanup

## 🗂️ Project Structure

```
vtbot/
├── main.py                 # Entry point & message handler
├── config.py                # Environment-based configuration
├── requirements.txt
├── .env                      # Your secrets (not committed)
├── locales/                  # Language files
│   ├── en.json
│   ├── id.json
│   ├── pt.json
│   └── ar.json
└── modules/
    ├── start.py               # /start & /language commands
    ├── detector.py             # File / URL detection logic
    ├── downloader.py            # Telegram file downloader
    ├── virustotal.py             # VirusTotal file scan integration
    ├── url_scanner.py             # VirusTotal URL scan integration
    ├── formatter.py                # Report formatting (HTML output)
    ├── language.py                  # i18n loader
    └── cleaner.py                    # Temp file cleanup
```

## 🧰 Tech Stack

| Component | Library |
|---|---|
| Telegram Bot Framework | [`python-telegram-bot`](https://python-telegram-bot.org/) `21.10` |
| Malware/URL Scanning | [VirusTotal API v3](https://docs.virustotal.com/reference/overview) |
| Async HTTP Client | `aiohttp` |
| Env Management | `python-dotenv` |

## ⚙️ Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/ryucodelab/VirusTotal-Telegram
cd VirusTotal-Telegram
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` (or edit `.env`) and fill in your own credentials:

```env
BOT_TOKEN=your_telegram_bot_token
VIRUSTOTAL_API_KEY=your_virustotal_api_key
TEMP_DIR=temp
DEFAULT_LANGUAGE=en
SCAN_TIMEOUT=180
MAX_FILE_SIZE=52428800
```

| Variable | Description | Default |
|---|---|---|
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) | — |
| `VIRUSTOTAL_API_KEY` | API key from [VirusTotal](https://www.virustotal.com/gui/join-us) | — |
| `TEMP_DIR` | Local folder for temporary downloads | `temp` |
| `DEFAULT_LANGUAGE` | Fallback language code | `en` |
| `SCAN_TIMEOUT` | Max seconds to wait for a scan result | `180` |
| `MAX_FILE_SIZE` | Max file size in bytes | `52428800` (50MB) |

> ⚠️ Never commit your real `.env` file — keep your `BOT_TOKEN` and `VIRUSTOTAL_API_KEY` private.

### 5. Run the bot

```bash
python main.py
```

If everything is set up correctly, you'll see:

```
INFO | Bot started
```

## 💬 Usage

| Action | Command |
|---|---|
| Start the bot | `/start` |
| Change language | `/language` |
| Scan a file | Just send/forward a file to the bot |
| Scan a URL | Send a message containing a link |

## 🌐 Supported Languages

🇬🇧 English &nbsp;•&nbsp; 🇮🇩 Bahasa Indonesia &nbsp;•&nbsp; 🇵🇹 Português &nbsp;•&nbsp; 🇸🇦 العربية

Want to add your own language? Just drop a new `<code>.json</code>` file in `/locales` following the existing key structure.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/ryucodelab/vtbot/issues) or open a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

## 🙏 Credits

Built and maintained with ❤️ by **[ryucodelab](https://github.com/ryucodelab)**

Powered by:
- [VirusTotal](https://www.virustotal.com/) — malware & URL analysis engine
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — Telegram Bot API wrapper

---

<div align="center">

If you find this project useful, consider giving it a ⭐ on GitHub!

</div>
