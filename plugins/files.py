import subprocess
import os
import asyncio
from telegram import Update

async def handle_find(update: Update, context):
    """
    Search for files on the PC.
    Jugaad: Try Everything (es.exe) first, then fallback to PowerShell.
    """
    if not context.args:
        await update.message.reply_text("Usage: /find <filename>")
        return
        
    query = " ".join(context.args)
    msg = await update.message.reply_text(f"🔍 Searching for `{query}`...", parse_mode="Markdown")
    
    # Attempt 1: es.exe (Everything CLI - super fast)
    es_path = os.path.join(os.getcwd(), "utils", "es.exe")
    try:
        proc = await asyncio.create_subprocess_exec(
            es_path, query, "-n", "10",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        if stdout:
            results = stdout.decode().strip()
            await msg.edit_text(f"🚀 *Everything Results:*\n```\n{results}\n```", parse_mode="Markdown")
            return
    except:
        pass # Everything not installed
        
    # Attempt 2: PowerShell (Jugaad - works everywhere)
    await msg.edit_text(f"🔍 Everything not found. Using PowerShell (slower)...")
    try:
        ps_cmd = f"Get-ChildItem -Path C:\\Users\\$env:USERNAME -Filter '*{query}*' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 10 FullName | Out-String"
        proc = await asyncio.create_subprocess_exec(
            "powershell", "-Command", ps_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        results = stdout.decode().strip()
        
        if results:
            await msg.edit_text(f"📂 *PowerShell Results:*\n```\n{results}\n```", parse_mode="Markdown")
        else:
            await msg.edit_text(f"❌ No files found for `{query}`.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Search failed: {e}")

async def handle_ls(update: Update, context):
    """
    List directory contents.
    Usage: /ls <path>
    """
    path = " ".join(context.args) if context.args else os.path.expanduser("~")
    
    if not os.path.exists(path):
        await update.message.reply_text(f"❌ Path not found: `{path}`", parse_mode="Markdown")
        return
        
    if not os.path.isdir(path):
        await update.message.reply_text(f"📄 `{path}` is a file. Use /fetch to get it.", parse_mode="Markdown")
        return

    try:
        items = os.listdir(path)
        # Separate dirs and files
        dirs = [f"📁 {item}/" for item in items if os.path.isdir(os.path.join(path, item))]
        files = [f"📄 {item}" for item in items if os.path.isfile(os.path.join(path, item))]
        
        # Sort and limit
        dirs.sort()
        files.sort()
        
        all_items = dirs + files
        limit = 30
        visible_items = all_items[:limit]
        
        header = f"📂 *Contents of:* `{path}`\n\n"
        body = "\n".join(visible_items)
        if len(all_items) > limit:
            body += f"\n\n... and {len(all_items) - limit} more items."
            
        await update.message.reply_text(f"{header}{body}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error listing directory: {e}")

async def handle_fetch(update: Update, context):
    """
    Fetch a file from PC to mobile.
    Usage: /fetch <filepath>
    """
    if not context.args:
        await update.message.reply_text("Usage: /fetch <filepath>")
        return
        
    filepath = " ".join(context.args)
    if not os.path.exists(filepath):
        await update.message.reply_text(f"❌ File not found: `{filepath}`", parse_mode="Markdown")
        return
        
    msg = await update.message.reply_text(f"📤 Uploading `{filepath}`...", parse_mode="Markdown")
    try:
        await update.message.reply_document(document=open(filepath, 'rb'))
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Failed to upload: {e}")

async def handle_document(update: Update, context):
    """
    Receive a file from mobile to PC.
    """
    from plugins.routing import get_media_route
    route = get_media_route()

    doc = update.message.document or (update.message.photo[-1] if update.message.photo else None)
    if not doc:
        return
        
    file = await context.bot.get_file(doc.file_id)
    filename = getattr(doc, 'file_name', f"photo_{doc.file_id}.jpg")
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, filename)
        msg = await update.message.reply_text(f"📥 Downloading `{filename}`...", parse_mode="Markdown")
        await file.download_to_drive(filepath)

        # Image analysis routing (MiniCPM multimodal vision; supports legacy 'gemma4' alias)
        if route in ("minicpm", "cpm", "vision", "gemma4") and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                from plugins.voice import _ask_gemma4_multimodal
                await msg.edit_text("👁️ *Analyzing Image with MiniCPM Vision Model...*", parse_mode="Markdown")
                caption = update.message.caption or "Please describe this image in detail."
                response = await _ask_gemma4_multimodal(prompt=caption, image_path=filepath)
                await msg.edit_text(f"🤖 *MiniCPM Vision:*\n{response}", parse_mode="Markdown")
                return
            except (ImportError, Exception):
                pass  # Fall through to standard file saving if vision model/server is absent

        # Default save to Downloads or specified route
        download_dir = route if os.path.isabs(route) and os.path.isdir(route) else os.path.join(os.path.expanduser("~"), "Downloads", "WexxyBot")
        os.makedirs(download_dir, exist_ok=True)
        final_path = os.path.join(download_dir, filename)
        
        import shutil
        shutil.copy(filepath, final_path)
        await msg.edit_text(f"✅ File saved to:\n`{final_path}`", parse_mode="Markdown")

PLUGINS = [
    {
        "name": "Finder",
        "command": "find",
        "description": "Search for files on PC — formerly 'File Finder' (Fast + Fallback)",
        "handler": handle_find,
        "row": 4,
    },
    {
        "name": "Fetcher",
        "command": "fetch",
        "description": "Send a file from PC to Mobile — formerly 'Fetch File'",
        "handler": handle_fetch,
        "row": 4,
    },
    {
        "name": "Dir",
        "command": "ls",
        "description": "List directory contents — formerly 'List Files'",
        "handler": handle_ls,
        "row": 4,
    }
]
