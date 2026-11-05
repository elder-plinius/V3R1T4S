context: subagent (fresh context, spawned as the criterion judge)

# Criterion-judge verdict — N=4153, `polished03.txt`

**Claim carrier (single object):** `attempts/deep-polish-4153/output/polished03.txt` — 4153 rows, sha256 `78e5f27ee4ad7650b05428ed80473d4feb231c05d8375f2e44ae17d4b742242b`.

## Condition-by-condition

**(a) Margin ≥ 1e-11 at 50 digits — PASS**

- `certify_polished03.log`: r\* = `0.014599128044136329418467568075`, margin `2.706e-06`.
- Recomputed against the correct table value in `data/radius.txt` (row 4153: `0.014596422226478759387097611060`, sha256 `6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead`; `data/radius-verify.txt` byte-identical): margin = **+2.70581765757e-06**, i.e. **~270,582× the 1e-11 threshold**.
- `recompute.log` independently agrees: polished03 `+2.705818e-06`, block-pairwise and kD-tree agree (`agree=True`).
- Checker validated: `data/selftest.log` ALL PASS (posted cci100 reproduces table to 8.7e-31; perturbed centre collapses to −4.659e-07).
- Minor discrepancy, immaterial: the certify log's printed table value (`…478758879530950310`) differs from `radius.txt` (`…478759387097611060`) by 5.08e-19 — it changes the margin only in the 19th decimal. Also, `deep_polish.log`'s ranked value for polished03 (`+2.930e-06`) is a tracked polish-loop figure and disagrees with the recomputed `+2.706e-06`; per the prereg margin-reporting rule the recomputed value governs. Neither affects the verdict.

**(b) Non-isometric to posted seed — PASS**

- Posted seed `data/cci4153.txt`: 4153 rows, sha256 `bca1f6739e2a898d6862658e092f0e105667652dac18340da863a8d2eb94ffae` — matches prereg and scout.
- `non_isometry.log`: multiset sizes 8,621,628 each (= 4153·4152/2), max abs multiset diff `3.178732e-03`, mean abs diff `4.800206e-04`, `identical multisets: False`. Sorted pairwise-distance multisets differ, as required.

**(c) No History-of-updates line newer than the scout touching N=4153 — PASS**

- Scout `data/cci.html`, sha256 `de37305f030c7380a1f92f2039c0a5a8a937a9b81a1efa2b16c0a3652dcae5e0`. Newest History-of-updates line is **11-Oct-2026: Zii Fave, two computer-assisted proofs for N=15**; it is the only 2026 date in the file, and no history line mentions N=4153. The one-line move since 2026-11-04 is cosmetic only (ref [31] year 2024 → 2026).
- Caveat: this is judged on the scout's 2026-11-05 `cci.html` fetch; no separate verification-time `cci.html` re-fetch was in the evidence set (the verification-time re-fetch supplied was the pending-requests page, for (d)).

**(d) N=4153 outside every live cci pending range at verification time — PASS**

- `data/pending-requests-verify.html` (sha256 `d3d58d3213208ddf652aaeb712a07ba13826f0492b9ee6c130743617b77d9b61`, header/footer dated 05-Nov-2026): the only `cci` lines are **Patankar 652–3943** (15-Oct-2026) and **Karl Desfontaines 126–4141** (03-Nov-2026 20:33). 4153 is outside both (12 above Karl's 4141 ceiling). The string "4153" occurs **0 times** in the file. The Warren Smith lines (ccis 76–99, ccic 55–98) are different categories, not cci.
- Diff vs the scout pending page (sha256 `5bdaeb2c…`) is only the 04→05-Nov date header/footer plus an empty HTML comment — no range changed.

## Bank criterion

**FULL CRITERION MET** (not partial-only).

The bank success criterion for `packomania-cci-equal-circles-in-circle` requires exactly (a)–(d) above for one N listed in `radius.txt`, and all four pass. The p2 partial-win description **also fits**: N=4153 is a gap value > 2600 listed in the table, and `data/author.txt` line 2712 gives author **Eckard Specht** for 4153 (scout: Specht lattice-like seed, density 0.8848). But p2 is subsumed — the claim satisfies the full criterion, so it is not merely a partial win. p1 does not apply (margin is far above 1e-11, not a tie); p3 is a different table (chx) and does not apply.

## Scope guard

One object per claim is respected: the claim is **polished03.txt only**. The run also polished three other above-bar candidates — `polished00 +2.349101e-06`, `polished01 +1.987954e-06`, `polished02 +2.476255e-06` (recompute.log, both evaluators agreeing) — but they are not bundled into this claim and do not affect the verdict; polished03 is the best and the sole carrier. The N=4000 walk state is not part of this claim.

## Overall verdict

**FULL CRITERION MET** — single-judge ruling. Per the prereg verdict scale, a `CONFIRMED_*` label still requires the three-skeptic panel plus `CHECK_RUN: PASS`; this ruling is one judge's pass on all four prereg conditions.

pass: true
