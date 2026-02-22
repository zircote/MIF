#!/usr/bin/env bash
# scaffold_ontology.sh - Generate a new MIF ontology skeleton
#
# Usage: scaffold_ontology.sh <id> <version> [--extends base1,base2]
#        scaffold_ontology.sh my-domain 0.1.0
#        scaffold_ontology.sh my-domain 0.1.0 --extends mif-base
#
# Outputs valid YAML to stdout. Redirect to file:
#   scaffold_ontology.sh my-domain 0.1.0 > my-domain.ontology.yaml
set -euo pipefail

usage() {
	echo "Usage: $0 <id> <version> [--extends base1,base2]"
	echo ""
	echo "  id       Ontology ID (lowercase, hyphens)"
	echo "  version  Semver version (e.g. 0.1.0)"
	echo "  --extends  Comma-separated parent ontology IDs"
	exit 1
}

[[ $# -lt 2 ]] && usage

ID="$1"
VERSION="$2"
shift 2
EXTENDS=""

while [[ $# -gt 0 ]]; do
	case "$1" in
	--extends)
		EXTENDS="$2"
		shift 2
		;;
	*) usage ;;
	esac
done

# Validate ID format
if [[ ! "$ID" =~ ^[a-z][a-z0-9-]*$ ]]; then
	echo "Error: ID '$ID' must match ^[a-z][a-z0-9-]*$" >&2
	exit 1
fi

# Validate version format
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
	echo "Error: Version '$VERSION' must be semver (X.Y.Z)" >&2
	exit 1
fi

# Build extends block
EXTENDS_BLOCK=""
if [[ -n "$EXTENDS" ]]; then
	EXTENDS_BLOCK=$'\n  extends:'
	IFS=',' read -ra BASES <<<"$EXTENDS"
	for base in "${BASES[@]}"; do
		EXTENDS_BLOCK+=$'\n'"    - $base"
	done
fi

cat <<EOF
---
# MIF Ontology: $ID
#
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# Schema: https://mif-spec.dev/schema/ontology/ontology.schema.json

ontology:
  id: $ID
  version: "$VERSION"
  description: >-
    TODO: Describe this ontology
  schema_url: >-
    https://mif-spec.dev/schema/ontology/ontology.schema.json${EXTENDS_BLOCK}

# Namespace Hierarchy (Cognitive Triad)
namespaces:
  _semantic:
    description: >-
      Facts, concepts, relationships
    type_hint: semantic
    children:
      decisions:
        description: >-
          Architectural and design choices
        type_hint: semantic
      knowledge:
        description: >-
          Domain knowledge and learnings
        type_hint: semantic

  _episodic:
    description: >-
      Events, experiences, timelines
    type_hint: episodic
    children:
      incidents:
        description: >-
          Issues and incident reports
        type_hint: episodic

  _procedural:
    description: >-
      Step-by-step processes
    type_hint: procedural
    children:
      patterns:
        description: >-
          Conventions and best practices
        type_hint: procedural

# Entity Types
entity_types:
  - name: example-entity
    description: >-
      TODO: Describe this entity type
    base: semantic
    traits:
      - timestamped
      - confidence
    schema:
      required:
        - name
      properties:
        name:
          type: string
          description: >-
            Entity name

# Traits (reusable mixins)
traits:
  timestamped:
    description: >-
      Adds creation and update timestamps
    fields:
      created_at:
        type: string
        format: date-time
        description: >-
          When created
      updated_at:
        type: string
        format: date-time
        description: >-
          When last updated

  confidence:
    description: >-
      Adds confidence score
    fields:
      confidence:
        type: number
        description: >-
          Confidence score (0.0-1.0)

# Relationships
relationships:
  relates_to:
    description: >-
      General association
    from: []
    to: []
    symmetric: true

  derived_from:
    description: >-
      Derived from another memory
    from: []
    to: []
    symmetric: false

# Discovery Patterns
discovery:
  enabled: true
  confidence_threshold: 0.8
  content_patterns: []
  file_patterns: []
EOF
