# Portfolio query and refresh protocol

## Why this exists

MasterIndex should answer questions such as “what could break if I change
this?”, “which apps are ready to release?”, or “what needs attention?” across
the entire software portfolio. It must not turn a convenient answer into an
untraceable assertion. This protocol makes the index a small, grounded
knowledge system: stable facts, explicitly dated observations, open gaps, and
separate operational instructions.

The local [MCP server](../mcp/README.md) is the query plane. Its portfolio
tools are read-only. The two explicit Project Intake tools are the exception:
they write a review proposal or, after exact-name confirmation, provision a
new project under [the Project Intake protocol](project-intake-protocol.md).
The existing JSON registries remain the source of truth.

## Authority boundaries

| File | Owns | Does not own |
| --- | --- | --- |
| `current/index.json` | Current observed portfolio facts, relationships, links, gaps | Schedules or next-cycle instructions |
| `tasks/index.json` | Recurring task definitions and cadence | Proof that a task actually ran |
| `current/handoffs/index.json` | Targeted, temporary maintenance instructions | Current facts or historical source evidence |
| `current/inventory.md` | Human narrative derived from the index | Facts not represented in `current/index.json` |
| `mcp/server.py` | Query/freshness views; explicit project-intake actions | Arbitrary inventory mutation or external action |

Keep these distinctions. In particular, an active task does not prove a
service is healthy, and an active handoff does not replace a verified fact.

## Answering a portfolio question

An MCP client or agent should follow this sequence:

1. For anything time-sensitive, call `get_freshness` first.
2. Call `search_portfolio` with the outcome, product name, dependency, or
   service in the question.
3. Call `get_entity` for the likely records. It joins the entity with active
   tasks, targeted handoffs, services, dependencies, and consumers.
4. Answer with the observed date(s), source limits, and relevant gaps. Use
   “not recorded” rather than turning absence into a negative claim.
5. If the result needs verification, route it through the refresh procedure
   below rather than updating facts in a chat response.

`portfolio_brief` is for a cross-cutting starting point; it should not be the
only evidence for a release or operational decision.

### Source ladder

Use the least expansive source that can answer the question, and say which
one was used:

1. **Recorded inventory** — `get_freshness`, `search_portfolio`, and
   `get_entity` answer from committed MasterIndex facts and dates.
2. **Local source state** — `check_local_sources` reads the current local Git
   worktree for MasterIndex and selected entity repositories. It never fetches
   or contacts a remote, so it cannot establish GitHub synchronization.
3. **Public availability** — `verify_public_links` makes bounded public HTTP
   checks only when a URL matters. A reachable URL is not proof of release,
   identity, or service health.
4. **Authoritative live systems** — App Store Connect, deployment providers,
   GitHub remote state, and private service health need their own explicit,
   authenticated source. Until one is connected, record that gap rather than
   calling the portfolio current.

## Observation standard

Every new or replaced fact needs an observation. New refreshes should retain
this optional additive shape on the changed entity or gap; it does not change
the existing public schema:

```json
{
  "observedAt": "2026-11-10T15:30:00-06:00",
  "source": {
    "kind": "repository | service-probe | App-Store-Connect | public-web | owner-report",
    "locator": "repository path, command summary, stable URL, or support case",
    "authority": "first-party | owner-report | derived"
  },
  "collector": "agent or person that observed it",
  "confidence": "verified | reported | inferred",
  "note": "What was observed and any scope limitation"
}
```

For high-value or complex refreshes, save one immutable session artifact at
`current/observations/YYYY-MM-DD/<run-id>.json`. It should contain the
observation envelope, every target entity id, source locators, unavailable
sources, commands or API operation names (never credentials), and the commit
that incorporated the facts. These artifacts are audit evidence, not a new
source of truth.

Use only these confidence terms:

- `verified`: directly observed in the authoritative source at `observedAt`.
- `reported`: supplied by the owner or another source, not independently
  checked yet.
- `inferred`: a carefully labeled conclusion from observed facts; do not use
  it for release, money, or availability claims.

When sources disagree, retain the previous verified fact, record a gap or
ambiguity, and describe the conflict. Do not silently merge the more
convenient value.

## Refresh transaction

The established index-before-narrative order is mandatory. A routine refresh
is a transaction with these phases:

1. **Route** — read `current/index.json`, then `tasks/index.json`, then
   `current/handoffs/index.json`. Identify target entities, shared cadence,
   and active directives addressed to them or `all-entities`.
2. **Observe** — use the authoritative source for each fact: repository for
   source state, deploy/service probe for runtime, App Store Connect for ASC,
   and a public URL for public availability. Record unavailability explicitly.
   No observation may include credentials, raw private user data, or private
   endpoint responses in this repository.
3. **Reconcile** — preserve prior facts unless newer observed evidence
   replaces them. Capture public links whenever verified. Turn uncertainty
   into a dated `gaps` entry rather than guessing.
4. **Write** — update `current/index.json` first, including `generatedAt`
   only when the inventory itself was actually reconciled. Then update
   `current/inventory.md` if the changed facts affect its narrative. Do not
   rewrite `tasks/index.json` during an ordinary inventory pass.
5. **Verify** — run `tools/masterindex-drift-check.sh --strict` and the MCP
   smoke test. Resolve validation errors before handoff.
6. **Publish evidence** — commit the fact changes and any observation
   artifact together with a concise source/date summary. A task run is not
   complete merely because the scheduler fired.

Use event-triggered refreshes (a deploy, submission, domain change, or owner
report) in addition to the existing six-hour verification and daily inventory
refresh cadence. The daily sweep should prioritize entries whose recorded
observation is older than seven days, live services, release candidates, and
active handoff targets.

## Freshness semantics

`generatedAt` means when the whole inventory was assembled. An entity's
`lastModified` is a portfolio record signal, not necessarily when its runtime
was checked. `observedAt` in new evidence is the time-specific claim. The MCP
freshness tool deliberately reports all three registries separately and calls
old data stale; it never treats staleness as a proof the fact is false.

This fixes a common failure mode: changing one entity must not make an old
App Store, service, or repository observation appear newly verified.

## Safety and mutation policy

Portfolio query tools remain read-only. They can reveal planning and
operational context, but they must not deploy, submit, send mail, change App
Store data, or overwrite inventory facts. Project Intake is the sole defined
write exception, governed by its exact-name confirmation and separate
[protocol](project-intake-protocol.md). All other operational actions remain
explicit follow-on work in the appropriate repository/session.

If later we add write tools, they should create a reviewable observation
proposal outside the canonical index—not commit facts directly—and require
human confirmation before a maintainer applies it.
