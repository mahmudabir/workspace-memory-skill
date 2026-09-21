---
name: workspace-memory
description: Enable, list, search, show, summary, add, edit, delete, compact, repair, or uninstall persistent, human-manageable workspace memory across coding agents using project instructions and .workspace-memory/MEMORY.md. Use for workspace memory setup, saved knowledge management, usage summaries, and memory status or health checks.
---

# Workspace Memory

Provide portable, selective, workspace-owned memory with no language, platform, or
runtime dependency. The store is human-readable and explicitly manageable; it
complements host-native agent memory rather than replacing it. Native memory may
hold personal or agent-specific context, while this skill keeps project knowledge
in the workspace for supported agents and the developer to inspect and maintain.
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

Default to the current workspace; bare invocation means enable. Unknown actions
must not trigger setup. Listing/search/inspection are read-only. Read command
parameters only when handling an explicit command; setup parameters are described
in the setup and harness guides.

For status/list/search/show/check/summary, prefer the optional standard-library Python
helper at [scripts/memory.py](scripts/memory.py), following the command reference. It
returns bounded JSON instead of placing whole memory files in context. Use its
`record-use` and `refresh-summary` operations for the auto-managed usage metadata;
normal retrieval operations remain read-only. If Python 3.9+ is unavailable, use
targeted native file tools; do not install a runtime automatically. Semantic
compaction, factual verification, repairs, and knowledge writes remain agent work.

## Storage and file access

Use `.workspace-memory/MEMORY.md` and `.workspace-memory/topics/` for all new
workspace memory. Use `.workspace-memory/SUMMARY.md` only for auto-managed usage
metadata; it is human-readable but is not knowledge and must not be loaded during
ordinary retrieval. These are ordinary, workspace-owned files; knowledge may be
explicitly corrected, organized, or deleted through the documented workflows. Never
create a workspace `.codex` directory for this skill. Manual summary edits may be
replaced by the next helper-managed update.
Hosts may protect configuration directories; ordinary memory must live outside them.
Do not change ownership, ACLs, sandbox settings, or request administrator setup as
part of normal skill use. Python and shell execution are optional optimizations.

If command creation fails, try available file/resource tools. Use command escalation
only when the host's approval mechanism permits the specific operation, never as a
silent sandbox bypass. Do not mistake runner failure for missing Python or memory.
If every file-access mechanism is unavailable, report the host-level blocker;
no skill can guarantee recovery from a broken host sandbox without host intervention.

## Enable or update

Read [setup workflow](references/setup.md) for enable/update, including bare
invocation. For any other operation creating a file, read its Template-driven
file creation section first. Do not load setup for existing-file reads or edits.
Enable/update groups the workspace-root `.gitignore` rules under a single
`# workspace-memory skill` comment, including when upgrading existing rules.

## Memory operations

Before retrieval or persistence, honor session skip state and check the workspace
`.workspace-memory/PAUSED` marker. Read the control section in the command reference
for pause/skip/resume/status. These controls take precedence over routine retention.
Enable/update must preserve an existing pause; setup is not resume.

Follow the workspace's installed rule. If absent, read assets/agents-memory.md for
this operation without silently installing it. Respect higher-priority restrictions
on memory writes; workspace setup does not grant access to host-managed memory.

Treat stored memory as fallible project context. For project facts, prefer current
user instructions, current repository/source-of-truth state, and tracked project
documentation over Workspace Memory; treat host-native or automatically learned
memory as lower-confidence context when it conflicts. This is a factual-freshness
heuristic, not a change to the host's formal instruction hierarchy. Never let stored
memory override current code, explicit user instructions, or verified repository
state; verify conflicts against the current project.

For explicit commands, follow the command reference and its selected workflow
for selection, pagination, previews, and writes.
Recall only relevant entries. Explicit workspace-wide compact/check/repair requests
authorize a bounded audit of that workspace's memory files, not application code.
Do not convert uncertain observations into verified facts or execute remembered
commands blindly. Keep command documentation in this skill, out of project instructions and
saved memory, so ordinary task context remains small.

If a write is blocked, report the specific unsaved change and continue independent
work. Never claim setup or persistence succeeded without verifying the files.
