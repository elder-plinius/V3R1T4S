# Patch note: the deep_rig.py pre-filter fix made during run 2026-10-24-0818

(This package uses the same patched program, byte for byte: sha256 0e7d7d72…, as recorded in the k ≤ 25 package
2026-10-24-adb991-201bcc74. The note is kept here because the patch is part of the enumeration's history.)

During the run, the main session found that the double-precision pre-filter in `deep_rig.py` (function
`enum_pairs`, branch r ≠ 0) could drop a valid pair: it computed u = r + s·Qn in float64, and r and s have opposite
signs, so u loses its relative accuracy when Qn = q_m/q_{m+1} is tiny. The patched program (`object/deep_rig.py`,
sha256 0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341) computes u from the exact integer q in the
cells where float cancellation could exceed a relative 1e-9; elsewhere the float u is kept. Every enumeration output
in `object/out/` comes from the patched program. The unpatched program (sha256
80b744166f3c2c123baf8347e6ab39a777b4bf1543b691da6ba27968f9605161, not shipped) differs only in the lines shown in
`deep_rig_patch.diff` (output of `diff -u deep_rig_unpatched.py deep_rig.py` in the lens's code folder).

Consequences recorded in the claim (`claim/CLAIM.md`, "Things a skeptic should know"): for k = 3..18 the per-k counts
of the patched and unpatched code are identical; for k = 19..23 the window-candidate counts equal those of an earlier
unpatched run (2026-10-15). The CRITERION skeptic re-derived the error bound and confirmed the patch logic
(`panel/criterion.md`, section 3 (b)).

The lens's log entries about the patch (`attempts/extender-r2/NOTES.md` of the run, verbatim; PIDs are the lens's
own processes):

```
- ~08:48 FOUND a rigor gap in deep_rig.py's float pre-filter (enum_pairs, r ≠ 0 branch). It computed
  g = (r + s·Qn)(r·D1 + s·D0) in float64. Because r and s have opposite signs, u = r + s·Qn = q/q_{m+1} can lose all
  relative accuracy when Qn = q_m/q_{m+1} is tiny: the absolute error is ≈ |r|·2^-53 while u ≥ Qn. The filter keeps a
  pair only if g is within a relative 1e-6 of [L, U], so for Qn below about |r|·1e-10 a pair in the window could be
  dropped before the 1050-digit check. With |r| ≤ 2U + 1 ≈ 500, the risk needs a partial quotient above about 10^7.
  Gauss–Kuzmin gives P(a > A) ≈ 1/(A ln 2); with about 1000 quotients per curve over about 80,000 curves, a handful of
  such cells are expected. So this is a real hole in the completeness argument, not a theoretical one (HEURISTIC
  estimate; not measured).
  Fix: u = q/q_{m+1} computed from the exact integer q = r·q_{m+1} + s·q_m (gmpy2.mpq → float, correctly rounded).
  w = r·D1 + s·D0 has no cancellation, because both terms have the same sign. The s-interval bounds stay in float
  with a ±2 margin; their absolute error is ≤ |r|·1e-4 even at the program's amax = 10^12 cap. Unpatched copy:
  code/deep_rig_unpatched.py.
  The k = 19..25 jobs on unpatched code were stopped (own PIDs 1499, 1501, 1525; their outputs are in out/unpatched/).
- 08:5x patched run k=3..16 (validation against the unpatched counts) started in the foreground;
  08:59:15 patched k=17..22, 23..24 and 25 relaunched (PIDs in pids.txt).
- 09:04 the fully exact patch (code/deep_rig_slowpatch.py) was about 6× slower: the k = 3..16 validation reached only
  k = 15 by 673 s, against 116 s unpatched; my 900 s cap stopped it. Every count it finished (k = 3..15) equals the
  unpatched counts (out/slowpatch/).
  Final patch (code/deep_rig.py): the exact u is used only in cells where float cancellation could matter, i.e.
  Qn < 1e-4 or 3.4e-16·(R+1)/Qn > 1e-9. Elsewhere the float u has absolute error ≤ 3(|r|+1)·2^-53, so its relative
  error is ≤ 1e-9, three orders below the filter's 1e-6 tolerance. The slow-patch jobs for k = 17..25 were stopped
  (own PIDs 29421, 29423, 29424).
- 09:06:59 final runs launched: k = 3..18, 19..22, 23, 24 and 25 (out/deep_rig_final_k*_d1040.txt; PIDs in pids.txt).
- 09:27:16 final k = 3..18 done: TOTAL window candidates=42649 product solutions=0; every per-k count identical to the unpatched run (diff of out/deep_rig_k3-18_d1040.txt vs out/deep_rig_final_k3-18_d1040.txt with times stripped: empty).
```
