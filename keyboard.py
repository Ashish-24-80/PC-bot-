from telegram import ReplyKeyboardMarkup
from plugins import load_plugins

def build_keyboard(max_per_row=5):
    """
    Builds the ReplyKeyboardMarkup by scanning loaded plugins.
    Plugins specify their own row. Automatically splits rows exceeding max_per_row.
    """
    plugins = load_plugins()
    rows = {}
    for p in plugins:
        rows.setdefault(p["row"], []).append(p["name"])
    
    keyboard_layout = []
    for i in sorted(rows.keys()):
        row_buttons = rows[i]
        for start_idx in range(0, len(row_buttons), max_per_row):
            keyboard_layout.append(row_buttons[start_idx:start_idx + max_per_row])
            
    return ReplyKeyboardMarkup(keyboard_layout, resize_keyboard=True)
