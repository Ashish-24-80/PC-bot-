import pyautogui
import time
import pyperclip

async def handle_launch(update, context):
    if not context.args:
        await update.message.reply_text(
            "Usage: `/launch appname`\n\n"
            "Example: `/launch chrome`",
            parse_mode="Markdown"
        )
        return

    # Join args to support app names with spaces
    appname = " ".join(context.args)

    try:
        # Copy to clipboard
        pyperclip.copy(appname)
        
        # Open Windows Start Menu
        pyautogui.press('winleft')
        time.sleep(1.0)  # Wait for start menu animation
        
        # Paste the app name
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)  # Wait for Windows Search to find the best match
        
        # Hit enter to launch the first search result
        pyautogui.press('enter')
        
        await update.message.reply_text(f"🚀 Launched `{appname}` via Windows Search", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to launch `{appname}`: {e}", parse_mode="Markdown")

PLUGIN = {
    "name": "Launcher",
    "command": "launch",
    "description": "Launch an app by name (Usage: /launch appname)",
    "handler": handle_launch,
    "row": 99,  # Hidden from keyboard — command only
}
