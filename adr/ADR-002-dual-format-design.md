# ADR-002: Dual Format Design (Markdown + JSON-LD)

## Status

Accepted

## Date

2026-01-27

## Context

MIF needs to support:
- Human authoring and reading of memories
- Machine processing and validation
- Semantic web integration for linked data
- Existing knowledge management workflows

Alternative approaches:
1. **JSON-only** - Poor human readability, difficult to edit
2. **Markdown-only** - Limited semantic structure, no validation
3. **YAML** - Good balance but no semantic web support
4. **RDF/Turtle** - Excellent semantics but poor human authoring
5. **Dual format** - Best of both worlds

## Decision

Support both **Markdown** and **JSON-LD** as first-class formats:

### Markdown Format
```markdown
---
id: uuid
type: semantic
namespace: _semantic/knowledge
created: 2026-01-27T10:00:00Z
---

# Memory Title

Memory content in readable Markdown...
```

### JSON-LD Format
```json
{
  "@context": "https://raw.githubusercontent.com/zircote/MIF/main/schema/context.jsonld",
  "@type": "Memory",
  "@id": "urn:mif:memory:uuid",
  "memoryType": "semantic",
  "content": "Memory content..."
}
```

Both formats are semantically equivalent and bidirectionally convertible.

## Consequences

### Positive
- Human authors can write in Markdown (familiar, readable)
- Machines can process JSON-LD (structured, validatable)
- Semantic web compatibility via JSON-LD context
- Supports existing tools (Obsidian, VS Code, etc.)
- Progressive disclosure: simple for basic use, rich for advanced

### Negative
- Dual implementation complexity
- Must maintain format parity
- Conversion tooling required

## Implementation Notes

- YAML frontmatter in Markdown maps directly to JSON-LD properties
- JSON-LD `@context` provides RDF vocabulary mapping
- Content field preserves full Markdown in JSON-LD
