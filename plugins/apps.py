import os
import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def handle_apps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List installed applications from common Start Menu locations."""
    msg = await update.message.reply_text("🔎 Scanning for apps...")
    
    # Common Start Menu paths
    paths = [
        os.path.join(os.environ.get("ProgramData", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
        os.path.join(os.environ.get("AppData", ""), "Microsoft", "Windows", "Start Menu", "Programs")
    ]
    
    apps = set()
    for path in paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".lnk"):
                        name = file.replace(".lnk", "")
                        # Filter out common system tools if needed, or just include all
                        if not name.lower().startswith("uninstall"):
                            apps.add(name)
    
    if not apps:
        await msg.edit_text("❌ No apps found in Start Menu.")
        return
    
    # Sort and format
    sorted_apps = sorted(list(apps))
    
    # Chunk into messages if too long
    header = "📂 *Installed Apps:*\n\n"
    current_msg = header
    
    for app in sorted_apps:
        line = f"• `{app}`\n"
        if len(current_msg) + len(line) > 4000:
            await update.message.reply_text(current_msg, parse_mode="Markdown")
            current_msg = header
        current_msg += line
        
    await msg.delete()
    await update.message.reply_text(current_msg, parse_mode="Markdown")

PLUGIN = {
    "name": "Apps",
    "command": "apps",
    "description": "List installed apps",
    "handler": handle_apps,
    "row": 3,
}
