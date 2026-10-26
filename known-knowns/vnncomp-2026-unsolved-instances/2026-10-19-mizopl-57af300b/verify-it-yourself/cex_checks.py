"""Persistent counterexample validation artifacts."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import Any, Callable

import onnx
import onnxruntime as ort

SCHEMA_VERSION = 1
CHECKER_VERSION = "vnncomp2026-cex-1"
CPU_PROVIDER = "CPUExecutionProvider"


def check_path_for(ce_path: str | Path) -> Path:
    path = Path(ce_path)
    name = path.name
    if name.endswith(".counterexample.gz"):
        return path.with_name(name[:-3] + ".check.json")
    if name.endswith(".counterexample"):
        return path.with_name(name + ".check.json")
    return path.with_suffix(path.suffix + ".check.json")


def file_sha256(path: str | Path) -> str | None:
    path = Path(path)
    if not path.is_file():
        return None

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_identity(row: list[str] | tuple[str, ...] | None) -> str:
    if row is None:
        return ""
    content = json.dumps(list(row), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def dependency_versions() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "onnx": onnx.__version__,
        "onnxruntime": ort.__version__,
    }


def result_metadata(result: str) -> dict[str, bool | str]:
    if result == "correct":
        return {
            "classification": "correct",
            "establishes_sat": True,
            "score_credit": True,
        }
    if result == "correct_up_to_tolerance":
        return {
            "classification": "correct_with_tolerance",
            "establishes_sat": False,
            "score_credit": True,
        }
    if result == "no_ce":
        return {
            "classification": "missing",
            "establishes_sat": False,
            "score_credit": False,
        }
    if result == "malformed_ce":
        return {
            "classification": "malformed",
            "establishes_sat": False,
            "score_credit": False,
        }
    if result == "unsupported":
        return {
            "classification": "unsupported",
            "establishes_sat": False,
            "score_credit": False,
        }
    return {
        "classification": "incorrect",
        "establishes_sat": False,
        "score_credit": False,
    }


def expected_identity(
    ce_path: str | Path,
    cat: str,
    net: str,
    prop: str,
    benchmark_version: str | None,
    row: list[str] | tuple[str, ...] | None,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "checker_version": CHECKER_VERSION,
        "dependency_versions": dependency_versions(),
        "provider": CPU_PROVIDER,
        "benchmark": {
            "category": cat,
            "version": benchmark_version,
            "network_field": net,
            "property_field": prop,
        },
        "witness_path": str(ce_path),
        "witness_sha256": file_sha256(ce_path),
        "results_row_identity": row_identity(row),
    }


def is_valid_cached_check(check: dict[str, Any], expected: dict[str, Any]) -> bool:
    keys = [
        "schema_version",
        "checker_version",
        "dependency_versions",
        "provider",
        "benchmark",
        "witness_sha256",
        "results_row_identity",
    ]
    return all(check.get(key) == expected.get(key) for key in keys)


def load_cached_check(path: Path, expected: dict[str, Any]) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        with path.open("r", encoding="utf-8") as stream:
            check = json.load(stream)
    except (OSError, json.JSONDecodeError):
        return None

    if is_valid_cached_check(check, expected):
        return check
    return None


def write_check(path: Path, check: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        json.dump(check, stream, indent=2, sort_keys=True)
        stream.write("\n")


def get_or_create_check(
    ce_path: str | Path,
    cat: str,
    net: str,
    prop: str,
    benchmark_version: str | None,
    row: list[str] | tuple[str, ...] | None,
    validator: Callable[[], tuple[str, str]],
) -> dict[str, Any]:
    path = check_path_for(ce_path)
    expected = expected_identity(ce_path, cat, net, prop, benchmark_version, row)
    cached = load_cached_check(path, expected)
    if cached is not None:
        return cached

    result, rationale = validator()
    check = {
        **expected,
        **result_metadata(result),
        "result": result,
        "rationale": rationale,
    }
    write_check(path, check)
    return check
