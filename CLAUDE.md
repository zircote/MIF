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

For MIF-specific decisions and learnings:
- **Architecture decisions** → `./.claude/mnemonic/decisions/project/`
- **API patterns** → `./.claude/mnemonic/apis/project/`
- **Testing strategies** → `./.claude/mnemonic/testing/project/`
- **Security considerations** → `./.claude/mnemonic/security/project/`

### Blackboard

Use `./.claude/mnemonic/.blackboard/` for temporary working notes during complex tasks.
