# Wexxy PC Bot 🤖🖥️

**Wexxy PC Bot** is a lightweight, production-ready remote control orchestrator for Windows, operated entirely through Telegram and zero-config Cloudflare tunnels (`cloudflared`).

Designed as both a standalone personal remote desktop companion and a **Manual Heavy-Lifting Support System ("Agentic AI Unblocker")** for autonomous frameworks like Antigravity, ClawX, and OpenClaw.

---

## ⚡ Highlights & Key Features

- 📱 **Low-Latency Absolute Touchpad & Screen Stream**: Real-time MJPEG desktop streaming to any mobile browser with pixel-perfect coordinate mapping.
- ⌨️ **Mouse & Keyboard Emulation**: Move cursor, left/right click, double-click, scroll, type text safely, and dispatch complex hotkeys (`Alt+Tab`, `Ctrl+C`, `Ctrl+V`, etc.).
- 🐚 **Interactive Terminal & Linux-Like Shell**: Run live terminal commands (`/run <cmd>`) or step into an interactive persistent session with `/sh` (`ls`, `cd`, `cat`, `mkdir`, `tree`...).
- 📦 **Windows Package Management**: Manage software headlessly via `/winget` (`install`, `upgrade`, `search`, `list`).
- 👁️ **Screen OCR**: Capture screens and extract text on-the-fly (`/ocr`) using EasyOCR without external Tesseract dependencies.
- 🗂️ **Blazing File Search & Retrieval**: Search hard drives in milliseconds with Everything CLI (`/find`), download files to mobile (`/fetch`), and send files directly from phone to PC.
- 🤖 **Agentic IDE Control**: Bridge with local IDEs via `/control_antigravity <prompt>` to focus windows, paste prompts, and trigger workflows.
- 🔒 **Zero-Config Tunnels**: Tunnel Flask endpoints securely to mobile using Cloudflare with no open firewall ports.
- 🛡️ **Zero-Trust Security**: Strict single-user authorization (`ADMIN_ID` middleware) dropping unauthorized updates, plus token isolation via `.env`.

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   TELEGRAM MESSENGER                   │
└───────────────────────────┬────────────────────────────┘
                            │ (Async Bot Updates / Long Poll)
                            ▼
┌────────────────────────────────────────────────────────┐
│                     WEXXY BOT CORE                     │
│  - bot.py (Single Instance Process Lock & Dispatcher)  │
│  - middleware.py (Admin ID Verification Filter)        │
│  - plugins/ (Modular Hot-Loaded Handlers)              │
└───────┬─────────────────────────────┬───────────┬──────┘
        │                             │           │
        ▼                             ▼           ▼
