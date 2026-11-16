"""Non-destructive checks for agent session tracking: detection, ledger, and restore selection."""

import importlib.util
import json
import sqlite3
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("agent_sessions.py")
SPEC = importlib.util.spec_from_file_location("agent_sessions", MODULE_PATH)
sessions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sessions)


def main():
    with tempfile.TemporaryDirectory() as directory:
        home = Path(directory)
        # Claude: one record per live process; a dead pid or a background session is ignored.
        records = home / ".claude" / "sessions"
        records.mkdir(parents=True)
        for pid, kind in ((11, "interactive"), (12, "interactive"), (13, "background")):
            (records / f"{pid}.json").write_text(json.dumps(
                {"pid": pid, "sessionId": f"claude-{pid}", "cwd": "/work/app", "name": "APP", "kind": kind, "status": "idle"}))
        transcript = home / ".claude" / "projects" / "-work-app"
        transcript.mkdir(parents=True)
        (transcript / "claude-11.jsonl").write_text(
            '{"type":"last-prompt","lastPrompt":"older"}\n{"type":"user"}\n{"type":"last-prompt","lastPrompt":"fix the build"}\n')
        procs = [{"pid": 11, "ppid": 1, "tty": "ttys001", "name": "claude"}, {"pid": 13, "ppid": 1, "tty": "ttys003", "name": "claude"}]
        live = sessions.claude_live(home, procs)
        assert [(s["sessionId"], s["lastPrompt"]) for s in live] == [("claude-11", "fix the build")]

        # Codex: newest user-facing threads for the directory; subagent, exec and archived threads are skipped.
        (home / ".codex").mkdir()
        database = sqlite3.connect(home / ".codex" / "state_5.sqlite")
        database.execute("create table threads (id, name, preview, cwd, archived, has_user_event, source, updated_at)")
        database.executemany("insert into threads values (?,?,?,?,?,?,?,?)", [
            ("old", "OLD", "p", "/work/app", 0, 1, "cli", 1), ("new", "NEW", "ship it", "/work/app", 0, 1, "cli", 5),
            ("sub", None, "p", "/work/app", 0, 1, '{"subagent":"review"}', 9), ("gone", None, "p", "/work/app", 1, 1, "cli", 9),
            ("exec", None, "p", "/work/app", 0, 1, "exec", 9), ("else", None, "p", "/work/other", 0, 1, "cli", 9)])
        database.commit(); database.close()
        assert [t["sessionId"] for t in sessions.codex_threads(home, "/work/app", 5)] == ["new", "old"]
        assert sessions.codex_threads(home, "/work/app", 1)[0] == {"sessionId": "new", "name": "NEW", "lastPrompt": "ship it"}

    def entry(agent, session_id, cwd="/work/app"):
        return {"agent": agent, "sessionId": session_id, "cwd": cwd, "name": "", "lastPrompt": ""}

    # Three sessions die in a shutdown a few seconds apart; one was closed on purpose an hour earlier.
    ledger = {"sessions": {}}
    sessions.record_snapshot(ledger, [entry("claude", "early")], 1000)
    everyone = [entry("claude", "a"), entry("codex", "b", "/work/b"), entry("claude", "c", "/work/c")]
    sessions.record_snapshot(ledger, everyone, 4600)
    sessions.record_snapshot(ledger, everyone[:2], 4660)      # "c" was killed first
    assert {e["sessionId"] for e in sessions.restore_candidates(ledger, [])} == {"a", "b", "c"}
    # A session that is running again is not offered.
    assert {e["sessionId"] for e in sessions.restore_candidates(ledger, [entry("codex", "b")])} == {"a", "c"}
    # Once everything is running, nothing is offered except the older deliberate close.
    assert [e["sessionId"] for e in sessions.restore_candidates(ledger, everyone)] == ["early"]
    # Closed sessions are forgotten after the retention period.
    sessions.record_snapshot(ledger, [], 1000 + sessions.KEEP_SECONDS + 1)
    assert "claude:early" not in ledger["sessions"] and "claude:a" in ledger["sessions"]

    # Only the project, the agent and the session's name are published; unindexed folders are left out.
    index = {"entities": [{"id": "app-one", "repo": "~/AppOne"}, {"id": "no-repo", "repo": None}, {"id": "remote", "repo": "github:x/y"}]}
    live = [{"agent": "codex", "cwd": str(Path.home() / "appone"), "name": "", "sessionId": "s1", "lastPrompt": "secret plan"},
            {"agent": "claude", "cwd": str(Path.home() / "AppOne"), "name": "ONE", "sessionId": "s2", "lastPrompt": "x"},
            {"agent": "claude", "cwd": str(Path.home() / "scratch"), "name": "SCRATCH", "sessionId": "s3", "lastPrompt": "x"}]
    assert sessions.sessions_by_project(index, live) == [
        {"entityId": "app-one", "agent": "claude", "name": "ONE"}, {"entityId": "app-one", "agent": "codex", "name": ""}]

    assert sessions.resume_command(entry("claude", "abc")) == "claude --resume abc"
    assert sessions.resume_command(entry("codex", "abc")) == "codex resume abc"
    assert sessions.resume_command(entry("codex", "abc"), recap=True).startswith("codex resume abc 'We were interrupted")
    print("Agent session tests passed")


if __name__ == "__main__":
    main()
