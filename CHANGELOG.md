# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The in-progress 1.0.0 release. Major, breaking. Repositions MIF as **MIF —
Modeled Information Format**, the opinionated, OKF-compliant content model that
fills OKF's deliberately empty envelope. AI memory becomes the first domain
*profile* of MIF, not its identity.

### Breaking Changes

- **[Format]**: Concept files use the `.md` extension only — the `.memory.md`
  infix is **removed** (an OKF concept ID is the path minus `.md`). The
  `.memory.json` sidecar is replaced by a derived `*.jsonld` projection.
- **[Format]**: Markdown is now the **canonical** representation; JSON-LD is a
  derived, regenerable projection (`scripts/mif_convert.py`). Lossless
  `markdown → json-ld → markdown` round-trip is a tested invariant.
- **[Relationships]**: Typed relationships are authoritative in the frontmatter
  `relationships` array **and** mirrored as OKF-legible body markdown links in a
  `## Relationships` section (`- <type> [Text](/path/target.md)`). Obsidian
  wiki-links are no longer the canonical edge representation.
- **[Identity]**: `id` MUST be a UUID (OKF concept ID is the path; the UUID is
  MIF's stable, location-independent identity). Legacy slug ids migrate to a
  deterministic UUIDv5 with the slug preserved as an `alias`.
- **[Schema]**: `schema/mif.schema.json` v1.0 — `@type: Concept`, `conceptType`
  replaces required `memoryType` (kept as a deprecated alias), and the
  `Relationship` shape is `{ type, target }`.
- **[Temporal]**: The bi-temporal/decay model is reframed as **validity windows
  & freshness** (answering OKF's open live-vs-stale question). The math is
  unchanged; the forgetting-curve/Ebbinghaus rationale moves to the AI Memory
  profile.
- **[Profile]**: All memory-specific normative material (decay tuning, episodic
  *session* framing, retrieval embeddings, and the Mem0/Zep/Letta/Subcog/
  Basic-Memory migration guides) moves out of the core into
  `profiles/ai-memory/`.

### Added

- **[OKF]**: `docs/okf-conformance.md` — pinned OKF v0.1 conformance criteria
  (version-stamped) and the MIF → OKF mapping. MIF takes no normative dependency
  on OKF's live draft (Invariant 5).
- **[OKF]**: Reserved filenames `index.md` / `log.md` adopted verbatim.
- **[Positioning]**: "MIF answers OKF's open questions" table in both
  `README.md` and `SPECIFICATION.md`.
- **[Tooling]**: `scripts/okf_validate.py` (conformance + relationship sync +
  round-trip), `scripts/mif_convert.py` (markdown↔json-ld), and
  `scripts/migrate_0_1_to_1_0.py` (0.1→1.0 transform).
- **[Profile]**: `profiles/ai-memory/` — profile spec, ontology, and examples.
- **[Docs]**: `MIGRATION.md` upgrade guide (`0.1.0-draft → 1.0.0`).
- **[CI]**: `validate.yml` runs the OKF conformance + lossless round-trip tests
  and validates the JSON-LD projection against the schema.
- **[Tooling]**: `scripts/okf_validate.py` gains a temporal-consistency check — a
  `derived-from` / `supersedes` / `cites` target must not be `created` after the
  concept that derives from it. Warns by default; `--strict-temporal` promotes it
  to a failing check once a corpus is known clean. (#79)
- **[Schema]**: first-class scalar `properties` field (string / number / boolean /
  null) for literal-object knowledge-graph triples that have no concept `target`.
  Additive and backward compatible. (#79)
- **[Schema]**: additive versioned schema mirrors under `public/schema/` —
  `1.0.0/` (immutable), `latest/`, major alias `v1/`, plus `index.json` (catalog)
  and `VERSIONING.md`. Canonical `$id` values are unchanged (ADR-007). (#72)
- **[Schema]**: immutable `0.1.0/` schema mirror and `v0/` alias snapshotted from
  the v0.1.0 tag; `index.json` extended (`v0` → 0.1.0, `v1` → 1.0.0). (#73)
- **[CI]**: `schema-check.yml` — meta-validates every schema set as JSON Schema
  2020-12, parses all JSON-LD contexts, and verifies mirror alias consistency
  (`latest` == canonical, `v1` == 1.0.0, `v0` == 0.1.0) as a required gate. (#75)
- **[Brand]**: `mif-brand` applied to the spec site — chevron-M logos, two-accent
  brand CSS, favicon. (#72)

### Changed

- **[Ontology]**: Base ontology re-motivated as a general knowledge taxonomy
  (declarative / time-bound / how-to); memory-only framing removed.
- **[Examples]**: Core `examples/` regenerated as a generalized (non-memory)
  bundle; memory examples relocated to `profiles/ai-memory/examples/`.
- **[Docs]**: ecosystem docs rehomed from the spec site to `doc-site`; the
  Starlight spec site is trimmed to spec-only content (sidebar and index). (#72)
- **[CI]**: `validate.yml` actions are SHA-pinned (org policy) and the workflow
  runs on all pull requests (PR path filter removed) so it can serve as a required
  gate. (#74)

### Removed

- **[Tooling]**: `scripts/validate-memories.py` and `scripts/test-conversion.py`
  superseded by `okf_validate.py` + `mif_convert.py`.

### Fixed

- **[Tooling]**: `scripts/mif_convert.py` restores `compressedAt` and `memoryType`
  to the round-trip passthrough; both were silently dropped on
  `markdown → json-ld → markdown`, breaking the lossless invariant. A regression
  test now enumerates every top-level schema field so a dropped field fails CI. (#79)
- **[Tooling]**: the temporal check skips targets that resolve outside the bundle
  (no out-of-bundle reads) and no longer crashes on a malformed-YAML target. (#79)

### Migration

See [MIGRATION.md](MIGRATION.md) and run
`python scripts/migrate_0_1_to_1_0.py <old> <new>`.

## [0.1.0] - 2026-01-23

### Added

- Initial project setup
- MIF specification draft v0.1
- Market research framework

[Unreleased]: https://github.com/zircote/MIF/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/zircote/MIF/releases/tag/v0.1.0
