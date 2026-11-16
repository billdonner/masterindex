# Agent Session Restore

Reopens your Claude Code and Codex terminal sessions after a reboot, a
terminal crash, or anything else that closes them all at once.

```sh
agent-sessions                    # what is open now
agent-sessions restore            # reopen what was open when it last died
agent-sessions restore --dry-run  # show the list, change nothing
```

`restore` lists the sessions, asks once (Return reopens all; type numbers to
pick some; `n` cancels), then opens one Ghostty tab per session in the right
folder and resumes the exact conversation. Nothing is sent to any model: each
session comes back idle with its history. Add `--recap` to have each one open
with a three-line "where were we" summary; that costs tokens in every session,
so it is off by default. The list itself shows each session's last prompt,
which is usually enough.

`--print` prints the `cd … && claude --resume …` lines instead of opening
tabs, for use in another terminal app.

## How it works

- A launchd agent (`com.billdonner.agent-sessions`) runs
  `agent-sessions snapshot` every 60 seconds and records the open sessions in
  `~/.local/state/agent-sessions/ledger.json`. This is machine-local state,
  not part of the index.
- `restore` offers the sessions that are not running now and were last seen
  within ten minutes of each other. A session you closed on purpose earlier
  falls outside that window and is not offered. After a restore the offered
  batch is cleared, whether or not you reopened all of it.
- Closed sessions are forgotten after seven days.

## Agents

Each agent is one entry in `ADAPTERS` in `tools/agent_sessions.py`: a function
that finds its live sessions and the command that resumes one.

| Agent | Live sessions found from | Resumed with |
|---|---|---|
| Claude Code | `~/.claude/sessions/<pid>.json` (exact session id) | `claude --resume <id>` |
| Codex | terminal `codex` processes, paired with the newest thread for that folder in `~/.codex/state_*.sqlite` | `codex resume <id>` |

Codex does not expose which thread a running process holds, so the pairing is
by folder and recency. It is exact for one Codex session per folder; with two
in the same folder it restores the two most recent threads there. A Codex
session with no prompt yet has no thread and is not recorded. Codex desktop-app
threads and Claude background sessions (`claude --bg`) are not tracked; this
covers interactive terminal sessions only.

## Install

```sh
ln -sf ~/masterindex/tools/agent_sessions.py ~/bin/agent-sessions
agent-sessions install     # writes and loads the launchd agent
```

Other agents can ask what is open with `agent-sessions list --json`, which is
the lookup the Session routing rule in `AGENTS.md` needs.

Tests: `python3 tools/test_agent_sessions.py`.

## Publishing open sessions

Every snapshot also publishes which indexed projects have a session open, so
other displays (the iOS app) can show it. Only three things are published per
session: the project, the agent, and the session's name. No prompts, folders
or session ids leave this Mac.

It writes `current/sessions.json` straight to GitHub with `gh api`, and only
when the set of open sessions has changed. It never touches the local
checkout, so it cannot disturb work in progress there; a `git pull` brings the
file in. `agent-sessions publish` does it on demand.
