context: subagent (fresh context, spawned as the criterion skeptic)
# CRITERION verdict — N=4357 claim (polished01.txt), run 2026-11-20-0200

Judge: CRITERION skeptic (independent). All numbers below were recomputed
by this judge from the candidate file and from fresh live fetches; no
checker.py code was reused. My scripts: an independent scratch directorycriterion_rstar.py
(mpmath 50-digit r* via float64 screening + exact recompute of the binding
terms) and an independent scratch directorycriterion_noniso.py (own sorted-multiset code).
Live fetches in an independent scratch directory (radius-live.txt, cci-live.html,
pending-live.html, cci4357-live.txt), curl, UA "V3R1T4S-criterion-judge".

## Hash verification (scout / verify copies vs my fresh live fetch)
- radius.txt: scout 6c60da0a… / radius-verify.txt 6c60da0a… / my live fetch
  6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead — identical.
- cci.html: scout/verify de37305f… / my live fetch de37305f030c7380a1f92f2039c0a5a8a937a9b81a1efa2b16c0a3652dcae5e0 — identical.
- pending-requests.html: scout/verify 5d253931… / my live fetch
  5d2539316e409ed4359db5b1b040bc9bc51d4a120dd1ce37ee0abd34ce8523bd — identical.
- cci4357.txt: run copy 778c91a9… / my live fetch
  778c91a9e89b42372303330e2d3faf7a8bea563cb402da399cd893d1d13da959 — identical.
- Candidate polished01.txt sha256 d82bab7925486928eec1ff24ff9a562768928c24d34d15263b2535295a6b9248.
- Live table row N=4357 (my fetch): 0.014255170553446144330034824715. Author: Eckard Specht (data/author.txt).

## (a) Margin >= 1e-11 at 50 digits — PASS
- My recomputation (mpmath dps=50, exact decimals from the file):
  - binding term is the WALL at center index 4347 (0-based):
    1 - |c_4347| = 0.014260109006447964520992528545637
  - nearest pair (4109, 4347)/2 = 0.014260414315076214818780048668902,
    i.e. 3.053e-07 above the wall term — the wall binding is robust, not
    a near-tie. Second-smallest pair/2 is 1.19e-07 above the smallest pair,
    so the pair identification is robust against float64 noise (~1e-16).
  - r* = 0.014260109006447964520992528545637 — matches the claimed
    0.01426010900644796452099252854564 to 29 digits (diff ~3e-30).
  - margin r* - r_table = +4.938453e-06, i.e. ~493,800x the 1e-11 bar.
    Requirement met with no tolerance involved.
- Parser sanity (my recomputation of the posted seed, live fetch):
  seed r* = 0.014255170553446144330034824715021, margin +2.1e-32 vs the
  table — reproduces the table to ~1e-31, well inside the 1e-20 sanity
  bound. Note: the lens check50 log records the seed margin as -3.436e-31;
  mine is +2.1e-32. Both are ~1e-31 effects at the last digits (the seed
  has near-degenerate pairs at float64 resolution); immaterial to the
  claim and to parser sanity. Recorded for the record, not a failure.

## (b) Non-isometry vs posted seed — PASS
- My own sorted pairwise-distance multisets (9,489,546 pairs each,
  float64, own code): max |diff| = 3.765097e-03; 100.00% of sorted pairs
  differ by >1e-9; 99.93% differ by >1e-6; median |diff| = 3.670e-04.
- max|c| differs too: candidate 0.98573989099355208 vs seed
  0.98574482944655395. The configurations are not isometric.

## (c) No History-of-updates line for N=4357 newer than the scout — PASS
- Live cci.html (byte-identical to scout, hash above): newest History of
  updates entry is 11-Oct-2026, Zii Fave N=15 proofs. No N=4357 entry
  anywhere in the updates section. No table movement since the scout.

## (d) N outside every cci range on the live pending page — PASS
- Live pending-requests.html (byte-identical to scout, hash above): the
  only cci ranges are Vidit Patankar 652–3943 and Karl Desfontaines
  126–4141. N=4357 is outside both.
- Bank caveat (Moki & Julio "many 4666 candidates" bundle): the string
  "4666" does not appear anywhere on the live pending page, and none of
  the 24 Moki & Julio rows is category cci (they are csq, crc_*, ccq,
  crt, chx, cpd, cpt, csc, cxd, hsp4/5/6, scu, ssp). The bundle cannot be
  tied to cci on the live page; the caveat is discharged for this N.

## p2 vs FULL — recorded disagreement (not a hedge)
- The four prereg conditions (a)–(d) are exactly the bank's FULL success
  criterion, and all four PASS literally. The FULL criterion text places
  no N<=2600 restriction: it covers "one N listed in radius.txt".
- p2's text ("A certified improvement for one of the gap values N > 2600
  that the table lists (e.g. N = 4495, 5000), where the record is a
  lattice-like seed by Specht") is also satisfied literally: N=4357 is a
  listed gap value > 2600 and its author is Eckard Specht.
- The bank text never states that p2 wins are excluded from FULL, nor
  that FULL is restricted to N <= 2600 — so on a literal reading this
  claim satisfies BOTH the FULL criterion and the p2 description, and p2
  states no weaker threshold than FULL. The two labels therefore collide:
  p2 reads as a descriptive subclass of FULL wins for gap values, not as
  a weaker tier.
- Against that, the PREREG for this run labels the row "bank partial win
  p2 class", the lens verdict is CONFIRMED_PARTIAL, and the three prior
  rotation nights (N=4315, N=4339, N=4345) were all filed as
  CONFIRMED_PARTIAL under the same convention. The prereg is the frozen
  operative document for this run.
- Recommendation: follow the prereg and file this as CONFIRMED_PARTIAL
  (p2 class) for consistency with the three prior nights, and record the
  literal-FULL reading as an open classification question for the main
  session — the conditions themselves PASS either way, so this does not
  change the claim's substance, only its label. If the main session rules
  the literal bank text governs, the same evidence supports FULL.

## Scope guard — PASS (respected)
- One object per claim: the carrier is polished01.txt (N=4357) only.
  polished00 is a below-bar polish result (-2.348e-07) cited in the lens
  report/NOTES as work history ("Carrier: polished01 only; polished00
  cited, not bundled") — it is not packaged, not claimed, and not a
  second object. No bundling across N values. Dedupe: single carrier.
- Consistent with the prereg, the narrow-walk-4357 lens does not run: a
  verified above-bar claim supersedes it.

## Overall verdict: PASS
Conditions (a), (b), (c), (d) all PASS on independent recomputation
against fresh live fetches. The claim is a certified improvement at
N=4357, margin +4.938453e-06 (≈493,800x the bar), non-isometric to the
posted seed, with no live-table or live-queue obstacle. Classification:
CONFIRMED_PARTIAL per the prereg's p2-class label (see the recorded
FULL-vs-p2 disagreement above); the underlying PASS is unaffected by
that labeling question.

pass: true
