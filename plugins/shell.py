"""
plugins/shell.py — Linux-like interactive shell for Wexxy
Supports: ls, cd, pwd, cat, mkdir, rm, mv, cp, tree, echo,
          whoami, hostname, env, head, tail, find, touch, clear
State: cwd is stored per chat_id so each user has their own session.
Usage: /sh <command>   e.g. /sh ls -la   or   /sh cd Documents
"""

import os
import shutil
import socket
import platform
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

# Per-session working directory keyed by chat_id
_cwd_store: dict[int, Path] = {}

def _cwd(chat_id: int) -> Path:
    if chat_id not in _cwd_store:
        _cwd_store[chat_id] = Path.home()
    return _cwd_store[chat_id]

def _set_cwd(chat_id: int, path: Path):
    _cwd_store[chat_id] = path

def _format_block(text: str) -> str:
    """Wrap output in monospace code block, truncating at 4000 chars."""
    text = text[:4000] if len(text) > 4000 else text
    return f"```\n{text}\n```"

# ── Command Handlers ──────────────────────────────────────────────────────────

def cmd_ls(cwd: Path, args: list[str]) -> str:
    target = Path(args[0]).expanduser() if args else cwd
    if not target.is_absolute():
        target = cwd / target
    if not target.exists():
        return f"ls: {target}: No such file or directory"
    show_hidden = "-a" in args or "-la" in args or "-al" in args
    long_fmt = "-l" in args or "-la" in args or "-al" in args

    items = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    if not show_hidden:
        items = [i for i in items if not i.name.startswith(".")]

    if not long_fmt:
        names = ["📁 " + i.name + "/" if i.is_dir() else "📄 " + i.name for i in items]
        return "\n".join(names) or "(empty)"

    # Long format
    lines = []
    for i in items:
        try:
            stat = i.stat()
            size = stat.st_size
            mtime = os.path.getmtime(i)
            import datetime
            mt = datetime.datetime.fromtimestamp(mtime).strftime("%b %d %H:%M")
            kind = "d" if i.is_dir() else "-"
            lines.append(f"{kind}  {size:>10}  {mt}  {i.name}")
        except PermissionError:
            lines.append(f"?  {'?':>10}  {'?':>12}  {i.name}")
    return "\n".join(lines) or "(empty)"

def cmd_cd(cwd: Path, args: list[str], chat_id: int) -> tuple[str, Path]:
    if not args or args[0] == "~":
        new = Path.home()
    else:
        new = Path(args[0]).expanduser()
        if not new.is_absolute():
            new = cwd / new
    new = new.resolve()
    if not new.exists():
        return f"cd: {new}: No such file or directory", cwd
    if not new.is_dir():
        return f"cd: {new}: Not a directory", cwd
    return f"→ {new}", new

def cmd_pwd(cwd: Path, _) -> str:
    return str(cwd)

def cmd_cat(cwd: Path, args: list[str]) -> str:
    if not args:
        return "cat: missing file operand"
    results = []
    for a in args:
        p = Path(a).expanduser()
        if not p.is_absolute():
            p = cwd / p
        if not p.exists():
            results.append(f"cat: {a}: No such file or directory")
            continue
        if p.is_dir():
            results.append(f"cat: {a}: Is a directory")
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            results.append(content[:3000])
        except Exception as e:
            results.append(f"cat: {a}: {e}")
    return "\n".join(results)

def cmd_head(cwd: Path, args: list[str]) -> str:
    n, files = 10, []
    i = 0
    while i < len(args):
        if args[i] == "-n" and i + 1 < len(args):
            n = int(args[i+1]); i += 2
        else:
            files.append(args[i]); i += 1
    if not files:
        return "head: missing file operand"
    p = Path(files[0]).expanduser()
    if not p.is_absolute(): p = cwd / p
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[:n])
    except Exception as e:
        return f"head: {e}"

def cmd_tail(cwd: Path, args: list[str]) -> str:
    n, files = 10, []
    i = 0
    while i < len(args):
        if args[i] == "-n" and i + 1 < len(args):
            n = int(args[i+1]); i += 2
        else:
            files.append(args[i]); i += 1
    if not files:
        return "tail: missing file operand"
    p = Path(files[0]).expanduser()
    if not p.is_absolute(): p = cwd / p
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[-n:])
    except Exception as e:
        return f"tail: {e}"

def cmd_mkdir(cwd: Path, args: list[str]) -> str:
    if not args:
        return "mkdir: missing operand"
    results = []
    for a in args:
        p = Path(a).expanduser()
        if not p.is_absolute(): p = cwd / p
        try:
            p.mkdir(parents=True, exist_ok=True)
            results.append(f"✅ Created: {p}")
        except Exception as e:
            results.append(f"❌ {a}: {e}")
    return "\n".join(results)

def cmd_rm(cwd: Path, args: list[str]) -> str:
    if not args:
        return "rm: missing operand"
    recursive = "-r" in args or "-rf" in args or "-fr" in args
    targets = [a for a in args if not a.startswith("-")]
    results = []
    for a in targets:
        p = Path(a).expanduser()
        if not p.is_absolute(): p = cwd / p
        try:
            if p.is_dir():
                if recursive:
                    shutil.rmtree(p)
                    results.append(f"✅ Removed dir: {p}")
                else:
                    results.append(f"rm: {a}: Is a directory (use -r)")
            else:
                p.unlink()
                results.append(f"✅ Removed: {p}")
        except Exception as e:
            results.append(f"❌ {a}: {e}")
    return "\n".join(results)

def cmd_mv(cwd: Path, args: list[str]) -> str:
    if len(args) < 2:
        return "mv: missing operand"
    src = Path(args[0]).expanduser()
    dst = Path(args[1]).expanduser()
    if not src.is_absolute(): src = cwd / src
    if not dst.is_absolute(): dst = cwd / dst
    try:
        shutil.move(str(src), str(dst))
        return f"✅ Moved: {src} → {dst}"
    except Exception as e:
        return f"❌ mv: {e}"

