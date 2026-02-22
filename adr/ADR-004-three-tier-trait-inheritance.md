# ADR-004: Three-Tier Trait Inheritance

## Status

Accepted

## Date

2026-01-27

## Context

MIF ontologies need reusable field definitions (traits) that can be composed into entity types. Challenges:
- Avoid repetition across ontologies
- Support domain-specific extensions
- Maintain consistency across implementations
- Enable progressive enhancement

Alternative approaches:
1. **Flat inheritance** - Simple but leads to duplication
2. **Single base** - Inflexible for domain needs
3. **Unlimited inheritance** - Complex, hard to reason about
4. **Three-tier model** - Balanced flexibility and simplicity

## Decision

Implement a **three-tier trait inheritance** model:

### Tier 1: mif-base
Core traits provided by MIF specification:
- `timestamped` - created/modified dates
- `identified` - URN identifiers
- `typed` - memory type classification
- `tagged` - classification tags

### Tier 2: shared-traits
Common cross-domain traits:
- `located` - geographic coordinates
- `bounded` - area/boundary definitions
- `owned` - ownership information
- `certified` - certification status
- `auditable` - audit trail support
- `lifecycle` - status workflow
- `measured` - quantitative data
- `scheduled` - temporal scheduling
- `transactional` - financial aspects

### Tier 3: Domain Ontologies
Domain-specific traits extending shared-traits:
- Agriculture: `seasonal`, `harvestable`
- Research: `peer-reviewed`, `fundable`
- Publishing: `adoptable`, `gradeable`

### Inheritance Chain
```
mif-base → shared-traits → domain-ontology
```

## Consequences

### Positive
- DRY: Define traits once, use everywhere
- Consistency: Common fields have common definitions
- Extensibility: Domains can add specific traits
- Interoperability: Shared traits enable cross-domain queries
- Progressive enhancement: Start simple, add complexity as needed

### Negative
- Three-tier limit may feel arbitrary. Three tiers balance reusability (shared-traits) with domain specificity while keeping the inheritance chain shallow enough for straightforward debugging and override reasoning.
- Trait conflicts require resolution strategy (see SPECIFICATION.md Section 6.3, Trait Conflict Resolution)
- Requires understanding inheritance chain

## Related Decisions

- [ADR-006](ADR-006-entitydata-vs-entityreference.md) - EntityData ties into the trait system for structured entity representation
- [ADR-001](ADR-001-cognitive-triad-taxonomy.md) - Three base memory types form the foundation that traits extend

## Implementation

Ontologies declare inheritance via `extends` field:
```yaml
ontology:
  id: my-domain
  extends:
    - mif-base
    - shared-traits
```

Traits are composed via entity `traits` array:
```yaml
entity_types:
  - name: my-entity
    traits:
      - timestamped
      - owned
      - domain:custom-trait
```
