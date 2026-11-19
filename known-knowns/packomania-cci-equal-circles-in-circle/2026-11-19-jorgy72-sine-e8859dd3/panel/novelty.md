context: subagent (fresh context, spawned as the argue-against skeptic)

# NOVELTY / ARGUE-AGAINST report — N=4345 claim, run 2026-11-19-0200

Claim under attack: `attempts/deep-polish-4345/output/polished03.txt` holds 4345 centers with
feasible radius r* exceeding the live Packomania table radius for N=4345
(0.014273228279866076598567467525) by >= 1e-11. Claimed r* = 0.01427701232602575290682290312898,
margin +3.784e-06. Second file polished00.txt claimed at margin +1.713e-06.
Posted seed: `data/cci4345.txt` (sha256 69ad4fb26db93650da3deb76382d1f01a7e99acb884b65a51cf951dd93b20285 — verified, matches).

Method: all checks done with my own code (a scratch script written fresh for this check, numpy float64 pre-filter +
exact mpmath at 50 digits on near-binding terms only). The run's `checker.py` was NOT used for
any numeric result. Live pages re-fetched by me with curl, UA "V3R1T4S-skeptic", HTTP 200 both.

## Attack 1 — NON-ISOMETRY: PASS (attack failed, claim survives)

Recomputed sorted pairwise-distance multisets independently (9,437,340 pairs each, float64):

- seed vs polished03: max |diff| = 2.664e-03, fraction differing by >1e-9 = 1.000000,
  median |diff| = 6.826e-04, fraction >1e-12 = 1.000000.
- seed vs polished00: max |diff| = 2.418e-03, fraction differing by >1e-9 = 0.999999,
  median |diff| = 6.154e-04, fraction >1e-12 = 1.000000.

An isometry would agree to ~1e-15. Observed differences are ~1e-3 — twelve orders of magnitude
above float noise, and essentially every pair differs. Both polished files are genuinely
different configurations from the posted seed, not relabelled/rotated copies. I also tried the
cheap version of this attack first (comparing raw row order) and discarded it: row order is
arbitrary, the multiset is the correct test, and it still kills the isometry hypothesis outright.

## Attack 2 — QUEUE RULE: PASS (attack failed, claim survives)

Re-fetched https://packomania.com/pending-requests.html myself (HTTP 200).
sha256 5d2539316e409ed4359db5b1b040bc9bc51d4a120dd1ce37ee0abd34ce8523bd — byte-identical to the
run's stored `data/pending-requests.html`. The only cci ranges on the page are:
- Vidit Patankar, 15-Oct-2026: cci 652–3943 (193 candidates)
- Karl Desfontaines, 03-Nov-2026: cci 126–4141 (487 candidates)

N=4345 is inside NEITHER range (4141 < 4345), and the string "4345" does not occur anywhere on
the page. No pending candidate covers N=4345, so no queue-rule block applies. (Other categories
on the page — csq, ccq, scu, etc. — are different packing problems, not cci.)

## Attack 3 — HISTORY: PASS (attack failed, claim survives)

Re-fetched https://packomania.com/cci/cci.html myself (HTTP 200).
sha256 de37305f030c7380a1f92f2039c0a5a8a937a9b81a1efa2b16c0a3652dcae5e0 — exactly the expected
value, and byte-identical to the run's stored `data/cci.html`.
- Live table row for N=4345 confirmed: r = 0.014273228279866076598567467525 (row `cci4345.html`).
  This is the value the claim is measured against.
- History-of-updates section: newest entry is 11-Oct-2026 (Zii Fave, computer-assisted proofs
  for N=15). No update line newer than 11-Oct-2026 exists at all, and no History line mentions
  N=4345 (string "4345" absent from the whole Updates section). The table has not moved under
  the claim.

## Attack 4 — MARGIN REALITY: PASS (attack failed, claim survives)

My own 50-digit recomputation (float64 pre-filter, exact mpmath on all pairs within 1e-6 of the
minimum distance and all radii within 1e-6 of the maximum — float64 error ~1e-16, so the 1e-6
window cannot miss a binding term):