def cmd_cp(cwd: Path, args: list[str]) -> str:
    if len(args) < 2:
        return "cp: missing operand"
    src = Path(args[0]).expanduser()
    dst = Path(args[1]).expanduser()
    if not src.is_absolute(): src = cwd / src
    if not dst.is_absolute(): dst = cwd / dst
    try:
        if src.is_dir():
            shutil.copytree(str(src), str(dst))
        else:
            shutil.copy2(str(src), str(dst))
        return f"✅ Copied: {src} → {dst}"
    except Exception as e:
        return f"❌ cp: {e}"

def cmd_touch(cwd: Path, args: list[str]) -> str:
    if not args:
        return "touch: missing operand"
    results = []
    for a in args:
        p = Path(a).expanduser()
        if not p.is_absolute(): p = cwd / p
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch(exist_ok=True)
            results.append(f"✅ {p}")
        except Exception as e:
            results.append(f"❌ {a}: {e}")
    return "\n".join(results)

def cmd_tree(cwd: Path, args: list[str], depth: int = 2) -> str:
    target = Path(args[0]).expanduser() if args else cwd
    if not target.is_absolute(): target = cwd / target
    lines = [str(target)]
    def _walk(path: Path, prefix: str, current_depth: int):
        if current_depth > depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
        except PermissionError:
            return
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + entry.name + ("/" if entry.is_dir() else ""))
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                _walk(entry, prefix + extension, current_depth + 1)
    _walk(target, "", 1)
    return "\n".join(lines)

def cmd_env(cwd: Path, args: list[str]) -> str:
    env = os.environ
    if args:
        val = env.get(args[0], f"(not set)")
        return f"{args[0]}={val}"
    pairs = [f"{k}={v}" for k, v in list(env.items())[:30]]
    return "\n".join(pairs) + (f"\n... (+{len(env)-30} more)" if len(env) > 30 else "")

def cmd_whoami(_cwd, _args) -> str:
    return os.getenv("USERNAME") or os.getenv("USER") or "unknown"

def cmd_hostname(_cwd, _args) -> str:
    return socket.gethostname()

def cmd_echo(_cwd, args: list[str]) -> str:
    return " ".join(args)

HELP_TEXT = """🐧 *Wexxy Shell — Available Commands*

`ls [-la] [path]`  — list directory
`cd <path>`        — change directory  
`pwd`              — print working directory
`cat <file>`       — read file contents
`head [-n N] <f>`  — first N lines
`tail [-n N] <f>`  — last N lines
`mkdir <dir>`      — create directory
`rm [-r] <path>`   — remove file/dir
`mv <src> <dst>`   — move/rename
`cp <src> <dst>`   — copy
`touch <file>`     — create empty file
`tree [path]`      — directory tree (2 levels)
`echo <text>`      — print text
`env [VAR]`        — environment variables
`whoami`           — current user
`hostname`         — machine name
`help`             — show this menu

Usage: `/sh <command>`
Example: `/sh ls -la ~/Documents`"""

# ── Main Handler ──────────────────────────────────────────────────────────────

async def handle_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    cwd = _cwd(chat_id)

    if not context.args:
        prompt = f"$ {cwd}\nUsage: /sh <command>\nType `/sh help` for all commands."
        await update.message.reply_text(prompt, parse_mode="Markdown")
        return

    cmd = context.args[0].lower()
    args = context.args[1:]
    output = ""

    try:
        if cmd == "help":
            await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")
            return
        elif cmd == "ls" or cmd == "dir":
            output = cmd_ls(cwd, args)
        elif cmd == "cd":
            output, new_cwd = cmd_cd(cwd, args, chat_id)
            _set_cwd(chat_id, new_cwd)
        elif cmd == "pwd":
            output = cmd_pwd(cwd, args)
        elif cmd == "cat":
            output = cmd_cat(cwd, args)
        elif cmd == "head":
            output = cmd_head(cwd, args)
        elif cmd == "tail":
            output = cmd_tail(cwd, args)
        elif cmd == "mkdir":
            output = cmd_mkdir(cwd, args)
        elif cmd == "rm":
            output = cmd_rm(cwd, args)
        elif cmd == "mv":
            output = cmd_mv(cwd, args)
        elif cmd == "cp":
            output = cmd_cp(cwd, args)
        elif cmd == "touch":
            output = cmd_touch(cwd, args)
        elif cmd == "tree":
            output = cmd_tree(cwd, args)
        elif cmd == "echo":
            output = cmd_echo(cwd, args)
        elif cmd == "env":
            output = cmd_env(cwd, args)
        elif cmd == "whoami":
            output = cmd_whoami(cwd, args)
        elif cmd == "hostname":
            output = cmd_hostname(cwd, args)
        elif cmd in ("clear", "cls"):
            output = "🧹 (Shell state cleared)"
            _set_cwd(chat_id, Path.home())
        else:
            output = f"sh: {cmd}: command not found\nType `/sh help` for available commands."
    except Exception as e:
        output = f"❌ Error: {e}"

    # Format: show prompt + output
    prompt_line = f"$ {_cwd(chat_id)}"
    full_cmd = " ".join(context.args)
    reply = f"`{prompt_line}`\n`> {full_cmd}`\n\n{_format_block(output)}"
    await update.message.reply_text(reply, parse_mode="Markdown")


PLUGIN = {
    "name": "Shell",
    "command": "sh",
    "description": "Linux-like interactive shell (ls, cd, cat, mkdir, rm...)",
    "handler": handle_shell,
    "row": 5,
}
