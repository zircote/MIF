# MIF Examples

This directory contains reference examples for each MIF conformance level.

## Conformance Levels

| Level | File | Description |
|-------|------|-------------|
| **Level 1: Core** | `level-1-minimal.memory.md` | Minimal required fields only |
| **Level 2: Standard** | `level-2-standard.memory.md` | Adds namespace, entities, relationships |
| **Level 3: Full** | `level-3-full.memory.md` | Complete with bi-temporal, decay, provenance |
| **Level 3: Citations** | `level-3-citations.memory.md` | Full example with citations |

Each example is provided in both formats:
- `.memory.md` - Human-readable Markdown with YAML frontmatter
- `.memory.json` - Machine-processable JSON-LD

## Level 1: Core (Minimal)

The simplest valid MIF memory.

**Required fields:**
- `id` - UUID identifier
- `type` - Memory type (`semantic`, `episodic`, or `procedural`)
- `created` - Creation timestamp
- Content body

**Recommended (shown in example):**
- `namespace` - Hierarchical scope (e.g., `_semantic/preferences`)

Note: The Level 1 example includes `namespace` as a practical minimum because it's essential for organizing memories, though technically optional per the schema.

## Level 2: Standard

Adds organizational and relational features:
- `namespace` - Hierarchical scope
- `tags` - Classification labels
- `aliases` - Alternative names
- Relationships section with wiki-links
- Entities section with typed references

## Level 3: Full

Complete feature demonstration:
- `temporal` - Bi-temporal validity, TTL, decay model
- `provenance` - Source type, agent, confidence, trust level
- `embedding` - Model reference for re-embedding
- `extensions` - Provider-specific metadata
- Block references for granular linking

## Level 3: Citations

Demonstrates the citations feature (Level 3 optional):
- `citations` array in frontmatter with structured metadata
- Citation types: specification, article, documentation, paper, repository
- Citation roles: source, supports, background, methodology, extends
- Entity references in author field using `@[[Name|Type]]` syntax
- Optional `## Citations` body section for detailed annotations
- Relevance scores and access dates

## Note on Wiki-Links

The wiki-links in these examples (e.g., `[[vue-exploration-2025]]`, `@[[React|Technology]]`) are intentionally unresolved. They demonstrate MIF's linking syntax but do not point to actual files in this repository. In a real vault, these would link to other memory files.

## Usage

These examples can be:
1. Used as templates for new memories
2. Validated against the MIF specification
3. Tested with MIF tooling for format conversion
