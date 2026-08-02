# AGENTS.md Snippet

Use this in shared or machine-local `AGENTS.md` files when you want agents to consult MasterIndex before cross-project work.

```md
## MasterIndex Bootstrap

Before doing portfolio-wide or cross-project work:

1. Read the canonical MasterIndex inventory:
   - `current/index.json`
2. Read the task registry if recurring or operational work is involved:
   - `tasks/index.json`
3. Use `entities[].id` as the canonical target keys.
4. Treat the web page as presentation only; do not use it as the source of truth.
5. If a verified external public link exists for an entry, preserve it in the entry's `links` object.
6. Default to most recently modified entries first unless there is a better explicit sort for the task.

When updating MasterIndex:

- update `current/index.json` first
- update `current/inventory.md` second if narrative needs to change
- do not silently rewrite `tasks/index.json` during a normal inventory refresh
```