- seed: r* = 0.01427322827986607659856746752391, margin = -1.091e-30, binding pair (3381, 3386).
  Reproduces its table row to ~1e-30, as expected from 30-decimal rounding of the posted
  coordinates. The seed is exactly the posted packing, not something better.
- polished03: r* = 0.01427701232602575290682290312898, margin = +3.78405e-06,
  x-bar multiple = 378,405. WALL binds (outermost center idx 4344; r_wall = 0.01427701232602575290682290312898
  vs r_pair = 0.01427704874094016452444505505442 for binding pair (4070, 4319)).
  Margin is 378,405x the 1e-11 bar.
- polished00: r* = 0.01427494170770364823724347769621, margin = +1.71343e-06,
  x-bar multiple = 171,343. WALL binds (outermost center idx 4332; binding pair (4088, 4332)).

All three r* values reproduce the run's check50 logs digit-for-digit to all 31 printed digits.
The margins are real, far above the bar, and rest on a single outermost center in each case —
which is legitimate: r* is defined as min(pair/2, 1 − max|c|), and the wall term is the binding
one. No hidden tolerance or rounding props the numbers up.

## Attack 5 — FILE INTEGRITY: PASS (attack failed, claim survives)

All three files (seed, polished03, polished00): 4345 rows each, indices 1..4345 in order,
exactly 3 fields per line, all coordinates finite, no duplicate centers (checked both exact
string duplicates and float duplicates). |c| maxima: seed 0.98572677172013401,
polished03 0.98572298767397426, polished00 0.9857250582922964 — all inside the unit circle,
consistent with the wall-binding radii above.

## Attack 6 — HONEST-ARTIFACT HUNT: PASS (attack failed, claim survives)

Inspected `code/checker.py` in full and the three check50 logs plus `data/selftest.log`.
- `feasible_radius` is a full O(n^2) mpmath computation at dps=50, exact decimal parsing via
  `mp.mpf` on the coordinate strings, no tolerance, no float64 anywhere in the radius path.
  `float()` appears only in `distance_multiset` (isometry sanity, not the margin) and in the
  margin's `%.3e` display formatting.
- One wording correction, not an artifact: the logs print `mp.nstr(r_star, 31)` — 31 significant
  digits, not 50. That is still far more precision than needed: print truncation is ~1e-33
  absolute, and mpmath rounding at dps=50 is ~1e-49. Total possible flattery is bounded at
  ~1e-30 — 19 orders of magnitude below the 1e-11 bar and 24 orders below the 3.784e-06 margin.
  My independent 50-digit recomputation reproduced every printed digit exactly, which
  independently confirms the printed values are the true values.
- `data/selftest.log`: positive test reproduces the N=100 table to 8.7e-31, multiset self-match
  passes, negative test (one center perturbed by 1e-6) collapses the margin to −4.659e-07.
  The checker demonstrably detects both exact reproduction and genuine breakage.
- `data/radius.txt` row for N=4345 (0.014273228279866076598567467525) matches the live table row
  I fetched myself; the run's stored `cci.html` / `pending-requests.html` are byte-identical to
  my fresh fetches, so no stale-page substitution is in play.
- No float-rounding or printing artifact capable of flattering the margin was found. The
  largest conceivable artifact (~1e-30) is negligible against both the bar and the margin.

## Verdict

Every attack failed. The claim survives all six lenses:
- polished03 beats the live table by +3.784e-06 (378,405x the bar), wall-binding;
- polished00 independently beats it by +1.713e-06 (171,343x the bar), wall-binding;
- neither is isometric to the posted seed; N=4345 is in no pending queue range; the live table
  and its history are unchanged since 11-Oct-2026; files are clean; the checker has no
  flattering artifact and my independent 50-digit recomputation agrees digit-for-digit.

No "Needs you" items. Nothing in this review blocks the claim; submission remains Michael's call.

pass: true
