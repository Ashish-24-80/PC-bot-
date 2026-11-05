import psutil
import socket

async def handle_info(update, context):
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        ip = socket.gethostbyname(socket.gethostname())
        bat_str = f"{battery.percent}% {'(charging)' if battery.power_plugged else ''}" if battery else "N/A"
        msg = (
            f"CPU: {cpu}%\n"
            f"RAM: {ram.percent}% used ({round(ram.used/1e9,1)}GB / {round(ram.total/1e9,1)}GB)\n"
            f"Battery: {bat_str}\n"
            f"IP: {ip}"
        )
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Failed to get PC status: {e}")

PLUGIN = {
    "name": "Status",
    "command": "pc_status",
    "description": "CPU, RAM, battery, IP — formerly 'PC Status'",
    "handler": handle_info,
    "row": 0,
}
