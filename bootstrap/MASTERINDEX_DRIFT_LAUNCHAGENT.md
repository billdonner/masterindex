# MasterIndex Drift LaunchAgent

`com.billdonner.masterindex.drift` is a safe macOS LaunchAgent for checking whether a local MasterIndex checkout has drifted from the shared contract or from `origin/main`.

## Safety Contract

The scheduled job runs `tools/masterindex-drift-check.sh` every six hours. It is intentionally read-only:

- validates `current/index.json`, `tasks/index.json`, and `current/handoffs/index.json`
- checks required top-level keys in `current/index.json`
- reports dirty working-tree state
- compares local `HEAD` with `origin/main` using `git ls-remote`
- writes only its installed checker copy and LaunchAgent logs under `~/Library/Application Support/MasterIndex` and `~/Library/Logs/MasterIndex`

It does not pull, rebase, commit, push, edit inventory files, or rewrite task definitions.

## Install

From the checkout that should be monitored:

```sh
bootstrap/install-masterindex-drift-launchagent.sh --check-now
```

To monitor a different checkout, pass its path:

```sh
bootstrap/install-masterindex-drift-launchagent.sh --check-now ~/masterindex
```

If the installer is running from one checkout but should monitor another, keep the checker source explicit:

```sh
bootstrap/install-masterindex-drift-launchagent.sh --check-now --source-root /path/to/main-checkout ~/masterindex
```

The installer writes:

- `~/Library/LaunchAgents/com.billdonner.masterindex.drift.plist`
- `~/Library/Application Support/MasterIndex/masterindex-drift-check.sh`
- `~/Library/Logs/MasterIndex/drift.out.log`
- `~/Library/Logs/MasterIndex/drift.err.log`

## Test Manually

Strict mode exits non-zero when drift or schema problems are detected:

```sh
tools/masterindex-drift-check.sh --strict ~/masterindex
```

LaunchAgent status:

```sh
launchctl print gui/$UID/com.billdonner.masterindex.drift
```

Recent output:

```sh
tail -50 ~/Library/Logs/MasterIndex/drift.out.log
tail -50 ~/Library/Logs/MasterIndex/drift.err.log
```

## Uninstall

```sh
bootstrap/install-masterindex-drift-launchagent.sh --unload
```
