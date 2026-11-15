# Terminal Project Monitor

Run the local, read-only status display from the MasterIndex checkout:

```sh
python3 tools/project_monitor.py --interactive
```

It lists the important portfolio entities one per line with their recorded
kind/status, local Git worktree state, active task count, recorded update date,
and your comment. It does not fetch, pull, push, deploy, or call external
systems. Use `--all` to include retired and reference records; use `--no-local`
for a fast display without Git checks.

In interactive mode, type either a line number plus your note or `c` plus a
line number and note:

```text
monitor> 4 finish the iPad screenshots before the next build
monitor> e 4
monitor> x 4
```

`e` opens an edit prompt and `x` clears that comment. You can also save a note
from a one-off terminal command:

```sh
python3 tools/project_monitor.py --comment qross-app "Review landscape build"
```

## Focus and open sessions

The index records what each project *is*; the Focus column records where your
attention is. Set it with `f`:

```text
monitor> f 4 now        # one of the few things you are actively working on
monitor> f 9 maint      # live and quiet: touch it only when something breaks
monitor> f 12 parked    # deliberately not now
monitor> f 4 none       # clear
```

`now` projects sort to the top, then unsorted ones, then `maint`, then
`parked`. The header counts your `now` projects and says so when there are more
than six. From a shell: `project-monitor --focus qross-app now`.

On a terminal the display is coloured: `now` in bold green, `maint` in blue,
`parked` rows dimmed, a project with no focus yet in yellow, open agent
sessions in cyan, a dirty working tree in yellow and a missing repo in red.
Set `NO_COLOR=1` to turn colour off; piped output is always plain.

`p 4` pins a project to the top of its focus tier (shown as `now*`); `p 4`
again unpins it. From a shell: `project-monitor --pin masterindex`.

The Agent column shows which projects have a Claude Code or Codex terminal
session open right now (from `tools/agent_sessions.py`; see
`docs/agent-session-restore.md`).

`project-monitor` in `~/bin` is a symlink to `tools/project_monitor.py`.

Comments and focus live in `current/project-comments.json`. They are owner-entered
annotations, deliberately separate from verified facts in `current/index.json`,
and are never treated as source evidence by a refresh agent.

## The published list

The same list is published as JSON for other displays, starting with the iOS
app workin On:

`https://billdonner.github.io/masterindex/current/monitor.json`

The site workflow builds it on every push with
`tools/project_monitor.py --export`, so it always matches the index and your
ledger. It leaves out the two columns that are facts about this Mac (Git state
and open agent sessions). The file is public, like the rest of this repository,
so your focus tiers and comments are publicly readable.

So that the phone sees your edits, the monitor commits and pushes
`current/project-comments.json` by itself: when you quit the interactive
monitor, and after each `--comment`, `--focus` or `--pin` command. Add
`--no-publish` to keep a change local.

The iOS app can edit the same ledger: it commits through GitHub. The monitor
pulls those edits when it starts, on `r`, and before each edit command.
