---
name: ontology-manager
description: >-
  Create, validate, inspect, and convert MIF ontology definition files.
  Use when the user asks to: create a new ontology, scaffold an ontology,
  validate an ontology YAML, inspect ontology contents (entities, traits,
  relationships, namespaces, discovery patterns), convert between YAML
  and JSON formats, convert to JSON-LD, or get guidance on MIF ontology
  structure. Triggers on: "ontology", "create ontology", "validate
  ontology", "inspect ontology", "convert ontology", "ontology schema",
  "entity types", "traits", "discovery patterns", "namespace hierarchy".
---

# MIF Ontology Manager

Manage MIF ontology definition files using `yq`, `jq`, and bundled
shell scripts. All operations are grounded in the MIF ontology JSON
Schema at `schema/ontology/ontology.schema.json`.

## Prerequisites

```bash
# Required
brew install yq jq    # or equivalent package manager
# Optional (for JSON Schema validation)
pip install jsonschema
# Optional (for JSON-LD conversion)
pip install pyyaml
```

## Workflow Decision Tree

```
User wants to...
|
+-> Create a new ontology
|   scaffold_ontology.sh <id> <ver> [--extends mif-base]
|   Then edit the generated YAML to add domain content.
|
+-> Validate an ontology
|   validate_ontology.sh <file.yaml> [schema.json]
|
+-> Inspect ontology contents
|   inspect_ontology.sh <file.yaml> [--section X] [--json]
|   Sections: entities, namespaces, traits, relationships, discovery
|
+-> Convert formats
|   convert_format.sh yaml2json <in.yaml> [out.json]
|   convert_format.sh json2yaml <in.json> [out.yaml]
|   convert_format.sh yaml2jsonld <in.yaml> [out.jsonld]
|
+-> Understand the schema
|   Read references/schema-reference.md
|
+-> Add entity types / traits / relationships / patterns
    Use yq commands documented below.
```

## Scripts

All scripts are in `scripts/` relative to this skill directory.
Set `SKILL_DIR` to this skill's path before running.

### scaffold_ontology.sh

Generate a new ontology skeleton with valid structure.

```bash
# Standalone ontology
bash "$SKILL_DIR/scripts/scaffold_ontology.sh" \
  my-domain 0.1.0 > my-domain.ontology.yaml

# Extending mif-base
bash "$SKILL_DIR/scripts/scaffold_ontology.sh" \
  my-domain 0.1.0 --extends mif-base \
  > my-domain.ontology.yaml

# Extending multiple parents
bash "$SKILL_DIR/scripts/scaffold_ontology.sh" \
  my-domain 0.1.0 --extends mif-base,shared-traits \
  > my-domain.ontology.yaml
```

### validate_ontology.sh

Validate ontology YAML for correctness.

```bash
# Basic validation (syntax, required fields, formats)
bash "$SKILL_DIR/scripts/validate_ontology.sh" my.ontology.yaml

# With JSON Schema validation
bash "$SKILL_DIR/scripts/validate_ontology.sh" my.ontology.yaml \
  schema/ontology/ontology.schema.json
```

Checks: YAML syntax, required fields (`ontology.id`, `ontology.version`),
ID format, semver, base types, entity name format, trait references,
discovery regex validity, optional JSON Schema compliance.

### inspect_ontology.sh

Introspect ontology contents.

```bash
# Full summary
bash "$SKILL_DIR/scripts/inspect_ontology.sh" my.ontology.yaml

# Specific section
bash "$SKILL_DIR/scripts/inspect_ontology.sh" my.ontology.yaml \
  --section entities

# JSON output (pipe to jq for queries)
bash "$SKILL_DIR/scripts/inspect_ontology.sh" my.ontology.yaml \
  --section traits --json
```

Sections: `entities`, `namespaces`, `traits`, `relationships`,
`discovery`, `all` (default).

### convert_format.sh

Convert between YAML, JSON, and JSON-LD.

