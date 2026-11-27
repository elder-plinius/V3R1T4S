# CRITERION verdict — round 3 (17-cell row-29 claim), fresh-context panelist

context: subagent

Claim judged: the 17 integers T(29,k), k=12..28, of OEIS A210662 (monomer-dimer
tilings of the n x k board), against bank partial win p2 of target
square-grid-lattice-gas-exact-counts-oeis, quoted verbatim in CLAIM.md:
"A new row of an associated rectangular table (A210662 monomer-dimer m x n,
A089980 hard squares m x n) extending the largest published m by one for all
n up to the published range, same rules."

## What I ran myself (all numbers below are from my own command output)

1. Official checker: `verify_claim.py` in the claim folder, run by me —
   prints PASS: own exact DP 78 published cells (n<=12) + claimed k=12;
   22+22 primes disjoint, all Miller-Rabin (bases 2..37) prime; runA CRT
   378 published + 27 anchor cells exact, 17/17 claimed exact; runB same.
   Cosmetic defect noted: its step-1 print says "12 claimed cells" but the
   object holds k=12..28, so only k=12 is DP-checked in that step (loop is
   correct, message overstates — leftover from the 28-cell round-1 object).
2. My own from-definition exact big-integer DP (panel/indep_dp.py — a
   column-transfer formulation with memoized per-mask column fills, a
   different code structure from the checker's cell-frontier sweep):
   88 published cells exact (all 36 with n<=8, plus the deep slab
   n=24..27, k<=13); all 11 disclosed context cells T(29,1..11) exact;
   14 anchor cells T(28,1..14) exact; CLAIMED cells T(29,12), T(29,13),
   T(29,14), T(29,15) exact; 8 individual residue lines (k=13 and k=15,
   two primes from each run) match my exact values mod p. INDEP_DP: PASS.
3. My own CRT over the residue files (panel/indep_crt_growth.py): all
   17 cells reconstructed exactly from EACH run separately (22 residues
   per cell per run); min combined modulus 1343 bits vs the rigorous need
   29*28*log2(3) = 1287.0 bits (bound T(m,n) <= 3^(mn): every matching
   injects into {monomer, right-dimer, down-dimer} per cell). Primes:
   |A|=22 (min 2^61+3,000,027), |B|=22 (min 2^61+103,000,017), overlap 0,
   all pass MR bases 2..37 (deterministic below 3.3e24; these are ~2.3e18).
4. My own growth fit (no numpy, my own 2-parameter least squares): on all
   53 published cells of rows 26-27: lnW=0.658491669, W=1.9318762 (exactly
   the claim's recorded fit), c=4.1524, maxres=1.06e-2, tol=3.19e-2.
   Row-29 worst deviation 1.19e-3 vs tol 3.19e-2 -> PASS with 27x headroom.
   Roots exp(lnT/(29k)): 1.9068768 (k=12) rising monotonically to
   1.9197398 (k=28), all below Finch's 1.9402139258. Finite-size ladder
   r(27,k)<r(28,k)<r(29,k): k=20: 1.9152256/1.9155602/1.9158718; k=24:
   1.9174563/1.9178037/1.9181272; k=27: 1.9186966/1.9190512/1.9193813.
5. Live re-fetch today (WebFetch of oeis.org): b210662.txt has exactly 378
   data lines = rows n=1..27, ending at T(27,27), tail identical to the
   claim's local copy; entry page: name "Triangle read by rows: T(n,k)
   (1<=k<=n) = number of monomer-dimer tilings of an n X k board"; FORMULA
   maps exactly columns T(1..11,n)=A000045(n+1), A030186(n),
   A033506..A033514(n) and the diagonal T(n,n)=A028420(n); b-file extent
   "Rows n = 1..27, flattened"; no row-28/29 material published.

## The four explicit criterion questions

(a) Is 17 cells "a new row ... for all n up to the published range", or a
stretched partial? NOT a stretch. The published range of the second index is
k=1..27 (fullest published row, row 27). Row 29 is delivered complete over
that range: k=12..27 are the 16 claimed novel cells, and k=1..11 are the
entry's own published column terms (FORMULA line, verified live; T(29,1)=
832040=A000045(30)=F(30) checked by me against my DP as well), disclosed in
row29_crosspublished_context.json and equal to my from-definition DP on all
eleven. k=28 extends one beyond the range. The diagonal T(29,29)=a(29) of
A028420 is properly excluded — p2 only requires n up to the published range,
and that cell is main-criterion material. Decisive reductio against the
stricter reading: NO row-extension of this table could ever claim novel
k=1..11 cells (they are published by the entry's own FORMULA for every row),
so "a new row" must mean the row delivered complete — exactly what this
package does, with honest disclosure of which cells are new.

(b) "Extending the largest published m by one": live largest published m=27
(verified today); row 28 (the literal +1 row) exists as the same author's
open unmerged PR #960 and sits inside this package as the 27-cell anchor
object — verified by me against the definition by exact DP (k=1..14) and by
both runs' CRT (27/27 each, checker plus my own CRT where covered). The
claimed row 29 extends the frontier by one beyond row 28, i.e. by two beyond
the live b-file. I read "extending ... by one" as the minimal qualifying
increment of a partial-win clause, not a cap: a package that establishes the
complete +1 row (row 28, verified here to the same standard) AND the next
row's novel cells strictly contains the p2 deliverable; rejecting it for
exceeding the bar would punish supersets. No reading of the bank sentence
makes "by one and no more" sensible. The claim's own framing ("row 29
extends the computed frontier by one beyond it") is accurate.

(c) Two-run independence / reproduction: satisfied and over-verified. RunA
(22 primes > 2^61+3e6, left-to-right sweeps, mode=sliced) and runB (22
disjoint primes > 2^61+103e6, right-to-left sweeps, mode=fast) are described
as independently written; each reproduces ALL 378 published cells and ALL 27
row-28 anchor cells exactly, and agree on every claimed cell (my own CRT,
not only the checker's). On top: the checker's own exact DP confirms claimed
k=12 from the definition, and MY independent from-definition DP confirms
k=12..15 plus 88 published, 14 anchor, 11 context cells and 8 raw residue
lines — a third and fourth implementation. Residual shared-bug exposure is
confined to k=16..28 at j=29 only; any such bug would have to survive two
independent codes, vanish on 405 verified cells spanning state widths up to
27, vanish at j=29 for k<=15, and land all 13 cells within 0.12% of the
fitted growth surface (my worst trajectory deviation 1.19e-3 in ln) — for
exact integers produced by computational error modes (truncation, overflow,
off-by-one), not credible. The L2R-vs-R2L sweep-direction difference is a
weaker form of "different decomposition" than the criterion's row-vs-column
example, but the criterion's alternative escape ("or one exact big-integer
run") is literally met for k=12..15, and the reproduction web covers the
rest to a standard I accept.

(d) GROWTH in substance: the frozen test (fit rows 26-27, predict the
trajectory; frozen since the row-28 arc, unchanged through PREREG.v2/.v3 —
no threshold moved) passes: my refit reproduces W=1.9318762 exactly;
row-29 worst deviation 1.19e-3 vs tol 3.19e-2; roots monotone rising,
all below Finch. The literal 1e-3 parenthetical of the MAIN criterion is
NOT met by the finite-size fit (|1.9318762-1.9402139258| = 8.338e-3), but
it cannot be met at these sizes by TRUE values either: the published
diagonal itself gives a(27)^(1/729) = 1.9186966, which misses Finch by
2.152e-2 — the parenthetical, written as a(N)^(1/N^2) guide, is vacuous at
N~27-29 and the preregistered trajectory test is its faithful instantiation.
The deviation is honestly disclosed in the claim and identical in the two
prior packages. Consistency with the known growth constant holds in
substance: every claimed cell sits on the published rows-26/27 trajectory,
27x inside tolerance, converging toward Finch from below exactly as rows
27->28->29 should (ladder increments ~3.3e-4).

## Remaining caveats (do not change the verdict)

- The anchor row 28 is the claimant's own unmerged PR; it is used as an
  anchor, not claim material, and I verified 14 of its 27 cells against the
  definition myself. If PR #960 were rejected, the p2 deliverable still
  stands on this package's evidence (rows 28 and 29 both computed and
  verified here).
- verify_claim.py's step-1 print overstates ("12 claimed cells" — only
  k=12 is in scope of the 17-cell object); cosmetic, the gates are real.
- runA/runB scan-direction independence is weaker than a row-vs-column
  design; noted above, compensated by two from-definition exact DPs and
  full-table reproduction.

Conclusion: the 17-cell claim is the precise novel content of a complete
row-29 extension of A210662 (published columns disclosed, diagonal
excluded), verified to a standard exceeding the "same rules" bar, novel
against the live entry as re-fetched today, and growth-consistent under the
frozen preregistered test. p2 is met in substance and exceeded; none of the
strict-literal objections survives scrutiny (the "+1" reading as a cap is
absurd; the all-n-cells reading is impossible for this table; the 1e-3
parenthetical fails published truth itself). I confirm at the claim's own
scope and no wider.

confirmed_scope: The 17 integers T(29,k) for k=12..28 of OEIS A210662 (monomer-dimer tiling counts of the 29 x k board) — the cells of row 29 beyond the entry's published columns k=1..11 — are correct as claimed (two-run CRT verified with all 378 published cells and the 27-cell row-28 anchor reproduced, from-definition exact DP confirmation for k=12..15, growth on the published trajectory below Finch's constant), meeting bank partial win p2 for target square-grid-lattice-gas-exact-counts-oeis.

pass: true
