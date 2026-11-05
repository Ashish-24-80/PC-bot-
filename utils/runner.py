"""
utils/runner.py — universal command runner
Import and use anywhere: from utils.runner import run, run_powershell, open_app
"""
import subprocess
import shutil


def run(cmd: str, timeout: int = 30) -> str:
    """
    Run any shell command. Returns stdout or stderr as string.
    Works with: python, node, powershell, raw exe, anything in PATH.
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        out = result.stdout.strip() or result.stderr.strip()
        return out or "✅ Done (no output)"
    except subprocess.TimeoutExpired:
        return f"⏱ Timed out after {timeout}s"
    except Exception as e:
        return f"❌ Error: {e}"


def run_powershell(cmd: str, timeout: int = 30) -> str:
    """Run a PowerShell command specifically."""
    return run(f"powershell -NoProfile -Command \"{cmd}\"", timeout)


def open_app(name: str) -> str:
    """
    Robust app launcher — tries 3 layers:
    1. Direct PATH lookup via shutil
    2. PowerShell Get-Command
    3. Windows shell resolver (nuclear — same as Win+R)
    Returns status string.
    """
    # Layer 1: shutil which
    found = shutil.which(name)
    if found:
        subprocess.Popen([found])
        return f"✅ Launched `{name}` (PATH)"

    # Layer 2: PowerShell Get-Command
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         f"(Get-Command '{name}' -ErrorAction SilentlyContinue).Source"],
        capture_output=True, text=True
    )
    path = result.stdout.strip()
    if path:
        subprocess.Popen([path])
        return f"✅ Launched `{name}` (PowerShell)"

    # Layer 3: nuclear — Windows shell resolver
    subprocess.Popen(name, shell=True)
    return f"✅ Launched `{name}` (shell resolver)"