┌──────────────────┐          ┌─────────────┐ ┌────────────────┐
│   LOCAL FLASK    │          │  AI ROUTER  │ │  WINDOWS OS    │
│  (Port: 58392)   │          │ (plugins/   │ │ (Subprocesses) │
│                  │          │  routing)   │ │                │
│ - trackpad.html  │          │             │ │ - Everything   │
│ - MJPEG Stream   │◄─────────┤ - Gemma4    │ │ - PyAutoGUI    │
│ - Cloudflare     │          │ - Whisper   │ │ - pycaw / mss  │
│   Tunnel         │          │ - Qwen      │ │ - Winget CLI   │
└──────────────────┘          └─────────────┘ └────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Windows 10/11
- Python 3.10+ (Miniconda / Python 3.13 recommended)
- [Cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (for remote streaming/touchpad)
- Everything CLI (`es.exe` in `utils/` for instant file search)

### 2. Setup Environment & Credentials
1. Clone the repository:
   ```powershell
   git clone <REPO_URL>
   cd Wexxy-pc-bot
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials:
   ```powershell
   copy .env.example .env
   ```
   Edit `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_ADMIN_ID=your_telegram_numeric_user_id
   CLOUDFLARED_PATH=C:\path\to\cloudflared.exe
   FLASK_PORT=58392
   STREAM_FPS=10
   STREAM_QUALITY=85
   ```

### 3. Run the Bot
- **Interactive Terminal**:
  ```powershell
  python bot.py
  ```
- **Windows Batch Launcher** (auto-restart loop):
  ```cmd
  StartWexxyBot.bat
  ```
- **Background Startup**:
  Run `setup_startup.ps1` or `add_to_startup_folder.ps1` to launch Wexxy automatically whenever you log in to Windows.

---

## 📋 Command Catalog

| Command | Plugin | Description |
| :--- | :--- | :--- |
| `/start` | Core | Display bot status and launch persistent quick-action keyboard |
| `/help` | `help.py` | Display full command directory and usage instructions |
| `/rustdesk` | `touchpad.py` | Launch RustDesk remote desktop control (alias: `/touchpad`) |
| `/stop_rustdesk` | `touchpad.py` | Terminate active RustDesk session |
| `/sh <cmd>` | `shell.py` | Run interactive Linux-style shell session (`ls`, `cd`, `cat`, etc.) |
| `/winget <cmd> <app>` | `software.py` | Manage packages via winget (`search`, `install`, `upgrade`, `list`) |
| `/ocr` | `easy_ocr.py` | Capture screen and perform OCR on active monitor |
| `/control_antigravity <prompt>` | `antigravity.py` | Focus IDE, copy prompt, and send to workspace |
| `/apps` | `apps.py` | List installed applications and shortcuts |
| `/launch <app>` | `launcher.py` | Launch any application via Windows Start search |
| `/run <cmd>` | `runner.py` | Execute raw shell commands in CMD or PowerShell |
| `/find <query>` | `files.py` | Fast file search across PC using Everything CLI |
| `/fetch <path>` | `files.py` | Download file from PC directly to Telegram |
| `/ls <dir>` | `files.py` | Directory listing of local folders |
| `/screenshot` | `screenshot.py` | Capture primary screen and send image to Telegram |
| `/pc_status` | `info.py` | Hardware status (CPU, RAM, Disk utilization) |
| `/monitor` | `monitor.py` | Toggle Guardian background resource monitoring & critical alerts |
| `/close` | `close.py` | Send `Alt+F4` to close active window |
| `/web <url>` | `web.py` | Open website in default browser |
| `/web_search <query>` | `web.py` | Search Google in default browser |
| `/web_ai <prompt>` | `web.py` | Open Perplexity AI search in browser |
| `/media_route_reveal` | `routing.py` | Check current routing destination for audio/images |
| `/change_media_route <target>` | `routing.py` | Route media to Gemma4, Whisper, Qwen, or folder |
| `/vol_up` / `/vol_down` / `/mute`| `volume.py` | System volume control |
| `/sleep` / `/lock` / `/logout` | `system.py` | System power states |
| `/restart_bot` | Core | Gracefully reload bot process |

---

## 🧩 Extending with Plugins

Wexxy uses dynamic auto-discovery. Any Python file added to `plugins/` exporting a `PLUGIN` dictionary is automatically registered in the command menu and Telegram persistent keyboard:

```python
# plugins/my_custom_tool.py
from telegram import Update

async def handle_custom(update: Update, context):
    await update.message.reply_text("Custom plugin executed!")

PLUGIN = {
    "name": "My Tool",               # Button label on Telegram keyboard
    "command": "mytool",              # Slash command (/mytool)
    "description": "Tool summary",    # Tooltip in /help
    "handler": handle_custom,         # Async handler coroutine
    "row": 3                          # Keyboard row index
}
```

---

## 🔒 Security Architecture

1. **Token Protection**: Credentials live in `.env` (strictly excluded via `.gitignore`). Never push API tokens or Admin IDs to git.
2. **Admin Authorization**: All incoming Telegram updates are intercepted by `middleware.py`. Any update from a Telegram user ID not matching `ADMIN_ID` is silently dropped.
3. **Single Instance Locking**: `bot.py` creates and holds a lock on `wexxy.bot.lock` to prevent duplicate polling conflicts.

---

## 🤖 For AI Agents

Autonomous agents working in or with this codebase should refer to:
- [`AGENTS.md`](./AGENTS.md): Operational guide, conventions, and safety rules for AI coders.
- [`PROJECT_MANUAL.md`](./PROJECT_MANUAL.md): Deep-dive system documentation and troubleshooting playbooks.
- [`CHANGELOG.md`](./CHANGELOG.md): History of system enhancements and architectural refactors.
- [`removed/`](./removed/): Archive of deprecated drafts, experimental scratch code, and backup files.

