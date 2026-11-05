# UI/UX Design
## Wexxy PC Bot

### 1. Telegram Interface
Since this is a Telegram Bot, the UI is primarily conversational and text-based.
- **Bot Menu**: A persistent keyboard provides quick access to frequently used commands (`/help`, `/apps`, `/launch`, `/control_antigravity`).
- **Rich Responses**: The bot uses Markdown formatting for clear, readable responses (bold text for status, code blocks for command output).
- **Feedback**: Emojis are used extensively to provide immediate visual feedback (e.g., ✅ for success, ❌ for errors, ⏳ for processing, 📥 for downloading).

### 2. Touchpad Web Interface
The remote touchpad is a local HTML/JS single-page application served via Flask and exposed via Cloudflared.
- **Responsive Design**: Designed primarily for mobile screens.
- **Interaction Model**:
  - Dragging a finger across the screen moves the PC cursor.
  - A single tap triggers a left-click.
  - A two-finger tap triggers a right-click.
  - Two-finger drag triggers scrolling.
- **Live View Tab**: A secondary tab within the UI displays a low-latency MJPEG stream of the PC's primary monitor.
