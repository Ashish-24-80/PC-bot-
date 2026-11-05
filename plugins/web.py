import webbrowser
import urllib.parse
import urllib.request
import json

async def handle_web(update, context):
    try:
        if not context.args:
            await update.message.reply_text("Usage: /web <url>")
            return
        url = context.args[0]
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        webbrowser.open(url)
        await update.message.reply_text(f"Opened {url} on PC.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def handle_web_search(update, context):
    try:
        if not context.args:
            await update.message.reply_text("Usage: /web_search <query>")
            return
        query = " ".join(context.args)
        
        # Try DuckDuckGo Instant Answer API (Free)
        api_url = "https://api.duckduckgo.com/?q=" + urllib.parse.quote(query) + "&format=json"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'WexxyBot/1.0'})
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        abstract = data.get("AbstractText")
        if abstract:
            await update.message.reply_text(f"Search Result:\n{abstract}")
        else:
            # Fallback to opening on PC
            search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
            webbrowser.open(search_url)
            await update.message.reply_text(f"No summary found. Opened Google search for '{query}' on PC browser.")
            
    except Exception as e:
        await update.message.reply_text(f"Search error: {e}")

async def handle_web_ai(update, context):
    try:
        if len(context.args) < 2:
            await update.message.reply_text(
                "Usage: /web_ai <api_key> <prompt>\n"
                "Example: /web_ai sk-or-v1-xxx What is the capital of France?\n"
                "(Uses OpenRouter.ai API by default, which supports free models)"
            )
            return
            
        api_key = context.args[0]
        prompt = " ".join(context.args[1:])
        
        # Using OpenRouter as it provides a standard OpenAI-compatible endpoint and has free models
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            # You can change the model here if you are using a different provider
            "model": "google/gemini-2.5-flash-free", 
            "messages": [{"role": "user", "content": prompt}]
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        await update.message.reply_text("Thinking...")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply = result['choices'][0]['message']['content']
            await update.message.reply_text(reply)
            
    except Exception as e:
        await update.message.reply_text(f"AI Request failed: {e}")

PLUGINS = [
    {
        "name": "Browser",
        "command": "web",
        "description": "Open a website on PC — formerly 'Open Web'",
        "handler": handle_web,
        "row": 4,
    },
    {
        "name": "Search",
        "command": "web_search",
        "description": "Search the web via API — formerly 'Web Search'",
        "handler": handle_web_search,
        "row": 4,
    },
    {
        "name": "WebAI",
        "command": "web_ai",
        "description": "Chat with AI using API key — formerly 'Web AI'",
        "handler": handle_web_ai,
        "row": 4,
    }
]
