#!/usr/bin/env python3
"""Public launcher for the frozen portable Bernstein checker; stdlib only.

This wrapper reuses the checker. It is not a second independent mathematical
verification. It authenticates inputs, isolates temporary output, and checks
the completion receipt before printing the package's terminal PASS/FAIL.
"""
if not __debug__:
    print("Optimized execution cannot validate the certificate.")
    print("FAIL")
    raise SystemExit(1)

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from fractions import Fraction


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def positive_integer(value):
    return type(value) is int and value > 0


def load_config(directory):
    try:
        config = json.loads((directory / "config.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise VerificationError("Cannot read a valid verification configuration.") from None
    expected = {"schema", "object_path", "object_sha256", "threshold", "checker_sha256",
                "max_seconds", "process_timeout_seconds", "max_depth", "checkpoint_seconds"}
    require(isinstance(config, dict) and set(config) == expected,
            "Invalid verification configuration fields.")
    require(config["schema"] == "integer-chebyshev-public-runner-v1",
            "Unsupported verification configuration.")
    for field in ("object_sha256", "checker_sha256"):
        value = config[field]
        require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
                "Invalid configured SHA256.")
    value = config["threshold"]
    require(isinstance(value, str) and re.fullmatch(r"(?:0|[1-9][0-9]*)\.[0-9]+", value) is not None,
            "Threshold must be an exact positive decimal string.")
    require(Fraction(value) > 0, "Threshold must be positive.")
    for field in ("max_seconds", "process_timeout_seconds", "max_depth", "checkpoint_seconds"):
        require(positive_integer(config[field]), "Invalid verification resource limit.")
    require(config["max_seconds"] < config["process_timeout_seconds"] < 900,
            "Verification time limits must fit the package-check timeout.")
    value = config["object_path"]
    require(isinstance(value, str) and value, "Invalid object path.")
    relative = PurePosixPath(value)
    require(not relative.is_absolute() and ".." not in relative.parts and "\\" not in value,
            "Object path must stay inside the package.")
    require(bool(relative.parts) and relative.parts[0] == "object",
            "Object must be in the package object directory.")
    return config


def read_checked(path, expected_hash, label):
    try:
        raw = path.read_bytes()
    except OSError:
        raise VerificationError("Cannot read " + label + ".") from None
    require(hashlib.sha256(raw).hexdigest() == expected_hash, label + " SHA256 mismatch.")
    return raw


def check_receipt(result, config):
    require(isinstance(result, dict), "Malformed checker receipt.")
    require(result.get("core_controls") == "PASS", "Checker controls did not pass.")
    require(result.get("claim_level") == "PROVED-HERE" and
            result.get("finite_cover_complete") is True and result.get("pending_cells") == 0,
            "The full continuum cover was not certified.")
    require(result.get("site_packages_disabled") is True,
            "Checker did not disable external site packages.")
    require(result.get("certificate_sha256") == config["object_sha256"],
            "Checker receipt has the wrong object hash.")
    require(result.get("threshold_decimal_input") == config["threshold"] and
            Fraction(result.get("threshold_exact", "0")) == Fraction(config["threshold"]),
            "Checker receipt has the wrong exact threshold.")
    for field in ("factor_count", "w_degree", "x_degree", "normalization", "accepted_leaves", "visited"):
        require(positive_integer(result.get(field)), "Checker receipt has invalid exact counts.")
    require(result["x_degree"] == result["normalization"] == 2 * result["w_degree"],
            "Checker receipt has inconsistent degree normalization.")
    upper = int(result.get("max_accepted_upper_scaled", "0"))
    target = int(result.get("comparison_target_scaled", "0"))
    margin = int(result.get("minimum_acceptance_margin_scaled", "0"))
    require(target - upper == margin > 0, "Checker receipt lacks strict integer separation.")
    require(int(result.get("common_scale_denominator", "0")) > 0,
            "Checker receipt has invalid logarithm scaling.")


def verify():
    directory = Path(__file__).resolve().parent
    package = directory.parent
    config = load_config(directory)
    object_path = (package / config["object_path"]).resolve()
    require(object_path.is_relative_to(package), "Object path escapes the package.")
    raw = read_checked(object_path, config["object_sha256"], "Object")
    checker = directory / "portable_v2.py"
    checker_raw = read_checked(checker, config["checker_sha256"], "Checker")
    print("Object SHA256: " + config["object_sha256"], flush=True)
    print("Checker SHA256: " + config["checker_sha256"], flush=True)
    print("Computing the full rigorous continuum certificate.", flush=True)
    environment = os.environ.copy()
    environment["PYTHONOPTIMIZE"] = "0"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    # Retain no proof outputs in the package. Even failure/timeout cleans up.
    with tempfile.TemporaryDirectory(prefix="chebyshev_verification_") as temporary:
        work = Path(temporary)
        witness = work / "candidate.json"
        witness.write_bytes(raw)  # Verify exactly the bytes authenticated above.
        frozen_checker = work / "portable_v2.py"
        frozen_checker.write_bytes(checker_raw)
        output = work / "result"
        command = [sys.executable, "-S", str(frozen_checker), "--certificate", str(witness),
                   "--threshold", config["threshold"], "--out", str(output),
                   "--seconds", str(config["max_seconds"]),
                   "--max-depth", str(config["max_depth"]),
                   "--checkpoint-seconds", str(config["checkpoint_seconds"])]
        try:
            with (work / "checker.log").open("w", encoding="utf-8") as log:
                completed = subprocess.run(command, cwd=work, env=environment,
                                           stdout=log, stderr=subprocess.STDOUT,
                                           timeout=config["process_timeout_seconds"], check=False)
        except subprocess.TimeoutExpired:
            raise VerificationError("The rigorous checker exceeded its time limit.") from None
        require(completed.returncode == 0,
                "The rigorous checker rejected the input or could not complete the cover.")
        try:
            result = json.loads((output / "result.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raise VerificationError("Cannot read the completed checker receipt.") from None
        check_receipt(result, config)
    # TemporaryDirectory cleanup completed before any terminal PASS.
    print("Exact threshold: " + config["threshold"])
    print("Integer factors: " + str(result["factor_count"]))
    print("Exact x-degree: " + str(result["x_degree"]))
    print("Certified dyadic intervals: " + str(result["accepted_leaves"]))
    print("Maximum subdivision depth: " + str(result["maximum_depth"]))
    print("Finite cover: complete")
    print("Strict integer acceptance margin: " + result["minimum_acceptance_margin_scaled"])
    print("Verification seconds: " + format(result["elapsed_seconds"], ".6f"))
    print("Peak RSS (KiB on Linux): " + str(result["peak_rss_kib"]))


def main():
    try:
        verify()
    except VerificationError as error:
        print(str(error))
        print("FAIL")
        return 1
    except (OSError, ValueError, TypeError, KeyError, OverflowError, RuntimeError):
        # Do not expose runtime paths, tracebacks or process identifiers.
        print("Verification failed because an input or runtime result was invalid.")
        print("FAIL")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
