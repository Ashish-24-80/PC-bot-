# Wexxy PC Bot - Learnings & Troubleshooting

This document tracks critical issues encountered during development and how they were resolved to prevent them from happening again.

## 1. Telegram Bot Conflict Error (`telegram.error.Conflict`)

**The Problem:**
The bot crashed unexpectedly with the following traceback during transcription and `/launch` commands:
`telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`

**What we learned:**
This happens when multiple instances of the Python bot script are running simultaneously and polling Telegram using the same API token. They fight over the `getUpdates` requests, causing the connection to terminate and interrupting whatever background task (like Whisper transcription) the bot was running.

**How we solved it:**
- Identified ghost Python processes running in the background (`python.exe` and `pythonw.exe`) using PowerShell (`Get-Process`).
- Force-killed the duplicate processes.
- Ensured that `StartWexxyBot.bat` is used as the single source of truth for running the bot. The script has a `:loop` to automatically restart the bot if it crashes, but stops us from accidentally running multiple overlapping instances in the background.

## 2. Accidental Feature Downgrades (File Overwrites)

**The Problem:**
The streaming service lost its "Absolute Touch" capability, and the `/launch` command reverted to a less robust version. 

**What we learned:**
When migrating or integrating code from `reference_files`, blindly copying files can overwrite newer, heavily-customized implementations. 
- `plugins/launcher.py` was overwritten, losing the robust `pyautogui` Start-Menu search implementation.
- `static/trackpad.html` was overwritten, losing the Javascript logic that mapped touch coordinates on the stream directly to the PC monitor.

**How we solved it:**
- **Launcher:** Restored `launcher.py` from an automatically generated `launcher.py.bak` backup file, reinstating the method that uses `pyperclip`, `winleft`, and `Ctrl+V` to search the Start Menu dynamically.
- **Absolute Touch Stream:** Re-implemented the `getAbsoluteCoords` logic in `trackpad.html`. The logic calculates the exact touch position relative to the `stream-img` DOM element, accounts for `object-fit: contain` letterboxing and scaling, and maps it back to the PC's native resolution (e.g., 1920x1080). It then sends a `move_absolute` POST request so tapping the stream directly clicks that exact icon on the PC.
- **Typing Fix:** Fixed the `sendText` function in the HTML to correctly send the `typetext` action rather than iterating characters through the `keypress` action.
