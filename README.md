# Workspace Memory

<img src="assets/icon.svg" width="64" height="64" alt="Memory icon">

Portable, selective project memory for AI coding agents. Keep useful decisions,
constraints, and discoveries between sessions without loading a growing task log.

The skill installs project instructions that guide the agent to retrieve relevant
knowledge, save useful findings, and maintain compact memory as it works.
**Installing the skill and enabling it in a workspace are separate steps.**

## Installation

Clone this repository into your harness's project skill directory. For example,
from the project root, for GitHub Copilot:

```sh
git clone https://github.com/mahmudabir/workspace-memory-skill.git .github/skills/workspace-memory
```

For another harness, use its destination below. Alternatively, download the
repository and copy its contents into that folder. Keep `SKILL.md`, `assets/`,
`references/`, and `scripts/` together. The installed folder must be named
`workspace-memory`.

| Harness | Project skill directory | Default project instructions |
| --- | --- | --- |
| Codex | `.agents/skills/workspace-memory/` | `AGENTS.md` or effective `AGENTS.override.md` |
| Claude Code | `.claude/skills/workspace-memory/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/skills/workspace-memory/` | `GEMINI.md` |
| OpenCode | `.opencode/skills/workspace-memory/` | `AGENTS.md` |
| Cursor | `.cursor/skills/workspace-memory/` | `AGENTS.md` |
| GitHub Copilot | `.github/skills/workspace-memory/` | `.github/copilot-instructions.md` |

These paths describe project installation. Personal installation uses the host's
supported user skill location; see the [harness guide and official documentation](references/harnesses.md).
Existing imports and configured instruction filenames are respected.

## Quick start

After the host discovers the skill, ask:

> Use workspace-memory to enable memory for this workspace.

Or invoke it directly where supported:

```text
# Codex
$workspace-memory enable

# Claude Code
/workspace-memory enable
```

Other hosts can use their skill picker or natural language. Dollar and slash
prefixes are not universal shell commands. A new session may be needed to load
new project instructions.

Setup adds a managed rule while preserving unrelated instructions. It does not
scan the application to invent memories or create an empty memory store.
After meaningful work, the agent can save verified, useful knowledge automatically.
It operates during agent work, not as a background service.

## Where memory lives

All paths are relative to the project workspace root:

```text
.workspace-memory/
  MEMORY.md       # Compact knowledge and, when needed, a topic index
  topics/         # Optional topic files created as knowledge grows
  PAUSED          # Present only while persistent writes are paused
```

Memory is shared by agents working in the same workspace. It is not stored inside
the installed skill or copied to user-global memory. Topics are created when useful,
not preallocated. The entry point targets roughly 100 lines and 5-8 KB, with larger
domains moved into linked topics.

## Commands

Use these actions with the skill invocation or equivalent natural language:

| Action | Purpose |
| --- | --- |
| `enable` | Install the workspace memory instructions. Bare invocation also enables. |
| `uninstall` | Remove saved memory, controls, managed project instructions, and verified project-local skill copies. |
| `update` | Refresh the installed rule without clearing pause controls. |
| `help` | Show commands or help for a specific action. |
| `status` | Show setup, memory, and control state; during skip, show controls only. |
| `list` | List saved knowledge with selectable numbers and sources. |
| `search` / `recall` | Find relevant saved knowledge. |
| `show` | Display a selected entry. |
| `add` / `remember` | Save supplied knowledge, merging equivalent entries. |
| `edit` / `correct` | Update selected knowledge. |
| `delete` / `forget` | Remove selected knowledge and equivalent copies. |
| `compact` | Consolidate, shorten, and reorganize memory while retaining useful facts. |
| `check` | Inspect memory health without changing it. |
| `repair` | Fix demonstrable structural or routing problems. |
| `pause` | Persistently block all knowledge changes; reading remains enabled. |
| `skip` | Stop memory reading, use, and changes in this session. |
| `resume` | Clear both persistent pause and session skip. |

### Examples

These examples use Codex notation; adapt the invocation for your host.

```text
$workspace-memory list limit=20 page=1
$workspace-memory search query="authentication decisions"
$workspace-memory show target=3
$workspace-memory add topic="testing" text="Use an isolated database for integration tests."
$workspace-memory edit target=3 text="Use a separate database for each integration test run."
$workspace-memory delete target=3
$workspace-memory compact dry-run=true
$workspace-memory check
$workspace-memory repair
```

Numbered targets refer to the latest displayed results in the same conversation.
The examples are independent; list or search before selecting a number.

### Pause and session skip

