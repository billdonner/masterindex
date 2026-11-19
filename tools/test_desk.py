#!/usr/bin/env python3
"""Tests for desk.py. Run: python3 tools/test_desk.py"""
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import desk  # noqa: E402

PORT = 8797


class DeskTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.logs = mock.patch.object(desk, "LOGS", Path(self.directory.name) / "logs")
        self.logs.start()
        self.addCleanup(self.logs.stop)

    def config(self, displays):
        path = Path(self.directory.name) / "desk.json"
        path.write_text(json.dumps({"displays": displays}))
        return path

    def test_shipped_list_loads_and_keeps_every_display(self):
        ids = [display["id"] for display in desk.load_displays(desk.DEFAULT_CONFIG)]
        self.assertEqual(ids, ["projects", "picklefamilia", "flywall", "systrix", "feedback"])

    def test_unknown_kind_and_duplicate_id_are_refused(self):
        with self.assertRaises(SystemExit):
            desk.load_displays(self.config([{"id": "a", "kind": "window"}]))
        with self.assertRaises(SystemExit):
            desk.load_displays(self.config([{"id": "a", "kind": "page"}, {"id": "a", "kind": "page"}]))

    def test_choose_refuses_an_unknown_name(self):
        displays = [{"id": "a", "kind": "page"}, {"id": "b", "kind": "page"}]
        self.assertEqual(desk.choose(displays, ["b"]), [displays[1]])
        self.assertEqual(desk.choose(displays, []), displays)
        with self.assertRaises(SystemExit):
            desk.choose(displays, ["c"])

    def test_service_starts_once_and_stops(self):
        service = {"id": "svc", "title": "Service", "kind": "service", "port": PORT, "url": f"http://127.0.0.1:{PORT}",
                   "command": f"{sys.executable} -m http.server {PORT} --bind 127.0.0.1", "cwd": self.directory.name}
        self.addCleanup(desk.bring_down, [service])
        self.assertEqual(desk.bring_up([service], open_pages=False), [("Service", "started")])
        first = desk.pids_listening(PORT)
        self.assertEqual(len(first), 1)
        self.assertEqual(desk.bring_up([service], open_pages=False), [("Service", "already running")])
        self.assertEqual(desk.pids_listening(PORT), first)
        self.assertEqual(desk.status_rows([service])[0][2], "up")
        self.assertEqual(desk.bring_down([service]), [("Service", "stopped")])
        deadline = time.time() + 5
        while time.time() < deadline and desk.pids_listening(PORT):
            time.sleep(0.1)
        self.assertEqual(desk.pids_listening(PORT), [])
        self.assertEqual(desk.bring_down([service]), [("Service", "was not open")])

    def test_terminal_is_found_by_its_command_and_closed(self):
        process = subprocess.Popen(["sleep", "98764"])
        self.addCleanup(process.kill)
        terminal = {"id": "t", "title": "Terminal", "kind": "terminal", "command": "sleep 98764", "match": "^sleep 98764$"}
        with mock.patch.object(desk.agent_sessions, "open_in_ghostty") as opened:
            self.assertEqual(desk.bring_up([terminal]), [("Terminal", "already open")])
            opened.assert_not_called()
        self.assertEqual(desk.bring_down([terminal]), [("Terminal", "closed")])
        self.assertIsNotNone(process.wait(timeout=5))

    def test_terminal_opens_a_tab_that_execs_the_command(self):
        terminal = {"id": "t", "title": "Terminal", "kind": "terminal", "command": "sleep 98765", "match": "^sleep 98765$", "cwd": "/tmp"}
        with mock.patch.object(desk.agent_sessions, "open_in_ghostty", return_value=True) as opened, \
                mock.patch.object(desk, "screen_locked", return_value=True), \
                mock.patch.object(desk, "confirm_started", wraps=lambda t, o, d: desk.__dict__["_real_confirm"](t, o, d, wait=0.1)):
            report = desk.bring_up([terminal])
        opened.assert_called_once_with([("/tmp", "exec sleep 98765")])
        self.assertEqual(report, [("Terminal", "tab opened; it starts when the screen is unlocked")])

    def test_page_served_by_something_else_is_never_stopped(self):
        page = {"id": "p", "title": "Page", "kind": "page", "port": PORT + 1, "url": "http://127.0.0.1"}
        self.assertEqual(desk.bring_up([page], open_pages=False), [("Page", f"NOT running: nothing is listening on port {PORT + 1}")])
        self.assertEqual(desk.bring_down([page]), [("Page", "left running (not started by desk)")])


desk.__dict__["_real_confirm"] = desk.confirm_started

if __name__ == "__main__":
    unittest.main()
