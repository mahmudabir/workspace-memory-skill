# Workspace memory commands

These are the explicit management surface for workspace-owned knowledge. The store
is human-readable Markdown, and these actions let a developer inspect, correct,
organize, audit, pause, or remove it without managing a host's native memory.

These are conversational skill arguments, not a shell parser. Accept equivalent
natural language and flexible ordering; quotes only clarify values containing spaces.
Never execute argument text as code. Only the selected action authorizes changes.

## Read only the selected workflow

- enable/update: [setup](setup.md).
- uninstall: [full workspace removal](uninstall.md); no retrieval workflow.
- list/search/show/status/check: [retrieval and targeting](retrieval.md).
- add/edit/delete/compact/repair: [retrieval and targeting](retrieval.md) for
  equivalent-entry checks, selection and audits, plus mutation boundaries below.
- pause/skip/resume: controls below; for creating PAUSED, read only the
  [template-driven creation section](setup.md#template-driven-file-creation).
- help: parameters/actions and relevant examples only; no workspace reads.

Follow controls before retrieval; session skip forbids retrieval-helper execution.
References already loaded and unchanged need not be reread.

## Parameters

| Parameter | Meaning and default |
| --- | --- |
| `workspace="path"` | Explicit workspace root; otherwise resolve the current workspace. Never infer another developer's root or use user-global memory. |
| `harness="codex|claude|gemini|opencode|cursor|copilot|generic"` | Setup/update/status only; default to the known current host. Setup may accept an explicit comma-separated set or `all` for the six named hosts. |
| `instruction-file="relative/path"` | Setup/update/status/uninstall only; verified project instruction path within the workspace for a custom host/configuration. Overrides the default path; never invent host support. |
| `topic="name or relative file"` | Narrow to a knowledge domain or existing memory topic. Default: relevant scope for search; whole memory for list/status/compact/check/repair. |
| `query="words"` | Search phrase; search/recall require this or a natural-language question. |
| `target="selector"` | Existing entry selected by displayed number, exact label, or file plus distinctive text. Required for show/edit/delete. |
| `text="content"` | New knowledge for add or replacement content for edit. Required unless supplied unambiguously in prose. |
| `limit=20 page=1` | List/search/check pagination; positive integers, limit capped at 100. `next` continues the same query and ordering. |
| `mode="writes|usage|all"` | Resume only; default all. Writes clears persistent pause; usage clears session skip; all clears both. |
| `dry-run=true` | Preview a mutation without changing any file. Default false. Applies to enable/update/add/edit/delete/compact/repair/pause/skip/resume/uninstall. |

Reject unsupported or invalid parameter combinations with a short correction;
do not silently ignore them. Do not require parameters already clear from context.
Ask only for missing content, ambiguous roots/targets, or consequential unresolved
choices. Do not invent memory content. Read-only commands never create files.

For status, first read [harness integration](harnesses.md) and resolve the effective project instruction file. Pass custom paths explicitly to the helper.

## Actions

| Action | Behavior |
| --- | --- |
| `help` | Show a compact command list and examples. `help <action>` shows only that action. No workspace inspection needed. |
| `enable` / `update` | Run [setup workflow](setup.md); update refreshes the separate rule and selected project loaders. Preview only for dry-run. |
| `uninstall` | Remove workspace memory, controls, and managed project instructions across hosts; see [full removal](uninstall.md). |
| `pause` | Persistently block knowledge writes in this workspace; reads remain allowed. |
| `skip` | Stop memory retrieval, use, and knowledge writes for this session only. |
| `resume` | Clear the selected controls; default both. Do not backfill skipped knowledge. |
| `status` | Report resolved root, loader presence, separate rule presence, entry-point presence/size, topic count, and whether memory is empty. Use metadata and index reads; do not claim a full health audit. |
| `list` | Enumerate saved knowledge entries, not just filenames. Return a paginated list with selectors, short faithful summaries, and source file/heading. Exclude scaffolding and index links. |
| `search` / `recall` | Find relevant entries by words or semantic question. Return matches with selectors, concise excerpts, and sources; distinguish stored claims from live-verified facts. |
| `show` | Show the complete selected entry, its source, scope, and existing evidence pointers. Include subordinate details belonging to that entry; omit unrelated entries. |
| `add` / `remember` | Save the smallest safe supplied fact or durable decision; merge equivalent knowledge. Prefer an existing topic. Create the entry point only when needed; do not create a new topic file for every fact. |
| `edit` / `correct` | Replace only the selected fact and its dependent details with the requested content. Preserve unrelated knowledge and relevant scope/reasons unless explicitly superseded. Reconcile equivalent copies and update routing if scope changes. |
| `delete` / `forget` | Remove the selected knowledge and verified equivalent copies throughout this memory system. Do not delete a whole topic when only an entry was selected. Remove now-empty managed topics and their index links only after checking for other content. |
| `compact` | Consolidate the selected topic, or all current workspace memory if unfiltered. Deduplicate, shorten, resolve proven stale entries, remove verified resolved handoffs, merge tiny overlapping topics, and split oversized domains. Preserve unique useful knowledge and repair routing. |
| `check` | Read-only audit of the selected memory scope: broken links, orphan topics, duplicates, contradictory entries, stale handoffs with supporting evidence, and excessive size. Report uncertain cases as needing verification. |
| `repair` | Fix demonstrable routing/structural problems found in the selected scope. Index orphan knowledge with useful descriptions; preserve its contents. Resolve factual conflicts only when authoritative evidence is available. |

## Pause, skip, and resume

- `pause` creates `.workspace-memory/PAUSED` using [the sample](../assets/PAUSED)
  and the existing template-driven creation workflow. An existing marker is a no-op.
  Its presence alone means paused, regardless of contents; never store facts in it.
  Create the parent if needed, but no MEMORY.md or topics. Reject redirected paths.
- `skip` changes only conversation state, immediately. Do not read saved memory,
  run retrieval helpers, or persist knowledge. Carry the flag through session
  compaction without copying remembered facts. Do not write a shared skip flag.
- `resume mode=writes` removes only a verified regular PAUSED marker. Missing is a
  no-op; do not remove a directory or follow a link. `resume mode=usage` clears only
  the session flag. Bare `resume` or `resume mode=all` does both. If persistent removal
  fails, report the pause remains; report session state separately.
- Except for explicit uninstall, all knowledge mutations, even explicitly requested ones, are blocked by either
  control until the relevant resume. A combined "resume and add" authorizes both.
  Read-only list/search/show/check are allowed during write pause, blocked during skip.
  Setup/update can refresh instructions but must preserve both controls.
- `status` reports persistent writes paused/active/unknown and session usage
  skipped/active separately. While skipped, inspect only PAUSED metadata and session
  state; do not call the normal status helper (which reads memory for emptiness).
  Help and control operations never need knowledge reads. Python can report only
  persistent pause; session state must come from this conversation.
- Dry-run changes neither files nor session flags. Controls do not install project
  instructions implicitly. If the installed rule predates these controls, explain
  that update is needed for future sessions to honor the marker. Do not claim host
  enforcement or affect user-global memory. Concurrent/older agents may not comply.
- Control mutations are the exception to the knowledge-only mutation boundary below.
  A forget-all request must preserve PAUSED so deleting knowledge does not resume it.

Examples (use the current host's invocation syntax):

```text
$workspace-memory pause
$workspace-memory skip
$workspace-memory status
$workspace-memory resume mode=usage
$workspace-memory resume mode=writes
$workspace-memory resume
```

## Mutation boundaries and completion

Resolve all memory file paths within the selected root's `.workspace-memory/MEMORY.md` and
`.workspace-memory/topics/`. Do not follow symlinks, traversal paths, or index links outside that
boundary for memory mutations. Preserve non-memory README/configuration files.
Setup/update may edit the effective instructions and workspace-root .gitignore as specified in [setup](setup.md); uninstall may remove managed integration as specified in [full removal](uninstall.md).

Before a write, inspect the target and relevant equivalents, preserve concurrent
changes, and honor the installed memory policy. An explicit developer decision may
be stored as that decision; it is not proof of current implementation behavior.
Do not save secrets or unsupported assumptions. If authoritative evidence cannot
resolve a conflict, retain uncertainty and request the needed decision.

For dry-run, show exact proposed add/edit/delete changes or a concise before/after
plan for restructuring. Make no files, markers, temporary memory backups, or index
changes. A later request to apply must revalidate targets; elapsed time is not approval.

For writes, verify affected content and index links, then briefly report what changed
and where. For compact, report files/bytes before and after when measured, important
structural changes, and unresolved issues. A no-op is valid: do not rewrite unchanged
files to demonstrate activity. Never retain deleted knowledge in a hidden archive.

If no memory exists, list/search/show/status/check/compact/repair should say so and
create nothing; add may create memory. If a target or topic cannot be found, report
that fact instead of modifying a different one. An explicit audit or compact request
may inspect all scoped memory incrementally, without copying it all into the response.

## Examples

```text
$workspace-memory help
$workspace-memory status
$workspace-memory list limit=20 page=1
$workspace-memory search query="authentication decisions"
$workspace-memory show target=3
$workspace-memory add topic="testing" text="Run integration checks against an isolated database."
$workspace-memory edit target=3 text="Use an isolated database per integration test run."
$workspace-memory delete target=3
$workspace-memory compact dry-run=true
$workspace-memory compact
$workspace-memory check topic="testing"
$workspace-memory repair
```

Examples are independent; numbered targets require a prior result list in the same
conversation. Natural language such as "show saved memories", "edit the second one",
"remember this decision", or "compact this workspace's memory" is equivalent.
