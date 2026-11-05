# -*- coding: utf-8 -*-
import logging
from telegram import Update
from telegram.ext import (
    Application, MessageHandler, CommandHandler, filters
)
import sys, os
libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libs'))
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
from config import TOKEN
from plugins import load_plugins
from middleware import admin_only
from keyboard import build_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("wexxy.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

STARTUP_MSG = """
🤖 *Wexxy PC Bot is up.*

*Quick Menu:*
/help — Show all available commands
/apps — Browse all installed apps
/launch `appname` — Open any app
/media_route_reveal — Check where media files are going
/change_media_route `path` — Route media to gemma4 or folder
/control\\_antigravity `prompt` — Control IDE

*Interactions:*
🎤 Voice Note → Transcribe & Execute
💬 Direct Text → Chat with AI
🖥️ RustDesk Button → Remote Desktop Control

Type /help for the full command list.
""".strip()


async def start(update: Update, context):
    try:
        
        from plugins.routing import get_media_route
        route = get_media_route()
        status_msg = "\n\n*Server Connection Status:*\n"
        status_msg += f"🔀 *Current Media Route:* `{route}`"
    except Exception:
        status_msg = ""

    await update.message.reply_text(
        f"✅ *Bot is running.*\n\n{STARTUP_MSG}{status_msg}",
        parse_mode="Markdown",
        reply_markup=build_keyboard()
    )


async def handle_restart_bot(update: Update, context):
    await update.message.reply_text("🔄 Restarting bot...")
    # Give it a second to send the message
    import asyncio
    await asyncio.sleep(1)
    # Pass the chat ID to the new process
    os.environ["RESTART_CHAT_ID"] = str(update.effective_chat.id)
    # Restart the process
    os.execv(sys.executable, [sys.executable] + sys.argv)

async def handle_media_route_reveal(update: Update, context):
    from plugins.routing import get_media_route
    route = get_media_route()
    await update.message.reply_text(f"🔀 Current Media Route: `{route}`", parse_mode="Markdown")

async def handle_change_media_route(update: Update, context):
    if not context.args:
        await update.message.reply_text("Usage: `/change_media_route <gemma4|whisper|qwen|C:\\path\\to\\folder>`", parse_mode="Markdown")
        return
    route = " ".join(context.args)
    from plugins.routing import set_media_route
    set_media_route(route)
    await update.message.reply_text(f"✅ Media route successfully changed to: `{route}`\n\nAll voice notes and images will now be sent there.", parse_mode="Markdown")


import os
import sys

def main():
    lock_path = "wexxy.bot.lock"
    try:
        if os.path.exists(lock_path):
            os.remove(lock_path)
    except OSError:
        logger.error("🛑 CRITICAL: Another instance of Wexxy Bot is already running (lock file busy). Exiting.")
        sys.exit(1)
        
    try:
        global _lock_file_handle
        _lock_file_handle = open(lock_path, 'w')
        _lock_file_handle.write(str(os.getpid()))
        _lock_file_handle.flush()
        # On Windows, keeping it open is enough to prevent os.remove by others.
    except Exception as e:
        logger.error(f"⚠️ Could not create lock file: {e}")
        # Not exiting here as it might be a permissions issue but still allowed to run 
        # (though risky)

    async def post_init(application: Application):
        from telegram import BotCommand
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show all commands"),
            BotCommand("launch", "Launch an app (usage: /launch <app>)"),
            BotCommand("run", "Run a raw shell command"),
            BotCommand("restart_bot", "Restart bot service"),
            BotCommand("gemma4", "Chat with Gemma 4 12B"),
            BotCommand("gemma", "Chat directly with Gemma 2B"),
            BotCommand("qwen", "Chat directly with Qwen 7B"),
            BotCommand("media_route_reveal", "Show current media route"),
            BotCommand("change_media_route", "Change media destination"),
        ]
        
        # Dynamically add all loaded plugins to the autocomplete menu
        from plugins import load_plugins
        for p in load_plugins():
            if p.get("command") and p.get("row", 0) != 99:
                # Telegram has a 32-character limit for command names, and they must be lowercase
                cmd_name = p["command"].lower()[:32]
                cmd_desc = p.get("description", p["name"])[:256]
                commands.append(BotCommand(cmd_name, cmd_desc))

        await application.bot.set_my_commands(commands)

        # Send restart confirmation if applicable
        restart_chat_id = os.environ.get("RESTART_CHAT_ID")
        if restart_chat_id:
            try:
                await application.bot.send_message(chat_id=restart_chat_id, text="✅ *Restart Complete!*", parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Failed to send restart confirmation: {e}")
            os.environ.pop("RESTART_CHAT_ID", None)

    app = Application.builder().token(TOKEN).post_init(post_init).build()

    # Global update logger
    async def log_update(update: Update, context):
        logger.info(f"📡 RAW UPDATE: {update}")
    app.add_handler(MessageHandler(filters.ALL, log_update), group=-1)

    # /start
    app.add_handler(CommandHandler("start", admin_only(start)))
    app.add_handler(CommandHandler("restart_bot", admin_only(handle_restart_bot)))

    # Load and register all plugins
    plugins = load_plugins()
    for plugin in plugins:
        # Button press handler
        app.add_handler(MessageHandler(
            filters.Text([plugin["name"]]),
            admin_only(plugin["handler"])
        ))
        # Slash command (skip row 99 — internal only)
        if plugin.get("command") and plugin.get("row", 0) != 99:
            try:
                app.add_handler(CommandHandler(
                    plugin["command"],
                    admin_only(plugin["handler"])
                ))
            except Exception:
                pass

    # /launch — args needed, register separately
    from plugins.launcher import handle_launch
    app.add_handler(CommandHandler("launch", admin_only(handle_launch)))

    # /run — raw shell runner
    from plugins.runner import handle_run
    app.add_handler(CommandHandler("run", admin_only(handle_run)))

    # /startllm + voice pipeline (optional plugin)
    try:
        from plugins.voice import handle_startllm, handle_voice, handle_text, handle_gemma_cmd, handle_qwen_cmd, handle_gemma4_cmd
        app.add_handler(CommandHandler("startllm", admin_only(handle_startllm)))
        app.add_handler(CommandHandler("gemma4", admin_only(handle_gemma4_cmd)))
        app.add_handler(CommandHandler("gemma", admin_only(handle_gemma_cmd)))
        app.add_handler(CommandHandler("qwen", admin_only(handle_qwen_cmd)))
        app.add_handler(CommandHandler("media_route_reveal", admin_only(handle_media_route_reveal)))
        app.add_handler(CommandHandler("change_media_route", admin_only(handle_change_media_route)))
        app.add_handler(MessageHandler(filters.VOICE, admin_only(handle_voice)))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_only(handle_text)))
    except ImportError:
        logger.warning("plugins.voice module not found, skipping voice handlers.")
    
    # Receive files from mobile
    from plugins.files import handle_document
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, admin_only(handle_document)))

    # Global error handler
    async def error_handler(update, context):
        logger.error(f"Update {update} caused error {context.error}")
    app.add_error_handler(error_handler)

    logger.info("Wexxy PC Bot started.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    import time
    while True:
        try:
            main()
        except KeyboardInterrupt:
            logger.info("🛑 Bot manually stopped by user.")
            break
        except Exception as e:
            logger.error(f"💥 CRASH DETECTED: {e}. Auto-restarting bot engine in 5 seconds...", exc_info=True)
            time.sleep(5)
