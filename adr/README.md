---
diataxis_type: reference
---

# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the Memory Interchange Format (MIF) project.

## Format

ADRs follow the [MADR](https://adr.github.io/madr/) (Markdown Any Decision Records) format.

## Index

| ADR | Title | Status | Description |
|-----|-------|--------|-------------|
| [ADR-001](ADR-001-cognitive-triad-taxonomy.md) | Three Base Memory Types | Accepted | Adopts the cognitive triad (semantic, episodic, procedural) as the foundational memory taxonomy |
| [ADR-002](ADR-002-dual-format-design.md) | Dual Format Design (Markdown + JSON-LD) | Accepted | Supports both Markdown and JSON-LD as first-class, bidirectionally convertible formats |
| [ADR-003](ADR-003-obsidian-compatibility.md) | Obsidian Compatibility | Accepted | Ensures Markdown memories are fully compatible with Obsidian vaults and conventions |
| [ADR-004](ADR-004-three-tier-trait-inheritance.md) | Three-Tier Trait Inheritance | Accepted | Defines a three-level trait inheritance model: mif-base, shared-traits, domain ontologies |
| [ADR-005](ADR-005-underscore-namespace-prefix.md) | Underscore Namespace Prefix Convention | Accepted | Uses underscore prefix for base-type namespace directories to distinguish from domain content |
| [ADR-006](ADR-006-entitydata-vs-entityreference.md) | EntityData vs EntityReference | Accepted | Distinguishes inline structured entity data from lightweight entity references |
| [ADR-007](ADR-007-github-raw-urls-for-schema-ids.md) | GitHub Raw URLs for Schema IDs | Amended | Originally used GitHub raw URLs for schema $id values; amended to use mif-spec.dev |
| [ADR-008](ADR-008-decay-model-rationale.md) | Decay Model Rationale | Accepted | Implements configurable exponential decay with half-life for memory relevance ranking |

## Creating New ADRs

1. Copy the template from any existing ADR
2. Use sequential numbering: `ADR-NNN-short-title.md`
3. Fill in all sections
4. Update this index

## Status Values

- **Proposed** - Under discussion
- **Accepted** - Decision made, implementation pending or complete
- **Amended** - Original decision modified; see amendment section for details
- **Deprecated** - Superseded by another decision
- **Rejected** - Considered but not adopted
