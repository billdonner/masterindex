#!/usr/bin/env python3
"""Track open coding-agent terminal sessions and reopen them after a reboot.

Each agent (Claude Code, Codex) is one adapter: how to find its live sessions
and how to resume one. `snapshot` records what is open (launchd runs it every
minute), `restore` reopens the sessions that were open when they last died.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import plistlib
import shlex
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

HOME = Path.home()
LEDGER = HOME / ".local" / "state" / "agent-sessions" / "ledger.json"
LAUNCH_LABEL = "com.billdonner.agent-sessions"
LAUNCH_PLIST = HOME / "Library" / "LaunchAgents" / f"{LAUNCH_LABEL}.plist"
BATCH_WINDOW = 600          # sessions last seen within 10 min of each other died together
KEEP_SECONDS = 7 * 86400    # forget closed sessions after a week
RECAP = "We were interrupted by a restart. In three lines: what were we doing, what state is it in, and what is the next step?"


def run(command: list[str]) -> str:
    try:
        return subprocess.run(command, text=True, capture_output=True, timeout=10, check=False).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def processes() -> list[dict[str, Any]]:
    rows = []
    for line in run(["ps", "-axo", "pid=,ppid=,tty=,comm="]).splitlines():
        parts = line.split(None, 3)
        if len(parts) == 4:
            rows.append({"pid": int(parts[0]), "ppid": int(parts[1]), "tty": parts[2], "name": os.path.basename(parts[3])})
    return rows


def process_cwd(pid: int) -> str:
    for line in run(["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"]).splitlines():
        if line.startswith("n"):
            return line[1:]
    return ""


# ── Claude Code ──────────────────────────────────────────────────────────────

def claude_last_prompt(home: Path, session_id: str) -> str:
    for path in glob.glob(str(home / ".claude" / "projects" / "*" / f"{session_id}.jsonl")):
        with open(path, "rb") as handle:
            handle.seek(max(os.path.getsize(path) - 400_000, 0))
            for line in reversed(handle.read().splitlines()):
                if b'"type":"last-prompt"' in line:
                    try:
                        return str(json.loads(line).get("lastPrompt", ""))
                    except ValueError:
                        continue
    return ""


def claude_live(home: Path, procs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Claude Code keeps one record per running process in ~/.claude/sessions/<pid>.json."""
    alive = {proc["pid"]: proc for proc in procs if proc["name"] == "claude"}
    sessions = []
    for path in glob.glob(str(home / ".claude" / "sessions" / "*.json")):
        try:
            record = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        proc = alive.get(record.get("pid"))
        if not proc or record.get("kind") != "interactive" or not record.get("sessionId"):
            continue
        sessions.append({
            "agent": "claude", "sessionId": record["sessionId"], "cwd": record.get("cwd", ""),
            "name": record.get("name", ""), "status": record.get("status", ""), "tty": proc["tty"],
            "lastPrompt": claude_last_prompt(home, record["sessionId"]),
        })
    return sessions


# ── Codex ────────────────────────────────────────────────────────────────────

def codex_threads(home: Path, cwd: str, limit: int) -> list[dict[str, Any]]:
    """Newest user-facing Codex threads for a directory, from Codex's own state database."""
    databases = sorted(glob.glob(str(home / ".codex" / "state_*.sqlite")))
    if not databases:
        return []
    try:
        connection = sqlite3.connect(f"file:{databases[-1]}?mode=ro", uri=True, timeout=2)
        rows = connection.execute(
            "select id, coalesce(name, ''), preview from threads where cwd = ? and archived = 0 "
            "and has_user_event = 1 and source not like '{%' and source != 'exec' "
            "order by updated_at desc limit ?", (cwd, limit)).fetchall()
        connection.close()
    except sqlite3.Error:
        return []
    return [{"sessionId": row[0], "name": row[1], "lastPrompt": row[2] or ""} for row in rows]


