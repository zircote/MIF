#!/usr/bin/env bash
# validate_ontology.sh - Validate MIF ontology YAML
#
# Usage: validate_ontology.sh <ontology.yaml> [schema.json]
#
# Validates:
#   - YAML syntax (yq)
#   - Required fields: ontology.id, ontology.version
#   - ID format: ^[a-z][a-z0-9-]*$
#   - Version format: semver (X.Y.Z)
#   - Base types: semantic|episodic|procedural
#   - Trait references resolve
#   - Entity type name format
#   - Discovery pattern regex validity
#   - JSON Schema compliance (if schema provided)
set -euo pipefail

FILE="${1:?Usage: validate_ontology.sh <file.yaml> [schema.json]}"
SCHEMA="${2:-}"
ERRORS=0
WARNINGS=0

err() {
	echo "  ERROR: $1"
	ERRORS=$((ERRORS + 1))
}
warn() {
	echo "  WARN:  $1"
	WARNINGS=$((WARNINGS + 1))
}
ok() { echo "  OK:    $1"; }

echo "Validating: $FILE"
echo "---"

# 1. File exists
if [[ ! -f "$FILE" ]]; then
	err "File not found: $FILE"
	exit 1
fi

# 2. Valid YAML
if ! yq '.' "$FILE" >/dev/null 2>&1; then
	err "Invalid YAML syntax"
	yq '.' "$FILE" 2>&1 | head -5
	exit 1
fi
ok "Valid YAML syntax"

# 3. Required: ontology.id
ID=$(yq -r '.ontology.id // ""' "$FILE")
if [[ -z "$ID" ]]; then
	err "Missing required field: ontology.id"
else
	if [[ "$ID" =~ ^[a-z][a-z0-9-]*$ ]]; then
		ok "ontology.id: $ID"
	else
		err "ontology.id '$ID' must match ^[a-z][a-z0-9-]*$"
	fi
fi

# 4. Required: ontology.version
VER=$(yq -r '.ontology.version // ""' "$FILE")
if [[ -z "$VER" ]]; then
	err "Missing required field: ontology.version"
else
	if [[ "$VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
		ok "ontology.version: $VER"
	else
		err "ontology.version '$VER' is not valid semver"
	fi
fi

# 5. Namespace type_hint values
NS_HINTS=$(yq -r '
  [.. | .type_hint? // ""] | .[] | select(. != "")
' "$FILE" 2>/dev/null || true)
for hint in $NS_HINTS; do
	case "$hint" in
	semantic | episodic | procedural) ;;
	*) err "Invalid type_hint: '$hint' (must be semantic|episodic|procedural)" ;;
	esac
done
ok "Namespace type_hints validated"

# 6. Entity type checks
ET_COUNT=$(yq -r '.entity_types | length' "$FILE" 2>/dev/null || echo 0)
if [[ "$ET_COUNT" -gt 0 ]]; then
	# Check each entity name format
	yq -r '.entity_types[].name' "$FILE" 2>/dev/null | while read -r name; do
		if [[ -n "$name" && ! "$name" =~ ^[a-z][a-z0-9-]*$ ]]; then
			err "Entity name '$name' must match ^[a-z][a-z0-9-]*$"
		fi
	done
	# Check base types
	yq -r '.entity_types[].base' "$FILE" 2>/dev/null | while read -r base; do
		case "$base" in
		semantic | episodic | procedural) ;;
		*) err "Entity base '$base' invalid (must be semantic|episodic|procedural)" ;;
		esac
	done
	ok "Entity types: $ET_COUNT defined"
fi

# 7. Trait reference check
DEFINED_TRAITS=$(yq -r '.traits | keys | .[]' "$FILE" 2>/dev/null || true)
HAS_EXTENDS=$(yq -r '.ontology.extends | length' "$FILE" 2>/dev/null || echo 0)

USED_TRAITS=$(yq -r '.entity_types[].traits[]?' "$FILE" 2>/dev/null || true)
for trait in $USED_TRAITS; do
	if ! echo "$DEFINED_TRAITS" | grep -qx "$trait"; then
		if [[ "$HAS_EXTENDS" -eq 0 ]]; then
			err "Trait '$trait' referenced but not defined"
		fi
	fi
done
ok "Trait references checked"

# 8. Discovery pattern regex validation
PATTERNS=$(yq -r '
  .discovery.content_patterns[]?.pattern // "",
  .discovery.patterns[]?.content_pattern // ""
' "$FILE" 2>/dev/null || true)
PAT_COUNT=0
PAT_ERR=0
while IFS= read -r pat; do
	[[ -z "$pat" ]] && continue
	PAT_COUNT=$((PAT_COUNT + 1))
	if ! python3 -c "import re; re.compile(r'''$pat''')" 2>/dev/null; then
		err "Invalid regex in discovery pattern: $pat"
		PAT_ERR=$((PAT_ERR + 1))
	fi
done <<<"$PATTERNS"
if [[ "$PAT_COUNT" -gt 0 ]]; then
	ok "Discovery patterns: $PAT_COUNT checked, $PAT_ERR invalid"
fi

# 9. JSON Schema validation (optional)
if [[ -n "$SCHEMA" && -f "$SCHEMA" ]]; then
	echo "---"
	echo "JSON Schema validation against: $SCHEMA"
	# Convert YAML to JSON then validate
	TMPJSON=$(mktemp /tmp/ont-XXXXXX.json)
	trap 'rm -f "$TMPJSON"' EXIT
	yq -o=json '.' "$FILE" >"$TMPJSON"
	# Prefer python3+jsonschema (supports draft 2020-12)
	VALIDATED=false
	if command -v python3 >/dev/null 2>&1; then
		if python3 -c "
import json, sys
try:
    from jsonschema import validate, ValidationError
    with open(sys.argv[1]) as s, open(sys.argv[2]) as d:
        validate(json.load(d), json.load(s))
    print('  OK:    JSON Schema validation passed')
except ValidationError as e:
    print(f'  ERROR: {e.message}')
    sys.exit(1)
except ImportError:
    sys.exit(2)
" "$SCHEMA" "$TMPJSON" 2>&1; then
			VALIDATED=true
		else
			RC=$?
			if [[ "$RC" -eq 1 ]]; then
				ERRORS=$((ERRORS + 1))
				VALIDATED=true
			fi
		fi
	fi
	if ! $VALIDATED && command -v ajv >/dev/null 2>&1; then
		if ajv validate -s "$SCHEMA" -d "$TMPJSON" 2>&1; then
			ok "JSON Schema validation passed"
		else
			err "JSON Schema validation failed"
		fi
		VALIDATED=true
	fi
	if ! $VALIDATED; then
		warn "No JSON Schema validator (pip install jsonschema)"
	fi
fi

# Summary
echo "---"
echo "Result: $ERRORS error(s), $WARNINGS warning(s)"
if [[ "$ERRORS" -gt 0 ]]; then
	echo "Status: INVALID"
	exit 1
else
	echo "Status: VALID"
	exit 0
fi
