#!/usr/bin/env python3
"""Start, stop and check the monitoring displays as one set.

  desk                 show what is running (same as `desk status`)
  desk up [id ...]     open every display that is not already open
  desk up --sessions   also reopen the agent sessions lost in the last reboot
  desk down [id ...]   close what `up` opens
  desk install         run `desk up` at every login
  desk uninstall       stop doing that

The set is the list in desk.json beside this file (or --config FILE). Kinds:

  terminal  a command in its own Ghostty tab; `down` ends the command and the tab closes
  service   a local server this tool starts and stops, plus the page it serves
  app       a Mac app; `down` quits it
  page      a page served by something else (launchd); `up` opens it, `down` leaves it alone
"""
from __future__ import annotations

import argparse
import json
import os
import plistlib
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_sessions  # noqa: E402

HOME = Path.home()
DEFAULT_CONFIG = Path(__file__).resolve().with_name("desk.json")
LOGS = HOME / "Library/Logs/desk"
LAUNCH_LABEL = "com.billdonner.desk"
LAUNCH_PLIST = HOME / "Library/LaunchAgents" / f"{LAUNCH_LABEL}.plist"
KINDS = {"terminal", "service", "app", "page"}


def load_displays(path: Path) -> list[dict[str, Any]]:
    displays = json.loads(path.read_text())["displays"]
    seen: set[str] = set()
    for display in displays:
        if display.get("kind") not in KINDS:
            raise SystemExit(f"{path}: {display.get('id')!r} has unknown kind {display.get('kind')!r}")
        if display["id"] in seen:
            raise SystemExit(f"{path}: duplicate id {display['id']!r}")
        seen.add(display["id"])
    return displays


def choose(displays: list[dict[str, Any]], ids: list[str]) -> list[dict[str, Any]]:
    if not ids:
        return displays
    known = {display["id"] for display in displays}
    unknown = [name for name in ids if name not in known]
    if unknown:
        raise SystemExit(f"No display named {', '.join(unknown)}. Known: {', '.join(sorted(known))}")
    return [display for display in displays if display["id"] in ids]


def expand(path: str) -> str:
    return str(Path(path).expanduser())


# ── What is running ──────────────────────────────────────────────────────────

def pids_matching(pattern: str) -> list[int]:
    """Processes whose command line matches, never this tool or its parents."""
    result = subprocess.run(["pgrep", "-f", pattern], text=True, capture_output=True, check=False)
    mine = {os.getpid(), os.getppid()}
    return [int(pid) for pid in result.stdout.split() if int(pid) not in mine]


def pids_named(name: str) -> list[int]:
    result = subprocess.run(["pgrep", "-x", name], text=True, capture_output=True, check=False)
    return [int(pid) for pid in result.stdout.split()]


def pids_listening(port: int) -> list[int]:
    result = subprocess.run(["lsof", "-nP", "-t", f"-iTCP:{port}", "-sTCP:LISTEN"], text=True, capture_output=True, check=False)
    return sorted({int(pid) for pid in result.stdout.split()})


def pids_of(display: dict[str, Any]) -> list[int]:
    kind = display["kind"]
    if kind == "terminal":
        return pids_matching(display["match"])
    if kind == "app":
        return pids_named(display["process"])
    return pids_listening(display["port"])


# ── Up ───────────────────────────────────────────────────────────────────────

def start_service(display: dict[str, Any]) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(LOGS / f"{display['id']}.log", "ab") as log:
        subprocess.Popen(shlex.split(display["command"]), cwd=expand(display.get("cwd", "~")),
                         stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True)
    deadline = time.time() + 15
    while time.time() < deadline and not pids_listening(display["port"]):
        time.sleep(0.3)


def screen_locked() -> bool:
    result = subprocess.run(["ioreg", "-n", "Root", "-d1"], text=True, capture_output=True, check=False)
    return '"CGSSessionScreenIsLocked"=Yes' in result.stdout


def confirm_started(title: str, outcome: str, displays: list[dict[str, Any]], wait: float = 8.0) -> str:
    """Ghostty starts a tab's command only once the tab is drawn, which a locked screen prevents."""
    if outcome != "opened in a new tab":
        return outcome
    display = next(item for item in displays if item["title"] == title)
    deadline = time.time() + wait
    while time.time() < deadline:
        if pids_of(display):
            return outcome
        time.sleep(0.5)
    if screen_locked():
        return "tab opened; it starts when the screen is unlocked"
    return "tab opened, but the command has NOT started"


def bring_up(displays: list[dict[str, Any]], open_pages: bool = True) -> list[tuple[str, str]]:
    """Open what is not open. Returns (title, what happened) per display."""
    report: list[tuple[str, str]] = []
    tabs: list[tuple[str, str]] = []
    pages: list[str] = []
    for display in displays:
        kind, running = display["kind"], bool(pids_of(display))
        if kind == "terminal":
            if running:
                report.append((display["title"], "already open"))
            else:
                # exec, so ending the command later closes the tab with it.
                tabs.append((expand(display.get("cwd", "~")), "exec " + display["command"]))
                report.append((display["title"], "opened in a new tab"))
        elif kind == "app":
            if running:
                report.append((display["title"], "already open"))
            else:
                subprocess.run(["open", expand(display["path"])], check=False)
                report.append((display["title"], "opened"))
        elif kind == "service":
            if running:
                report.append((display["title"], "already running"))
            else:
                start_service(display)
                started = bool(pids_listening(display["port"]))
                report.append((display["title"], "started" if started else f"FAILED to start; see {LOGS / (display['id'] + '.log')}"))
                if started:
                    pages.append(display["url"])
        elif kind == "page":
            if running:
                pages.append(display["url"])
                report.append((display["title"], "page opened"))
            else:
                report.append((display["title"], f"NOT running: nothing is listening on port {display['port']}"))
    if tabs and not agent_sessions.open_in_ghostty(tabs):
        report.append(("Ghostty", "FAILED to open tabs"))
    elif tabs:
        report = [(title, confirm_started(title, outcome, displays)) for title, outcome in report]
    if open_pages:
        for url in pages:
            subprocess.run(["open", url], check=False)
    return report


