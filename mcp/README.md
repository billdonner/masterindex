# MasterIndex MCP server

`server.py` makes the Master Index useful as portfolio knowledge rather than
as a file an agent has to interpret from scratch. It is a dependency-free MCP
server using standard input/output JSON lines. Its portfolio tools read the
canonical JSON files for each request, so a completed refresh is visible to
connected clients without restarting the server.

## Add it to an MCP client

For Codex CLI, register the local server once:

```sh
codex mcp add masterindex -- python3 /Users/billdonner/masterindex/mcp/server.py
```

Or add this to `~/.codex/config.toml` (or this trusted project's
`.codex/config.toml`):

```toml
[mcp_servers.masterindex]
command = "python3"
args = ["/Users/billdonner/masterindex/mcp/server.py"]
cwd = "/Users/billdonner/masterindex"
default_tools_approval_mode = "writes"
```

The ChatGPT desktop app, Codex CLI, and Codex IDE extension share this Codex
configuration; the desktop UI can also add the same command as a STDIO server.
Other MCP clients may use their own JSON configuration format, but should run
the exact same command and arguments.

It has no third-party dependencies or embedded credentials. Query tools need no
network access. The deliberate provisioning tool invokes local `git` and `gh`
only after its exact-name confirmation, so keep the server local: the
inventory can contain private operational facts.

## Tools

- `search_portfolio` — broad discovery across names, descriptions,
  dependencies, repositories, links, statuses, and clusters.
- `get_entity` — one asset's full record, related entities/services, active
  tasks, active handoffs, and recorded freshness.
- `portfolio_brief` — an attention, release, operations, or combined brief.
- `get_freshness` — registry and entity ages, explicitly separate from truth.
- `check_local_sources` — current, read-only local Git evidence for
  MasterIndex and selected entity repositories; it never contacts a remote.
- `verify_public_links` — deliberate, bounded public HTTP availability checks
  for selected entities; it is not a release or ownership check.
- `get_maintenance_worklist` — current recurring work and active directives.
- `capture_project_idea` — writes a reviewable idea proposal only; no folder
  or remote repository is created.
- `provision_project` — creates the explicitly confirmed project’s local Git
  repository, default private GitHub repository, scaffold, and MasterIndex
  registration.

The first five tools are read-only. The two project tools are deliberately
marked write-capable for MCP clients. Keep approval mode at `writes`; the
provisioning tool also requires an exact project-name confirmation.

The server also exposes the three canonical files as MCP resources. Tools are
usually the better starting point because they constrain context and attach
tasks, handoffs, and relationships to the answer.

## Grounding rule for clients

For a question whose answer can change, call `get_freshness` first. Then use
`search_portfolio` to locate candidates and `get_entity` for the facts behind
the answer. State an observation date and any recorded gap; a missing record
means "not recorded", never "does not exist."

For local source truth, follow it with `check_local_sources` for the entities
that matter. For example: search “PickleFamilia,” then inspect the returned
entity ids. This is intentionally a separate check: a clean local worktree
does not prove GitHub, deployment, or App Store state. Use
`verify_public_links` only when public URL availability is relevant; it makes
network requests and is marked accordingly.

## Project Intake

Tell Codex: “Capture a new project named **X** for **Y**.” It will use the
capture tool and return a reviewable proposal. When you explicitly say to
create it, call `provision_project` with the project id and exact name. The
full safety and lifecycle contract is in
[`docs/project-intake-protocol.md`](../docs/project-intake-protocol.md).

## Verify locally

```sh
python3 mcp/test_server.py
```

The smoke test exercises MCP initialization, tool discovery, a portfolio
search, and a freshness call.
