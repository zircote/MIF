# ADR-001: Cognitive Triad Taxonomy

## Status

Accepted

## Date

2026-01-27

## Context

MIF needs a memory classification system that is:
- Universally applicable across domains
- Grounded in established theory
- Simple enough for practical use
- Expressive enough for AI memory systems

Alternative approaches considered:
1. **Domain-specific categories** - Too fragmented, no portability
2. **Flat tagging** - No semantic hierarchy, poor organization
3. **Custom ontology per system** - No interoperability
4. **Cognitive psychology model** - Well-researched, universal

## Decision

Adopt the **cognitive triad** from cognitive psychology:

1. **Semantic Memory** - Facts, concepts, and knowledge
   - General world knowledge
   - Definitions and relationships
   - Domain expertise

2. **Episodic Memory** - Events and experiences
   - Timestamped occurrences
   - Personal experiences
   - Contextual incidents

3. **Procedural Memory** - Skills and processes
   - How-to instructions
   - Workflows and procedures
   - Learned behaviors

## Consequences

### Positive
- Based on Tulving (1972) for the semantic/episodic distinction and Cohen & Squire (1980) for procedural memory as a distinct category
- Intuitive for both humans and AI systems
- Universal applicability across all domains
- Clear mental model for memory organization
- Enables meaningful cross-system memory portability

### Negative
- Some memories may span categories (addressed via traits)
- Requires understanding of cognitive psychology concepts
- May feel limiting for domain-specific use cases (addressed via namespace extensions)

## Related Decisions

- [ADR-005](ADR-005-underscore-namespace-prefix.md) - Namespace prefix convention derives from the three base memory types
- [ADR-008](ADR-008-decay-model-rationale.md) - Default decay half-lives vary by memory type

## References

- Tulving, E. (1972). Episodic and semantic memory. Organization of Memory.
- Cohen, N. J. & Squire, L. R. (1980). Preserved learning and retention of pattern-analyzing skill in amnesia.
- Squire, L. R. (2004). Memory systems of the brain.
