# Enable, update, and file creation

Read for enable/update. For other actions creating files, read only Template-driven file creation.


### Template-driven file creation

Before creating a file, read the appropriate sample asset. Treat the sample as the
source of its structure; never encode headings or layouts in Python. When its exact
contents are appropriate, use [scripts/create_file.py](../scripts/create_file.py):

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

1. Apply [automatic repository routing](../SKILL.md#automatic-repository-routing).
   For unqualified project-wide enable/update, select all attached repository
   roots automatically; for an explicit workspace or repository-scoped request,
   select only that scope. Repeat steps 2-7 separately for each deduplicated root.
   Do not create a shared parent store or move existing knowledge. Ask only when
   the target cannot be resolved from context, not because the project has two repos.
2. Read [harness integration](harnesses.md) to select the current host's
   effective project instruction file. Honor explicit harness/instruction-file arguments;
   do not infer the running host from installed folders. Read applicable instructions
   and relevant existing memory to detect equivalent systems; do not scan application code.
3. Read [the installable rule](../assets/agents-memory.md) and install it at
   `.workspace-memory/AGENTS.md` using the template-driven workflow. Create the
   directory for this instruction file, without creating empty knowledge files.
   Read [the loader sample](../assets/agents-loader.md) and add only that small managed
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
5. Do not create empty MEMORY.md, topic files, or SUMMARY.md during setup. Keep the
   bundled [starter](../assets/MEMORY.md) for first meaningful persistence, or explicit
   template requests. When updating a workspace that already has saved knowledge,
   initialize or refresh its auto-managed `.workspace-memory/SUMMARY.md` with the
   helper's `refresh-summary --brief` operation; it is metadata, not retrievable knowledge.
   Topic directory guidance is already in the installed memory rule; do not create
   a redundant README when sharding begins.
6. Ensure the workspace-root .gitignore contains this labeled section:

   ```gitignore
   
   # workspace-memory skill
   .workspace-memory/PAUSED
   .workspace-memory/
   ```

   Read it first, preserve unrelated content, and add missing rules once; create
   it if absent, even without an initialized Git repository. Use native file tools
   or the reviewed-source creation workflow; reject linked/redirected paths.
   On existing installations, add the comment above the rules if missing. Keep
   one labeled section on repeated enable/update; consolidate only these exact
   rules and this comment, preserving unrelated rules and comments. Place the
   section after conflicting negations without duplicating its lines. Dry-run
   previews the edit without writing.
   With Git available in a repository, verify representative paths with
   git check-ignore --no-index and inspect git ls-files for tracked memory.
   Ignore rules do not untrack existing files: report those paths without changing
   the index or history. Without Git, verify content and state that Git behavior
   was not tested. Report blocked ignore edits as incomplete setup.
7. Verify the separate rule, each loader and its workspace-root target, ignore rules
   and their single section comment,
   preservation of unrelated instructions, and any
   affected links. Report the installation path and explain that a new task/session
   may be needed to load changed instructions. Do not claim a fresh-session test
   unless performed. No automatic Git staging, committing, pushing, or index changes.

