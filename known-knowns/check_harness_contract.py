#!/usr/bin/env python3
"""Validate release-wrapper inventory and completed negative-checker evidence.

Standard library only. This is orchestration validation, not a scientific checker.
Contracts match the checker sources shipped at 91419e28.
"""
import argparse
import csv
import hashlib
from pathlib import Path
import re
import sys

CODE_FILES = """
A25_6_11_8718 A25_6_12_9895 A26_6_8_3603 A26_6_9_5986 A26_6_11_12222 A26_6_13_16225
A27_6_9_8325 A27_8_10_1737 A27_8_11_2421 A28_8_9_1406 A28_8_11_3785 A28_8_12_4962
A28_8_14_6359 A29_6_10_25974 A29_6_11_41219 A29_6_12_61823 A30_8_8_1166 A33_8_8_1809
A34_8_7_602 A34_8_8_1965 A35_6_6_2217 A45_8_7_1907 A51_6_5_1785 A51_6_6_11184
A52_8_7_3799 A53_8_7_3987 A54_8_7_4193 A55_8_7_4426 A56_8_7_4685 A58_6_5_2684
""".split()
CERT_FILES = "cert_A31_12_10 cert_A31_12_11 cert_A32_12_10 cert_A32_12_15 cert_A32_12_16".split()
NETWORK = "3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30"
HEX = r"[0-9a-f]{64}"
NUMBER = r"-?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory(root):
    # Scope is the original release codes/ and certificates/ directories.
    # Sibling contributed packages have their own indexes and verification.
    for directory, index, names, extension, fields in [
        ("codes", "INDEX.csv", CODE_FILES, ".txt", ("n", "d", "w", "M")),
        ("certificates", "INDEX_delsarte.csv", CERT_FILES, ".json", ("n", "d", "w")),
    ]:
        expected = {directory + "/" + name + extension for name in names}
        folder = root / directory
        need(folder.is_dir() and not folder.is_symlink(), "missing or symlinked " + directory)
        actual = set()
        for path in folder.rglob("*"):
            need(not path.is_symlink(), "symlink in " + directory)
            if path.is_file():
                actual.add(path.relative_to(root).as_posix())
        need(actual == expected, f"{directory} inventory mismatch; missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}")
        index_path = root / index
        need(index_path.is_file() and not index_path.is_symlink(), "missing or symlinked " + index)
        with index_path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream, strict=True)
            headers = reader.fieldnames or []
            need(len(set(headers)) == len(headers), index + ": duplicate column")
            need(set(fields + ("file", "sha256")).issubset(headers), index + ": missing columns")
            seen = set()
            for row in reader:
                need(None not in row and None not in row.values(), index + ": malformed CSV row")
                name = row["file"]
                need(name in expected, index + ": unexpected or unsafe file " + repr(name))
                need(name not in seen, index + ": duplicate file " + name)
                seen.add(name)
                stem = Path(name).stem
                if stem.startswith("cert_"):
                    stem = stem[5:]
                params = stem[1:].split("_")
                need([row[f] for f in fields] == params, index + ": metadata differs from filename " + name)
                need(re.fullmatch(HEX, row["sha256"]) is not None, index + ": malformed SHA-256")
                need(digest(root / name) == row["sha256"], index + ": SHA-256 mismatch for " + name)
            need(seen == expected, index + ": missing indexed files " + repr(sorted(expected - seen)))
    print("HARNESS INVENTORY PASS codes=30 certificates=5")


def one(lines, pattern, label):
    matches = []
    for line in lines:
        match = re.fullmatch(pattern, line)
        if match:
            matches.append(match)
    need(len(matches) == 1, "missing or ambiguous " + label)
    return matches[0]


def graph(args, lines):
    need(args.file is not None, "graph file is required")
    one(lines, re.escape("file=" + str(args.file)), "graph identity")
    need(lines[-1] == "INVALID", "missing completed INVALID verdict")
    header = one(lines, r"N=(\d+) edges=(\d+) loops=0 duplicates=0 unused_labels=0 mindeg=(\d+) maxdeg=(\d+) "
                 + re.escape(f"(DELTA={args.delta}, D={args.diameter})"), "valid graph structure")
    need(int(header[4]) <= args.delta, "negative graph fails degree bound")
    far = one(lines, re.escape(f"ordered_pairs_at_distance_gt_{args.diameter}=") + r"(\d+) \(of (\d+)\)", "completed far-pair count")
    count, total = int(far[1]), int(far[2])
    need(total == int(header[1]) ** 2 and 0 < count <= total, "invalid far-pair count")
    if args.far is not None:
        need(count == args.far, "near-miss must have exactly " + str(args.far) + " far ordered pairs")