```text
$workspace-memory pause
$workspace-memory skip
$workspace-memory status
$workspace-memory resume mode=usage
$workspace-memory resume mode=writes
$workspace-memory resume
```

- **Pause** persists across sessions and hosts through the `PAUSED` marker. It blocks
  automatic maintenance and explicit add/edit/delete/compact/repair until resumed.
- **Skip** stays in the current conversation, including context-compaction handoffs.
  It ends when resumed or when a new independent session starts. It creates no file.
- `resume mode=usage` clears only session skip; `resume mode=writes` clears only
  persistent write pause. Plain `resume` clears both.
- Already loaded context cannot be erased. During skip, the agent avoids relying
  on saved memory and uses current sources instead. Skipped knowledge is not
  automatically saved later.

These controls are instructions followed by agents, not filesystem locks. Existing
workspaces need `update` to receive new control rules; older active sessions may
need to reload them.

### Remove from a workspace

```text
$workspace-memory uninstall dry-run=true
$workspace-memory uninstall
```

Uninstall deletes saved memory and the pause marker, removes managed memory rules
across project instruction files, and removes verified project-local skill copies.
It preserves unrelated content, Git history, and personal/global skill installations.
It works while paused or skipped. Removal uses native file tools, without requiring
Python. Unsafe paths or ambiguous content are preserved and reported.

The current session stops using and saving memory. Use `enable` to set it up again;
`resume` does not reinstall it. Refresh other active sessions so their old instructions
do not recreate memory. See [full removal details](references/commands.md#full-workspace-removal).
### Parameters

| Parameter | Use |
| --- | --- |
| `workspace="path"` | Select the workspace; otherwise use the current resolved root. |
| `topic="name"` | Narrow knowledge operations to a topic. |
| `query="words"` | Supply a search query. |
| `target="selector"` | Select an existing entry for show/edit/delete. |
| `text="content"` | Supply knowledge for add/edit. |
| `limit=20 page=1` | Paginate list/search/check; maximum limit is 100. |
| `dry-run=true` | Preview a change without changing files or session state. |
| `harness="copilot"` | Select a host for setup/update/status. Setup also accepts a list or `all`. |
| `instruction-file="relative/path"` | Use a verified custom project instruction destination. |
| `mode="writes\|usage\|all"` | Choose what resume clears; default is all. |

Parameters apply only to relevant actions. See the [full command reference](references/commands.md)
for exact scope, defaults, and mutation boundaries. `harness=all` configures the six
named hosts; it does not install those applications.

## Optional Python helpers

Python 3.9+ with the standard library is optional. Agents can use native file tools
when Python or shell execution is unavailable; no runtime is installed automatically.

From this skill's directory, using your available Python interpreter:

```sh
python -B scripts/memory.py status --workspace /path/to/project --harness copilot
python -B scripts/memory.py list --workspace /path/to/project --limit 20
python -B scripts/memory.py search --workspace /path/to/project --query "testing"
python -B scripts/memory.py check --workspace /path/to/project
```

Quote paths as required by your shell. Some systems use `python3` instead of `python`.

`memory.py` returns compact JSON and never writes files. Its keyword search and
structural checks do not establish factual freshness or semantic equivalence.
Session skip belongs to the conversation and cannot be detected by the helper;
while skipped, the agent must not call retrieval helpers, including normal status.

`create_file.py` copies a reviewed sample or agent-prepared source into a new file
without overwriting an existing file. It does not generate hardcoded memory layouts.
The agent handles semantic edits, controls, compaction, and repairs.

## Compatibility and limits

The skill includes integration guidance for the six named hosts and custom
instruction paths for other agents. A host needs file access and a supported way
to load project instructions for persistent behavior. Skill activation, permissions,
and model adherence depend on the host; universal or unattended operation is not
guaranteed. Copilot support targets agent-capable surfaces, not automatic writes
from code review or inline completions.

The Python helper tests have been run locally on Windows. End-to-end behavior in
all supported harnesses has not been verified. Concurrent agents must avoid
clobbering each other's edits; this skill provides no transactional write lock.

Keep credentials, secrets, sensitive personal data, raw logs, and speculative facts
out of memory. Memory may be shared through version control. The skill does not
stage, commit, push, or change ignore settings automatically.

## Development

Run the helper tests from the skill directory:

```sh
python -B scripts/test_memory.py
python -B scripts/test_create_file.py
```

Tests use temporary workspaces. Symlink tests may skip when the operating system
does not permit creating symlinks. They validate helper behavior, not live harness
integration or model compliance.

- [Skill instructions](SKILL.md)
- [Commands](references/commands.md)
- [Harness integration](references/harnesses.md)
- [Installable memory rule](assets/agents-memory.md)
