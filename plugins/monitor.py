import psutil
import asyncio
from telegram import Update

# Global state for monitor
MONITOR_TASK = None

def get_top_processes():
    """Get the top 3 processes by memory usage."""
    procs = []
    for proc in psutil.process_iter(['name', 'memory_percent']):
        try:
            procs.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by memory usage
    procs = sorted(procs, key=lambda p: p['memory_percent'] or 0, reverse=True)
    
    top_str = ""
    for p in procs[:3]:
        top_str += f"- {p['name']}: {p['memory_percent']:.1f}%\n"
    return top_str

async def monitor_loop(context, chat_id):
    """Background loop to check system health."""
    iterations = 0
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        
        if cpu > 90 or ram > 90:
            top_procs = get_top_processes()
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🚨 *CRITICAL SYSTEM ALERT*\nCPU: {cpu}%\nRAM: {ram}%\n\n*Top RAM Consumers:*\n{top_procs}\nShould I close some heavy apps?",
                parse_mode="Markdown"
            )
        elif iterations % 5 == 0:
            # Regular update every 5 minutes
            top_procs = get_top_processes()
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"📊 *System Status Update*\nCPU: {cpu}%\nRAM: {ram}%\n\n*Top RAM Consumers:*\n{top_procs}",
                parse_mode="Markdown"
            )
            
        iterations += 1
        await asyncio.sleep(60) # Check every minute

async def handle_monitor(update: Update, context):
    """Toggle the background monitor."""
    global MONITOR_TASK
    chat_id = update.effective_chat.id
    
    if MONITOR_TASK is None:
        MONITOR_TASK = asyncio.create_task(monitor_loop(context, chat_id))
        
        # Immediate readout on start
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        top_procs = get_top_processes()
        
        msg = f"✅ *Guardian Mode ON*\n\n📊 *Initial System Status:*\nCPU: {cpu}%\nRAM: {ram}%\n\n*Top RAM Consumers:*\n{top_procs}\n\n_You will receive updates every 5 minutes._"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        MONITOR_TASK.cancel()
        MONITOR_TASK = None
        await update.message.reply_text("💤 *Guardian Mode OFF*", parse_mode="Markdown")

PLUGIN = {
    "name": "Guardian",
    "command": "monitor",
    "description": "Background resource monitoring & alerts — formerly 'System Guardian'",
    "handler": handle_monitor,
    "row": 5,
}
