# ADR-003: Obsidian Compatibility

## Status

Accepted

## Date

2026-01-27

## Context

Many knowledge workers use Obsidian for personal knowledge management. Key Obsidian features:
- YAML frontmatter for metadata
- Wiki-style `[[links]]` for cross-references
- `^block-id` references for granular linking
- Folder-based organization
- Local-first, plain text files

MIF should work seamlessly with Obsidian while maintaining format independence.

## Decision

Adopt Obsidian-compatible conventions:

1. **YAML Frontmatter** - Store memory metadata in standard YAML frontmatter
2. **Wiki-links** - Use `[[target]]` syntax for memory relationships
3. **Block References** - Support `^block-id` for granular citations
4. **File Structure** - Namespace maps to folder path
5. **Plain Text** - All memories are valid Markdown files

### Example
```markdown
---
id: abc123
type: semantic
namespace: _semantic/knowledge
---

# My Memory

This relates to [[other-memory]] and specifically to [[another#^block-id]].

Key insight here. ^important-point
```

## Consequences

### Positive
- Zero-friction Obsidian integration
- Existing Obsidian users can adopt immediately
- Bidirectional sync with Obsidian vaults
- Rich linking and navigation in Obsidian
- Works with Obsidian plugins (graph view, backlinks, etc.)

### Negative
- Wiki-link validation requires tooling (Marksman warnings are expected)
- Block IDs add syntax complexity
- Obsidian-specific features may not translate to all MIF consumers
- Some validation tools may flag intentional wiki-links as errors

## Related Decisions

- [ADR-002](ADR-002-dual-format-design.md) - Obsidian is one of the dual formats supported by MIF
- [ADR-005](ADR-005-underscore-namespace-prefix.md) - Underscore prefix convention ensures filesystem compatibility with Obsidian vaults

## Notes

Wiki-link validation warnings from tools like Marksman are **intentional** in example files - they demonstrate MIF relationship syntax, not broken references.
