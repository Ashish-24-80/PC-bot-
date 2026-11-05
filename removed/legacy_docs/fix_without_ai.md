# How to Fix Wexxy PC Bot (Without AI) - Easy Debug Guide for Humans

If the bot stops working, behaves weirdly, or commands fail, follow this guide to troubleshoot and fix common issues yourself without needing an AI agent.

## 1. Cloudflared / Touchpad Feature Fails
**Symptom:** You click "Touchpad" and it says "Tunnel failed to start" or it just hangs.
**Why it happens:** 
- A previous `cloudflared.exe` process might be stuck in the background, blocking the port.
- Cloudflared might be trying to run an automatic update, which freezes the tunnel creation.
- Your internet connection to Cloudflare might be temporarily slow, causing a timeout.
**How to fix:**
1. Open **Task Manager** (Ctrl + Shift + Esc).
2. Go to the **Details** tab.
3. Find `cloudflared.exe`. If you see any running, right-click and select **End task**.
4. Try clicking the "Touchpad" button in the bot again.
*(Note: We recently added a fix to automatically kill old `cloudflared.exe` processes and disable auto-updates, so this should happen less often now!)*

## 2. Bot Fails to Start ("Lock file busy" / 409 Conflict)
**Symptom:** You run `StartWexxyBot.bat` and the bot crashes immediately saying "Another instance of Wexxy Bot is already running" or you see "409 Conflict" in the logs.
**Why it happens:** You have multiple instances of the bot trying to connect to Telegram with the same token. The script creates a `wexxy.bot.lock` file to prevent this, but sometimes it doesn't get cleaned up properly if the bot crashed.
**How to fix:**
1. Close all command prompt windows running the bot.
2. Open Task Manager, find any stray `python.exe` processes, and end them.
3. In the bot folder (`Wexxy-pc-bot`), find the file named `wexxy.bot.lock` and **delete it**.
4. Run `StartWexxyBot.bat` again.

## 3. Voice Commands or Transcriptions Fail
**Symptom:** You send a voice note, but the bot ignores it or throws an error.
**Why it happens:** The Whisper model might be missing, FFmpeg might not be installed correctly, or the audio file format isn't supported.
**How to fix:**
1. Ensure `ffmpeg` is installed and added to your system PATH.
2. Check the console logs. If it says "whisper model not found", you might need to run `/startllm` or ensure your environment has an active internet connection to download the model the first time.

## 4. App Launching (`/launch` or `/apps`) Fails
**Symptom:** `/launch chrome` does nothing.
**Why it happens:** The bot relies on indexing shortcuts in your Start Menu. If the shortcut isn't there, or the index hasn't refreshed, it won't find it.
**How to fix:**
1. Ensure the app is actually installed.
2. Wait a few seconds for the `apps.py` plugin to index your shortcuts on startup.
3. If it still fails, use `/find <appname>.exe` to manually locate the executable and then launch it via the terminal using the `/run` command.

## 5. Cannot Find or Send Files
**Symptom:** Using `/fetch` or `/find` doesn't return anything.
**Why it happens:** Windows Search/PowerShell is sometimes slow.
**How to fix:**
1. Ensure the file name is spelled correctly.
2. Install the **Everything CLI (es.exe)** if you haven't already. It's significantly faster and more reliable than the fallback PowerShell script.

---
**General Debugging Tip:** 
Always keep the Command Prompt window open and visible when testing. The logs will explicitly tell you exactly which line of code failed and why. If all else fails, type `/restart_bot` to reboot the bot cleanly.
