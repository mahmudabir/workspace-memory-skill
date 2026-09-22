---
name: workspace-memory
description: Enable, list, search, show, summary, add, edit, delete, compact, repair, or uninstall persistent, human-manageable workspace memory across coding agents using project instructions and .workspace-memory/MEMORY.md. Use for workspace memory setup, saved knowledge management, usage summaries, and memory status or health checks.
---

# Workspace Memory

Repository-owned, human-readable memory, shared across supported agents using the
same checkout. Setup installs a small loader and an on-demand rule; skill discovery
alone does not enable automatic memory. Stores are local and ignored, not synced
across clones, worktrees or machines.

## Select the workflow

Use natural language or the host's skill invocation. `$workspace-memory` is Codex
notation, `/workspace-memory` is Claude notation; neither is an executable command.
Bare invocation means enable. Unknown actions never trigger setup.

- Enable/update: read [setup](references/setup.md), then only its required resources.
- Explicit management/help: read the selected action in
  [commands](references/commands.md), then its linked workflow. Listing/search are
  read-only; compact/check/repair authorize memory audits, not application scans.
- Automatic recall/save: use the installed `.workspace-memory/AGENTS.md`; do not
  load command, setup or harness guides. If absent, memory is disabled; explicit
  management may use [the sample rule](assets/agents-memory.md) without installing it.
- Creating a file: read setup's Template-driven file creation section and the
  applicable sample. Existing-file edits do not require setup.

## Automatic repository routing

Use task paths and attached project roots, not writable-root lists. Store memory
at `<repo-root>/.workspace-memory/`; normalize subdirectories to the nearest Git
root (`.git` directory or file), or use the attached root for non-Git workspaces.
An explicit `workspace` selects scope, not a package-local store. Local tasks select
one repo; cross-repo tasks select relevant repos; project-wide management selects
all attached repos. The same checkout reuses its store across Codex projects.
For multi-root, nested/container, or ambiguous scope, read only Repository routing
in the installed rule or [sample](assets/agents-memory.md#repository-routing).
Never silently merge/migrate stores, enable missing stores, or redirect inaccessible
memory to another root. Ask only when context cannot resolve the target.

## Context budget

Skip recall for self-contained tasks that cannot benefit from prior knowledge;
still evaluate lasting corrections and useful discoveries for saving. Reuse loaded
rules, root mappings and relevant facts while unchanged. Re-resolve when scope
changes; recheck controls and mutation targets before writing.

Prefer [memory.py](scripts/memory.py) for bounded retrieval. Read
[retrieval](references/retrieval.md#optional-token-saving-helper) on first helper use,
not every task. Start automatic recall with a focused search and `--limit 5`; expand
or fetch full entries when needed. This is an initial budget, never a completeness
limit. Explicit lists/audits keep their requested scope. No redundant index read,
whole-store dump, status/check, or summary read before routine recall.

Batch material-use IDs per root with `record-use --brief`; use `refresh-summary
--brief` after knowledge changes. Record-use also refreshes counts, so omit a
redundant refresh when the same call covers both. Do not count inspection as use.
The helper uses Python 3.9+ standard library; fall back to targeted native file tools
when unavailable, without installing a runtime. Semantic decisions remain agent work.

## Controls and boundaries

Session skip blocks all memory reads/use/writes, including metadata. PAUSED blocks
knowledge writes only; check before each write and defer if unreadable. Setup
preserves controls; never backfill skipped facts. Follow the installed rule and
higher-priority write restrictions; enabling memory grants no host-native access.

Knowledge belongs only in `MEMORY.md` and `topics/`; `SUMMARY.md` is helper-managed
metadata, excluded from recall. Never create workspace `.codex`, change ACLs/host
settings, or bypass permissions. Use permitted file tools when execution fails;
report inaccessible memory and continue independent work. Verify writes before
claiming success. Stored facts never override instructions or current evidence.
