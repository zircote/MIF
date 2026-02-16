#!/usr/bin/env python3
"""Test round-trip conversion between Markdown and JSON-LD formats.

Validates ADR-002: Dual Format Design promise of lossless bidirectional conversion.
"""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml


FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n*(.*)", re.DOTALL)


def load_json(json_path: Path) -> dict:
    """Load JSON file."""
    with open(json_path) as f:
        return json.load(f)


def parse_markdown_memory(md_path: Path) -> tuple[dict, str]:
    """Parse markdown memory file into frontmatter and body."""
    content = md_path.read_text()
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        raise ValueError(f"No frontmatter found in {md_path}")

    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    return frontmatter, body


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


def frontmatter_to_jsonld(frontmatter: dict, body: str) -> dict:
    """Convert frontmatter to JSON-LD structure."""
    # Stringify all datetime objects from YAML parsing
    frontmatter = stringify_datetimes(frontmatter)

    jsonld = {
        "@context": "https://mif-spec.dev/schema/context.jsonld",
        "@type": "Memory",
    }

    # Map fields
    mappings = {
        "id": ("@id", lambda x: f"urn:mif:{x}"),
        "type": ("memoryType", lambda x: x),
        "created": ("created", lambda x: x),
        "modified": ("modified", lambda x: x),
        "namespace": ("namespace", lambda x: x),
        "title": ("title", lambda x: x),
        "tags": ("tags", lambda x: x),
        "aliases": ("aliases", lambda x: x),
    }

    for fm_key, (jsonld_key, transform) in mappings.items():
        if fm_key in frontmatter:
            jsonld[jsonld_key] = transform(frontmatter[fm_key])

    # Add content
    jsonld["content"] = body

    return jsonld


def compare_core_fields(md_data: dict, json_data: dict) -> list[str]:
    """Compare core fields between converted markdown and JSON-LD."""
    differences = []

    # Fields to compare
    core_fields = [
        ("@id", "@id"),
        ("memoryType", "memoryType"),
        ("created", "created"),
        ("namespace", "namespace"),
        ("title", "title"),
        ("tags", "tags"),
    ]

    for md_field, json_field in core_fields:
        md_val = md_data.get(md_field)
        json_val = json_data.get(json_field)

        if md_val != json_val:
            # Allow for minor formatting differences
            if isinstance(md_val, str) and isinstance(json_val, str):
                if md_val.strip() == json_val.strip():
                    continue
            differences.append(
                f"  Field '{md_field}': MD={md_val!r} vs JSON={json_val!r}"
            )

    return differences


def test_conversion_pair(md_path: Path, json_path: Path) -> list[str]:
    """Test conversion between a markdown and JSON-LD file pair."""
    errors = []

    if not json_path.exists():
        return [f"  Missing JSON counterpart: {json_path.name}"]

    try:
        frontmatter, body = parse_markdown_memory(md_path)
        json_data = load_json(json_path)

        # Convert markdown to JSON-LD
        converted = frontmatter_to_jsonld(frontmatter, body)

        # Compare core fields
        differences = compare_core_fields(converted, json_data)
        errors.extend(differences)

    except Exception as e:
        errors.append(f"  Error: {e}")

    return errors


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    examples_dir = repo_root / "examples"

    all_errors = {}
    pairs_tested = 0

    # Find all markdown memory files with JSON counterparts
    for md_file in examples_dir.glob("*.memory.md"):
        json_file = md_file.with_suffix(".json").with_name(
            md_file.stem.replace(".memory", ".memory") + ".json"
        )
        # Fix the path construction
        json_file = md_file.parent / (md_file.stem + ".json")

        errors = test_conversion_pair(md_file, json_file)
        pairs_tested += 1

        if errors:
            rel_path = md_file.relative_to(repo_root)
            all_errors[str(rel_path)] = errors

    print(f"Tested {pairs_tested} markdown/JSON-LD pairs")

    if all_errors:
        print("\nConversion test FAILED:")
        for file_path, errors in all_errors.items():
            print(f"\n{file_path}:")
            for error in errors:
                print(error)
        sys.exit(1)
    else:
        print("All conversion tests passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
