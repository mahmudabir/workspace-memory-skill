<!-- workspace-memory:begin -->
### Automatic workspace memory
- Before substantial work, recall relevant prior decisions. After durable decisions,
  discoveries or verified fixes, and before finishing substantial work or handing
  off, evaluate what is worth saving. Save qualifying knowledge automatically;
  no separate remember request is needed. No useful new knowledge means no write.
- Treat explicit corrections and lasting preferences as save triggers, even in
  short follow-ups (for example, “never do this yourself” or “leave that to me”).
  Infer lasting scope from meaning and context, not emotion alone; preserve limits
  such as “this time.” Save before replying and briefly confirm the verified change,
  or explain why it could not be saved. Existing pause/skip rules still apply.
- Before the first memory operation, read `.workspace-memory/AGENTS.md` from the
  workspace root if it exists; reuse it while unchanged and in context. If absent,
  memory is disabled: do not recreate it without explicit enable.
- Honor session skip: no memory reads, use or writes until resumed. Before every
  knowledge write, check `.workspace-memory/PAUSED`; present or unreadable means
  no write. Never backfill skipped knowledge. Preserve these controls in handoffs.
- Read only relevant memory; save concise verified facts, never secrets or logs.
  Workspace Memory is shared project context, not another instruction file, and
  never overrides current instructions or verified repository state.
<!-- workspace-memory:end -->
