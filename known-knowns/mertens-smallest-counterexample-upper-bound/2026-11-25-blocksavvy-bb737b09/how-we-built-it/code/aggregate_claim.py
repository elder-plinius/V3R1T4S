"""Claim checker: sums chunks_head128/ (n = 1..600,000, 128-bit; or the dir given as argv[1], e.g. chunks_head = 96-bit) and chunks_tail/ (n = 600,001..2,325,573) written by k2_chunks.py,
checks contiguity, recomputes the two zeros at the T0 boundary (n = 2,325,572 and 2,325,573) and removes the
n = 2,325,573 term (gamma > T0), then compares K2 with inputs/bzyzz_k2_certificate.json.
Run from claim/: python code/aggregate_claim.py"""
import os, json, glob
from flint import arb, acb, acb_series, ctx
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
V = arb("3484971332733132396.5383341489440461"); K = arb("1.5e-10"); T0 = arb(1300000); NT0 = 2325572
def contiguous(d, a):
    fs = {}
    for f in glob.glob(os.path.join(R, d, "c_*.json")):
        j = json.load(open(f)); fs[j["n0"]] = j
    ctx.prec = 192; n, S, k = a, arb(0), 0
    while n in fs: S += arb(fs[n]["S"]); n += fs[n]["cnt"]; k += 1
    return S, n - 1, k, len(fs)
import sys
HEAD = sys.argv[1] if len(sys.argv) > 1 else "chunks_head128"
Sh, lh, kh, fh = contiguous(HEAD, 1); St, lt, kt, ft = contiguous("chunks_tail", 600001)
ctx.prec = 128
z = acb.zeta_zeros(NT0, 2); g1, g2 = z[0].imag, z[1].imag
zp = acb_series([z[1], 1], prec=2).zeta().coeffs()[1]
ctx.prec = 192
term = (-(K * g2 * g2)).exp() * (acb(0, g2 * V).exp() / (z[1] * zp)).real
K2 = 2 * (Sh + St - term)
bz = json.load(open(os.path.join(R, "inputs", "bzyzz_k2_certificate.json")))
E = arb("2.391e-11")  # the certificate's own error bound (bzyzz THEOREM.md, E <= 2.391e-11); taken as given, not checked here
out = {"head_dir": HEAD, "head": [1, lh, kh, fh], "tail": [600001, lt, kt, ft], "complete": lh == 600000 and lt == NT0 + 1,
       "gamma_2325572": g1.str(22, radius=True), "gamma_2325573": g2.str(22, radius=True),
       "boundary_ok": bool(g1 < T0 and g2 > T0),
       "K2_head": (2 * Sh).str(18, radius=True), "K2_tail": (2 * (St - term)).str(12, radius=True),
       "K2": K2.str(18, radius=True), "bzyzz_K2": bz["K2"], "bzyzz_main_n<=600000": bz["K2_main_(n<=600000)"],
       "head_overlaps_bzyzz_main": bool((2 * Sh).overlaps(arb(bz["K2_main_(n<=600000)"]))),
       "overlaps_bzyzz_K2": bool(K2.overlaps(arb(bz["K2"]))), "contained_in_bzyzz_K2": bool(arb(bz["K2"]).contains(K2)), "lower_K2_minus_E_minus_1": float((K2 - E - 1).lower())}
print(json.dumps(out, indent=1))
