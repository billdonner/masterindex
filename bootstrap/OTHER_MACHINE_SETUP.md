# Other-Machine MasterIndex Setup

The canonical MasterIndex instructions are kept in `bootstrap/MASTERINDEX_MANAGED_BLOCK.md`. Run `bootstrap/install-agent-handoff.sh` after cloning or pulling MasterIndex to install or update that block in every available tracked repository.

The installer updates only the delimited MasterIndex block in `AGENTS.md` and `CLAUDE.md`. It skips a dirty `CLAUDE.md` so existing agent work is never swept into a handoff commit.

MasterIndex defines the six-hour verification and daily-refresh policy; a machine still needs a scheduler and an authorized coding-agent command to execute work. Configure that runner locally rather than hard-coding a particular agent vendor in the shared repository.
