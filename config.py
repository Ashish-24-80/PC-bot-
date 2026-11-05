import os
from pathlib import Path

# Load .env file automatically without third-party dependencies
_env_path = Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
    except Exception as _e:
        print(f"Warning: Failed to parse .env file: {_e}")

# Telegram Bot Credentials
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("TELEGRAM_ADMIN_ID", "0"))

# Remote Touchpad & Streaming Settings
CLOUDFLARED_PATH = os.getenv("CLOUDFLARED_PATH", r"C:\Users\SUBU\Downloads\Programs\cloudflared.exe")
FLASK_PORT = int(os.getenv("FLASK_PORT", "58392"))
STREAM_FPS = int(os.getenv("STREAM_FPS", "10"))
STREAM_QUALITY = int(os.getenv("STREAM_QUALITY", "85"))  # JPEG quality (1-95)
