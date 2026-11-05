import subprocess
import os

async def handle_shutdown(update, context):
    await update.message.reply_text("Shutting down...")
    subprocess.run(["shutdown", "/s", "/t", "5"])

async def handle_restart(update, context):
    await update.message.reply_text("Restarting...")
    subprocess.run(["shutdown", "/r", "/t", "5"])

async def handle_sleep(update, context):
    await update.message.reply_text("Sleeping...")
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])

async def handle_lock(update, context):
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    await update.message.reply_text("Locked.")

async def handle_logout(update, context):
    await update.message.reply_text("Logging out...")
    subprocess.run(["shutdown", "/l"])

PLUGINS = [
    {"name": "Sleep",    "command": "sleep",    "description": "Sleep PC",    "handler": handle_sleep,    "row": 99},
    {"name": "Lock",     "command": "lock",     "description": "Lock screen", "handler": handle_lock,     "row": 99},
    {"name": "Logout",   "command": "logout",   "description": "Log out",     "handler": handle_logout,   "row": 99},
]
