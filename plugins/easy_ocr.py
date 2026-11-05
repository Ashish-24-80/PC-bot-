import pyautogui, os, asyncio
import easyocr
from telegram import Update

async def handle_ocr(update: Update, context):
    """Capture screen and run EasyOCR, replying with image and detected text."""
    msg = await update.message.reply_text("📸 Taking screenshot…")
    screenshot_path = "ocr_temp.png"
    pyautogui.screenshot(screenshot_path)

    # EasyOCR (CPU only)
    reader = easyocr.Reader(["en"], gpu=False)
    result = reader.readtext(screenshot_path, detail=0)
    text = " ".join(result) if result else "(no text detected)"

    with open(screenshot_path, "rb") as photo:
        await update.message.reply_photo(
            photo,
            caption=f"📝 *OCR Detected Text:*\n```\n{text[:500]}\n```",
            parse_mode="Markdown",
        )
    # cleanup
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
    await msg.delete()

PLUGIN = {
    "name": "OCR",
    "command": "ocr",
    "description": "Read screen text using EasyOCR (no Tesseract data required)",
    "handler": handle_ocr,
    "row": 5,
}
