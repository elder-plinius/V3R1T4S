#!/usr/bin/env python3
"""Standalone 60-digit verifier for the submitted (3, 34) complex line packing."""
from decimal import Decimal, getcontext
import hashlib
import os
import sys

D = 3
N = 34
TABLE_MU = Decimal("0.75683480")
LOWER_BOUND = Decimal("0.67202151")
THRESHOLD = Decimal("1e-8")
EXPECTED_SHA256 = "7b0745355c9f502a7eb731c0ec7541db1d21edfabe543f6274eacda06f2b0597"
EXPECTED_MU_MAX = Decimal("0.75649479818227171")

BASELINE_URL = (
    "https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/"
    "CurrentBestPackings/3x34_jrr.txt"
)
BASELINE_SHA256 = "159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e"
RECORDED_BASELINE_MU_60 = Decimal(
    "0.756834797253628206097823785778147954374744559786819000003653"
)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def eval_mu_60(path: str, enforce_sigfigs: bool = True):
    getcontext().prec = 60
    with open(path, "r", encoding="utf-8") as f:
        toks = f.read().split()
    expected = 2 * D * N
    if len(toks) != expected:
        fail(f"Expected {expected} floats in {path}, got {len(toks)}")
    try:
        nums = [Decimal(t) for t in toks]
    except Exception as exc:
        fail(f"Non-numeric token in {path}: {exc}")
    for idx, val in enumerate(nums):
        if not val.is_finite():
            fail(f"Non-finite coordinate at index {idx}")
    if enforce_sigfigs:
        for t, val in zip(toks, nums):
            sig = len(t.lstrip("-+").replace(".", "").lstrip("0"))
            if val != 0 and sig < 16:
                fail(f"Coordinate {t!r} has only {sig} < 16 significant digits")

    half = D * N
    vecs = []
    for i in range(N):
        re = nums[i * D : (i + 1) * D]
        im = nums[half + i * D : half + (i + 1) * D]
        sq = sum(r * r + m * m for r, m in zip(re, im))
        if sq <= Decimal("1e-30"):
            fail(f"Zero-norm vector {i}")
        inv = Decimal(1) / sq.sqrt()
        vecs.append(([r * inv for r in re], [m * inv for m in im]))

    max_sq = Decimal(0)
    worst = None
    for j in range(N):
        rj, ij = vecs[j]
        for k in range(j + 1, N):
            rk, ik = vecs[k]
            gr = sum(rj[c] * rk[c] + ij[c] * ik[c] for c in range(D))
            gi = sum(rj[c] * ik[c] - ij[c] * rk[c] for c in range(D))
            ov_sq = gr * gr + gi * gi
            if ov_sq > max_sq:
                max_sq = ov_sq
                worst = (j, k)
    return max_sq.sqrt(), worst


def main():
    args = sys.argv[1:]
    skip_hash = "--skip-hash" in args
    pos = [a for a in args if not a.startswith("--")]

    pkg = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cand = pos[0] if pos else os.path.join(pkg, "object", "3x34_new.txt")
    base = pos[1] if len(pos) > 1 else None

    if not os.path.isfile(cand):
        fail(f"Missing candidate file: {cand}")

    if not skip_hash:
        with open(cand, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h != EXPECTED_SHA256:
            fail(f"SHA-256 mismatch for {cand}: {h} != {EXPECTED_SHA256}")

    mu_new, pair_new = eval_mu_60(cand, enforce_sigfigs=True)
    imp_table = TABLE_MU - mu_new
    imp_recorded_base = RECORDED_BASELINE_MU_60 - mu_new

    try:
        cand_label = os.path.relpath(os.path.abspath(cand), pkg)
        if cand_label.startswith(".."):
            cand_label = os.path.basename(cand)
    except ValueError:
        cand_label = os.path.basename(cand)

    print(
        f"candidate={cand_label} mu={mu_new} worst={pair_new} "
        f"imp_vs_table={imp_table}"
    )
    print(
        f"upstream_baseline_url={BASELINE_URL} "
        f"upstream_baseline_sha256={BASELINE_SHA256} "
        f"recorded_baseline_mu_60={RECORDED_BASELINE_MU_60} "
        f"imp_vs_recorded_baseline={imp_recorded_base}"
    )

    if mu_new < LOWER_BOUND:
        fail(f"mu {mu_new} < lower_bound {LOWER_BOUND}")
    if imp_table < THRESHOLD:
        fail(f"improvement vs table {imp_table} < 1e-8")
    if imp_recorded_base < THRESHOLD:
        fail(f"improvement vs recorded baseline {imp_recorded_base} < 1e-8")
    if not skip_hash and mu_new > EXPECTED_MU_MAX:
        fail(f"mu {mu_new} exceeds expected {EXPECTED_MU_MAX}")

    if base is not None:
        if not os.path.isfile(base):
            fail(f"Missing optional baseline file: {base}")
        with open(base, "rb") as f:
            bh = hashlib.sha256(f.read()).hexdigest()
        if not skip_hash and bh != BASELINE_SHA256:
            fail(f"Baseline SHA-256 mismatch: {bh} != {BASELINE_SHA256}")
        mu_base, _ = eval_mu_60(base, enforce_sigfigs=False)
        imp_base = mu_base - mu_new
        print(
            f"baseline={os.path.basename(base)} sha256={bh} "
            f"mu={mu_base} imp_vs_baseline={imp_base}"
        )
        if imp_base < THRESHOLD:
            fail(f"improvement vs baseline {imp_base} < 1e-8")

    print("PASS")


if __name__ == "__main__":
    main()
