#!/usr/bin/env bash
# convert_format.sh - Convert MIF ontology between formats
#
# Usage:
#   convert_format.sh yaml2json <input.yaml> [output.json]
#   convert_format.sh json2yaml <input.json> [output.yaml]
#   convert_format.sh yaml2jsonld <input.yaml> [output.jsonld]
#
# Requires: yq, jq
# For yaml2jsonld: also requires python3 + pyyaml
set -euo pipefail

MODE="${1:?Usage: convert_format.sh <yaml2json|json2yaml|yaml2jsonld> <input> [output]}"
INPUT="${2:?Usage: convert_format.sh <mode> <input> [output]}"
OUTPUT="${3:-}"

if [[ ! -f "$INPUT" ]]; then
	echo "Error: File not found: $INPUT" >&2
	exit 1
fi

case "$MODE" in
yaml2json)
	# Default output: replace .yaml with .json
	if [[ -z "$OUTPUT" ]]; then
		OUTPUT="${INPUT%.ontology.yaml}.ontology.json"
		[[ "$OUTPUT" == "$INPUT" ]] && OUTPUT="${INPUT%.yaml}.json"
	fi
	yq -o=json '.' "$INPUT" | jq '.' >"$OUTPUT"
	echo "Converted: $INPUT -> $OUTPUT"
	;;

json2yaml)
	# Default output: replace .json with .yaml
	if [[ -z "$OUTPUT" ]]; then
		OUTPUT="${INPUT%.ontology.json}.ontology.yaml"
		[[ "$OUTPUT" == "$INPUT" ]] && OUTPUT="${INPUT%.json}.yaml"
	fi
	yq -P '.' "$INPUT" >"$OUTPUT"
	echo "Converted: $INPUT -> $OUTPUT"
	;;

yaml2jsonld)
	# Default output: replace .yaml with .jsonld
	if [[ -z "$OUTPUT" ]]; then
		OUTPUT="${INPUT%.ontology.yaml}.ontology.jsonld"
		[[ "$OUTPUT" == "$INPUT" ]] && OUTPUT="${INPUT%.yaml}.jsonld"
	fi
	# Find MIF project root (contains schema/ dir)
	MIF_ROOT=""
	DIR="$(cd "$(dirname "$INPUT")" && pwd)"
	while [[ "$DIR" != "/" ]]; do
		if [[ -d "$DIR/schema/ontology" ]]; then
			MIF_ROOT="$DIR"
			break
		fi
		DIR="$(dirname "$DIR")"
	done
	if [[ -n "$MIF_ROOT" && -f "$MIF_ROOT/scripts/yaml2jsonld.py" ]]; then
		python3 "$MIF_ROOT/scripts/yaml2jsonld.py" "$INPUT" "$OUTPUT"
	else
		echo "Warning: yaml2jsonld.py not found, using yq fallback" >&2
		echo "  (JSON-LD @context will be minimal)" >&2
		yq -o=json '.' "$INPUT" | jq '{
        "@context": "https://mif-spec.dev/schema/context.jsonld",
        "@type": "mif:Ontology"
      } + .' >"$OUTPUT"
	fi
	echo "Converted: $INPUT -> $OUTPUT"
	;;

*)
	echo "Error: Unknown mode '$MODE'" >&2
	echo "Modes: yaml2json, json2yaml, yaml2jsonld" >&2
	exit 1
	;;
esac
