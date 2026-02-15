#!/usr/bin/env python3
"""Validate memory file frontmatter against the MIF schema."""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


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
