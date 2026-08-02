# Housekeeping Task Template

Use this as a starting prompt for recurring or agentic tasks that depend on MasterIndex.

```text
Before acting, read the canonical MasterIndex files:

- current/index.json
- tasks/index.json

Use `entities[].id` as canonical target keys.
Prefer most recently modified entries first unless the task says otherwise.
Treat the web page as presentation only.
If verified external public links exist, preserve them in the entry `links` object.

Task target:
- entity id: <target-entity-id>

Task type:
- <release-check | link-check | health-check | metadata-refresh | report>

Required behavior:
1. Locate the target entry by id.
2. Verify the relevant facts.
3. Update `current/index.json` first if facts changed.
4. Update `current/inventory.md` only if the narrative also needs to change.
5. Leave `tasks/index.json` alone unless the task definition itself must change.
6. Report any gaps, blocked access, or ambiguities explicitly.
```
