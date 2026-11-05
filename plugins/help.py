from telegram import Update
from telegram.ext import ContextTypes

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dynamically generate help message from loaded plugins."""
    from plugins import load_plugins
    plugins = load_plugins()
    
    help_text = "🤖 *Wexxy PC Bot - Help Menu*\n\n"
    
    help_text += "🛠 *Core Commands*\n"
    help_text += "• `/start` — Restart interaction & show menu\n"
    help_text += "• `/help` — Show this comprehensive help list\n"
    help_text += "• `/restart_bot` — Reboot the bot service\n\n"
    
    help_text += "🔌 *Available Commands*\n"
    
    # Filter and sort plugin commands
    command_list = []
    for p in plugins:
        cmd = p.get("command")
        if cmd:
            desc = p.get("description", "No description")
            command_list.append((cmd, desc))
            
    seen = set()
    unique_commands = []
    for cmd, desc in command_list:
        if cmd not in seen:
            unique_commands.append((cmd, desc))
            seen.add(cmd)
            
    for cmd, desc in sorted(unique_commands):
        help_text += f"• `/{cmd}` — _{desc}_\n"
        
    help_text += "\n✨ *Advanced Features*\n"
    help_text += "• 🎤 *Voice:* Send voice notes to control your PC naturally.\n"
    help_text += "• 💬 *Chat:* Send direct text for AI-powered assistance.\n"
    help_text += "• 🖥️ *RustDesk:* Use the menu button for remote desktop access.\n"
    help_text += "• 🚀 *Auto-Launch:* Type `/launch` followed by any app name.\n"

    help_text += "\n📛 *Renamed Buttons* _(for reference)_\n"
    help_text += "• `Close Keyboard` → *CK* (`/close`)\n"
    help_text += "• `File Finder` → *Finder* (`/find`)\n"
    help_text += "• `Fetch File` → *Fetcher* (`/fetch`)\n"
    help_text += "• `List Files` → *Dir* (`/ls`)\n"
    help_text += "• `Screenshot` → *Shot* (`/screenshot`)\n"
    help_text += "• `PC Status` → *Status* (`/pc_status`)\n"
    help_text += "• `Software Manager` → *Winget* (`/winget`)\n"
    help_text += "• `Open Web` → *Browser* (`/web`)\n"
    help_text += "• `Web Search` → *Search* (`/web_search`)\n"
    help_text += "• `Web AI` → *WebAI* (`/web_ai`)\n"
    help_text += "• `Stop RustDesk` → *No Touch* (`/stop_rustdesk`)\n"
    help_text += "• `Ide Control` → *IDE* (`/control_antigravity`)\n"
    help_text += "• `System Guardian` → *Guardian* (`/monitor`)\n"

    await update.message.reply_text(help_text, parse_mode="Markdown")

PLUGIN = {
    "name": "Help ❓",
    "command": "help",
    "description": "Show available commands",
    "handler": handle_help,
    "row": 0,
}
