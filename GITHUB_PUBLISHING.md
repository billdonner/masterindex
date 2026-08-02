# GitHub Publishing Contract

As of Sunday, August 2, 2026, this is the recommended GitHub sharing model for MasterIndex.

## Recommended repo

- Repository name: `masterindex` or `masterindex-hub`
- Default branch: `main`
- Put the contents of this folder at the repository root

## Canonical paths

- Core index: `current/index.json`
- Narrative companion: `current/inventory.md`
- Task registry: `tasks/index.json`
- Browser entry point: `site/index.html`

## Raw URL patterns

Replace `<owner>` and `<repo>` with your real GitHub owner and repo name.

### Core index

```text
https://raw.githubusercontent.com/<owner>/<repo>/main/current/index.json
```

### Narrative companion

```text
https://raw.githubusercontent.com/<owner>/<repo>/main/current/inventory.md
```

### Task registry

```text
https://raw.githubusercontent.com/<owner>/<repo>/main/tasks/index.json
```

### Entry task template

```text
https://raw.githubusercontent.com/<owner>/<repo>/main/tasks/templates/entry-task.template.json
```

## GitHub Pages pattern

If you publish `site/` through GitHub Pages, use one stable browser URL such as:

```text
https://<owner>.github.io/<repo>/
```

Recommended behavior:

- keep the site reading `../current/index.json` when served from the repo structure
- or rewrite the fetch path to `/current/index.json` if Pages is configured at the site root

## Recommended agent contract

For machines that can reach GitHub:

1. Fetch `current/index.json`
2. Optionally fetch `tasks/index.json`
3. Use `entities[].id` from `current/index.json` as the stable task target keys
4. Never infer entry ids from display names if the ids are available

## Public link expectation

When an entity has a verified external public link, include it in that entity's `links` object.

Examples:

- marketing website
- public service URL
- public App Store page
- other durable public landing page directly associated with the entity

## Suggested future split

When you later need non-GitHub access, keep the same file contract and mirror it elsewhere:

- `current/index.json`
- `current/inventory.md`
- `tasks/index.json`
- `site/`

That way agents do not need a new schema, only a new base URL.
