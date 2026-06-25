#!/usr/bin/env python3
"""Test entity-type subsumption (`subtype_of`) integrity.

Exercises `check_subtype_of` from validate-ontologies.py against the fixtures in
test/subtype_of/: a valid local subtype and a valid extends-resolved parent pass; a
dangling parent (no extends), a cycle, and a self-reference are each rejected.
"""
import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "validate_ontologies", ROOT / "scripts" / "validate-ontologies.py"
)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _load(name: str) -> dict:
    return yaml.safe_load((ROOT / "test" / "subtype_of" / name).read_text())


CASES = [
    ("valid.ontology.yaml", True),
    ("extended.ontology.yaml", True),
    ("dangling.ontology.yaml", False),
    ("cyclic.ontology.yaml", False),
    ("self.ontology.yaml", False),
]


def main() -> int:
    failed = []
    for fname, should_pass in CASES:
        errs = _mod.check_subtype_of(_load(fname))
        ok = (len(errs) == 0) == should_pass
        verdict = "PASS" if ok else "FAIL"
        expect = "no errors" if should_pass else "errors"
        print(f"{verdict}: {fname} (expected {expect}) -> {errs or 'no errors'}")
        if not ok:
            failed.append(fname)
    if failed:
        print(f"\nsubtype_of integrity test FAILED: {failed}")
        return 1
    print("\nAll subtype_of integrity tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
