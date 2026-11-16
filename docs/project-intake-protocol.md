# Project Intake protocol

## Job

Project Intake is the portfolio's front door for a new idea. A name and a
purpose create a durable, searchable proposal before code, a folder, a GitHub
repository, or a product commitment exists. This avoids the two usual losses:
an idea that disappears in chat, and an empty repository that has no reason
to exist.

The intake registry lives at `intake/index.json`. It is intentionally
separate from `current/index.json`: captured ideas are not yet observed
software assets.

## Two explicit phases

| Phase | Trigger | Writes | Does not do |
| --- | --- | --- | --- |
| Capture | Name + purpose | `intake/index.json` review proposal | Create any external or local project asset |
| Provision | Exact project-name confirmation | Local `~/slug` Git repo, default private GitHub repo, scaffold, MasterIndex entity/repo/task/narrative records | Create a domain, deployment, App Store record, billing item, or public release |

Capture can be done from the local browser app or `capture_project_idea` MCP
tool. Provisioning is deliberately not inferred from “this sounds good”:
`provision_project` requires the exact captured name in its `confirmation`
field. A local UI asks the owner to type it.

## Defaults

- Folder: `~/slug`
- GitHub owner: `billdonner`
- GitHub visibility: private
- Initial MasterIndex cluster: `Incubator`
- Initial status: `incubating`
- Initial task: weekly intent review

These are conservative defaults, not permanent product decisions. The
project’s kind may be selected at intake; platform, product line, revenue,
and release posture remain explicit decisions.

## Provisioning transaction and failure behavior

Provisioning validates name/slug collisions, an empty destination, `git`, and
`gh` before it creates anything. It then creates the local scaffold and first
commit, creates/pushes the private GitHub repository, and registers the new
entity in the required order: `current/index.json`, `current/inventory.md`,
then the deliberate new entry task.

There is no automatic rollback after a local folder or GitHub repository has
been created. If any later step fails, the intake state becomes
`provisioning-needs-attention` with the partial local/remote result and error.
The owner or a maintainer can then resolve the actual state without an agent
silently deleting work.

## Local browser app

Run:

```sh
python3 intake/app.py
```

Then open `http://127.0.0.1:8787`. The app binds only to loopback, never
GitHub Pages. It is a local control surface because it can create repositories
and update the registry.

## After provisioning

Review and commit the MasterIndex changes, then begin normal work in the new
repository. The first weekly intent review should either advance evidence
(prototype, dependency decision, user outcome) or record that the project is
still exploratory. Do not manufacture App Store, deployment, domain, or
public-link facts merely because a repository now exists.

## Ideas sent from a phone

The iOS app can send an idea (a name, a purpose and a kind). It appends the
idea to an `inbox` list in `intake/index.json` by committing through GitHub;
it creates nothing else. The next time ideas are listed on the Mac (the intake
page, the MCP tools, or `ProjectIntakeStore.list_projects()`), each inbox idea
goes through the normal capture checks. One that passes becomes a captured
idea; one that fails stays in the inbox with the reason. Provisioning is
unchanged: it happens on the Mac, with the exact-name confirmation.
