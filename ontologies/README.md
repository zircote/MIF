# MIF Ontologies

This directory contains ontology definitions for the Memory Interchange Format.

## Base Ontology

### mif-base.ontology.yaml

The base ontology defines the cognitive triad namespace hierarchy:

```
semantic/              # Facts, concepts, relationships
├── decisions/         # Architectural choices, rationale
├── knowledge/         # APIs, context, learnings, security
└── entities/          # Entity definitions

episodic/              # Events, experiences, timelines
├── incidents/         # Production issues, postmortems
├── sessions/          # Debug sessions, work sessions
└── blockers/          # Impediments, issues

procedural/            # Step-by-step processes
├── runbooks/          # Operational procedures
├── patterns/          # Code conventions, testing
└── migrations/        # Migration steps, upgrades
```

## Using Ontologies

### Path Format

Memories are stored using hierarchical namespace paths:

```
# User-level (includes org and project)
~/.claude/mnemonic/{org}/{project}/{namespace}/

# Project-level (namespace only)
./.claude/mnemonic/{namespace}/
```

Examples:
- `~/.claude/mnemonic/zircote/mif/semantic/decisions/`
- `./.claude/mnemonic/procedural/patterns/`

### Namespace Selection

Choose namespaces based on memory type:

| Memory Type | Namespace | Description |
|-------------|-----------|-------------|
| Architectural choices | `semantic/decisions` | Why we chose X over Y |
| API/technical facts | `semantic/knowledge` | How X works |
| Component definitions | `semantic/entities` | What X is |
| Production issues | `episodic/incidents` | When X broke |
| Debug sessions | `episodic/sessions` | Work session notes |
| Blockers/impediments | `episodic/blockers` | What's blocking progress |
| Operational procedures | `procedural/runbooks` | How to deploy X |
| Code conventions | `procedural/patterns` | How we write X |
| Upgrade steps | `procedural/migrations` | How to migrate to X |

## Examples

The `examples/` directory contains domain-specific ontologies:

- `software-engineering.ontology.yaml` - Software development entities

## Creating Custom Ontologies

1. Create an `ontology.yaml` file in your project:
   ```
   ./.claude/mnemonic/ontology.yaml
   ```

2. Define custom namespaces, entity types, and discovery patterns:
   ```yaml
   ontology:
     id: my-project
     version: "1.0.0"

   namespaces:
     features:
       description: "Product features"
       type_hint: semantic

   entity_types:
     - name: feature
       base: semantic
       schema:
         required: [name, status]
         properties:
           name: { type: string }
           status: { type: string, enum: [planned, active, deprecated] }
   ```

## JSON-LD Generation

Convert YAML ontologies to JSON-LD for semantic web compatibility:

```bash
python scripts/yaml2jsonld.py ontologies/mif-base.ontology.yaml
python scripts/yaml2jsonld.py --all  # Convert all
```
