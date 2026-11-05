# Application Flow
## Wexxy PC Bot

### 1. Initialization Flow
1. User executes `StartWexxyBot.bat`.
2. Python checks for `wexxy.bot.lock`. If it exists and is locked, exit. Otherwise, lock it.
3. `load_plugins()` iterates over `plugins/*.py` and registers handlers.
4. Telegram `Application` starts polling.

### 2. Request Processing Flow (General)
1. Telegram sends an Update (Message, Command, File) to the Bot API.
2. The bot intercepts the update.
3. The `admin_only` middleware verifies the sender's Telegram ID against the configured Admin ID. If unauthorized, the request is dropped.
4. The update is routed to the corresponding plugin handler.
5. The handler executes local OS commands or APIs.
6. The handler edits the Telegram message with the final status/output.

### 3. Touchpad Initialization Flow
1. User sends `/touchpad` or clicks the Touchpad button.
2. Bot starts the local Flask server in a background thread.
3. Bot spawns a `subprocess` for `cloudflared tunnel`.
4. Bot reads `cloudflared` stdout to extract the `trycloudflare.com` URL.
5. Bot sends the URL back to the user on Telegram.
6. User clicks the URL on mobile to access the web UI.
