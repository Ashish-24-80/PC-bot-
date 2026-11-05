import subprocess
import asyncio
from telegram import Update

async def handle_winget(update: Update, context):
    """
    Handle winget commands: install, upgrade, list, search.
    Usage: /winget <command> <appname>
    """
    if not context.args:
        await update.message.reply_text("Usage: /winget <search|install|upgrade|list> <appname>")
        return
        
    cmd_type = context.args[0].lower()
    app_name = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    
    msg = await update.message.reply_text(f"🛠 Running winget {cmd_type}...")
    
    # Jugaad: Winget sometimes needs --accept-source-agreements or --accept-package-agreements
    base_cmd = ["winget", cmd_type]
    if app_name:
        base_cmd.append(app_name)
    
    if cmd_type in ["install", "upgrade"]:
        base_cmd.extend(["--accept-source-agreements", "--accept-package-agreements", "--silent"])
        
    try:
        process = await asyncio.create_subprocess_exec(
            *base_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        result = stdout.decode().strip() or stderr.decode().strip()
        
        if not result:
             result = "✅ Action completed (no output)."
             
        await msg.edit_text(f"✅ *Winget Result:*\n```\n{result[:1000]}\n```", parse_mode="Markdown")
        
    except Exception as e:
        await msg.edit_text(f"❌ Winget failed: {e}\n\n*Jugaad Tip:* Try using /control_antigravity to install via browser if winget fails.")

PLUGIN = {
    "name": "Winget",
    "command": "winget",
    "description": "Manage apps with winget — formerly 'Software Manager'",
    "handler": handle_winget,
    "row": 4,
}
