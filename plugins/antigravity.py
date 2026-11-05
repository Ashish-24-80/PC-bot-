import pyautogui
import pyperclip
from telegram import Update
import asyncio

async def handle_control_antigravity(update: Update, context):
    try:
        if not context.args:
            await update.message.reply_text("Usage: /control_antigravity <prompt>\nExample: /control_antigravity write a hello world python script")
            return
            
        prompt = " ".join(context.args)
        await update.message.reply_text(f"📡 Automating Antigravity: `{prompt}`", parse_mode="Markdown")
        
        # 1. Copy to clipboard
        pyperclip.copy(prompt)
        
        # 2. Distract Mouse: Click in the center of the screen first
        # This ensures we aren't hovering over something that Ctrl+L might toggle off
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width / 2, screen_height / 2)
        await asyncio.sleep(0.2)
        
        # 3. Simulate Ctrl+L (Focus Antigravity/Search)
        pyautogui.hotkey('ctrl', 'l')
        await asyncio.sleep(0.3) # Small delay for UI response
        
        # 4. Simulate Ctrl+V (Paste)
        pyautogui.hotkey('ctrl', 'v')
        await asyncio.sleep(0.1)
        
        # 5. Press Enter
        pyautogui.press('enter')

        await update.message.reply_text("✅ Sequence executed: `Click Center` -> `Ctrl+L` -> `Ctrl+V` -> `Enter`")
    except Exception as e:
        await update.message.reply_text(f"❌ Error during automation: {e}")

PLUGIN = {
    "name": "IDE",
    "command": "control_antigravity",
    "description": "Send a prompt to Antigravity IDE — formerly 'Ide Control'",
    "handler": handle_control_antigravity,
    "row": 5,
}
