# Kill all python processes
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "pythonw" -Force -ErrorAction SilentlyContinue

# Wait to ensure they are dead
Start-Sleep -Seconds 5

# Start the bot
Start-Process "python" -ArgumentList "bot.py" -WorkingDirectory "C:\Users\SUBU\Documents\1MY_APPs\TelegramBot\Wexxy-pc-bot" -WindowStyle Hidden

Write-Output "Bot restarted."
