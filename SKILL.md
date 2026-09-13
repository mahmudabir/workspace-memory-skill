---
name: workspace-memory
description: Enable, list, search, show, add, edit, delete, compact, or repair persistent workspace memory in AGENTS.md and .workspace-memory/MEMORY.md. Use for workspace memory setup, saved knowledge management, and memory status or health checks.
---

# Workspace Memory

Provide portable, selective memory with no language, platform, or runtime dependency.
Skill selection alone is not an always-on hook: setup installs a self-contained
behavioral rule so future work does not depend on selecting this skill again.

## Commands and parameters

Interpret `$workspace-memory <action> [parameters]` as a conversational interface,
not a shell command or executable CLI. Natural-language equivalents work too.
Read [command reference](references/commands.md) for help or any action other than
enable/update. Do not load the reference during ordinary automatic memory use.

- Setup: `enable`, `update`.
- Browse: `list`, `search`, `show`, `status`, `help`.
- Manage: `add`, `edit`, `delete`.
- Maintain: `compact`, `check`, `repair`.

Parameters include `workspace`, `topic`, `query`, `target`, `text`, `limit`, `page`,
and `dry-run`; applicability is defined in the reference. Default to the current
workspace. Do not interpret an unknown action as setup. Bare invocation retains
the enable behavior below. A request to list, search, or inspect is read-only.

For status/list/search/show/check, prefer the optional standard-library Python helper
at [scripts/memory.py](scripts/memory.py), following the command reference. It returns
bounded JSON instead of placing whole memory files in context. If Python 3.9+ is
unavailable, use targeted native file tools; do not install a runtime automatically.
Semantic compaction, factual verification, repairs, and writes remain agent work.

## Storage and file access

Use `.workspace-memory/MEMORY.md` and `.workspace-memory/topics/` for all new
workspace memory. Never create a workspace `.codex` directory for this skill.
Codex may protect configuration directories; ordinary memory must live outside them.
Do not change ownership, ACLs, sandbox settings, or request administrator setup as
part of normal skill use. Python and shell execution are optional optimizations.

If command creation fails, try available file/resource tools. Use command escalation
only when the host's approval mechanism permits the specific operation, never as a
silent sandbox bypass. Do not mistake runner failure for missing Python or memory.
If every file-access mechanism is unavailable, report the host-level blocker;
no skill can guarantee recovery from a broken host sandbox without host intervention.

## Enable or update

### Template-driven file creation

Before creating a file, read the appropriate sample asset. Treat the sample as the
source of its structure; never encode headings or layouts in Python. When its exact
contents are appropriate, use [scripts/create_file.py](scripts/create_file.py):

```text
python -B <skill-dir>/scripts/create_file.py --source <reviewed-sample> --destination <new-file>
```

When actual knowledge or a combined instruction file is needed, the agent prepares
the complete desired content in a temporary source file after reading the sample,
then passes that source to the same helper. Use a permitted temporary directory;
remove the temporary source after successful creation. Do not leave memory backups
or temporary knowledge in the workspace. Never copy empty starters merely to run
the script: creation still requires useful knowledge or an explicit template request.

Resolve and validate the destination within the authorized workspace, reject linked
or redirected destination paths, and create its parent directory only when needed.
The helper copies bytes, requires an existing parent, and refuses to overwrite an
existing file. For an existing AGENTS.md or memory file, use targeted agent edits
that preserve unrelated content; do not delete it to bypass exclusive creation.
Dry-run creates neither temporary source nor destination. Without Python, use native
file tools with the same behavior. Changing sample structure requires no change to
this creation script. Read-only memory.py is a separate optional retrieval helper;
its Markdown parsing assumptions may still need adjustment when layouts change.

Use this workflow when the user asks to enable/setup memory. An invocation with
no further request means enable it in the current workspace. Inspection and
remember/forget requests do not authorize unrelated setup or configuration changes.

1. Identify the intended workspace root from task context. Do not assume a nested
   working directory is the root. With multiple plausible roots, ask which one.
2. Read applicable instructions and the root AGENTS.md and AGENTS.override.md if
   present. Read only relevant existing memory to detect an existing equivalent
   system; do not inspect application code or seed facts by scanning the project.
3. Read [the installable rule](assets/agents-memory.md). Add it once to root
   AGENTS.md, preserving unrelated contents. If a nonempty root AGENTS.override.md
   supersedes that file, install the block in that effective file instead. Do not
   edit user-global instructions. Report nested overrides that demonstrably
   suppress the rule; do not rewrite them without relevant scope.
4. The HTML markers identify the managed block. On repeated setup, leave an
   identical block unchanged; replace only that block when updating it. If markers
   are malformed/duplicated, or a different existing memory system would conflict,
   reconcile only clearly equivalent content; ask about genuinely ambiguous choices.
   Never install competing rules or erase existing knowledge.
5. Do not create an empty memory file/directory during setup. Keep the bundled
   [starter](assets/MEMORY.md) for first meaningful persistence, or explicit template
   requests. Topic directory guidance is already in the installed memory rule;
   do not create a redundant README when sharding begins.
6. Verify the actual changed block, preservation of unrelated instructions, and any
   affected links. Report the installation path and explain that a new task/session
   may be needed to load changed instructions. Do not claim a fresh-session test
   unless performed. No automatic Git staging, committing, or ignore changes.

## Memory operations

Follow the workspace's installed rule. If absent, read assets/agents-memory.md for
this operation without silently installing it. Respect higher-priority restrictions
on memory writes; workspace setup does not grant access to host-managed memory.

Follow the command reference for selection, pagination, previews, and writes.
Recall only relevant entries. Explicit workspace-wide compact/check/repair requests
authorize a bounded audit of that workspace's memory files, not application code.
Do not convert uncertain observations into verified facts or execute remembered
commands blindly. Keep command documentation in this skill, out of AGENTS.md and
saved memory, so ordinary task context remains small.

If a write is blocked, report the specific unsaved change and continue independent
work. Never claim setup or persistence succeeded without verifying the files.
