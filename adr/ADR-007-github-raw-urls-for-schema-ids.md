# ADR-007: GitHub Raw URLs for Schema IDs

## Status

Accepted

## Date

2026-01-27

## Context

JSON Schema requires `$id` values to be URIs. Options considered:

1. **Custom domain** (e.g., `https://mif.io/schema/...`)
   - Requires domain registration and hosting
   - Single point of failure
   - Ongoing maintenance cost

2. **JSON-LD standard namespaces** (e.g., `http://schema.org/...`)
   - Not appropriate for custom schemas
   - Would require schema.org integration

3. **URN namespace** (e.g., `urn:mif:schema:...`)
   - Not resolvable
   - Requires separate resolution mechanism

4. **GitHub raw URLs** (e.g., `https://raw.githubusercontent.com/...`)
   - Automatically resolvable
   - Zero hosting cost
   - Version control via branches/tags
   - Community-accessible

## Decision

Use **GitHub raw content URLs** for all schema `$id` values:

```
https://mif-spec.dev/schema/mif.schema.json
https://mif-spec.dev/schema/ontology/ontology.schema.json
https://mif-spec.dev/schema/context.jsonld
```

## Consequences

### Positive
- Immediately resolvable by any HTTP client
- No infrastructure to maintain
- Free, reliable GitHub CDN
- Natural versioning via git refs (`main`, `v0.1.0`, etc.)
- Open source transparency
- Community can fork and modify

### Negative
- Dependency on GitHub availability
- URLs are verbose
- Repository rename would break URLs (mitigated by stability commitment)
- Rate limits for heavy consumers (mitigated by caching)

## Implementation Notes

- Use `main` branch for latest stable schemas
- Use tags (e.g., `v0.1.0`) for version-specific URLs
- JSON-LD `@context` references same URL pattern
- Schema `$ref` uses relative paths within repository

## Migration History

Originally used placeholder domains:
- ~~`mif.io`~~ → Never existed (hallucinated)
- ~~`subcog.io`~~ → Never existed (hallucinated)
- ~~`subcog.dev`~~ → Never existed (hallucinated)

All replaced with GitHub raw URLs in v0.1.0.
