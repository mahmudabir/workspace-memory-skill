# Harness integration

Read for enable/update/status or installation help. The skill name and installed
directory must both be `workspace-memory`; the GitHub repository can have any
name. Keep the whole folder, including scripts, assets, and references. Resolve
resources relative to the loaded SKILL.md, never a hardcoded home directory.
`agents/openai.yaml` is optional Codex UI metadata; other hosts need no icon support.

## Select project instructions

| Harness | Default project instruction destination | Project skill location |
| --- | --- | --- |
| Codex | `AGENTS.md`; nonempty `AGENTS.override.md` takes precedence | `.agents/skills/workspace-memory/` |
| Claude Code | `CLAUDE.md` | `.claude/skills/workspace-memory/` |
| Gemini CLI | `GEMINI.md`; honor a known configured context filename | `.gemini/skills/workspace-memory/` |
| OpenCode | `AGENTS.md` | `.opencode/skills/workspace-memory/` |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/skills/workspace-memory/` |
| Cursor | `AGENTS.md` | `.cursor/skills/workspace-memory/` |

Use the active host from runtime context, or the requested harness. A folder's
presence does not identify the running host. If unknown, inspect available host
metadata; ask only if the correct destination remains unknown. Generic mode requires
verified support for AGENTS.md or an explicit supported instruction-file. A tool
without skill discovery can read SKILL.md explicitly and follow the same workflow;
automatic activation and persistence require that tool's documented support.

Read the selected file and applicable existing project instructions. Reuse an existing
equivalent rule loaded through a verified import instead of adding a second copy.
Claude may already use `.claude/CLAUDE.md`; honor that existing project arrangement.
Gemini can customize `context.fileName`; inspect relevant available configuration
without changing it. AGENTS.override.md has special meaning here only for Codex.
Never infer that another host implements Codex precedence. Preserve native auto-memory
and host settings; this skill manages only the shared `.workspace-memory` store.

Default setup targets the current host only. Explicit `harness=all` targets the six
named hosts; an explicit list targets that set. Deduplicate identical destinations.
Install only the loader from assets/agents-loader.md in each effective file. Keep
the full rule once at .workspace-memory/AGENTS.md, ignored with the memory store.
All hosts use that same rule and store. The loader retains automatic recall/save
triggers and control guards; detailed rules load only before memory operations
and are reused while unchanged and in context. Updates refresh the rule and requested loaders;
do not change unrequested hosts. Concurrent agents must reread before writes and
avoid overwriting newer content; no lock or transactional multi-agent guarantee exists.

Use root destinations by default. A custom instruction file must remain inside the
workspace, be an actual always-loaded project instruction mechanism, and preserve
any required host frontmatter. Memory paths always resolve from the chosen workspace
root, even when instructions are in a subdirectory. Use an explicit read-and-follow instruction, not a plain Markdown link. This is
agent-mediated loading, not a native import; existing imports need verified host support. Don't install all adapters
to compensate for uncertainty. No symlinks or host configuration changes are needed.

For Copilot, use an agent-capable surface with skills and repository instructions enabled.
Preserve existing `.github/copilot-instructions.md` content. Memory paths resolve from
the repository root, not `.github/`. Availability varies by Copilot surface; do not
promise automatic writes in code review or completions. Use the supported skill
selector or natural language; no universal Copilot slash syntax is assumed.

Codex loads at most one instruction file per directory. An arbitrary AGENTS.memory.md
is not automatically additive; configured fallback names are used only after the
standard names. Keep the loader in the effective AGENTS.md or AGENTS.override.md.
The nested .workspace-memory/AGENTS.md is read because the loader requests it,
not because Codex automatically discovers it for the whole workspace.

## Invocation and validation

Use the installed host's skill picker/tool or natural language. Codex examples use
`$workspace-memory list`; Claude Code supports `/workspace-memory list`.
Other hosts need not implement either spelling. The action/parameter semantics are
identical once loaded. Host trust, tool permissions, and activation prompts still apply.

The Python helpers use Python 3.9+ standard library on Windows, macOS, and Linux.
Resolve an available interpreter (`python3`, `python`, or an existing Windows Python
launcher) and quote paths with the actual shell's rules. If unavailable or execution
is blocked, use the host's permitted file tools; don't auto-install dependencies.

After setup verify content and preservation of unrelated instructions. On a fresh
session, verify the host loads the destination, then save a harmless test fact only
in an isolated test workspace and list/show/edit/delete it. Also exercise empty
read-only operations and a Python-unavailable file-tool path. Unit tests establish
helper behavior, not live host discovery, permissions, or model adherence. Report
which hosts were actually exercised; never claim universal compatibility from tests.

## Official references

- [Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) and [repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)

- [Claude skills](https://code.claude.com/docs/en/skills) and [project memory](https://code.claude.com/docs/en/memory)
- [Gemini skills](https://geminicli.com/docs/cli/skills/) and [project context](https://geminicli.com/docs/cli/gemini-md/)
- [OpenCode skills](https://opencode.ai/docs/skills/) and [instructions](https://opencode.ai/docs/instructions/)
- [Cursor skills](https://cursor.com/docs/skills) and [rules](https://cursor.com/docs/rules)
- [Codex skills](https://developers.openai.com/codex/skills/) and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
