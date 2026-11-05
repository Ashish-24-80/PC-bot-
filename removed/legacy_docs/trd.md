# Technical Requirements Document (TRD)
## Wexxy PC Bot

### 1. Architecture
- **Language**: Python 3.13 (Miniconda)
- **Framework**: `python-telegram-bot` for asynchronous Telegram API interactions.
- **Web Server**: `Flask` for the remote touchpad and MJPEG streaming interface.
- **Tunneling**: `cloudflared` for exposing the local Flask server to the internet securely.

### 2. Modular Plugin System
The bot uses a dynamic plugin loader. Plugins are Python modules stored in the `plugins/` directory, exposing a `PLUGIN` dictionary or `PLUGINS` list containing the name, command, description, and handler function.

### 3. Dependencies
- `python-telegram-bot`
- `Flask`
- `pyautogui` (Mouse/Keyboard control)
- `mss` (Fast screen capture)
- `Pillow` (Image processing)
- `psutil` (System monitoring)
- `whisper` (Voice transcription)

### 4. Concurrency & Locking
- A custom `.lock` file mechanism is implemented to prevent multiple instances of the bot from running simultaneously.
- Asynchronous handlers (`asyncio`) are used extensively for non-blocking I/O operations (e.g., executing shell commands, fetching files).
