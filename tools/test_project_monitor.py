"""Non-destructive checks for the terminal monitor and its comment ledger."""

import importlib.util
import json
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("project_monitor.py")
SPEC = importlib.util.spec_from_file_location("project_monitor", MODULE_PATH)
monitor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(monitor)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        write(root / "current" / "index.json", {"generatedAt": "2026-01-01", "entities": [
            {"id": "active-app", "name": "Active App", "kind": "app", "status": "active", "lastModified": "2026-01-01", "repo": None},
            {"id": "retired-app", "name": "Retired App", "kind": "app", "status": "retired", "lastModified": "2025-01-01", "repo": None}
        ]})
        write(root / "tasks" / "index.json", {"entryTasks": {"active-app": [{"status": "active"}]}})
        write(root / "current" / "handoffs" / "index.json", {"directives": [{"status": "active", "targets": ["active"]}]})
        monitor.set_comment(root, "active-app", "Check screenshots")
        rows, _ = monitor.build_rows(root, include_all=False, inspect_local=False)
        assert len(rows) == 1 and rows[0]["comment"] == "Check screenshots" and rows[0]["work"] == "1 task H"
        rows, _ = monitor.build_rows(root, include_all=True, inspect_local=False)
        assert len(rows) == 2
        # Focus is kept when the comment is cleared, and "now" sorts ahead of newer unfocused work.
        monitor.set_focus(root, "retired-app", "now")
        monitor.set_focus(root, "active-app", "parked")
        monitor.set_comment(root, "active-app", "")
        comments = monitor.load_comments(root)
        assert monitor.comment_text(comments, "active-app") == "" and monitor.focus_of(comments, "active-app") == "parked"
        rows, _ = monitor.build_rows(root, include_all=True, inspect_local=False)
        assert [row["id"] for row in rows] == ["retired-app", "active-app"]
        # A pin lifts a project to the top of its own tier only, and toggles off again.
        monitor.set_focus(root, "active-app", "now")
        assert monitor.toggle_pin(root, "active-app") is True
        rows, _ = monitor.build_rows(root, include_all=True, inspect_local=False)
        assert [row["id"] for row in rows] == ["active-app", "retired-app"] and rows[0]["pin"]
        assert monitor.toggle_pin(root, "active-app") is False
        # The exported feed carries the same order and owner fields, and only real links.
        index_path = root / "current" / "index.json"
        index = json.loads(index_path.read_text())
        index["entities"][0].update({"links": {"appStore": "https://example.com/app", "website": None}, "notes": ["newest", "older"]})
        write(index_path, index)
        feed = monitor.export_feed(root)
        first = feed["projects"][0]
        assert [project["id"] for project in feed["projects"]] == ["active-app"] and feed["nowLimit"] == monitor.NOW_LIMIT
        # Outside a Git checkout there is nowhere to save edits, and the feed says so.
        assert feed["name"] == "MasterIndex" and feed["ledger"] is None and monitor.export_feed(root, "Staging")["name"] == "Staging"
        assert first["focus"] == "now" and first["pinned"] is False and first["activeTasks"] == 1
        assert first["links"] == {"appStore": "https://example.com/app"} and first["latestNote"] == "newest"
        # Optional extras: who has a session open, and ideas waiting in the intake registry.
        assert first["sessions"] == [] and feed["ideas"] == [] and feed["intake"] is None and feed["sessionsObservedAt"] is None
        write(root / "current" / "sessions.json", {"generatedAt": "2026-01-02T03:04:05-0600", "host": "Mac",
              "sessions": [{"entityId": "active-app", "agent": "claude", "name": "APP"}, {"entityId": "gone", "agent": "codex", "name": ""}]})
        write(root / "intake" / "index.json", {"inbox": [{"name": "Phone Idea", "purpose": "typed on the phone", "kind": "app", "submittedAt": "t1"},
                                                          {"name": "Dup", "purpose": "p", "rejected": "name is taken"}],
              "projects": [{"name": "Captured", "purpose": "p", "state": "captured", "createdAt": "t0"}, {"name": "Made", "state": "provisioned"}]})
        feed = monitor.export_feed(root)
        assert feed["projects"][0]["sessions"] == [{"agent": "claude", "name": "APP"}] and feed["sessionsHost"] == "Mac"
        assert [(idea["name"], idea["state"]) for idea in feed["ideas"]] == [("Phone Idea", "sent"), ("Dup", "rejected"), ("Captured", "captured")]
        monitor.set_focus(root, "active-app", "none")
        assert "active-app" not in monitor.load_comments(root)["comments"]
        try:
            monitor.set_focus(root, "active-app", "urgent")
            raise AssertionError("an unknown focus tier must be rejected")
        except ValueError:
            pass
        # An open agent session is matched to its project by directory, ignoring case.
        open_sessions = monitor.sessions_by_repo([
            {"agent": "codex", "cwd": str(Path.home() / "Demo")}, {"agent": "claude", "cwd": str(Path.home() / "demo")}])
        assert monitor.open_session("~/demo", open_sessions) == "claude+codex"
        assert monitor.open_session("~/other", open_sessions) == "" and monitor.open_session(None, open_sessions) == ""
    # Colour wraps an already-padded cell and is a no-op when disabled.
    assert monitor.paint("now   ", "bold green", True) == "\033[1;38;5;46mnow   \033[0m"
    assert monitor.paint("now   ", "bold green", False) == "now   " and monitor.paint("x", "", True) == "x"
    assert monitor.local_style("main dirty") == "yellow" and monitor.local_style("missing") == "red" and monitor.local_style("main clean") == ""
    print("Project monitor tests passed")


if __name__ == "__main__":
    main()
