$StartupFolder = [System.IO.Path]::Combine($env:APPDATA, "Microsoft\Windows\Start Menu\Programs\Startup")
$ShortcutPath = Join-Path $StartupFolder "WexxyPCBot.lnk"
$TargetPath = "C:\Users\SUBU\Documents\1MY_APPs\TelegramBot\Wexxy-pc-bot\run_bot.bat"
$WorkingDirectory = "C:\Users\SUBU\Documents\1MY_APPs\TelegramBot\Wexxy-pc-bot"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $WorkingDirectory
$Shortcut.WindowStyle = 7 # Minimized
$Shortcut.Save()

Write-Host "Successfully created startup shortcut at: $ShortcutPath"
Write-Host "The bot will now start (hidden) whenever you log in."
