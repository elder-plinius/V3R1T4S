#!/usr/bin/env python3
"""Reconstruct the 6 v=47 LJCR ingredient designs and build the 125,236-block
47+47 combining baseline (built/94-13-5.txt) before running how-we-built-it/merge.c.

Ingredients for V = V_1 (0..46) union V_2 (47..93), j = |T cap V_1| in {0..5}:
  j=0: (47, 0, 0) [1 trivial empty block]        x C(47, 13, 5) [2,849 blocks, Jan de Heer & Steve Muir] =  2,849
  j=1: C(47, 2, 1) [24 trivial pair blocks]       x C(47, 11, 4) [  866 blocks, Jan de Heer & Steve Muir] = 20,784
  j=2: C(47, 5, 2) [113 blocks, Michael Dambmann] x C(47,  8, 3) [  345 blocks, Jan de Heer & Steve Muir] = 38,985
  j=3: C(47, 8, 3) [345 blocks, de Heer & Muir]   x C(47,  5, 2) [  113 blocks, Michael Dambmann]         = 38,985
  j=4: C(47,11, 4) [866 blocks, de Heer & Muir]   x C(47,  2, 1) [   24 trivial pair blocks]              = 20,784
  j=5: C(47,13, 5) [2,849 blocks, de Heer & Muir] x (47,  0, 0) [    1 trivial empty block]               =  2,849
  ---------------------------------------------------------------------------------------------------------------
  Total 47+47 combining baseline:                                                                          125,236 blocks

Can be run either:
  1. From Zenodo LJCR v1.2 covers.json (--covers-json /path/to/covers.json), OR
  2. Offline from the shipped object/design_94_13_5_part1.txt..part5.txt (default),
     verifying all 6 ingredient SHA-256 digests and writing built/94-13-5.txt.
"""
import argparse
import glob
import hashlib
import json
import os
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_TXT0_SHA256 = {
    "47-0-0.txt":  "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
    "47-2-1.txt":  "d5400aee5352427736a090d297a7dcd2a4fa97377654515928e7c715845310ef",
    "47-5-2.txt":  "abcf309f0123d234d71ba3d1fff6943922e6f0c90da338947d6a47dcabacca05",
    "47-8-3.txt":  "d9401d479f3b7a6abadcc8d45b6692f42e7995dfac46e2c8e1ce5499191419b7",
    "47-11-4.txt": "fe4b4cd936fa50ae0ca273b22bbcd1dfce55b808b56e5afbca0aaad28afdab06",
    "47-13-5.txt": "af0df98e87b41ad88537bd7f6ba9e26b65b0a337aa4d28d554b46ad471807835",
}
EXPECTED_COMBINED_SHA256 = "4ddf66cf9edf0cf96165e7514dbcd0cafb9c3dc67198326ea0586a63661ffcfb"


def extract_from_covers_json(covers_json_path: Path):
    target_kt = {(5, 2): "c5_2", (8, 3): "c8_3", (11, 4): "c11_4", (13, 5): "c13_5"}
    found = {}
    with open(covers_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        if entry.get("v") == 47 and (entry.get("k"), entry.get("t")) in target_kt:
            key = target_kt[(entry["k"], entry["t"])]
            found[key] = [tuple(x - 1 for x in blk) for blk in entry["blocks"]]
    return found["c5_2"], found["c8_3"], found["c11_4"], found["c13_5"]


def extract_from_shipped_parts():
    parts = sorted(glob.glob(str(PKG_ROOT / "object" / "design_94_13_5_part*.txt")))
    assert len(parts) == 5, f"Expected 5 part files, found {len(parts)}"
    lines = []
    for p in parts:
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    lines.append([int(x) for x in line.split()])
    c13_5 = sorted(set(
        tuple(x for x in b if x < 47)
        for b in lines
        if sum(1 for x in b if x < 47) == 13
    ))
    # 865 unmerged blocks of C(47,11,4) appear directly in the k1=2, k2=11 section,
    # and the 866th block is the swap16-fixed block (0, 1, 2, 3, 4, 5, 7, 9, 10, 22, 38)
    # whose 24 copies were pair-merged into lines 125132..125144 and 125159..125169.
    c11_4 = sorted(set(
        tuple(x - 47 for x in b if x >= 47)
        for b in lines
        if sum(1 for x in b if x < 47) == 2
    ) | {(0, 1, 2, 3, 4, 5, 7, 9, 10, 22, 38)})
    c8_3 = sorted(set(
        tuple(x for x in b if x < 47)
        for b in lines
        if sum(1 for x in b if x < 47) == 8
    ))
    c5_2 = sorted(set(
        tuple(x - 47 for x in b if x >= 47)
        for b in lines
        if sum(1 for x in b if x < 47) == 8
    ))
    return c5_2, c8_3, c11_4, c13_5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--covers-json", type=str, default=None, help="Optional path to Zenodo LJCR covers.json")
    parser.add_argument("--out-dir", type=str, default="built", help="Output directory (default: built)")
    args = parser.parse_args()

    c0_0 = [()]
    c2_1 = [(2 * i, 2 * i + 1) for i in range(23)] + [(45, 46)]
    if args.covers_json:
        c5_2, c8_3, c11_4, c13_5 = extract_from_covers_json(Path(args.covers_json))
    else:
        c5_2, c8_3, c11_4, c13_5 = extract_from_shipped_parts()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ingredients = [
        ("47-0-0.txt", c0_0),
        ("47-2-1.txt", c2_1),
        ("47-5-2.txt", c5_2),
        ("47-8-3.txt", c8_3),
        ("47-11-4.txt", c11_4),
        ("47-13-5.txt", c13_5),
    ]
    for fname, blks in ingredients:
        raw = "".join(" ".join(str(x) for x in b) + "\n" for b in blks).encode("utf-8")
        sha = hashlib.sha256(raw).hexdigest()
        assert sha == EXPECTED_TXT0_SHA256[fname], f"SHA-256 mismatch for {fname}: {sha}"
        (out_dir / fname).write_bytes(raw)
        print(f"wrote {out_dir / fname}: blocks={len(blks)} bytes={len(raw)} sha256={sha}")

    terms = [
        (0, "47-0-0", "47-13-5", c0_0, c13_5),
        (1, "47-2-1", "47-11-4", c2_1, c11_4),
        (2, "47-5-2", "47-8-3",  c5_2, c8_3),
        (3, "47-8-3", "47-5-2",  c8_3, c5_2),
        (4, "47-11-4", "47-2-1", c11_4, c2_1),
        (5, "47-13-5", "47-0-0", c13_5, c0_0),
    ]
    combined_path = out_dir / "94-13-5.txt"
    total_blocks = 0
    with open(combined_path, "w", encoding="utf-8") as f:
        for j, n1, n2, D1, D2 in terms:
            prod = len(D1) * len(D2)
            total_blocks += prod
            print(f"  j={j}: {n1} ({len(D1)}) x {n2} ({len(D2)}) = {prod} blocks")
            for b1 in D1:
                for b2 in D2:
                    blk = list(b1) + [x + 47 for x in b2]
                    f.write(" ".join(str(x) for x in blk) + "\n")

    comb_sha = hashlib.sha256(combined_path.read_bytes()).hexdigest()
    assert total_blocks == 125236, f"Expected 125236 blocks, got {total_blocks}"
    assert comb_sha == EXPECTED_COMBINED_SHA256, f"Combined SHA-256 mismatch: {comb_sha}"
    print(f"wrote {combined_path}: blocks={total_blocks} sha256={comb_sha}")


if __name__ == "__main__":
    main()
