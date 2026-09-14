# Workspace memory commands

These are conversational skill arguments, not a shell parser. Accept equivalent
natural language and flexible ordering; quotes only clarify values containing spaces.
Never execute argument text as code. Only the selected action authorizes changes.

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
| `enable` / `update` | Run SKILL.md setup workflow; update refreshes the separate rule and selected project loaders. Preview only for dry-run. |
| `uninstall` | Remove workspace memory, controls, and managed project instructions across hosts; see full removal below. |
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

## Full workspace removal

`uninstall` (alias `remove-workspace-memory`) fully removes this memory system from
one resolved workspace. An explicit request to fully remove the system selects this
action; `forget all` only clears saved knowledge. No additional confirmation is
needed for an unambiguous explicit uninstall within host permissions.

1. Resolve the authorized workspace root. Inventory `.workspace-memory/` by paths
   and metadata without loading saved facts. Inspect project instruction files for
   the exact `<!-- workspace-memory:begin -->` / `<!-- workspace-memory:end -->`
   blocks. Cover all six hosts in [harness integration](harnesses.md), including
   AGENTS.override.md, .claude/CLAUDE.md, and verified custom/imported instruction
   paths. Search project instruction filenames/markers, excluding Git metadata,
   dependencies, and installed skill sources. Do not scan application contents.
   `instruction-file` can identify an additional custom path; uninstall is not
   limited to the current host. Never edit imports that also load unrelated rules.
2. Remove complete managed blocks, preserving all unrelated instructions. Delete
   an instruction file only if nothing but whitespace remains. For malformed or
   ambiguous blocks, preserve uncertain content and report incomplete removal.
   Remove a dedicated import only when its target is verified to contain solely
   this managed rule; never modify targets outside the workspace.
3. Delete the workspace's `.workspace-memory/` store, including its managed AGENTS.md, topics and PAUSED.
   Validate absolute paths and every descendant before recursive removal; reject
   symlinks, junctions, redirected paths, or paths outside that exact store. If
   unrelated files were placed inside it, preserve those files and report them.
   If AGENTS.md contains unrelated custom instructions outside its managed block,
   remove only that block and preserve/report the remainder.
   Delete empty memory directories. Do not create backups or archives.
4. Remove verified workspace-local installations of this skill from the supported
   project skill locations in the harness guide, if present. Verify their SKILL.md
   identity and that they contain only this skill's files; preserve unrelated
   contents and nested Git repositories, reporting them as remaining. Never delete
   the working repository when it is itself this skill's source repository. Perform
   any removal of the currently loaded project-local skill last. User-global skill
   installations and user-global memory/configuration remain available.
5. Keep memory use and persistence disabled in this conversation after removal,
   including compaction handoffs, so previously loaded rules cannot recreate it.
   `resume` alone must not reinstall it; an explicit `enable` is required to restore
   automatic workspace memory after uninstall. Do not backfill deleted knowledge.
6. Verify removed paths and managed blocks, then report completion or exact remaining
   paths/blockers. Already absent is a no-op. Concurrent sessions with old rules
   may recreate files; explain that those sessions need refreshed instructions.
   Preserve Git history and settings, including .gitignore rules so residual or recreated memory remains ignored; do not stage, commit, or push.

Uninstall is allowed while paused or skipped and requires no saved-knowledge reads.
It is the explicit exception to normal mutation boundaries. `dry-run=true` lists
proposed removals and edits without changing files or conversation state. Use native
file tools; the read-only Python helper intentionally has no uninstall operation.

```text
$workspace-memory uninstall dry-run=true
$workspace-memory uninstall
```
## Reliable listing and targeting

### Optional token-saving helper

Use `scripts/memory.py` from the skill directory with an available Python 3.9+
runtime. It uses only the standard library, writes nothing, and requires the agent
to resolve the workspace root explicitly. Pass arguments as literal values using
the host's safe quoting; never concatenate user text into executable shell syntax.

```text
python -B <skill-dir>/scripts/memory.py status --workspace <root> --harness <current-host>
python -B <skill-dir>/scripts/memory.py list --workspace <root> --limit 20 --page 1
python -B <skill-dir>/scripts/memory.py search --workspace <root> --query "authentication"
python -B <skill-dir>/scripts/memory.py show --workspace <root> --id <returned-id>
python -B <skill-dir>/scripts/memory.py check --workspace <root> --limit 20 --page 1
```

