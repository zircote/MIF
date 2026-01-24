# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **[Specification]**: Initial MIF (Memory Interchange Format) specification
  - JSON-LD based format for AI memory interoperability
  - Bi-temporal model with valid time and transaction time
  - W3C PROV-compliant provenance tracking
  - Conformance levels (Core, Extended, Full)
  - Human-readable Markdown export support

- **[Specification]**: Citations structure (Level 3 optional feature)
  - Structured citation references with type/role taxonomy
  - Required fields: type, title, url, role
  - Optional fields: author, date, accessed, relevance, note
  - Entity references in author field using wiki-link syntax
  - Citation types: article, book, paper, website, documentation, repository, video, podcast, specification, dataset, tool
  - Citation roles: supports, refutes, background, methodology, contradicts, extends, derived, source, example, review
  - Frontmatter YAML schema and body section Markdown syntax
  - JSON-LD vocabulary with Schema.org alignment
  - Validation rules (Section 5.5.7) with field constraints and error handling
  - Appendix D: Citations Quick Reference

- **[Specification]**: Compression fields (Level 3 optional feature)
  - `summary` - Concise 2-3 sentence summary (max 500 characters)
  - `compressed_at` - Timestamp when compression was applied
  - Compression criteria: Age > 30 days AND lines > 100, OR Strength < 0.3 AND lines > 100

- **[Schema]**: JSON Schema for automated validation
  - `schema/mif.schema.json` - Complete MIF document validation
  - `schema/citation.schema.json` - Standalone citation object validation
  - Draft 2020-12 compliant schemas with comprehensive type definitions

- **[Examples]**: Reference MIF document examples
  - Basic memory interchange examples
  - Entity and relationship examples
  - Temporal metadata examples
  - Level 3 citations example (level-3-citations.memory.md/.json)

### Changed

- **[README]**: Updated to reflect new features
  - Added Citations and JSON Schema to Key Features table
  - Added Validation section with schema usage examples
  - Updated Level 3 conformance to include citations and compression
  - Updated examples description

- **[CONTRIBUTING]**: Added JSON Schema validation guidance

### Documentation

- **[Research]**: Comprehensive market research report
  - Competitive landscape analysis (Mem0, Zep, Letta, LangMem, Cognee, Graphlit)
  - Standards alignment review (JSON-LD, RDF/OWL, ONNX, PROV)
  - Enterprise requirements assessment (EU AI Act, GDPR, NIST AI RMF)
  - Adoption strategy recommendations

- **[Research]**: Executive brief for decision support
  - Market opportunity summary ($2.1B SAM)
  - Competitive positioning analysis
  - Prioritized action items

- **[Research]**: Trend models and forecasting
  - Market growth projections (2024-2030)
  - Technology adoption S-curve
  - Scenario analysis (standard adoption vs fragmentation)
  - Regulatory impact timeline (EU AI Act milestones)

## [0.1.0] - 2026-01-23

### Added

- Initial project setup
- MIF specification draft v0.1
- Market research framework

[Unreleased]: https://github.com/zircote/MIF/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/zircote/MIF/releases/tag/v0.1.0
