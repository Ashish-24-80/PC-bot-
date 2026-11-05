$TaskName = "WexxyPCBot"
$TaskDescription = "Starts the Wexxy PC Telegram Bot on User Logon."
$ActionExecutable = "cmd.exe"
$ActionArguments = "/c `"`"C:\Users\SUBU\Documents\1MY_APPs\TelegramBot\Wexxy-pc-bot\run_bot.bat`"`""
$WorkingDirectory = "C:\Users\SUBU\Documents\1MY_APPs\TelegramBot\Wexxy-pc-bot"

# Define the action
$Action = New-ScheduledTaskAction -Execute $ActionExecutable -Argument $ActionArguments -WorkingDirectory $WorkingDirectory

# Define the trigger (At Logon)
$Trigger = New-ScheduledTaskTrigger -AtLogOn

# Define settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

# Register the task
Register-ScheduledTask -TaskName $TaskName -Description $TaskDescription -Action $Action -Trigger $Trigger -Settings $Settings -Force

Write-Host "Successfully registered WexxyPCBot task in Task Scheduler."
Write-Host "The bot will now start automatically whenever you log in."
