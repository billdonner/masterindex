# Staging index

A second, invented MasterIndex for testing and staging. Nothing in it is real.

It has the same layout as the real index at the repository root (`current/`,
`tasks/`), its own owner ledger, and its own published feed:

`https://billdonner.github.io/masterindex/staging/current/monitor.json`

Work on it with the same tool:

```sh
python3 tools/project_monitor.py --root staging --interactive
```

The iOS app can be pointed at that feed, and its tests are. Edits made there
are committed to `staging/current/project-comments.json`, never to the real
ledger.
