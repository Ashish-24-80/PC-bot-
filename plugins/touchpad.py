import subprocess
import os
import shutil
from telegram import Update
from telegram.ext import ContextTypes

RUSTDESK_CANDIDATE_PATHS = [
    r"C:\Users\SUBU\Downloads\rustdesk-1.5.0-x86_64.exe",
    r"C:\Program Files\RustDesk\rustdesk.exe",
    r"C:\Program Files (x86)\RustDesk\rustdesk.exe",
    os.path.expanduser(r"~\AppData\Local\RustDesk\rustdesk.exe"),
]


def find_rustdesk_path():
    """Finds the RustDesk executable path."""
    for path in RUSTDESK_CANDIDATE_PATHS:
        if os.path.exists(path):
            return path
    which_path = shutil.which("rustdesk") or shutil.which("rustdesk.exe")
    if which_path and os.path.exists(which_path):
        return which_path
    return None


async def handle_start_rustdesk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Launch RustDesk for remote desktop control."""
    try:
        rustdesk_path = find_rustdesk_path()
        if not rustdesk_path:
            await update.message.reply_text(
                "❌ *RustDesk executable not found.*\n\n"
                f"Checked default location:\n`{RUSTDESK_CANDIDATE_PATHS[0]}`",
                parse_mode="Markdown"
            )
            return

        # Start RustDesk asynchronously in the background
        subprocess.Popen([rustdesk_path], shell=False)

        from keyboard import build_keyboard
        await update.message.reply_text(
            "🖥️ *RustDesk Remote Desktop Launched!*\n\n"
            "✅ RustDesk is now running on your PC.\n"
            "• Connect using your mobile or remote RustDesk app.\n"
            "• Use button *Stop RustDesk* or `/stop_rustdesk` to close it.",
            parse_mode="Markdown",
            reply_markup=build_keyboard()
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to launch RustDesk: {str(e)}")


async def handle_stop_rustdesk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Terminates running RustDesk processes."""
    try:
        from keyboard import build_keyboard
        res = subprocess.run(
            ["taskkill", "/F", "/IM", "rustdesk.exe", "/T"],
            capture_output=True,
            text=True
        )
        if "SUCCESS" in res.stdout or res.returncode == 0:
            await update.message.reply_text(
                "🛑 *RustDesk stopped successfully.*",
                parse_mode="Markdown",
                reply_markup=build_keyboard()
            )
        else:
            await update.message.reply_text(
                "ℹ️ *No active RustDesk process found.*",
                parse_mode="Markdown",
                reply_markup=build_keyboard()
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Error stopping RustDesk: {str(e)}")


PLUGINS = [
    {
        "name": "RustDesk",
        "command": "rustdesk",
        "description": "Launch RustDesk for remote desktop control",
        "handler": handle_start_rustdesk,
        "row": 4,
    },
    {
        "name": "Stop RustDesk",
        "command": "stop_rustdesk",
        "description": "Stop RustDesk remote desktop process",
        "handler": handle_stop_rustdesk,
        "row": 4,
    },
    # Backward compatibility aliases for old buttons cached on Telegram client
    {
        "name": "Touchpad",
        "handler": handle_start_rustdesk,
        "row": 99,
    },
    {
        "name": "No Touch",
        "handler": handle_stop_rustdesk,
        "row": 99,
    },
]
