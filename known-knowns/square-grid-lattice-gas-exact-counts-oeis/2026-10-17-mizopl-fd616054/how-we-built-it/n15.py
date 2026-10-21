#!/usr/bin/env python3
"""Attempt A054759(15) via TWO runs that differ in state encoding, inner entry
computation, AND prime set. Both are sector transfer-matrix + float64 modular matmul + CRT.

Run A: forward vertex order, closed-form (min/max prefix) entry, primes just below 2^20.
Run B: reversed vertex order, explicit two-walk entry, primes just below 2^19 (disjoint).

Requires: reproduction gate already passed (reproduce_output.txt). Ice entropy constant
W = (4/3)^(3/2) = 1.5396007... ; growth gate reports a(15)^(1/225) vs W literally.
"""
import sys, os, time, signal
import sixvertex as sv

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "n15_output.txt")
RESID = os.path.join(HERE, "n15_residues.txt")

HARD_LIMIT_S = int(os.environ.get("HARD_LIMIT_S", "1200"))
def on_alarm(s, f):
    raise TimeoutError(f"hard limit {HARD_LIMIT_S}s")
signal.signal(signal.SIGALRM, on_alarm)
signal.alarm(HARD_LIMIT_S)

N = 15
W = (4.0/3.0)**1.5   # Lieb ice constant per vertex

lines = []
def emit(s):
    print(s, flush=True)
    lines.append(s)
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")

def run(label, primes, reverse, builder):
    emit(f"## {label}: reverse={reverse} builder={builder.__name__} nprimes={len(primes)}")
    emit(f"   primes: {primes}")
    res = []
    for p in primes:
        t0 = time.time()
        r = sv.trace_Tn_mod(N, p, reverse=reverse, builder=builder)
        res.append(r)
        emit(f"   p={p}  r={r}  ({time.time()-t0:.1f}s)")
        with open(RESID, "a") as f:
            f.write(f"{label}\t{p}\t{r}\n")
    val, M = sv.crt(res, primes)
    emit(f"   {label} CRT value = {val}")
    emit(f"   {label} modulus bits = {M.bit_length()}")
    return val, M, res

def main():
    open(RESID, "w").close()
    emit(f"# A054759(15) two-run attempt  {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    primesA = sv.primes_below(1 << 20, 11)
    primesB = sv.primes_below(1 << 19, 12)
    assert not (set(primesA) & set(primesB)), "prime sets must be disjoint"

    t0 = time.time()
    valA, MA, resA = run("RUN_A", primesA, reverse=False, builder=sv.build_sector_matrix)
    valB, MB, resB = run("RUN_B", primesB, reverse=True, builder=sv.build_sector_matrix_explicit)
    emit(f"# wall total {time.time()-t0:.1f}s")

    agree = (valA == valB)
    emit(f"# AGREE: {agree}")
    emit(f"# a(15) candidate = {valA}")
    emit(f"# digits = {len(str(valA))}   bits = {valA.bit_length()}")
    # CRT-bound gate: product of moduli must exceed a(15)*2^64
    boundA = valA * (1 << 64)
    emit(f"# RUN_A modulus ({MA.bit_length()} bits) > a*2^64 ({boundA.bit_length()} bits)? {MA > boundA}")
    emit(f"# RUN_B modulus ({MB.bit_length()} bits) > a*2^64 ({boundB_ok:=MB > boundA})")
    # growth gate (reported literally)
    growth = valA ** (1.0/ (N*N))
    emit(f"# growth a(15)^(1/225) = {growth:.9f}")
    emit(f"# ice constant W=(4/3)^1.5 = {W:.9f}   |diff| = {abs(growth-W):.6e}  (<1e-3? {abs(growth-W)<1e-3})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
