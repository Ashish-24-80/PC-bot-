"""
watch_and_fix.py
Watches a target markdown file for changes and auto-runs fix_markdown.py on it.
Usage: python scratch/watch_and_fix.py <target_file.md>
Press Ctrl+C to stop.
"""
import sys
import time
import os
from pathlib import Path

def get_mtime(path: Path):
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None

def get_size(path: Path):
    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0

if len(sys.argv) < 2:
    print("Usage: python scratch/watch_and_fix.py <file.md>")
    sys.exit(1)

target = Path(sys.argv[1])
fixer = Path("scratch/fix_markdown.py")

print(f"[WATCHER] Watching: {target}")
print("[WATCHER] Save the file in your editor to trigger formatting.")
print("[WATCHER] Press Ctrl+C to stop.\n")

last_mtime = get_mtime(target)
last_size = get_size(target)

while True:
    time.sleep(1)
    current_mtime = get_mtime(target)
    current_size = get_size(target)

    if current_mtime is None:
        continue  # file doesn't exist yet

    if current_mtime != last_mtime or current_size != last_size:
        if current_size == 0:
            print(f"[WATCHER] File changed but is empty (0 bytes), skipping...")
            last_mtime = current_mtime
            last_size = current_size
            continue

        print(f"[WATCHER] Change detected! Size: {current_size} bytes. Running formatter...")
        exit_code = os.system(f'python "{fixer}" "{target}"')
        if exit_code == 0:
            print(f"[WATCHER] Formatting complete. Waiting for next save...")
        else:
            print(f"[WATCHER] Formatter exited with code {exit_code}")

        last_mtime = get_mtime(target)
        last_size = get_size(target)
