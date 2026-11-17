# Lens report: extender-r2 (Erdős 677), run 2026-10-24-0818

claim level: partial_win_claim

Partial win named: "an exhaustive, uncapped verification of the statement for a stated range of (n, k) with a
checkable certificate".

**Range:** every 1 ≤ k ≤ 25, every 0 ≤ n ≤ 10^494, and every m ≥ n + k.

**Result:** lcm(m+1..m+k) ≠ lcm(n+1..n+k) throughout. No counterexample exists in this range.

## How (all recomputed tonight, after PREREG.md at 2026-10-24T08:24:04Z)

- **k ≤ 2:** Lemma A gives R(k) = 1, so no admissible ratio exists (PROVED-HERE, claim/object/PROOF.md Step 1).
- **Small X** (n + k ≤ 1.1·10^6, all k): search677b, seed 4242, printed "# COMPLETE kmin=3 kmax=147
  total_candidates=2 elapsed=4s". Exact verification: "candidates: 2 exact-equal: 0" (out/search_N1.1e6.txt,
  out/verify_N1.1e6.txt).
- **Margin (k = 3..25):** proved in rigorous arithmetic by the rigor-margin lens, 63041 pairs, 0 failures. The ratio
  set is audited complete.
- **Enumeration** (QMAX = 10^495, 1040 + 50 digits, η = 0.001, X0 = 10^6), patched deep_rig.py (see below).
  Per-k counts in out/deep_rig_final_k*_d1040.txt:

| k range | file TOTAL line |
|---|---|
| 3..18 | TOTAL window candidates=42649 product solutions=0 |
| 19..22 | TOTAL window candidates=248311 product solutions=0 |
| 23 | TOTAL window candidates=314109 product solutions=0 |
| 24 | TOTAL window candidates=202516 product solutions=0 |
| 25 | TOTAL window candidates=367031 product solutions=0 |

The total is 1,174,616 window candidates and 0 product solutions. k = 24 and k = 25 are new: before tonight the
pipeline had run only to k = 23, unpanelled.

## Trying to break it myself (RUN.md step 5)

- **A completeness hole was found and fixed.** The float pre-filter dropped pairs whenever u = r' + s·Qn suffered
  cancellation (tiny Qn). The fix computes the exact u in the cells at risk (NOTES.md, 08:48–09:07). After the patch:
  - every per-k count for k = 3..18 is identical to the unpatched run;
  - for k = 19..23, the counts equal the 2026-10-15 unpatched run.
  So no pair was lost before either, but only the patched run has a proof of completeness.
- **The margin is no longer float-only.** Two independent rigorous checkers (rigor-margin lens) confirm it.
- **The margin is the one deep_rig.py uses.** It loops over admissible_r(k) with S = 1 or 4 and L, U = S·c(1∓η)
  (NOTES.md 09:36).
- **Remaining non-interval component.** L and U, and the final test q·e > L, are computed at 1090 digits, not in
  interval arithmetic. A NUMERICAL sanity solve (rigor-margin lens, out/sanity_margin_NS4.txt) puts true solutions
  within a relative 4.14e-11 of c, i.e. far inside (L, U).
- **Verdict:** SURVIVES, with the patch.

## Reproduce

See claim/REPRODUCE.md. The code is in code/:
- deep_rig.py (patched);
- deep_rig_unpatched.py and deep_rig_slowpatch.py (kept for the record);
- deep_cf.py;
- search677b.c;
- verify_cands.py.