# ── Down ─────────────────────────────────────────────────────────────────────

def bring_down(displays: list[dict[str, Any]]) -> list[tuple[str, str]]:
    report: list[tuple[str, str]] = []
    for display in displays:
        kind, pids = display["kind"], pids_of(display)
        if kind == "page":
            report.append((display["title"], "left running (not started by desk)"))
        elif not pids:
            report.append((display["title"], "was not open"))
        elif kind == "app":
            subprocess.run(["osascript", "-e", f'tell application "{display["process"]}" to quit'], capture_output=True, check=False)
            report.append((display["title"], "quit"))
        else:
            for pid in pids:
                try:
                    os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            report.append((display["title"], "closed" if kind == "terminal" else "stopped"))
    return report


# ── Status ───────────────────────────────────────────────────────────────────

def status_rows(displays: list[dict[str, Any]]) -> list[tuple[str, str, str, str]]:
    rows = []
    for display in displays:
        pids = pids_of(display)
        where = display.get("url") or display.get("command") or display.get("path", "")
        rows.append((display["id"], display["title"], "up" if pids else "down", where))
    return rows


def login_start_installed() -> bool:
    return LAUNCH_PLIST.exists()


def print_report(report: list[tuple[str, str]]) -> None:
    width = max(len(title) for title, _ in report)
    for title, outcome in report:
        print(f"  {title:<{width}}  {outcome}")


# ── Commands ─────────────────────────────────────────────────────────────────

def command_status(arguments: argparse.Namespace) -> None:
    rows = status_rows(choose(load_displays(arguments.config), arguments.ids))
    if arguments.json:
        print(json.dumps([dict(zip(("id", "title", "state", "where"), row)) for row in rows], indent=2))
        return
    for name, title, state, where in rows:
        colour = "\033[1;38;5;46m" if state == "up" else "\033[38;5;196m"
        print(f"  {colour}{state:<4}\033[0m  {name:<14} {title:<26} {where}")
    print(f"\n  Start at login: {'on' if login_start_installed() else 'off'}")


def command_up(arguments: argparse.Namespace) -> None:
    print_report(bring_up(choose(load_displays(arguments.config), arguments.ids), open_pages=not arguments.no_pages))
    if arguments.sessions:
        subprocess.run([sys.executable, agent_sessions.__file__, "restore", "--yes"], check=False)


def command_down(arguments: argparse.Namespace) -> None:
    print_report(bring_down(choose(load_displays(arguments.config), arguments.ids)))


def command_install(arguments: argparse.Namespace) -> None:
    program = [shutil.which("python3") or sys.executable, str(Path(__file__).resolve()), "--config", str(arguments.config.resolve()), "up"]
    LOGS.mkdir(parents=True, exist_ok=True)
    LAUNCH_PLIST.write_bytes(plistlib.dumps({
        "Label": LAUNCH_LABEL, "ProgramArguments": program, "RunAtLoad": True,
        "EnvironmentVariables": {"PATH": f"{HOME}/bin:{HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"},
        "StandardOutPath": str(LOGS / "login.log"), "StandardErrorPath": str(LOGS / "login.log"),
    }))
    print(f"Displays will open at every login ({LAUNCH_PLIST}). `desk uninstall` turns this off.")


def command_uninstall(_: argparse.Namespace) -> None:
    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{LAUNCH_LABEL}"], capture_output=True, check=False)
    LAUNCH_PLIST.unlink(missing_ok=True)
    print("Displays no longer open at login.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="The list of displays (default: desk.json beside this file).")
    commands = parser.add_subparsers(dest="command")
    status = commands.add_parser("status", help="Show what is running (default).")
    status.add_argument("ids", nargs="*")
    status.add_argument("--json", action="store_true")
    status.set_defaults(handler=command_status)
    up = commands.add_parser("up", help="Open every display that is not already open.")
    up.add_argument("ids", nargs="*")
    up.add_argument("--sessions", action="store_true", help="Also reopen the agent sessions lost in the last reboot.")
    up.add_argument("--no-pages", action="store_true", help="Start services but do not open browser pages.")
    up.set_defaults(handler=command_up)
    down = commands.add_parser("down", help="Close what `up` opens.")
    down.add_argument("ids", nargs="*")
    down.set_defaults(handler=command_down)
    commands.add_parser("install", help="Run `desk up` at every login.").set_defaults(handler=command_install)
    commands.add_parser("uninstall", help="Stop opening displays at login.").set_defaults(handler=command_uninstall)
    arguments = parser.parse_args()
    if not arguments.command:
        arguments = parser.parse_args(["--config", str(arguments.config), "status"])
    arguments.handler(arguments)


if __name__ == "__main__":
    main()
