# Full workspace removal


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
3. Delete the workspace's `.workspace-memory/` store, including its managed AGENTS.md, topics, auto-managed SUMMARY.md, and PAUSED.
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
It is the explicit exception to normal mutation boundaries in [commands](commands.md). `dry-run=true` lists
proposed removals and edits without changing files or conversation state. Use native
file tools; the read-only Python helper intentionally has no uninstall operation.

```text
$workspace-memory uninstall dry-run=true
$workspace-memory uninstall
```
