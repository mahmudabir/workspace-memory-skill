# Reliable listing and targeting

Follow the controls and mutation boundaries in [commands](commands.md).


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

