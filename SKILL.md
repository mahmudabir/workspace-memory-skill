---
name: workspace-memory
description: Enable, list, search, show, add, edit, delete, compact, repair, or uninstall persistent workspace memory across coding agents using project instructions and .workspace-memory/MEMORY.md. Use for workspace memory setup, saved knowledge management, and memory status or health checks.
---

# Workspace Memory

Provide portable, selective memory with no language, platform, or runtime dependency.
Skill selection alone is not an always-on hook: setup installs a self-contained
loader and a separate ignored behavioral rule so future work does not depend on
selecting this skill again.

## Commands and parameters

Use the host's skill invocation or natural language, such as "use workspace-memory
to list memories". `$workspace-memory <action> [parameters]` is Codex notation;
Claude Code uses `/workspace-memory <action>`. These are conversational arguments,
not a shell command or executable CLI. Never assume slash or dollar syntax is universal.
Read [command reference](references/commands.md) for help or any action other than
enable/update. Do not load the reference during ordinary automatic memory use.

- Setup: `enable`, `update`, `uninstall` (remove workspace memory and its integration).
- Controls: `pause`, `skip`, `resume` (see command reference).
- Browse: `list`, `search`, `show`, `status`, `help`.
- Manage: `add`, `edit`, `delete`.
- Maintain: `compact`, `check`, `repair`.

Parameters include `workspace`, `topic`, `query`, `target`, `text`, `limit`, `page`,
`harness`, `instruction-file`, `mode`, and `dry-run`; applicability is defined in the reference. Default to the current
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
Hosts may protect configuration directories; ordinary memory must live outside them.
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
existing file. For an existing project instruction or memory file, use targeted agent edits
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
2. Read [harness integration](references/harnesses.md) to select the current host's
   effective project instruction file. Honor explicit harness/instruction-file arguments;
   do not infer the running host from installed folders. Read applicable instructions
   and relevant existing memory to detect equivalent systems; do not scan application code.
3. Read [the installable rule](assets/agents-memory.md) and install it at
   `.workspace-memory/AGENTS.md` using the template-driven workflow. Create the
   directory for this instruction file, without creating empty knowledge files.
   Read [the loader sample](assets/agents-loader.md) and add only that small managed
   block to each selected project instruction file, preserving unrelated content.
   Follow the integration reference for configured filenames, overrides, and hosts.
   Install the rule before its loaders. Do not change user-global instructions or
   host settings. Keep automatic recall/save triggers and skip/pause guards in the
   loader so persistence does not depend on selecting the skill. Load the separate
   rule before a memory operation, reusing unchanged context; not on every task.
   This is agent-mediated loading, not a native import.
4. The HTML markers identify the managed block. On repeated setup, leave an
   identical block unchanged; replace only that block when updating it. If markers
   are malformed/duplicated, or a different existing memory system would conflict,
   reconcile only clearly equivalent content; ask about genuinely ambiguous choices.
   Apply this to both the separate rule and project loaders. Replace an existing
   complete inline workspace-memory block with the loader after installing the
   separate rule; preserve intentional custom memory guidance in that rule.
   Never install competing rules or erase existing knowledge.
5. Do not create empty MEMORY.md or topic files during setup. Keep the bundled
   [starter](assets/MEMORY.md) for first meaningful persistence, or explicit template
   requests. Topic directory guidance is already in the installed memory rule;
   do not create a redundant README when sharding begins.
6. Ensure the workspace-root .gitignore contains both explicit rules:
   - .workspace-memory/PAUSED
   - .workspace-memory/
   Read it first, preserve unrelated content, and add missing rules once; create
   it if absent, even without an initialized Git repository. Use native file tools
   or the reviewed-source creation workflow; reject linked/redirected paths.
   Place these rules after conflicting negations; move only these exact rules if
   necessary, without duplicating them. Dry-run previews the edit without writing.
   With Git available in a repository, verify representative paths with
   git check-ignore --no-index and inspect git ls-files for tracked memory.
   Ignore rules do not untrack existing files: report those paths without changing
   the index or history. Without Git, verify content and state that Git behavior
   was not tested. Report blocked ignore edits as incomplete setup.
7. Verify the separate rule, each loader and its workspace-root target, ignore rules,
   preservation of unrelated instructions, and any
   affected links. Report the installation path and explain that a new task/session
   may be needed to load changed instructions. Do not claim a fresh-session test
   unless performed. No automatic Git staging, committing, pushing, or index changes.

## Memory operations

Before retrieval or persistence, honor session skip state and check the workspace
`.workspace-memory/PAUSED` marker. Read the control section in the command reference
for pause/skip/resume/status. These controls take precedence over routine retention.
Enable/update must preserve an existing pause; setup is not resume.

Follow the workspace's installed rule. If absent, read assets/agents-memory.md for
this operation without silently installing it. Respect higher-priority restrictions
on memory writes; workspace setup does not grant access to host-managed memory.

Follow the command reference for selection, pagination, previews, and writes.
Recall only relevant entries. Explicit workspace-wide compact/check/repair requests
authorize a bounded audit of that workspace's memory files, not application code.
Do not convert uncertain observations into verified facts or execute remembered
commands blindly. Keep command documentation in this skill, out of project instructions and
saved memory, so ordinary task context remains small.

If a write is blocked, report the specific unsaved change and continue independent
work. Never claim setup or persistence succeeded without verifying the files.
