# Backend Schema & Data Models
## Wexxy PC Bot

Since Wexxy is a real-time control bot, it does not currently rely on a persistent database like PostgreSQL or MongoDB. State is managed primarily in memory, through the file system, and via Telegram's API.

### 1. Plugin Data Structure
Each plugin must expose its configuration in the following schema:
```python
{
    "name": str,          # Human-readable name
    "command": str,       # Telegram slash command (e.g., 'find' for /find)
    "description": str,   # Brief description for the /help menu
    "handler": Callable,  # Async function to execute
    "row": int            # Order priority for menu rendering
}
```

### 2. File Storage Schema
- **Logs**: Written to `wexxy.log` in the root directory.
- **Downloads**: Files sent from mobile are saved to `~/Downloads/WexxyBot/`.
- **Lock File**: `wexxy.bot.lock` stores the PID of the active bot instance.

### 3. API Interactions (Internal)
- **Flask Server**: Listens on `localhost:5000` (configurable).
- **Endpoints**:
  - `GET /` -> Serves `trackpad.html`
  - `GET /info` -> Returns screen dimensions `{"w": int, "h": int}`
  - `POST /mouse` -> Accepts actions `{"action": "move|click|scroll", "dx": int, ...}`
  - `GET /stream` -> Returns MJPEG stream