```bash
# YAML -> JSON
bash "$SKILL_DIR/scripts/convert_format.sh" yaml2json my.ontology.yaml

# JSON -> YAML
bash "$SKILL_DIR/scripts/convert_format.sh" json2yaml my.ontology.json

# YAML -> JSON-LD (uses scripts/yaml2jsonld.py if in MIF repo)
bash "$SKILL_DIR/scripts/convert_format.sh" yaml2jsonld my.ontology.yaml
```

## Common yq/jq Operations

### Query Operations

```bash
# List all entity type names
yq -r '.entity_types[].name' ontology.yaml

# Count entities by base type
yq '.entity_types | group_by(.base) |
  map({key: .[0].base, value: length}) |
  from_entries' ontology.yaml

# List all trait names
yq -r '.traits | keys | .[]' ontology.yaml

# List all relationship names
yq -r '.relationships | keys | .[]' ontology.yaml

# Show namespace tree (children only)
yq '.namespaces | .. | .children? // empty | keys' ontology.yaml

# Find entities using a specific trait
yq '.entity_types[] |
  select(.traits and (.traits[] == "timestamped")) |
  .name' ontology.yaml

# Count discovery patterns
yq '[.discovery.content_patterns // [],
  .discovery.file_patterns // []] |
  flatten | length' ontology.yaml
```

### Mutation Operations

```bash
# Add a new entity type
yq -i '.entity_types += [{
  "name": "my-entity",
  "description": "Description here",
  "base": "semantic",
  "traits": ["timestamped"],
  "schema": {
    "required": ["name"],
    "properties": {
      "name": {"type": "string", "description": "Name"}
    }
  }
}]' ontology.yaml

# Add a new trait
yq -i '.traits.my-trait = {
  "description": "My custom trait",
  "fields": {
    "my_field": {
      "type": "string",
      "description": "Field description"
    }
  }
}' ontology.yaml

# Add a new relationship
yq -i '.relationships.my-rel = {
  "description": "Links A to B",
  "from": ["entity-a"],
  "to": ["entity-b"],
  "symmetric": false
}' ontology.yaml

# Add a content discovery pattern
yq -i '.discovery.content_patterns += [{
  "pattern": "\\bmy-keyword\\b",
  "namespace": "_semantic/knowledge",
  "context": "my domain context"
}]' ontology.yaml

# Add a child namespace
yq -i '.namespaces._semantic.children.my-sub = {
  "description": "My sub-namespace",
  "type_hint": "semantic"
}' ontology.yaml

# Bump version
yq -i '.ontology.version = "0.2.0"' ontology.yaml
```

## Ontology Design Guidelines

### Naming Conventions

- **IDs**: lowercase, hyphens only (`my-domain`, not `myDomain`)
- **Entity names**: lowercase, hyphens (`support-ticket`)
- **Trait names**: lowercase, underscores for field names (`created_at`)
- **Namespaces**: underscore prefix for top-level (`_semantic`)

### Cognitive Triad Mapping

| Memory Type | Use For | Namespace |
|-------------|---------|-----------|
| semantic | Facts, concepts, entities, decisions | `_semantic/` |
| episodic | Events, incidents, sessions, timelines | `_episodic/` |
| procedural | Processes, runbooks, patterns, how-tos | `_procedural/` |

### When to Extend vs. Standalone

- **Extend `mif-base`**: Almost always. Provides cognitive triad
  namespaces, base traits, and base relationships.
- **Extend `shared-traits`**: When you need reusable traits like
  `lifecycle`, `auditable`, `categorized`, `tagged`, `scored`.
- **Standalone**: Only for experimental or self-contained ontologies.

### Entity Type Design

1. Choose the correct `base` type (semantic/episodic/procedural)
2. Compose with existing traits before defining new fields
3. Use `schema.required` for mandatory fields
4. Use `enum` for controlled vocabularies
5. Keep descriptions concise (use `>-` folded scalars in YAML)

### Discovery Pattern Tips

- Content patterns: use `\b` word boundaries for precision
- File patterns: match against file path segments
- Always test regex: `python3 -c "import re; re.compile(r'...')"`
- Set `suggest_entity` to auto-classify matched content

## Schema Reference

For complete field definitions, types, and constraints, see
[references/schema-reference.md](references/schema-reference.md).

The authoritative JSON Schema is at:
`schema/ontology/ontology.schema.json`
