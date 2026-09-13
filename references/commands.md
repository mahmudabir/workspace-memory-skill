# Workspace memory commands

These are conversational skill arguments, not a shell parser. Accept equivalent
natural language and flexible ordering; quotes only clarify values containing spaces.
Never execute argument text as code. Only the selected action authorizes changes.

## Parameters

| Parameter | Meaning and default |
| --- | --- |
| `workspace="path"` | Explicit workspace root; otherwise resolve the current workspace. Never infer another developer's root or use user-global memory. |
| `harness="codex|claude|gemini|opencode|cursor|copilot|generic"` | Setup/update/status only; default to the known current host. Setup may accept an explicit comma-separated set or `all` for the six named hosts. |
| `instruction-file="relative/path"` | Setup/update/status only; verified project instruction path within the workspace for a custom host/configuration. Overrides the default path; never invent host support. |
| `topic="name or relative file"` | Narrow to a knowledge domain or existing memory topic. Default: relevant scope for search; whole memory for list/status/compact/check/repair. |
| `query="words"` | Search phrase; search/recall require this or a natural-language question. |
| `target="selector"` | Existing entry selected by displayed number, exact label, or file plus distinctive text. Required for show/edit/delete. |
| `text="content"` | New knowledge for add or replacement content for edit. Required unless supplied unambiguously in prose. |
| `limit=20 page=1` | List/search/check pagination; positive integers, limit capped at 100. `next` continues the same query and ordering. |
| `dry-run=true` | Preview a mutation without changing any file. Default false. Applies to enable/update/add/edit/delete/compact/repair. |

Reject unsupported or invalid parameter combinations with a short correction;
do not silently ignore them. Do not require parameters already clear from context.
Ask only for missing content, ambiguous roots/targets, or consequential unresolved
choices. Do not invent memory content. Read-only commands never create files.

For status, first read [harness integration](harnesses.md) and resolve the effective project instruction file. Pass custom paths explicitly to the helper.

## Actions

| Action | Behavior |
| --- | --- |
| `help` | Show a compact command list and examples. `help <action>` shows only that action. No workspace inspection needed. |
| `enable` / `update` | Run SKILL.md setup workflow; update refreshes the managed rule. Preview only for dry-run. |
| `status` | Report resolved root, effective rule presence, entry-point presence/size, topic count, and whether memory is empty. Use metadata and index reads; do not claim a full health audit. |
| `list` | Enumerate saved knowledge entries, not just filenames. Return a paginated list with selectors, short faithful summaries, and source file/heading. Exclude scaffolding and index links. |
| `search` / `recall` | Find relevant entries by words or semantic question. Return matches with selectors, concise excerpts, and sources; distinguish stored claims from live-verified facts. |
| `show` | Show the complete selected entry, its source, scope, and existing evidence pointers. Include subordinate details belonging to that entry; omit unrelated entries. |
| `add` / `remember` | Save the smallest safe supplied fact or durable decision; merge equivalent knowledge. Prefer an existing topic. Create the entry point only when needed; do not create a new topic file for every fact. |
| `edit` / `correct` | Replace only the selected fact and its dependent details with the requested content. Preserve unrelated knowledge and relevant scope/reasons unless explicitly superseded. Reconcile equivalent copies and update routing if scope changes. |
| `delete` / `forget` | Remove the selected knowledge and verified equivalent copies throughout this memory system. Do not delete a whole topic when only an entry was selected. Remove now-empty managed topics and their index links only after checking for other content. |
| `compact` | Consolidate the selected topic, or all current workspace memory if unfiltered. Deduplicate, shorten, resolve proven stale entries, remove verified resolved handoffs, merge tiny overlapping topics, and split oversized domains. Preserve unique useful knowledge and repair routing. |
| `check` | Read-only audit of the selected memory scope: broken links, orphan topics, duplicates, contradictory entries, stale handoffs with supporting evidence, and excessive size. Report uncertain cases as needing verification. |
| `repair` | Fix demonstrable routing/structural problems found in the selected scope. Index orphan knowledge with useful descriptions; preserve its contents. Resolve factual conflicts only when authoritative evidence is available. |

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
- Status describes selected instruction markers and selected file metadata plus an
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
  require explicit selectors or a clearly requested set. An explicit request to remove
  all workspace memory defines a set; list the affected files in dry-run if requested,
  otherwise remove only memory knowledge within scope, preserving unrelated workspace
  files, installed instructions, skill files, and Git history. Do not expose sensitive
  content if encountered; report its location/category without reproducing it.

## Mutation boundaries and completion

Resolve all memory file paths within the selected root's `.workspace-memory/MEMORY.md` and
`.workspace-memory/topics/`. Do not follow symlinks, traversal paths, or index links outside that
boundary for memory mutations. Preserve non-memory README/configuration files.
Setup alone may edit the effective root instructions as specified in SKILL.md.

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
$workspace-memory-skill help
$workspace-memory-skill status
$workspace-memory-skill list limit=20 page=1
$workspace-memory-skill search query="authentication decisions"
$workspace-memory-skill show target=3
$workspace-memory-skill add topic="testing" text="Run integration checks against an isolated database."
$workspace-memory-skill edit target=3 text="Use an isolated database per integration test run."
$workspace-memory-skill delete target=3
$workspace-memory-skill compact dry-run=true
$workspace-memory-skill compact
$workspace-memory-skill check topic="testing"
$workspace-memory-skill repair
```

Examples are independent; numbered targets require a prior result list in the same
conversation. Natural language such as "show saved memories", "edit the second one",
"remember this decision", or "compact this workspace's memory" is equivalent.
