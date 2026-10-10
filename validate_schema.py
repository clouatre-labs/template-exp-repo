"""
Validate schema of experiment analysis.json files.

Checks that every experiments/*/analysis.json contains the required
top-level fields and run records with the expected structure. Certain
fields are nullable (allowed to be null) while others must have values.

Usage:
    uv run python validate_schema.py [--self-test] [FILE ...]

With no FILE arguments, discovers and validates all
experiments/*/analysis.json files under the repository root.

Exits with 0 if all files pass validation, 1 if any validation fails.
"""

import json
import pathlib
import sys

# Top-level fields that are allowed to be null.
NULLABLE_TOP_FIELDS = {"issue", "orchestrator_session"}

# Run-record fields that are allowed to be null.
NULLABLE_RUN_FIELDS = {"bytes", "note"}

REQUIRED_TOP_FIELDS = [
    "experiment",
    "schema_version",
    "title",
    "issue",
    "date",
    "model",
    "n_per_group",
    "control_condition",
    "treatment_condition",
    "rubric_version",
    "orchestrator_session",
    "repo_head",
    "experiment_start",
    "experiment_end",
    "analyzed_at",
    "runs",
    "scores",
    "statistical_test",
    "conclusion",
    "pre_acknowledged_limitations",
]

REQUIRED_RUN_FIELDS = [
    "group",
    "session_id",
    "messages",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "wall_clock_seconds",
    "bytes",
]


def validate_top_level(data, required_fields):
    missing = []
    for field in required_fields:
        if field not in data:
            missing.append(field)
        elif data[field] is None and field not in NULLABLE_TOP_FIELDS:
            missing.append(field)
    return missing


def validate_runs(runs, required_run_fields):
    errors = []
    if not isinstance(runs, dict):
        return [f"runs is not an object: {type(runs).__name__}"]
    for run_id, record in runs.items():
        if not isinstance(record, dict):
            errors.append(f"run {run_id} is not an object")
            continue
        for field in required_run_fields:
            if field not in record:
                errors.append(f"run {run_id} missing {field}")
            elif record[field] is None and field not in NULLABLE_RUN_FIELDS:
                errors.append(f"run {run_id} has null {field}")
    return errors


def validate_record(data):
    if not isinstance(data, dict):
        return [f"top-level JSON value is not an object: {type(data).__name__}"]
    errors = validate_top_level(data, REQUIRED_TOP_FIELDS)
    errors.extend(validate_runs(data.get("runs"), REQUIRED_RUN_FIELDS))
    return errors


def validate_path(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Failed to load {path}: {exc}")
        return False
    errors = validate_record(data)
    if errors:
        print(f"{path}: {errors}")
        return False
    return True


MINIMAL_VALID_RECORD = {
    "experiment": "exp-example",
    "schema_version": "1.0.0",
    "title": "Example Experiment",
    "issue": None,
    "date": "2026-01-01",
    "model": "model-under-test",
    "n_per_group": 5,
    "control_condition": "standard instructions",
    "treatment_condition": "modified instructions",
    "rubric_version": "rubric-v1",
    "orchestrator_session": None,
    "repo_head": "0000000000000000000000000000000000000000",
    "experiment_start": "2026-01-01T00:00:00Z",
    "experiment_end": "2026-01-01T01:00:00Z",
    "analyzed_at": "2026-01-02T00:00:00Z",
    "runs": {
        "control-1": {
            "group": "control",
            "session_id": "20260101_01",
            "messages": 10,
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "wall_clock_seconds": 30,
            "bytes": 1024,
            "note": None,
        }
    },
    "scores": {"control-1": {"pass": True}},
    "statistical_test": "fisher-exact",
    "conclusion": "No effect observed.",
    "pre_acknowledged_limitations": ["small sample size"],
}


def self_test():
    if validate_record(MINIMAL_VALID_RECORD):
        print("self-test FAILED: minimal valid record reported errors")
        return False
    malformed = json.loads(json.dumps(MINIMAL_VALID_RECORD))
    del malformed["title"]
    malformed["runs"]["control-1"]["total_tokens"] = None
    errors = validate_record(malformed)
    if "title" not in errors or "run control-1 has null total_tokens" not in errors:
        print(f"self-test FAILED: malformed record not caught: {errors}")
        return False
    array_errors = validate_record([MINIMAL_VALID_RECORD])
    if array_errors != ["top-level JSON value is not an object: list"]:
        print(f"self-test FAILED: JSON array not rejected: {array_errors}")
        return False
    scalar_errors = validate_record("not-an-object")
    if scalar_errors != ["top-level JSON value is not an object: str"]:
        print(f"self-test FAILED: JSON scalar not rejected: {scalar_errors}")
        return False
    print(
        "self-test passed: valid record accepted, malformed record rejected,"
        " non-mapping values rejected"
    )
    return True


def main():
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    file_args = [arg for arg in sys.argv[1:] if arg != "--self-test"]
    if file_args:
        all_ok = all(validate_path(pathlib.Path(arg)) for arg in file_args)
        sys.exit(0 if all_ok else 1)
    base = pathlib.Path(".").resolve()
    paths = sorted((base / "experiments").glob("*/analysis.json"))
    if not paths:
        print("No experiments/*/analysis.json files found; nothing to validate.")
        sys.exit(0)
    all_ok = all(validate_path(p) for p in paths)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
