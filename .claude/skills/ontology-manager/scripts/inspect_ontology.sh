#!/usr/bin/env bash
# inspect_ontology.sh - Introspect an MIF ontology
#
# Usage:
#   inspect_ontology.sh <file.yaml>
#   inspect_ontology.sh <file.yaml> --section entities
#   inspect_ontology.sh <file.yaml> --section namespaces
#   inspect_ontology.sh <file.yaml> --section traits
#   inspect_ontology.sh <file.yaml> --section relationships
#   inspect_ontology.sh <file.yaml> --section discovery
#   inspect_ontology.sh <file.yaml> --json
set -euo pipefail

FILE="${1:?Usage: inspect_ontology.sh <file.yaml> [--section X] [--json]}"
shift
SECTION="all"
JSON=false

while [[ $# -gt 0 ]]; do
	case "$1" in
	--section)
		SECTION="$2"
		shift 2
		;;
	--json)
		JSON=true
		shift
		;;
	*)
		echo "Unknown flag: $1" >&2
		exit 1
		;;
	esac
done

if [[ ! -f "$FILE" ]]; then
	echo "Error: File not found: $FILE" >&2
	exit 1
fi

show_header() {
	local id ver ext et_c tr_c rel_c ns_c dp_c
	id=$(yq -r '.ontology.id // "?"' "$FILE")
	ver=$(yq -r '.ontology.version // "?"' "$FILE")
	ext=$(yq -r '.ontology.extends // [] | join(", ")' "$FILE")
	et_c=$(yq '.entity_types | length' "$FILE" 2>/dev/null || echo 0)
	tr_c=$(yq '.traits | keys | length' "$FILE" 2>/dev/null || echo 0)
	rel_c=$(yq '.relationships | keys | length' "$FILE" 2>/dev/null || echo 0)
	ns_c=$(yq '[.namespaces | .. | .children? // "" | keys | .[]] | length' "$FILE" 2>/dev/null || echo 0)
	dp_c=$(yq '[.discovery.content_patterns // [], .discovery.file_patterns // [], .discovery.patterns // []] | flatten | length' "$FILE" 2>/dev/null || echo 0)

	echo "Ontology: $id v$ver"
	[[ -n "$ext" ]] && echo "Extends:  $ext"
	echo "Entities: $et_c | Traits: $tr_c | Relationships: $rel_c"
	echo "Namespaces: $ns_c (children) | Discovery: $dp_c patterns"
	echo "---"
}

show_namespaces() {
	echo "NAMESPACES:"
	yq -r '
    .namespaces | to_entries[] |
    "  " + .key + " (" + (.value.type_hint // "?") + ")" +
    (if .value.children then
      "\n" + (
        .value.children | to_entries[] |
        "    " + .key + " - " +
        (.value.description // "no description")
      )
    else "" end)
  ' "$FILE" 2>/dev/null
}

show_entities() {
	echo "ENTITY TYPES:"
	yq -r '
    .entity_types[] |
    "  " + .name + " [" + .base + "]" +
    (if .traits then
      " traits=" + (.traits | join(","))
    else "" end) +
    (if .description then
      "\n    " + .description
    else "" end)
  ' "$FILE" 2>/dev/null
}

show_traits() {
	echo "TRAITS:"
	yq -r '
    .traits | to_entries[] |
    "  " + .key +
    (if .value.fields then
      " fields=" +
      (.value.fields | keys | join(","))
    else "" end) +
    (if .value.description then
      "\n    " + .value.description
    else "" end)
  ' "$FILE" 2>/dev/null
}

show_relationships() {
	echo "RELATIONSHIPS:"
	yq -r '
    .relationships | to_entries[] |
    "  " + .key +
    (if .value.symmetric then " [symmetric]"
    else " [directed]" end) +
    (if .value.from and (.value.from | length) > 0 then
      " from=" + (.value.from | join(","))
    else "" end) +
    (if .value.to and (.value.to | length) > 0 then
      " to=" + (.value.to | join(","))
    else "" end)
  ' "$FILE" 2>/dev/null
}

show_discovery() {
	echo "DISCOVERY PATTERNS:"
	local enabled threshold
	enabled=$(yq -r '.discovery.enabled // false' "$FILE")
	threshold=$(yq -r '.discovery.confidence_threshold // 0.8' "$FILE")
	echo "  enabled: $enabled  threshold: $threshold"

	echo "  Content patterns:"
	yq -r '
    .discovery.content_patterns[]? |
    "    " +
    (.namespace // (.namespaces | join(","))) +
    " <- /" + .pattern + "/"
  ' "$FILE" 2>/dev/null || true

	echo "  File patterns:"
	yq -r '
    .discovery.file_patterns[]? |
    "    " +
    (.namespaces | join(",")) +
    " <- /" + .pattern + "/"
  ' "$FILE" 2>/dev/null || true
}

# JSON output mode
if $JSON; then
	case "$SECTION" in
	entities)
		yq -o=json '.entity_types' "$FILE" | jq '.'
		;;
	namespaces)
		yq -o=json '.namespaces' "$FILE" | jq '.'
		;;
	traits)
		yq -o=json '.traits' "$FILE" | jq '.'
		;;
	relationships)
		yq -o=json '.relationships' "$FILE" | jq '.'
		;;
	discovery)
		yq -o=json '.discovery' "$FILE" | jq '.'
		;;
	all | *)
		yq -o=json '.' "$FILE" | jq '.'
		;;
	esac
	exit 0
fi

# Text output
case "$SECTION" in
entities)
	show_header
	show_entities
	;;
namespaces)
	show_header
	show_namespaces
	;;
traits)
	show_header
	show_traits
	;;
relationships)
	show_header
	show_relationships
	;;
discovery)
	show_header
	show_discovery
	;;
all | *)
	show_header
	show_namespaces
	echo
	show_entities
	echo
	show_traits
	echo
	show_relationships
	echo
	show_discovery
	;;
esac
