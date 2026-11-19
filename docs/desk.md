# desk: the monitoring displays as one set

`desk` (`tools/desk.py`, symlinked at `~/bin/desk`) starts, stops and checks the
displays Bill watches, so they come up and go away together.

```
desk                 what is running
desk up              open everything that is not already open
desk up --sessions   also reopen the agent sessions lost in the last reboot
desk down            close what `up` opens
desk up flywall      one display by id (same for `down` and `status`)
desk install         open the displays at every login
desk uninstall       stop doing that
```

## The set

The list is `tools/desk.json`; add or remove a display by editing it. Another list
can be used with `--config FILE`.

| id | Display | Kind | What `up` does | What `down` does |
|---|---|---|---|---|
| projects | `project-monitor --interactive` | terminal | Opens a Ghostty tab | Ends it; the tab closes |
| picklefamilia | `pf-monitor` | terminal | Opens a Ghostty tab | Ends it; the tab closes |
| flywall | Local flywall board, 127.0.0.1:8765 | service | Starts `server.py`, opens the page | Stops the server |
| systrix | `~/Applications/Systrix.app` | app | Opens the app | Quits it |
| feedback | App Feedback dashboard, 127.0.0.1:4317 | page | Opens the page | Nothing: launchd runs that server |

All five are kept on purpose (owner decision, 2026-11-19), although Systrix
overlaps pf-monitor and flywall: the older two show their subject more concisely.

## Things to know

- `up` never opens a second copy of something already running.
- `down` does not close browser pages; close those by hand.
- `down` ends `project-monitor` without its quit step, so owner edits made in that
  run are saved locally but pushed only the next time the monitor is quit normally
  or an edit is made from the command line.
- Ghostty starts a tab's command only once the tab is drawn. While the screen is
  locked, `up` reports "it starts when the screen is unlocked". The same applies to
  `agent-sessions restore`.
- A service's output goes to `~/Library/Logs/desk/<id>.log`; login runs log to
  `~/Library/Logs/desk/login.log`.
- Background jobs (session snapshots, feedback collection, Product Authority) are
  launchd agents and are not part of the set; they already start at login. Systrix
  Core runs on Fly.

Tests: `python3 tools/test_desk.py`.
