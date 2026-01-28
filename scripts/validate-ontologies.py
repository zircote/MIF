#!/usr/bin/env python3
"""Validate ontology YAML files against the ontology JSON schema."""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def load_schema(schema_path: Path) -> dict:
    """Load JSON schema from file."""
    with open(schema_path) as f:
        return json.load(f)


def load_yaml(yaml_path: Path) -> dict:
    """Load YAML file."""
    with open(yaml_path) as f:
        return yaml.safe_load(f)


def validate_ontology(ontology_path: Path, schema: dict) -> list[str]:
    """Validate a single ontology file against the schema."""
    errors = []
    try:
        ontology = load_yaml(ontology_path)
        validator = Draft202012Validator(schema)
        for error in validator.iter_errors(ontology):
            errors.append(f"  - {error.json_path}: {error.message}")
    except yaml.YAMLError as e:
        errors.append(f"  - YAML parse error: {e}")
    except Exception as e:
        errors.append(f"  - Unexpected error: {e}")
    return errors


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / "schema" / "ontology" / "ontology.schema.json"
    ontology_dirs = [
        repo_root / "ontologies",
        repo_root / "ontologies" / "examples",
    ]

    if not schema_path.exists():
        print(f"ERROR: Schema not found: {schema_path}")
        sys.exit(1)

    schema = load_schema(schema_path)
    all_errors = {}

    for ontology_dir in ontology_dirs:
        if not ontology_dir.exists():
            continue
        for ontology_file in ontology_dir.glob("*.ontology.yaml"):
            errors = validate_ontology(ontology_file, schema)
            if errors:
                rel_path = ontology_file.relative_to(repo_root)
                all_errors[str(rel_path)] = errors

    if all_errors:
        print("Ontology validation FAILED:")
        for file_path, errors in all_errors.items():
            print(f"\n{file_path}:")
            for error in errors:
                print(error)
        sys.exit(1)
    else:
        print("All ontology files validated successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
