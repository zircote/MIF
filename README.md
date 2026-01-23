# Memory Interchange Format (MIF)

An open standard for portable AI memory representation.

## Overview

MIF is a proposed standard that aims to enable interoperability between AI memory providers by defining a common data model with dual representations:

- **Markdown** (`.memory.md`) - Human-readable, Obsidian-compatible
- **JSON-LD** (`.memory.json`) - Machine-processable, semantically linked

## Why MIF?

The AI memory ecosystem is fragmented. Mem0, Zep, Letta, LangMem, Subcog, and others all use proprietary schemas. MIF solves:

- **Vendor lock-in** - Move memories between providers
- **Data ownership** - Local-first, plain text files
- **Interoperability** - Common vocabulary for relationships and entities
- **Future-proofing** - Standard formats survive provider discontinuation

## Quick Start

### Minimal Memory (Markdown)

```markdown
---
id: 550e8400-e29b-41d4-a716-446655440000
type: preference
created: 2026-01-15T10:30:00Z
---

User prefers dark mode for all applications.
```

### Minimal Memory (JSON-LD)

```json
{
  "@context": "https://mif.io/context/v1",
  "@type": "Memory",
  "@id": "urn:mif:550e8400-e29b-41d4-a716-446655440000",
  "memoryType": "preference",
  "content": "User prefers dark mode for all applications.",
  "created": "2026-01-15T10:30:00Z"
}
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Dual Format** | Markdown AND JSON-LD representations |
| **Obsidian Native** | Valid Obsidian notes with wiki-links |
| **Typed Relationships** | 9 core relationship types (RelatesTo, DerivedFrom, Supersedes, etc.) |
| **Entity Types** | Person, Organization, Technology, Concept, File |
| **Bi-Temporal** | Track when recorded AND when facts are valid |
| **Flexible Namespaces** | `_public`, `_shared`, `{org}/{scope}+` with reserved prefixes |
| **Model-Agnostic Embeddings** | Store model + source text for re-embedding |
| **W3C PROV** | Standard provenance tracking |

## Specification

See [SPECIFICATION.md](./SPECIFICATION.md) for the complete technical specification.

## Examples

See the [examples/](./examples/) directory for:

- Minimal memories (Level 1)
- Standard memories with relationships (Level 2)
- Full-featured memories with temporal and provenance data (Level 3)

## Conformance Levels

| Level | Requirements |
|-------|--------------|
| **Level 1: Core** | id, type, content, created |
| **Level 2: Standard** | + namespace, entities, relationships, timestamps |
| **Level 3: Full** | + bi-temporal, decay, provenance, embeddings |

## Migration

MIF includes migration guides for:

- Mem0
- Zep
- Letta (Agent File)
- Subcog
- Basic Memory

## Contributing

This specification is open source. Contributions welcome:

1. Open an issue for discussion
2. Submit PRs for specification changes
3. Implement and share converters

## Related

- [Subcog](https://github.com/zircote/subcog) - AI memory system implementing MIF
- [Issue #82](https://github.com/zircote/subcog/issues/82) - Original proposal

## License

[MIT](./LICENSE)
