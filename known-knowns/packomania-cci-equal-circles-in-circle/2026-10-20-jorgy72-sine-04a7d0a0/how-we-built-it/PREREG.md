# PREREG — 2026-10-20T09:06Z (frozen BEFORE any attack output is scored)

Target: packomania-cci-equal-circles-in-circle, row N=3949 (bank partial win p2 class:
gap value N > 2600 with a lattice-like seed by Specht).

## Criterion (operative numbers, from the live scout 2026-10-20T08:59:32Z)
- Table radius r_table(3949) = 0.014965462848801963307763269064
  (line 3949 of data/radius.txt, sha256 6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead).
- WIN iff a file of 3949 centers (x_i, y_i) satisfies ALL of:
  (a) r* := min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) computed in mpmath at 50 digits
      directly from the submitted coordinates, no tolerance, satisfies r* − r_table ≥ 1e-11;
  (b) the configuration is not isometric to the posted data/cci3949.txt
      (sha256 b752757bcac8a46337373b99cec43c5c25b0abceed9bdfd0a054c00b5857180b):
      sorted pairwise-distance multisets differ;
  (c) N=3949 does not appear in a History-of-updates line on live cci.html newer than the
      scout (newest seen: 11-Oct-2026, Zii Fave N=15 proofs);
  (d) N=3949 is outside every cci range on the live pending-requests page at verification
      time (currently: 652–3943 by Vidit Patankar, 15-Oct-2026; page re-fetched before any claim).
- CAVEAT (always stated): the 26-Sep-2026 Moki & Julio "*many*" 4666-candidate bundle is
  category-unspecified and cannot be resolved; the N must be re-checked against the live
  table once that bundle disappears from the pending list.
- Verdict scale: CONFIRMED_* only via three-skeptic panel + CHECK_RUN: PASS; otherwise at
  most PROMISING (single context). A configuration equal to the table within 1e-11 but
  certified non-isometric = bank partial win p1. Clean negatives = NOTHING.

## Statistic / checker that judges it
code/checker.py: `check(path, N)` prints r*, table value, and margin = r* − r_table at 50
digits. Non-isometry via `distance_multiset()` differing from the posted seed's multiset.
Validated this run: positive (posted cci3949.txt reproduces table value) and negative
(single center perturbed by 1e-6 collapses the margin) — see attempts/*/output or the
selftest log in data/.

## Thresholds
- margin ≥ 1e-11 (mpmath 50 digits, no tolerance): required for any win claim.
- margin in (0, 1e-11): documented as negative (feasibility-slack artifact class).
- margin ≤ 0: negative.

## Null design
null_test: not needed because the claim is an explicit geometric object checked by a
deterministic checker against a published table value — there is no search statistic,
threshold tuned on data, or "beats chance" component. The checker itself is validated on a
known positive and a known negative before any attack output is scored.

## Scope guard
One object per claim (single N). No bundling across N values. Dedupe: if two lenses find
the same object, panel one carrier and cite the other.
