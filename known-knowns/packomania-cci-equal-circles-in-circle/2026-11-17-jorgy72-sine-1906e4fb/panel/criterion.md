context: subagent (fresh context, spawned as the criterion judge)

# CRITERION verdict — N=4315, carrier polished00.txt

Claim carrier (single object): `attempts/deep-polish-4315/output/polished00.txt`
— 4315 centers, sha256 `1906e4fbe7ef3aa8a9c86ebe76ba832b911353290310739b8be799a235fef3a8`
(file integrity re-verified by sha256sum this judgment).
Table value (live radius.txt row N=4315, sha256 `6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead`,
byte-identical in `data/radius.txt` and `data/radius-verify.txt`):
r_table = 0.014323541476018172725671907488.
Posted seed `data/cci4315.txt`, sha256 `9af86ffc1a5fcc6ba0165682e81f4576e39fe21caa31284b973164aa9f3bccc5`
(matches PREREG exactly).

## Independent recomputation by this judge (own script, written fresh for this judgment)

Method: double-precision full-pairwise screening (numpy blocks) to locate the
minimal pair distance and maximal radius, then exact mpmath evaluation at
50 digits of every pair within 1e-9 of the double minimum (candidate: 1 pair;
seed: 9062 pairs) and of every center within 1e-9 of the maximal radius.
Double rounding on a distance is ~1e-16, so no pair outside the 1e-9 screen
can be the true 50-digit minimum. This is a different code path from the
run's checker and from panel/verify_claim.py.

- polished00: 50-digit min pair distance = 0.02864909554138574257518887599171585937324
  (centers 4061, 3823); 50-digit max |c| = 0.9856753507682294949086219674238319197767.
  r* = min(dmin/2, 1-max|c|) = 0.01432454777069287128759443799585792968662
  (pair-limited; wall term 0.0143246492317705051 is larger).
- Margin: r* - r_table = 1.006294674698561922530507857929686619294e-06,
  i.e. 100,629x the 1e-11 threshold.
- Parser sanity: seed cci4315.txt recomputed the same way gives
  r* = 0.01432354147601817272567190748741258486229, i.e. r* - r_table = -5.874e-31,
  well within the bank's 1e-20 parser-sanity bound.

Note on the carried numbers: the brief's r* (0.014324547770692870607422975127)
and the check50 logs' r*/table prints are the run checker's float-rounded
`%.30f` prints of double values, not true 50-digit values — the true 50-digit
r* above differs from the carried value by ~6.8e-16. Immaterial: the margin
is +1.006e-06 under either reading. The check50 log's margin (+1.006e-06)
and the independent double recompute in panel/recompute.log
(feasible_r = 0.014324547770693, margin +1.006e-06) agree with my 50-digit
margin to ~1e-15.

## Condition-by-condition judgment (PREREG (a)–(d))

(a) r* - r_table >= 1e-11 at 50 digits, no tolerance: **PASS**.
    Margin verified by this judge at 50 digits: +1.0062946746985619e-06,
    100,629x the threshold. No tolerance was applied or needed.

(b) Not isometric to posted seed cci4315.txt (sorted pairwise-distance
    multisets differ): **PASS**, decisively.
    - Panel's full-multiset comparison (panel/non_isometry.log, 9,307,455
      pairs each side): max abs diff 6.607512e-03, mean 5.747546e-04,
      fraction of entries differing by >1e-9 = 1.0000; multisets not identical.
    - My independent invariants (different code path, scipy KD-tree/numpy):
      nearest-neighbour distance multisets differ (candidate min 0.028649095541,
      median 0.028660746690, sum 123.673238268; seed min 0.028647082952,
      median 0.028647082952, sum 123.623873792); sorted radii differ
      (candidate innermost |c| = 0.010255241832 vs seed innermost 0.000078275799 —
      the seed has a center essentially at the origin, the candidate does not);
      distances from center 1 differ (sums 2847.865 vs 4819.852).
      An isometry preserves all of these; they differ by orders of magnitude
      more than any rounding. Also corroborating: the seed has 9062 pairs within
      1e-9 of its minimum (jammed/lattice-like contact set) vs exactly 1 such
      pair in the candidate.