def fmm(args, lines):
    sha = digest(args.file)
    pattern = r"FMMCHECK FAIL file=" + re.escape(args.file.name) + r" format=<(\d+),(\d+),(\d+)> sorted=<(\d+),(\d+),(\d+)> terms=(\d+) rank_nonzero_terms=(\d+) sha256=" + sha
    summary = re.fullmatch(pattern, lines[-1])
    need(summary is not None, "missing completed identity-bound FMM rejection")
    dims = list(map(int, summary.group(1, 2, 3)))
    need(sorted(dims) == list(map(int, summary.group(4, 5, 6))), "inconsistent FMM dimensions")
    need(0 <= int(summary[8]) <= int(summary[7]), "inconsistent FMM rank")
    mods = [re.fullmatch(r"  mod (\d+): violated Brent equations = (\d+)", line) for line in lines]
    mods = [m for m in mods if m]
    proof = one(lines, r"  checked (\d+)\*(\d+)\*(\d+) = (\d+) Brent equations modulo (\d+) primes; log2\(prod primes\) = " + NUMBER + r" > log2\(2 L \(S\+1\)\) = " + NUMBER, "completed Brent-equation check")
    n1, n2, n3 = dims
    need([int(proof[i]) for i in (1, 2, 3, 4)] == [n1 * n2, n2 * n3, n3 * n1, (n1 * n2 * n3) ** 2], "inconsistent Brent-equation dimensions")
    need(len(mods) == int(proof[5]) and len(mods) >= 4, "incomplete modular checks")
    need(len({m[1] for m in mods}) == len(mods), "duplicate modular checks")
    need(any(int(m[2]) > 0 for m in mods), "no violated Brent equations")


def vnn(args, lines):
    need(args.instance in ("1703", "178") and args.mode in ("on_bound", "outside", "centre"), "unknown VNN control")
    prop = f"model_30_idx_{args.instance}_eps_1.00000"
    summary = r"VNNCHECK FAIL instance=" + re.escape(NETWORK + "/" + prop) + r" margin=" + NUMBER + r" min_input_slack=" + NUMBER + r" witness=.+/mut" + args.instance + "/" + args.mode + r"\.txt"
    need(re.fullmatch(summary, lines[-1]) is not None, "missing completed identity-bound VNN rejection")
    for label in ("onnx.gz", "onnx", "vnnlib.gz", "vnnlib"):
        one(lines, r"  " + re.escape(label) + r" +sha256 " + HEX + r" \(pinned\)", "pinned " + label)
    one(lines, r"  property: 5400 input assertions, [1-9][0-9]* output assertion\(s\); all 2700 coordinates bounded above and below: True", "complete property bounds")
    one(lines, r"  witness sha256 " + digest(args.file) + r"; every value exactly representable in float32: True", "exact identity-bound witness")
    strict = one(lines, r"  input box, exact rationals, strict: (True|False); smallest distance to a bound = [^ ]+ = " + NUMBER, "input-bound evaluation")
    output = one(lines, r"  onnxruntime [^ ]+ CPU float32: output assertion holds at zero tolerance: (True|False); margin " + NUMBER + r"; argmax [0-9]+", "completed ONNX runtime evaluation")
    if args.mode in ("on_bound", "outside"):
        need(strict[1] == "False", "bound control did not fail strict input check")
    else:
        need(strict[1] == "True" and output[1] == "False", "centre control did not fail output assertion")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("kind", choices=("inventory", "graph", "fmm", "vnn"))
    ap.add_argument("--root", type=Path)
    ap.add_argument("--stdout", type=Path)
    ap.add_argument("--stderr", type=Path)
    ap.add_argument("--exit-code", type=int)
    ap.add_argument("--file", type=Path)
    ap.add_argument("--delta", type=int)
    ap.add_argument("--diameter", type=int)
    ap.add_argument("--far", type=int)
    ap.add_argument("--instance")
    ap.add_argument("--mode")
    args = ap.parse_args()
    try:
        if args.kind == "inventory":
            need(args.root is not None, "--root is required")
            inventory(args.root)
            return 0
        need(args.exit_code == 1, "checker did not return semantic rejection exit 1")
        need(args.stdout is not None and args.stderr is not None, "checker output paths are required")
        stdout, stderr = args.stdout.read_text(), args.stderr.read_text()
        need("Traceback (most recent call last):" not in stdout + stderr, "checker raised an exception")
        need("MISMATCH" not in stdout + stderr, "checker integrity mismatch")
        lines = stdout.splitlines()
        need(bool(lines), "checker output is empty")
        if args.kind == "graph":
            need(args.delta is not None and args.diameter is not None, "graph dimensions are required")
            graph(args, lines)
        else:
            need(args.file is not None and args.file.is_file() and args.file.stat().st_size > 0, "mutant file is missing or empty")
            (fmm if args.kind == "fmm" else vnn)(args, lines)
        print("HARNESS CONTROL PASS " + args.kind + ": expected semantic rejection")
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        print("HARNESS CONTRACT FAIL: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