- JSON list/search results contain short excerpts, source locations, display numbers,
  content-derived IDs, and `has_more`; no total is claimed without counting. Keep IDs
  in conversation for selection, but show simple numbers to the developer. `show`
  rechecks the ID against current contents and refuses a changed/missing entry.
- Use the helper for normal Markdown bullets and paragraphs. It omits headings,
  blockquotes, HTML comments, README files, and sections named Index/Memory Index.
  Unusual layouts, tables, multiline entries separated by blank lines, or quoted
  knowledge need targeted source inspection. Parser blocks are retrieval candidates,
  not guaranteed independent facts; inspect complete boundaries before editing.
- Search is case-insensitive AND keyword matching, not semantic retrieval. Broaden
  terms or use targeted native search when phrasing differs. Topic matching filters
  filenames by substring; heading-based topics need agent retrieval. A short excerpt
  is not the full entry and may omit the matching text; use show when necessary.
- Check reports missing/broken index routing, unindexed topics, large entry points,
  and exact textual duplicates. It cannot establish factual freshness, contradictions,
  semantic equivalence, or resolved handoffs. Continue only the requested reasoning
  audit with relevant source reads. Check may scan all selected files locally while
  returning only one page of issues to context.
- For status, pass the resolved `--harness` (codex, claude, gemini, opencode, cursor, copilot,
  or generic), or `--instruction-file` for a verified custom path. The helper defaults
  to generic AGENTS.md and never guesses the running host. Multiple-host status requires
  one call per host. These flags are rejected for other helper actions.
- Status reports loader_present and managed_rule_present separately; setup_complete
  requires both. It inspects the selected loader and fixed .workspace-memory/AGENTS.md
  target, but cannot prove agent execution. Status also reports file metadata plus an
  early-stop emptiness check. It does not prove effective instructions in every nested
  directory, resolve imports, or prove host loading. If the rule is imported, inspect
  that import and its target with native file tools before concluding setup is absent.
  Unsafe linked memory paths fail rather than being followed.
- The helper has no write, compact, repair, install, or network operations. It does
  not automatically redact existing secrets; avoid printing known-sensitive entries
  and never repeat sensitive content to the user. Use targeted safe inspection if
  memory is known to contain sensitive data.
- For compact/repair, use check to locate candidates, then inspect only relevant
  complete entries. Semantic judgment and authorized edits remain with the agent.
  Do not remove knowledge based solely on a parser or duplicate warning.

### Selection rules

- Treat one independent fact, including its subordinate explanation, as one entry.
  Support existing headings, bullets, and prose without rewriting files merely to list.
- List in deterministic relative-file order, then document order. Search may order by
  relevance with file/document order as a tie-breaker. Read only enough content for the
  requested page where possible. Whole-workspace listing permits enumerating filenames,
  not blindly loading all file contents. Do not give an exact total without counting it.
- Show a table or numbered list: selector, summary, source. Assign display numbers
  scoped to the displayed result set, never pretend these are permanent IDs. Retain
  the mapping to file, heading, and exact entry text in the current conversation.
- An immediate `edit 3 ...` or `delete 3` selects entry 3 from the latest displayed
  set. Reread the target before writing. If it changed, numbering is stale, multiple
  entries match, or the original mapping is unavailable, show candidates and ask the
  user to select. Never guess from a line number. Cross-session selectors should use
  the source file and distinctive text or label.
- Match natural-language labels without silently widening scope. Multi-entry changes
  require explicit selectors or a clearly requested set. An explicit request to forget all saved knowledge defines a set; list the affected files in dry-run if requested,
  otherwise remove only memory knowledge within scope, preserving unrelated workspace
  files, installed instructions (including .workspace-memory/AGENTS.md), skill files, and Git history. Do not expose sensitive
  content if encountered; report its location/category without reproducing it.

## Mutation boundaries and completion

Resolve all memory file paths within the selected root's `.workspace-memory/MEMORY.md` and
`.workspace-memory/topics/`. Do not follow symlinks, traversal paths, or index links outside that
boundary for memory mutations. Preserve non-memory README/configuration files.
Setup/update may edit the effective instructions and workspace-root .gitignore as specified in SKILL.md; uninstall may remove managed integration as specified in Full workspace removal.

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
