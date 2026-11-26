#!/usr/bin/env python3
"""Standalone zero-dependency verifier for binary multiple-deletion code certificates.

Checks:
1. Exact word length, binary alphabet, uniqueness, and target cardinality.
2. Exact s-deletion ball disjointness: D_s(x) cap D_s(y) == empty for all x != y.
3. Independent full pairwise dynamic-programming LCS(x, y) < n - s cross-check.
4. Klein-4 <c, r> symmetry invariance on the primary (16, 3) = 44 code.
5. Sorted-list SHA-256 verification and SHA256SUMS integrity (if present).
6. Negative control (--corrupt): mutates 1 bit / injects collision and exits 1.
"""
import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

EXPECTED_PRIMARY = [
    ("object/code_15_2_137.json", 15, 2, 137, 136, "2b226e2f0f7ab7fd9da92a1a38144f44c609c944520314b49d066637b2bfb4dc", 3396, False),
    ("object/code_15_3_31.json", 15, 3, 31, 30, "427002b54632ecc1468af57617104a317783a397d0b3b75b7215f695da57c58d", 1397, False),
    ("object/code_16_3_44_klein4.json", 16, 3, 44, 42, "2580ff8bef1160cd9c7f3450e6fa4e7c263491b7502233dfb05dc9851275b816", 2344, True),
]

EXPECTED_COMPANIONS = [
    ("object/companions/code_16_3_44_rc.json", 16, 3, 44, "c8b9fd6a57335dc04256adf46674f2b7604be121b512987c9fc9735652b18a15", 2304),
    ("object/companions/code_16_3_44_r.json", 16, 3, 44, "549dc5d6b9f7cea4cf49330ccdaa29527d712156d009b6236bbbb7b469eef257", 2410),
    ("object/companions/code_16_3_44_c.json", 16, 3, 44, "bd70a4f084a4a5c258e53e1b1ee7589e9556f1e16ce5243298d2d8aef6d04b7a", 2468),
    ("object/companions/code_16_2_219_companion.json", 16, 2, 219, "f7241c96f86c0dbcc0a9a1d4510947747b7890773a5a13878cb70960a5334a2b", 6091),
]


def del_ball(word: str, s: int) -> set:
    keep = len(word) - s
    return {"".join(word[i] for i in idx) for idx in combinations(range(len(word)), keep)}


def lcs_len(a: str, b: str) -> int:
    dp = [0] * (len(b) + 1)
    for ca in a:
        prev = 0
        for j, cb in enumerate(b, 1):
            tmp = dp[j]
            dp[j] = prev + 1 if ca == cb else (dp[j] if dp[j] > dp[j - 1] else dp[j - 1])
            prev = tmp
    return dp[-1]


def verify_code(words, n: int, s: int, min_size: int, exp_wsha: str, exp_ds: int, check_klein4: bool = False):
    if len(words) < min_size:
        raise ValueError(f"size {len(words)} < expected {min_size}")
    if len(words) != len(set(words)):
        raise ValueError("duplicate codeword detected")
    for w in words:
        if not isinstance(w, str) or len(w) != n or any(ch not in "01" for ch in w):
            raise ValueError(f"invalid codeword: {w!r}")

    wsha = hashlib.sha256(("\n".join(sorted(words)) + "\n").encode("ascii")).hexdigest()
    if exp_wsha and wsha != exp_wsha:
        raise ValueError(f"sorted word-list SHA-256 mismatch: {wsha} != {exp_wsha}")

    seen = {}
    for w in words:
        for d in del_ball(w, s):
            if d in seen:
                raise ValueError(f"D_{s} collision on {d!r} between {seen[d]} and {w}")
            seen[d] = w
    if exp_ds and len(seen) != exp_ds:
        raise ValueError(f"|D_{s}| mismatch: {len(seen)} != {exp_ds}")

    max_lcs = 0
    for i in range(len(words)):
        wi = words[i]
        for j in range(i + 1, len(words)):
            ell = lcs_len(wi, words[j])
            if ell > max_lcs:
                max_lcs = ell
            if ell >= n - s:
                raise ValueError(f"LCS collision: LCS({wi}, {words[j]}) = {ell} >= {n - s}")

    if check_klein4:
        ws = set(words)
        for w in ws:
            comp = "".join("1" if c == "0" else "0" for c in w)
            rev = w[::-1]
            if comp not in ws or rev not in ws or rev[::-1] not in ws:
                raise ValueError(f"Klein-4 invariance violated by {w}")

    return len(words), len(seen), max_lcs, wsha


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify binary multiple-deletion code certificates.")
    ap.add_argument("--corrupt", action="store_true", help="Negative control: inject a single-word collision and expect exit 1.")
    ap.add_argument("--skip-checksums", action="store_true", help="Skip SHA256SUMS manifest check.")
    args = ap.parse_args()

    pkg_root = Path(__file__).resolve().parent.parent
    if not (pkg_root / "object").is_dir():
        pkg_root = Path(__file__).resolve().parent

    try:
        for rel, n, s, size, table_val, wsha, exp_ds, k4 in EXPECTED_PRIMARY:
            data = json.loads((pkg_root / rel).read_text(encoding="utf-8"))
            words = list(data["words"])
            if args.corrupt and rel.endswith("code_16_3_44_klein4.json"):
                # Replace word 1 with a 1-bit mutation of word 0 (guaranteed LCS >= 15 >= 13)
                w0 = words[0]
                words[1] = ("1" if w0[0] == "0" else "0") + w0[1:]
                verify_code(words, n, s, size, "", 0, False)
                print("ERROR: corrupt input unexpectedly passed")
                return 0
            got_sz, got_ds, got_lcs, got_sha = verify_code(words, n, s, size, wsha, exp_ds, k4)
            txt_path = (pkg_root / rel).with_suffix(".txt")
            if txt_path.is_file():
                txt_words = [ln.strip() for ln in txt_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
                if sorted(txt_words) != sorted(words):
                    raise ValueError(f"JSON/TXT mismatch for {rel}")
            print(f"[OK] ({n},{s}) | size={got_sz} (> Table 2 {table_val}) | |D_{s}|={got_ds} | maxLCS={got_lcs}<{n-s} | sha={got_sha[:16]}")

        for rel, n, s, size, wsha, exp_ds in EXPECTED_COMPANIONS:
            p = pkg_root / rel
            if not p.is_file():
                continue
            words = json.loads(p.read_text(encoding="utf-8"))["words"]
            got_sz, got_ds, got_lcs, got_sha = verify_code(words, n, s, size, wsha, exp_ds, False)
            print(f"[OK] companion ({n},{s}) {p.name} | size={got_sz} | |D_{s}|={got_ds} | maxLCS={got_lcs}<{n-s} | sha={got_sha[:16]}")

        sums = pkg_root / "SHA256SUMS"
        if not args.skip_checksums and sums.is_file():
            checked = 0
            for ln in sums.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                exp_h, fname = ln.split(None, 1)
                got_h = hashlib.sha256((pkg_root / fname).read_bytes()).hexdigest()
                if got_h != exp_h:
                    raise ValueError(f"SHA256SUMS mismatch on {fname}: {got_h} != {exp_h}")
                checked += 1
            print(f"[OK] SHA256SUMS verified ({checked} files)")

        if args.corrupt:
            print("ERROR: --corrupt did not trigger failure")
            return 0

        print("PASS")
        return 0
    except Exception as exc:
        print(f"[REJECTED] {exc}")
        print("FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
