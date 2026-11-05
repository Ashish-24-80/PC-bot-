import os
import requests
from config import TOKEN
if not TOKEN:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "REPLACED_TOKEN")
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
print("Webhook Info:", r.json())
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
print("Bot Info:", r.json())
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
print("Pending Updates:", r.json())
