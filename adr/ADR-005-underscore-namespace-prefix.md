# ADR-005: Underscore Namespace Prefix Convention

## Status

Accepted

## Date

2026-01-27

## Context

MIF uses three base types (semantic, episodic, procedural) as top-level namespace categories. These namespaces need to:
- Be visually distinguishable from domain namespaces
- Sort predictably in file listings
- Indicate "system" vs "user" namespaces
- Work well with existing tooling

Alternative approaches:
1. **No prefix** - `semantic/`, `episodic/`, `procedural/`
   - Mixes with domain content
   - No visual distinction
2. **Dot prefix** - `.semantic/`, `.episodic/`, `.procedural/`
   - Hidden by default in most file browsers
   - Inconsistent cross-platform behavior
3. **Underscore prefix** - `_semantic/`, `_episodic/`, `_procedural/`
   - Visible in all file browsers
   - Sorts to top alphabetically
   - Common convention for "special" directories

## Decision

Use **underscore prefix** for base type namespaces:

- `_semantic/` - Facts, concepts, knowledge
- `_episodic/` - Events, experiences, incidents
- `_procedural/` - Processes, workflows, how-to

Domain-specific sub-namespaces remain unprefixed:
- `_semantic/land/` (not `_semantic/_land/`)
- `_procedural/animal-welfare/`

## Consequences

### Positive
- Clear visual distinction from domain content
- Always sorts to top of directory listings
- Visible in all file browsers and IDEs
- Common convention (e.g., `_templates/`, `_includes/`)
- Signals "system-level" organization

### Negative
- Requires consistent enforcement
- Extra character in paths
- May conflict with other underscore conventions

## Examples

```
memories/
├── _episodic/
│   ├── blockers/
│   └── incidents/
├── _procedural/
│   ├── patterns/
│   └── workflows/
└── _semantic/
    ├── decisions/
    ├── knowledge/
    └── domain/
```

## Related Decisions

- [ADR-001](ADR-001-cognitive-triad-taxonomy.md) - Prefix convention derives from the three base memory types
- [ADR-003](ADR-003-obsidian-compatibility.md) - Underscore prefix ensures filesystem compatibility with Obsidian vaults

## Notes

This convention aligns with the mnemonic memory system implementation and is used consistently across all MIF tooling.
