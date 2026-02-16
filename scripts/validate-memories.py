#!/usr/bin/env python3
"""Validate memory file frontmatter against the MIF schema."""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def stringify_datetimes(obj):
    """Recursively convert datetime/date objects to ISO 8601 strings."""
    if isinstance(obj, datetime):
        s = obj.isoformat()
        return s.replace("+00:00", "Z")
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: stringify_datetimes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [stringify_datetimes(item) for item in obj]
    return obj


# Mapping from snake_case frontmatter keys to camelCase JSON-LD keys
TEMPORAL_KEY_MAP = {
    "valid_from": "validFrom",
    "valid_until": "validUntil",
    "recorded_at": "recordedAt",
    "access_count": "accessCount",
    "last_accessed": "lastAccessed",
}

DECAY_KEY_MAP = {
    "last_reinforced": "lastReinforced",
}

EMBEDDING_KEY_MAP = {
    "model_version": "modelVersion",
    "source_text": "sourceText",
}

PROVENANCE_KEY_MAP = {
    "source_type": "sourceType",
    "trust_level": "trustLevel",
}


def remap_keys(obj, key_map):
    """Remap dictionary keys using a mapping."""
    if not isinstance(obj, dict):
        return obj
    return {key_map.get(k, k): v for k, v in obj.items()}


def transform_citation(citation):
    """Transform a frontmatter citation to JSON-LD Citation format."""
    result = {"@type": "Citation"}
    key_map = {"type": "citationType", "role": "citationRole"}
    for k, v in citation.items():
        result[key_map.get(k, k)] = v
    return result


def load_schema(schema_path: Path) -> dict:
    """Load JSON schema from file."""
    with open(schema_path) as f:
        return json.load(f)


def extract_frontmatter(memory_path: Path) -> dict | None:
    """Extract YAML frontmatter from a memory file."""
    content = memory_path.read_text()
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def create_memory_from_frontmatter(frontmatter: dict, content: str) -> dict:
    """Convert frontmatter to JSON-LD-like structure for validation."""
    # Stringify all datetime objects from YAML parsing
    frontmatter = stringify_datetimes(frontmatter)

    # Map frontmatter fields to schema fields
    memory = {
        "@context": "https://mif-spec.dev/schema/context.jsonld",
        "@type": "Memory",
    }

    # Direct mappings
    field_map = {
        "id": "@id",
        "type": "memoryType",
        "created": "created",
        "modified": "modified",
        "namespace": "namespace",
        "title": "title",
        "tags": "tags",
        "aliases": "aliases",
        "temporal": "temporal",
        "provenance": "provenance",
        "embedding": "embedding",
        "entities": "entities",
        "relationships": "relationships",
        "citations": "citations",
        "blocks": "blocks",
        "extensions": "extensions",
    }

    for fm_key, schema_key in field_map.items():
        if fm_key in frontmatter:
            value = frontmatter[fm_key]
            if fm_key == "id":
                value = f"urn:mif:{value}"
            elif fm_key == "temporal":
                value = remap_keys(value, TEMPORAL_KEY_MAP)
                if "decay" in value and isinstance(value["decay"], dict):
                    value["decay"] = remap_keys(value["decay"], DECAY_KEY_MAP)
            elif fm_key == "embedding":
                value = remap_keys(value, EMBEDDING_KEY_MAP)
            elif fm_key == "provenance":
                value = remap_keys(value, PROVENANCE_KEY_MAP)
            elif fm_key == "citations" and isinstance(value, list):
                value = [transform_citation(c) for c in value]
            memory[schema_key] = value

    # Extract content from markdown body
    memory["content"] = content

    return memory


def validate_memory(memory_path: Path, schema: dict) -> list[str]:
    """Validate a single memory file against the schema."""
    errors = []

    frontmatter = extract_frontmatter(memory_path)
    if frontmatter is None:
        errors.append("  - Could not parse frontmatter")
        return errors

    # Get content after frontmatter
    content = memory_path.read_text()
    match = FRONTMATTER_PATTERN.match(content)
    if match:
        body = content[match.end() :].strip()
    else:
        body = ""

    memory = create_memory_from_frontmatter(frontmatter, body)

    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(memory):
        # Skip errors about missing content if we extracted it
        if "content" in error.json_path and body:
            continue
        errors.append(f"  - {error.json_path}: {error.message}")

    return errors


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / "schema" / "mif.schema.json"
    memory_dirs = [
        repo_root / "examples",
        repo_root / "ontologies" / "examples" / "memories",
    ]

    if not schema_path.exists():
        print(f"ERROR: Schema not found: {schema_path}")
        sys.exit(1)

    schema = load_schema(schema_path)
    all_errors = {}

    for memory_dir in memory_dirs:
        if not memory_dir.exists():
            continue
        for memory_file in memory_dir.rglob("*.memory.md"):
            errors = validate_memory(memory_file, schema)
            if errors:
                rel_path = memory_file.relative_to(repo_root)
                all_errors[str(rel_path)] = errors

    if all_errors:
        print("Memory frontmatter validation FAILED:")
        for file_path, errors in all_errors.items():
            print(f"\n{file_path}:")
            for error in errors:
                print(error)
        sys.exit(1)
    else:
        print("All memory frontmatter validated successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