def codex_live(home: Path, procs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A Codex terminal process does not say which thread it holds, so pair each
    one with the most recently updated thread recorded for its directory."""
    names = {proc["pid"]: proc["name"] for proc in procs}
    by_cwd: dict[str, list[dict[str, Any]]] = {}
    for proc in procs:
        if proc["name"] == "codex" and proc["tty"] != "??" and names.get(proc["ppid"]) != "codex":
            cwd = process_cwd(proc["pid"])
            if cwd:
                by_cwd.setdefault(cwd, []).append(proc)
    sessions = []
    for cwd, owners in by_cwd.items():
        for proc, thread in zip(owners, codex_threads(home, cwd, len(owners))):
            sessions.append({"agent": "codex", "cwd": cwd, "status": "", "tty": proc["tty"], **thread})
    return sessions


# One entry per agent: how to find live sessions, how to resume one. Add agents here.
ADAPTERS: dict[str, dict[str, Callable[..., Any]]] = {
    "claude": {"live": claude_live, "resume": lambda session_id: ["claude", "--resume", session_id]},
    "codex": {"live": codex_live, "resume": lambda session_id: ["codex", "resume", session_id]},
}


def live_sessions(home: Path = HOME) -> list[dict[str, Any]]:
    procs = processes()
    sessions = [session for adapter in ADAPTERS.values() for session in adapter["live"](home, procs)]
    return sorted(sessions, key=lambda session: (session["cwd"], session["agent"]))


def key(session: dict[str, Any]) -> str:
    return f"{session['agent']}:{session['sessionId']}"


def resume_command(session: dict[str, Any], recap: bool = False) -> str:
    command = ADAPTERS[session["agent"]]["resume"](session["sessionId"])
    return shlex.join(command + ([RECAP] if recap else []))


# ── Ledger ───────────────────────────────────────────────────────────────────

def load_ledger(path: Path = LEDGER) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"sessions": {}}


def save_ledger(ledger: dict[str, Any], path: Path = LEDGER) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def record_snapshot(ledger: dict[str, Any], live: list[dict[str, Any]], moment: float) -> dict[str, Any]:
    sessions = ledger.setdefault("sessions", {})
    for session in live:
        kept = {field: session[field] for field in ("agent", "sessionId", "cwd", "name", "lastPrompt")}
        sessions[key(session)] = {**kept, "lastSeen": moment}
    for stale in [name for name, entry in sessions.items() if moment - entry["lastSeen"] > KEEP_SECONDS]:
        del sessions[stale]
    return ledger


def restore_candidates(ledger: dict[str, Any], live: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The sessions that died together most recently and are not running now.

    A shutdown kills sessions over a few seconds, so "together" is a window,
    not one instant; a session closed on purpose earlier falls outside it.
    """
    running = {key(session) for session in live}
    closed = [entry for name, entry in ledger.get("sessions", {}).items() if name not in running]
    if not closed:
        return []
    newest = max(entry["lastSeen"] for entry in closed)
    batch = [entry for entry in closed if newest - entry["lastSeen"] <= BATCH_WINDOW]
    return sorted(batch, key=lambda entry: (entry["cwd"], entry["agent"]))


# ── Terminal ─────────────────────────────────────────────────────────────────

GHOSTTY_SCRIPT = """
on run argv
    tell application "Ghostty"
        activate
        repeat with i from 1 to (count of argv) by 2
            set cfg to new surface configuration
            set initial working directory of cfg to item i of argv
            set initial input of cfg to (item (i + 1) of argv) & linefeed
            if (count of windows) is 0 then
                new window with configuration cfg
            else
                new tab in window 1 with configuration cfg
            end if
        end repeat
    end tell
end run
"""


def open_in_ghostty(tabs: list[tuple[str, str]]) -> bool:
    arguments = [value for tab in tabs for value in tab]
    result = subprocess.run(["osascript", "-e", GHOSTTY_SCRIPT, *arguments], text=True, capture_output=True, check=False)
    if result.returncode:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode == 0


# ── Commands ─────────────────────────────────────────────────────────────────

def short(path: str) -> str:
    return "~" + path[len(str(HOME)):] if path.startswith(str(HOME)) else path


def print_table(sessions: list[dict[str, Any]], numbered: bool = False) -> None:
    for number, session in enumerate(sessions, start=1):
        prompt = " ".join(session.get("lastPrompt", "").split())
        prefix = f"{number:>2}  " if numbered else ""
        print(f"{prefix}{session['agent']:<7} {short(session['cwd']):<28.28} {session.get('name', ''):<22.22} {prompt[:70]}")


def command_list(arguments: argparse.Namespace) -> None:
    live = live_sessions()
    if arguments.json:
        print(json.dumps(live, indent=2, ensure_ascii=False))
    elif live:
        print_table(live)
    else:
        print("No agent sessions are open.")


def command_snapshot(_: argparse.Namespace) -> None:
    save_ledger(record_snapshot(load_ledger(), live_sessions(), time.time()))


def command_restore(arguments: argparse.Namespace) -> None:
    ledger = load_ledger()
    candidates = restore_candidates(ledger, live_sessions())
    if not candidates:
        print("Nothing to restore: every recorded session is already open.")
        return
    age = int((time.time() - max(entry["lastSeen"] for entry in candidates)) / 60)
    print(f"{len(candidates)} session(s) were open until about {age} min ago and are not running now:\n")
    print_table(candidates, numbered=True)
    if arguments.dry_run:
        return
    chosen = candidates
    if not arguments.yes:
        answer = input("\nReopen all? [Y] yes · numbers to pick (e.g. 1 3) · n to cancel: ").strip().lower()
        if answer in {"n", "no", "q"}:
            return
        if answer not in {"", "y", "yes"}:
            picks = {int(token) for token in answer.replace(",", " ").split() if token.isdigit()}
            chosen = [entry for number, entry in enumerate(candidates, start=1) if number in picks]
    missing = [entry for entry in chosen if not Path(entry["cwd"]).is_dir()]
    for entry in missing:
        print(f"Skipping {short(entry['cwd'])}: the folder no longer exists.")
    tabs = [(entry["cwd"], resume_command(entry, arguments.recap)) for entry in chosen if entry not in missing]
    if arguments.print or not Path("/Applications/Ghostty.app").exists():
        for cwd, command in tabs:
            print(f"cd {shlex.quote(cwd)} && {command}")
    elif tabs and not open_in_ghostty(tabs):
        sys.exit("Ghostty did not open the tabs; rerun with --print to get the commands.")
    else:
        print(f"Opened {len(tabs)} tab(s).")
    # The batch has been dealt with: reopened sessions are recorded again by the next snapshot.
    for entry in candidates:
        ledger["sessions"].pop(key(entry), None)
    save_ledger(ledger)


def command_install(_: argparse.Namespace) -> None:
    script = str(Path(__file__).resolve())
    LAUNCH_PLIST.write_bytes(plistlib.dumps({
        "Label": LAUNCH_LABEL, "ProgramArguments": [shutil.which("python3") or sys.executable, script, "snapshot"],
        "StartInterval": 60, "RunAtLoad": True, "ProcessType": "Background",
        "StandardErrorPath": str(LEDGER.parent / "snapshot.err"),
    }))
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", f"{domain}/{LAUNCH_LABEL}"], capture_output=True, check=False)
    subprocess.run(["launchctl", "bootstrap", domain, str(LAUNCH_PLIST)], check=True)
    print(f"Snapshot agent installed ({LAUNCH_PLIST}); it records open sessions every 60 s.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command")
    listing = commands.add_parser("list", help="Show agent sessions that are open now (default).")
    listing.add_argument("--json", action="store_true")
    listing.set_defaults(handler=command_list)
    commands.add_parser("snapshot", help="Record the open sessions (run by launchd).").set_defaults(handler=command_snapshot)
    restore = commands.add_parser("restore", help="Reopen the sessions that were open when they last died.")
    restore.add_argument("--dry-run", action="store_true", help="Show what would be reopened and change nothing.")
    restore.add_argument("--yes", action="store_true", help="Reopen all without asking.")
    restore.add_argument("--print", action="store_true", help="Print the resume commands instead of opening tabs.")
    restore.add_argument("--recap", action="store_true", help="Ask each session for a three-line recap on resume (uses tokens).")
    restore.set_defaults(handler=command_restore)
    commands.add_parser("install", help="Install the launchd agent that snapshots every minute.").set_defaults(handler=command_install)
    arguments = parser.parse_args()
    if not arguments.command:
        arguments = parser.parse_args(["list"])
    arguments.handler(arguments)


if __name__ == "__main__":
    main()
