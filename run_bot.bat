@echo off
cd /d "C:\Users\SUBU\Documents\1MY_APPs\TelegramBot\Wexxy-pc-bot"

:loop
"C:\ProgramData\miniconda3\pythonw.exe" bot.py
timeout /t 5 >nul
goto loop
