#!/usr/bin/env python3
"""Validate bookkeeping in a V3R1T4S inference experiment manifest."""
import json
import re
import sys
from pathlib import Path

HEX64 = re.compile(r"^sha256:[0-9a-f]{64}$")


def validate(data):
    errors = []
    required = {
        "schema_version", "experiment_id", "source", "model", "environment",
        "workload", "arms", "measurements", "quality_gate", "deviations", "limitations",
    }
    missing = sorted(required - data.keys())
    if missing:
        return ["missing top-level fields: " + ", ".join(missing)]
    if data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not isinstance(data["experiment_id"], str) or not data["experiment_id"].strip():
        errors.append("experiment_id must be a non-empty string")
    for group, fields in {
        "source": ("repository", "revision", "runner_version", "runtime"),
        "environment": ("hardware", "os", "software"),
        "workload": ("request_set_sha256", "request_count", "order", "concurrency", "warmup_requests", "decoding", "quality_rubric"),
        "arms": ("baseline", "intervention"),
        "measurements": ("raw_results_path_or_public_safe_uri", "raw_results_sha256", "record_per_request", "includes_queueing_in_end_to_end"),
        "quality_gate": ("threshold", "baseline_passed", "intervention_passed"),
    }.items():
        if not isinstance(data[group], dict):
            errors.append(f"{group} must be an object")
            continue
        for field in fields:
            if field not in data[group]:
                errors.append(f"{group}.{field} is required")
    for arm in ("baseline", "intervention"):
        value = data["arms"].get(arm)
        if isinstance(value, dict):
            for field in ("name", "command", "configuration_sha256"):
                if not value.get(field):
                    errors.append(f"arms.{arm}.{field} must be non-empty")
    workload = data["workload"]
    if isinstance(workload, dict):
        for field in ("request_count", "concurrency"):
            if not isinstance(workload.get(field), int) or workload[field] < 1:
                errors.append(f"workload.{field} must be a positive integer")
        if not isinstance(workload.get("warmup_requests"), int) or workload["warmup_requests"] < 0:
            errors.append("workload.warmup_requests must be a non-negative integer")
        if not HEX64.fullmatch(str(workload.get("request_set_sha256", ""))):
            errors.append("workload.request_set_sha256 must be sha256 plus 64 lowercase hex digits")
    measurements = data["measurements"]
    if isinstance(measurements, dict):
        if measurements.get("record_per_request") is not True:
            errors.append("measurements.record_per_request must be true")
        if measurements.get("includes_queueing_in_end_to_end") is not True:
            errors.append("measurements.includes_queueing_in_end_to_end must be true")
        if not HEX64.fullmatch(str(measurements.get("raw_results_sha256", ""))):
            errors.append("measurements.raw_results_sha256 must be sha256 plus 64 lowercase hex digits")
    if not isinstance(data["deviations"], list) or not isinstance(data["limitations"], list):
        errors.append("deviations and limitations must be lists")
    return errors


def main(argv):
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} MANIFEST.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2
    errors = validate(data) if isinstance(data, dict) else ["manifest root must be an object"]
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID (bookkeeping only; no performance claim verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
