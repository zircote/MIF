# MIF Project Instructions

## Mnemonic - Project Memory

This project uses the mnemonic memory system for persistent knowledge.

### Project Context
- **Organization**: zircote
- **Project**: MIF
- **User-level path**: ~/.claude/mnemonic/zircote/
- **Project-level path**: ./.claude/mnemonic/

### Project-Specific Recall

On session start, search for project memories:
```bash
rg -l "." ./.claude/mnemonic/ --glob "*.memory.md" | head -10
rg -l "MIF" ~/.claude/mnemonic/zircote/ --glob "*.memory.md" | head -10
```

### Project-Specific Capture

For MIF-specific decisions and learnings (cognitive triad namespaces):
- **Architecture decisions** → `./.claude/mnemonic/semantic/decisions/`
- **API/technical knowledge** → `./.claude/mnemonic/semantic/knowledge/`
- **Code patterns/testing** → `./.claude/mnemonic/procedural/patterns/`
- **Incidents/blockers** → `./.claude/mnemonic/episodic/blockers/`

### Blackboard

Use `./.claude/mnemonic/.blackboard/` for temporary working notes during complex tasks.
