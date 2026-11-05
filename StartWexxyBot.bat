
@echo off
title Wexxy PC Bot
cd /d "%~dp0"
 
echo ========================================
echo        Wexxy PC Bot Launcher
echo ========================================
echo.
 
:loop
"C:\ProgramData\miniconda3\python.exe" bot.py
 
echo.
echo [!] Bot stopped or crashed. Restarting in 5 seconds...
echo     Press Ctrl+C to exit.
timeout /t 5 >nul
goto loop
