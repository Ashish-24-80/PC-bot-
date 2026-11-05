"""
plugins/runner.py
/run <any shell command> → executes on PC → returns output
Last resort tool. Use /launch and voice commands first.
"""
from utils.runner import run as shell_run


async def handle_run(update, context):
    if not context.args:
        await update.message.reply_text(
            "Usage: `/run <command>`\n"
            "e.g. `/run clawx`\n"
            "e.g. `/run python myscript.py`\n"
            "e.g. `/run node -e \"console.log('hi')\"`",
            parse_mode="Markdown"
        )
        return

    cmd = " ".join(context.args)
    await update.message.reply_text(f"⚙️ Running: `{cmd}`", parse_mode="Markdown")

    output = shell_run(cmd, timeout=30)

    # Telegram message limit is 4096 chars
    if len(output) > 3800:
        output = output[:3800] + "\n... (truncated)"

    await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")


PLUGIN = {
    "name": "cmd-runner",
    "command": "run",
    "description": "Run any shell command on PC",
    "handler": handle_run,
    "row": 99,  # command only — no keyboard button
}
