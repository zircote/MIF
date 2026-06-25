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


def _entity_types(ontology: dict) -> list[dict]:
    """Normalize entity_types (list, or name-keyed dict) to a list of dicts."""
    ets = ontology.get("entity_types", []) or []
    if isinstance(ets, dict):
        return [{"name": k, **(v or {})} for k, v in ets.items()]
    return [et for et in ets if isinstance(et, dict)]


def check_subtype_of(ontology: dict) -> list[str]:
    """Entity-type subsumption integrity: every `subtype_of` parent must resolve to a
    declared entity type (locally, or — if the ontology `extends` another — possibly an
    ancestor's), no type may be its own subtype, and the subtype_of graph must be acyclic.
    """
    errors: list[str] = []
    ets = _entity_types(ontology)
    names = {et.get("name") for et in ets}
    has_extends = bool((ontology.get("ontology") or ontology).get("extends"))
    parents_map: dict[str, list] = {}
    for et in ets:
        name = et.get("name")
        parents = et.get("subtype_of")
        if not name or not parents:
            continue
        parents_map[name] = parents
        for p in parents:
            if p == name:
                errors.append(f"  - entity_type '{name}': subtype_of cannot reference itself")
            elif p not in names and not has_extends:
                errors.append(
                    f"  - entity_type '{name}': subtype_of parent '{p}' is not a declared "
                    f"entity type and the ontology extends nothing it could come from"
                )
    # Cycle detection over locally-declared subtype edges (DFS with grey/black coloring).
    GREY, BLACK = 1, 2
    color: dict[str, int] = {}

    def dfs(n: str, stack: list[str]) -> None:
        color[n] = GREY
        for p in parents_map.get(n, []):
            if p not in parents_map:
                continue
            if color.get(p) == GREY:
                errors.append(f"  - subtype_of cycle: {' -> '.join(stack + [n, p])}")
            elif color.get(p) is None:
                dfs(p, stack + [n])
        color[n] = BLACK

    for n in list(parents_map):
        if color.get(n) is None:
            dfs(n, [])
    return errors


def validate_ontology(ontology_path: Path, schema: dict) -> list[str]:
    """Validate a single ontology file against the schema."""
    errors = []
    try:
        ontology = load_yaml(ontology_path)
        validator = Draft202012Validator(schema)
        for error in validator.iter_errors(ontology):
            errors.append(f"  - {error.json_path}: {error.message}")
        errors.extend(check_subtype_of(ontology))
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
