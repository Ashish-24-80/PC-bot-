import pyautogui
import io

async def handle_screenshot(update, context):
    try:
        img = pyautogui.screenshot()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        await update.message.reply_photo(photo=buf)
    except Exception as e:
        await update.message.reply_text(f"Failed to capture screenshot: {e}")

PLUGIN = {
    "name": "Shot",
    "command": "screenshot",
    "description": "Capture and send screen — formerly 'Screenshot'",
    "handler": handle_screenshot,
    "row": 0,
}