(c) N=4315 does not appear in a History-of-updates line on live cci.html
    newer than the scout: **PASS**.
    Checked `data/cci-verify.html` (sha256 de37305f030c7380a1f92f2039c0a5a8a937a9b81a1efa2b16c0a3652dcae5e0,
    byte-identical to the scout fetch): the Updates section (lines 3173–3414)
    contains zero mentions of "4315" and zero of "4303"; its newest entry is
    11-Oct-2026 (Zii Fave N=15 proofs), matching the scout; the only other
    "11-Oct-2026" in the file is the page copyright footer. No date in the
    file is newer than 11-Oct-2026. The N=4315 table row in cci-verify.html
    reads 0.014323541476018172725671907488, matching radius.txt.

(d) N=4315 outside every cci range on the live pending-requests page at
    verification time: **PASS**.
    Checked `data/pending-requests-verify.html` (sha256
    a9dc3a8cdb18979f5053a009ed906d31ff1d14d0ab078ffbc23efa3bf8da103c,
    byte-identical to the scout fetch): the only cci ranges are
    Patankar 652–3943 (15-Oct-2026) and Karl Desfontaines 126–4141
    (03-Nov-2026). 4315 is outside both. "4315" occurs 0 times in the file.
    Moki & Julio caveat (bank): the "4666" bundle occurs 0 times — absent
    from the live pending page, so the caveat does not bite and no re-check
    deferral applies.

## Bank taxonomy ruling

The object meets the bank's FULL success criterion literally, clause by
clause: N=4315 is listed in radius.txt; r* exceeds the live 30-decimal table
value by >= 1e-11 at 50 digits with no tolerance (+1.006e-06); the
configuration is not isometric to the posted cci4315.txt (sorted distance
multisets differ); N=4315 appears in no History-of-updates line newer than
the scout fetch; N=4315 lies outside every cci range on the live
pending-requests page at verification time; and the Moki & Julio "4666"
bundle is absent from that page. The success_criterion text contains no
N-range restriction and no carve-out for gap values.

Taxonomy note / disagreement flagged for the panel: the bank ALSO lists
this exact shape as partial win p2 ("a certified improvement for one of
the gap values N > 2600 that the table lists ... where the record is a
lattice-like seed by Specht"), and the PREREG classifies the N=4315 row as
"p2 class" (author Eckard Specht, [31]). p1 does not apply (N=4315 is not
in 1..2600, and the margin exceeds 1e-11 rather than equalling the table
within 1e-11). p3 does not apply (sibling chx table, not cci). The bank
text does not state that satisfying p2 precludes the full criterion, nor
that gap values are excluded from full success — so on a literal reading
this object satisfies BOTH the full success criterion and the p2
description, and the precedence between the two labels is unresolved in
the bank text. My literal reading favours FULL (nothing in the success
criterion excludes it; the margin is 100,629x threshold, a genuine
improvement over a live table row, not a slack artifact); the panel/gate
may rule it CONFIRMED_p2 under the prereg's class framing. Either way the
claim is a certified improvement, not a partial-win-only or negative
outcome. This is a labelling question for the panel, not a defect in the
object.

## Scope guard

**Satisfied.** The claim as judged is the single object polished00.txt
(N=4315) only. polished01.txt (+9.735e-07 by the independent double
recompute in panel/recompute.log; its own check50 log agrees) is cited in
the brief but NOT bundled into this claim and was not counted here; it is
a separate object for a separate claim if ever carried. No cross-N
bundling (N=4303 is a different row, not part of this claim).

## Summary

- (a) margin +1.0062946746985619e-06 at 50 digits — PASS
- (b) non-isometric (full multiset + independent invariants) — PASS
- (c) no newer History line for N=4315; newest 11-Oct-2026 — PASS
- (d) outside Patankar 652–3943 and Karl 126–4141; "4666" bundle absent — PASS
- Scope guard (one object per claim) — satisfied
- Taxonomy: full success criterion met literally; p2 description also
  applies; precedence unresolved in bank text — flagged for panel; my
  literal reading favours FULL.

No outward action taken (verification only, inside the V3R1T4S workspace and a scratch folder).

pass: true
