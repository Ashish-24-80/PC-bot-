"""
Run as Administrator:
    python service/install.py          → install & start
    python service/install.py remove   → stop & remove
"""
import subprocess
import sys
import os

SERVICE_NAME = "WexxyPCBot"
PYTHON_EXE   = sys.executable
BOT_SCRIPT   = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bot.py"))
BOT_DIR      = os.path.dirname(BOT_SCRIPT)
NSSM         = "nssm"  # must be in PATH, or replace with full path

def run(cmd):
    print(f"  > {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def install():
    print(f"Installing '{SERVICE_NAME}' as Windows service...")
    run([NSSM, "install",   SERVICE_NAME, PYTHON_EXE, BOT_SCRIPT])
    run([NSSM, "set",       SERVICE_NAME, "AppDirectory",  BOT_DIR])
    run([NSSM, "set",       SERVICE_NAME, "AppStdout",     os.path.join(BOT_DIR, "wexxy.log")])
    run([NSSM, "set",       SERVICE_NAME, "AppStderr",     os.path.join(BOT_DIR, "wexxy_err.log")])
    run([NSSM, "set",       SERVICE_NAME, "Start",         "SERVICE_AUTO_START"])
    run([NSSM, "start",     SERVICE_NAME])
    print(f"\n✅ Service '{SERVICE_NAME}' installed and running.")
    print("   It will auto-start on every boot.")

def remove():
    print(f"Removing '{SERVICE_NAME}'...")
    subprocess.run([NSSM, "stop",   SERVICE_NAME])
    subprocess.run([NSSM, "remove", SERVICE_NAME, "confirm"])
    print(f"✅ Service '{SERVICE_NAME}' removed.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("remove", "uninstall"):
        remove()
    else:
        install()
