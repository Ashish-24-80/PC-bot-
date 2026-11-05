from telegram import ReplyKeyboardRemove

async def handle_close(update, context):
    """
    Removes the custom keyboard. It can be brought back with /start.
    """
    await update.message.reply_text(
        "Keyboard closed. Send /start to open it again.",
        reply_markup=ReplyKeyboardRemove()
    )

PLUGIN = {
    "name": "CK",
    "command": "close",
    "description": "Hide the bot keyboard — formerly 'Close Keyboard'",
    "handler": handle_close,
    "row": 4,
}
