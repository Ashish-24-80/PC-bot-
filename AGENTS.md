# AGENTS.md — Developer & Autonomous Agent Briefing

> **Target Audience:** Autonomous AI coding agents (Antigravity, ClawX, OpenClaw, Copilot) and human developers extending or maintaining **Wexxy PC Bot**.

---

## 🎯 1. System Mission & Operational Context

Wexxy PC Bot is an omnipresent, asynchronous Windows remote-control system. It serves two distinct roles:
1. **Human Remote Management:** Telegram-operated mobile touchpad, screen streamer, terminal shell, and file transfer tool.
2. **"Agentic AI Unblocker":** Acts as an out-of-band actuator when autonomous local agents get blocked on legacy GUIs, CAPTCHAs, or OS dialogs, enabling human-in-the-loop fallback.

---

## 📂 2. Repository Layout & File Responsibilities

```text
Wexxy-pc-bot/
├── bot.py                  # Core entry point: process lock, dispatcher, polling
├── config.py               # Loads configuration from .env and environment variables
├── middleware.py           # Admin authentication filter (drops unauthorized requests)
├── keyboard.py             # Constructs Telegram ReplyKeyboardMarkup from plugins
├── requirements.txt        # Production Python dependencies
├── .env.example            # Committed configuration template (dummy values)
├── .env                    # [GITIGNORED] Real production tokens and credentials
├── .gitignore              # Protects secrets, logs, locks, and vendorized libs
│
├── plugins/                # Modular plugin ecosystem (auto-discovered on startup)
│   ├── antigravity.py      # IDE integration bridge (/control_antigravity)
│   ├── apps.py             # Start menu shortcut indexer (/apps)
│   ├── close.py            # Active window closer (/close)
│   ├── easy_ocr.py         # Screen capture + EasyOCR (/ocr)
│   ├── files.py            # Fast file search & transfer (/find, /fetch, /ls)
│   ├── help.py             # Command catalog generator (/help)
│   ├── info.py             # System hardware metrics (/info)
│   ├── launcher.py         # Start menu application launcher (/launch)
│   ├── monitor.py          # Display power state controller (/monitor_off)
│   ├── routing.py          # Media destination manager (/change_media_route)
│   ├── runner.py           # Raw command executor (/run)
│   ├── screenshot.py       # Desktop screenshot transmitter (/screenshot)
│   ├── shell.py            # Persistent interactive Linux-like shell (/sh)
│   ├── software.py         # Windows Package Manager integration (/winget)
│   ├── system.py           # Windows power management (/lock, /restart, etc.)
│   ├── touchpad.py         # Flask MJPEG streaming server + cloudflared tunnel
│   ├── volume.py           # Master audio volume controller via pycaw
│   ├── web.py              # Browser launcher and web searches
│   └── __init__.py         # Dynamic plugin loader (load_plugins())
│
├── static/
│   └── trackpad.html       # Single-page mobile trackpad + MJPEG live stream UI
│
├── utils/
│   ├── es.exe              # Everything Search CLI binary for instant drive searches
│   ├── runner.py           # Subprocess runner utility with PowerShell support
│   └── __init__.py
│
├── nebula_dashboard/       # Glassmorphic web metrics dashboard
│   ├── app.py              # Flask server on port 5005
│   └── index.html          # Front-end UI with Chart.js
│
├── service/
│   └── install.py          # NSSM Windows service installer/uninstaller
│
├── removed/                # ARCHIVE: Obsolete drafts, backup files, and scratch
│   ├── backup_files/       # Pre-refactor .bak files
│   ├── disabled_plugins/   # Inactive/deprecated plugins (.disabled)
│   ├── legacy_docs/        # Early drafts synthesized into PROJECT_MANUAL.md
│   ├── one_off_scripts/    # Ad-hoc test scripts
│   ├── scratch/            # Old scratch and test suites
│   ├── swarm_system/       # SwarmSystem research files
│   └── README.md           # Catalog of removed files
│
├── README.md               # Main repository documentation
├── PROJECT_MANUAL.md       # Comprehensive architectural reference manual
├── CHANGELOG.md            # Version and modification history
└── AGENTS.md               # This document
```

---

## ⚙️ 3. Critical Agent Rules & Architectural Invariants

When writing code or modifying files in this repository, **all agents must adhere to the following rules**:

### Rule 1: Never Hardcode or Commit Secrets
- All credentials must be read via `config.py` using `os.getenv()`.
- Real credentials live strictly in `.env`.
- Ensure `.env` is listed in `.gitignore`.
- When adding new configuration keys:
  1. Add them to `.env.example` with dummy values.
  2. Add loading logic with fallbacks in `config.py`.
  3. Update `.env` locally.

### Rule 2: Single-Instance Process Lock
- `bot.py` creates and holds a write lock on `wexxy.bot.lock`.
- **Do not delete or modify `wexxy.bot.lock` while the bot is active.**
- If you need to test `bot.py`, stop existing instances first using Task Manager or PowerShell (`Stop-Process -Name python, pythonw`).

### Rule 3: Plugin Authoring Pattern
- Every new plugin in `plugins/` must export a `PLUGIN` dictionary (or `PLUGINS` list):
  ```python
  PLUGIN = {
      "name": "Display Name",       # Button text on mobile Telegram keyboard
      "command": "cmd_name",        # Lowercase slash command (max 32 chars)
      "description": "Short help",  # Shown in /help catalog
      "handler": async_handler,     # Async coroutine (update, context)
      "row": 4                      # Row on the persistent keyboard (1-5, or 99 for hidden)
  }
  ```
- Use `row = 99` for background or administrative handlers that should not create persistent keyboard buttons.
- All handlers must be decorated with `@admin_only` or wrapped via `admin_only(handler)` to prevent unauthorized execution.

### Rule 4: Non-Blocking Async Execution
- Telegram handlers are asynchronous (`async def`).
- Long-running CLI tasks (such as PowerShell searches or winget commands) **must** run asynchronously using `asyncio.create_subprocess_exec` or `run_in_executor` to avoid blocking polling for other updates.

### Rule 5: Coordinate Mapping on Touchpad
- Do not alter the coordinate transformation mathematics in `static/trackpad.html` (`getAbsoluteCoords`) without understanding CSS `object-fit: contain` letterboxing. Changing this breaks the absolute tap alignment on physical Windows monitors.

---

## 🧪 4. Testing & Verification Guide

### Quick Health Check
Run a quick Python environment verification:
```powershell
python -c "import config; print('Config OK, Admin ID:', config.ADMIN_ID)"
```

### Validate Dynamic Plugin Loader
```powershell
python -c "from plugins import load_plugins; plugins = load_plugins(); print(f'Loaded {len(plugins)} plugins successfully.')"
```

### Dry-Run Bot Import
```powershell
python -c "import bot; print('Bot module imports clean.')"
```

---

## 🛠️ 5. Known Gotchas & Troubleshooting

1. **`Conflict: terminated by other getUpdates request`:**
   - Multiple instances of `bot.py` running simultaneously.
   - Run `reset_bot.ps1` or terminate orphaned `python.exe` / `pythonw.exe` tasks.
2. **`Cloudflared tunnel failed to start`:**
   - Stray `cloudflared.exe` holding the tunnel.
   - Run `taskkill /F /IM cloudflared.exe` and retry `/touchpad`.
3. **`libs/` Directory Warning:**
   - `libs/` contains vendorized pip packages including PyTorch and OpenCV.
   - Do **not** commit `libs/` to git; it is ignored via `.gitignore` to prevent repository bloat.

