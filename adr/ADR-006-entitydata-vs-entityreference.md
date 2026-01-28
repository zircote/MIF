# ADR-006: EntityData vs EntityReference

## Status

Accepted

## Date

2026-01-27

## Context

MIF needs to represent entities in two contexts:
1. **Inline structured data** - Full entity details embedded in the memory
2. **References to entities** - Pointers to entities mentioned in content

These serve different purposes and have different constraints.

## Decision

Define two distinct entity representation patterns:

### EntityReference
For referencing entities mentioned in memory content:
```json
{
  "@type": "EntityReference",
  "entity": {
    "@id": "urn:mif:entity:person:jane-smith"
  },
  "entityType": "Person",
  "name": "Jane Smith",
  "role": "author"
}
```

**Use when:**
- Mentioning a person, organization, or concept
- Creating relationships to external entities
- Basic entity metadata is sufficient

**Constraints:**
- Core types: Person, Organization, Technology, Concept, File
- Custom types via lowercase pattern: `grazing-plan`, `soil-profile`
- Minimal schema, extensibility via `additionalProperties: false`

### EntityData
For structured ontology-typed data embedded in the memory:
```json
{
  "entity": {
    "name": "2026 Spring Grazing Plan",
    "entity_type": "grazing-plan",
    "entity_id": "grazing-plan-beef-2026",
    "herd_id": "herd-beef-main",
    "stock_density": 250000,
    "rest_period_days": 45
  }
}
```

**Use when:**
- Memory IS an entity (not just mentions one)
- Full structured data per ontology schema
- Entity-specific fields needed

**Constraints:**
- Requires `ontology` reference
- Schema defined by ontology `entity_types`
- `additionalProperties: true` for custom fields

## Consequences

### Positive
- Clear semantic distinction between use cases
- EntityReference: lightweight, standard types
- EntityData: rich, domain-specific structure
- Both can coexist in same memory

### Negative
- Two patterns to understand
- Potential confusion about when to use each
- Schema duplication for `name` field

## Guidelines

| Scenario | Use |
|----------|-----|
| Memory about a person | `entities: [EntityReference]` |
| Memory about a soil test | `entity: EntityData` with `entity_type: soil-profile` |
| Memory mentioning equipment | `entities: [EntityReference]` |
| Memory that IS a grazing plan | `entity: EntityData` with full fields |
