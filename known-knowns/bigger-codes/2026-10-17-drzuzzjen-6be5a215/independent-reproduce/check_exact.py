#!/usr/bin/env python3
"""Independent, exhaustive binary constant-weight code checker (stdlib only)."""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc():
    return datetime.now(timezone.utc).isoformat()


def check(words, n, w, d, expected_count):
    errors = []
    if len(words) != expected_count:
        errors.append("count")
    if any(len(word) != n for word in words):
        errors.append("length")
    if any(set(word) - {"0", "1"} for word in words):
        errors.append("alphabet")
    if len(set(words)) != len(words):
        errors.append("duplicate")
    if any(word.count("1") != w for word in words):
        errors.append("weight")
    if "length" in errors or "alphabet" in errors:
        return {"pass": False, "errors": errors, "count": len(words),
                "pairs_checked": 0, "minimum_distance": None}
    values = [int(word, 2) for word in words]
    pairs = 0
    minimum = None
    first_violation = None
    for i in range(len(values)):
        left = values[i]
        for j in range(i + 1, len(values)):
            distance = (left ^ values[j]).bit_count()
            pairs += 1
            if minimum is None or distance < minimum:
                minimum = distance
            if distance < d and first_violation is None:
                first_violation = {"i": i, "j": j, "distance": distance}
    if first_violation is not None:
        errors.append("distance")
    return {"pass": not errors, "errors": errors, "count": len(words),
            "distinct_count": len(set(words)), "pairs_checked": pairs,
            "minimum_distance": minimum, "first_distance_violation": first_violation}


def calibrate():
    # Each case is handmade, independent of the submitted object.
    cases = [
        ("positive", ["110000", "001100", "000011"], 6, 2, 4, 3, []),
        ("duplicate", ["110000", "110000"], 6, 2, 4, 2, ["duplicate", "distance"]),
        ("wrong_weight", ["111000"], 6, 2, 4, 1, ["weight"]),
        ("wrong_length", ["11000"], 6, 2, 4, 1, ["length"]),
        ("inadequate_distance", ["110000", "101000"], 6, 2, 4, 2, ["distance"]),
        ("wrong_count", ["110000"], 6, 2, 4, 2, ["count"]),
        ("nonbinary", ["11000x"], 6, 2, 4, 1, ["alphabet"]),
    ]
    outputs = []
    for name, words, n, w, d, count, expected_errors in cases:
        result = check(words, n, w, d, count)
        correct = result["errors"] == expected_errors
        if name == "positive":
            correct = correct and result["minimum_distance"] == 4 and result["pairs_checked"] == 3
        if name == "duplicate":
            correct = correct and result["minimum_distance"] == 0 and result["pairs_checked"] == 1
        if name == "inadequate_distance":
            correct = correct and result["minimum_distance"] == 2 and result["pairs_checked"] == 1
        outputs.append({"name": name, "words": words, "expected_errors": expected_errors,
                        "calibration_pass": correct, "actual": result})
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("object")
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--w", type=int, required=True)
    parser.add_argument("--d", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    started = utc()
    calibration = calibrate()
    data = Path(args.object).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    sha_matches = digest == args.sha256
    # splitlines removes only line boundaries, not spaces or other word characters.
    words = data.decode("ascii", errors="strict").splitlines()
    result = check(words, args.n, args.w, args.d, args.count)
    expected_pairs = args.count * (args.count - 1) // 2
    passed = (all(x["calibration_pass"] for x in calibration) and sha_matches
              and result["pass"] and result["pairs_checked"] == expected_pairs)
    exit_code = 0 if passed else 1
    print(json.dumps({
        "started_utc": started, "finished_utc": utc(),
        "definition": {"n": args.n, "w": args.w, "d_at_least": args.d, "M": args.count},
        "object_relative_path": args.object, "object_bytes": len(data),
        "object_sha256": digest, "expected_sha256": args.sha256,
        "sha256_matches": sha_matches, "expected_pairs": expected_pairs,
        "calibration": calibration, "object_result": result,
        "pass": passed, "exit_code": exit_code,
    }, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
