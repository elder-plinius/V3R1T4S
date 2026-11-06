# CRITERION skeptic verdict — A210662 row 28 (bank partial win p2)

Panel date 2026-11-03. Materials: the claim package (CLAIM.md, REPRODUCE.md, crt_ab.py,
object/, data/) and PREREG.v3.md only. Everything below marked "recomputed" comes from my
own code written for this panel: an independent CRT (pairwise merge via extended gcd), an
independent from-scratch monomer-dimer profile DP (recursive row-filling over dict
transitions — a different formulation from both claim programs), a numpy re-derivation of
the row-sweep transfer, and my own execution of run B's packaged gate/validate modes.

## 1. Is "a new row extending the largest published m by one for all n up to the published range" satisfied?

YES. The published table (claim/data/b210662.txt) is the triangular b-file: 378 terms,
rows m=1..27 with row m holding n=1..m (my decode checked against known values:
T(2,2)=7, T(3,3)=131, T(4,4)=10012, diagonal == b028420.txt for n=1..27). Largest
published m is 27; the largest published n anywhere is 27. The object (claim/object/
row28_final.json, byte-identical to the run-root copy, sha256 017aac21...) has keys
exactly 1..27 — 27 cells, none skipped, none beyond the published n-range; T(28,28) is
correctly absent (open PR #849). All 27 values are absent from the published value set,
strictly increasing (6 to 214 digits), and T(28,27) < a(28). Novelty re-checked live:
my own fetch of https://oeis.org/A210662/b210662.txt returned HTTP 200, 378 terms,
sha256 05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d — byte-identical
to the package copy. Each of the 27 cells is m=28, i.e. strictly beyond every published
cell. (T(28,1)=514229=F(29) of course exists in A000045, but it is a new cell of THIS
table, which is what p2 measures.)

## 2. Are the two runs genuinely different decompositions with disjoint prime sets?

YES, verified by code read and recomputation. Run A (data/runA_rowsweep.py) sweeps each
k x 28 board ROW-major with a 2^k-bit frontier, 27 independent width-k sweeps, reading
T(j,k) after each row. Run B (data/runB_chunked.py) sweeps the 28x28 board COLUMN-major
with a 2^28-bit frontier (in-RAM two-half sliced with explicit cross-half phase logic at
i=w-2 and i=w-1), reading T(28,j) after each column. Different frontier dimension,
different state count, different readout, different memory strategy. The two prime sets
(data/primes_A.txt, data/primes_B.txt) are disjoint (recomputed), all 26 pass my own
Miller-Rabin (bases 2..37 plus random bases), and both regenerate deterministically as
documented (first 13 primes above 2^61+10^6 and above 2^61+10^8). Both CRT moduli are
794 bits; the largest claim cell T(28,27) is 710 bits, the anchor a(28) 737 bits
(222 digits) — CRT uniqueness holds with large margin. I also reviewed run B's slicing
soundness argument (blocks never straddle halves; the i=w-2 domino add's three ordered
phases read the still-intact old low; the i=w-1 base pass's scratch ordering) and find
it correct; and I executed run B's own gate (exact n=1..12 vs A028420: PASS), gate-chunk
(the sliced production path incl. both cross-half cases: PASS) and validate (width-20
sliced sweep mod A-prime#1 == run A's stored T(20,20) residue 1885990177682531384:
MATCH). Shared lineage of the two programs (both descend from the a(28)-arc column DP,
disclosed in their docstrings) is a common-mode risk, but it is covered by point 3's
from-scratch recomputations, which agree everywhere they can be applied.

## 3. Reproduction of published terms, two-run agreement, anchor

Recomputed with my own CRT over the package's residue files (9828 run A lines complete
and duplicate-free, 364 run B lines complete; all residues in [0,p)):
- Two-run gate: CRT over the 13 A-primes of run A's j=28 lines == CRT over the 13
  B-primes of run B's j=k lines == the object, for all k=1..27 (27/27).
- Published reproduction: CRT of run A's residues reproduces all 378 published cells
  (row j, entry k, j=1..27). Additionally — my own extension — the 351 transpose cells
  (run A's T(j,k) for j<k equal the published T(k,j)) also reproduce, i.e. all 729 cells
  of the 27x27 square are consistent with the published table through run A's residues.
- Diagonal: T(n,n) via run A == b028420.txt for n=1..27.
- Anchor: CRT of run B's j=28 column == the PR #849 object a28_value.txt exactly.
- My own from-scratch DP (different formulation): reproduces all 78 published cells with
  m,n<=12; equals the object EXACTLY (big-int) for k=1..12; for k=13..16 my full 28-cell
  columns mod A-prime#1 equal run A's stored columns cell-for-cell, and my values mod a
  fresh prime equal the object mod that prime; for k=17..24 a numpy re-derivation of the
  row-sweep transfer again matches run A's stored full columns mod A-prime#1 and the
  object mod fresh primes; for k=25, 26, 27 my sweeps mod fresh primes
  (e.g. p=1907710305172284731 for k=27) equal the object cells mod p. Run B's stored
  residues equal the object mod B-prime#1 for j=1..27 and a(28) mod B-prime#1 at j=28.
  Thus every one of the 27 claimed cells has been recomputed by my own code (12 exactly,
  all 27 modularly), and both residue files are validated against data they did not
  reference. Timing plausibility: run A's 351 stamps span 2026-11-01 09:22:59Z to
  13:41:48Z (k=27 sweeps 570 s each); run B's 13 primes span 2026-11-02 13:26Z to
  16:41Z (1000-1400 s per prime) — consistent with single-core sweeps at these sizes.

## 4. Growth clause

Recomputed the preregistered two-parameter fit r(m,n) = ln W - c/(mn) on the published
rows 26-27 (53 cells, numpy lstsq): lnW = 0.6584917, c = 4.8456, W_fit = 1.9318762 —
matching the package's disclosed figure to all seven digits, 0.430% below Finch's
W = 1.9402139258 (within the 1%-below band; and the corrected constant's provenance is
right: 1.9402139258 is Finch's monomer-dimer constant, while v1's 1.33851 was indeed the
domino constant e^(G/pi) — a genuine transcription error, corrected in PREREG.v3 before
the panel sat, with no threshold loosened). Max fit residual 1.0643e-2, frozen tolerance
max(1e-5, 3x residual) = 3.1928e-2. All 27 row-28 roots T(28,k)^(1/(28k)) are strictly
below W and strictly increasing (1.5994471 at k=1 to 1.9172925 at k=27); worst deviation
from the trajectory is 1.5778e-2 in log space at k=1 (the package's "1.58e-2"; in
root space 2.5436e-2) — inside the tolerance either way. The literal parenthetical
("within 1e-3 of the entropy constant") is honestly disclosed as unattainable and I
verified that from the data: the closest any published root comes to W is 2.3341e-2
(largest published root T(27,27)^(1/729) = 1.9168732), the closest row-28 root 2.2921e-2,
and a(28)^(1/784) = 1.9177115 (2.2502e-2, matching the #849 package's own figure);
with c ~ 4.85 the 1e-3 band would need mn ~ 9400 cells (~97x97), unreachable. The
main-clause trajectory reading is therefore the only operative one and it passes.
Sensitivity note: an n>=13-only variant of the fit (not the frozen statistic) would fail
its own much tighter tolerance — the frozen all-cells rows-26-27 fit is what PREREG
specifies and its disclosed outputs reproduce digit-for-digit.

## 5. Subsumption / overlap

T(28,28) is properly excluded: the object's keys are exactly 1..27, and the #849 value
is used only as an external CRT anchor/cross-check, not as a claimed cell. The row cells
are not diagonal terms (A028420 territory), not in the live A210662 b-file, and no other
claim in the package's purview covers them. No overlap found.

## 6. Null models

Confirmed NOT APPLICABLE: this is an explicit-object claim (27 specific integers)
verified by exhaustive CRT and independent recomputation; there is no search or
statistical statistic for which a 400-control null could be run. The two-run agreement
over 26 disjoint primes (product ~2^1587 against ~710-bit values) is the analogous
random-agreement control and is overwhelming.

## Minor findings (none material)

- "61-bit primes" are actually 62-bit (2^61 + small offset); the int64 safety claim
  still holds (worst intermediate 3(p-1) ~ 6.92e18 < 2^63).
- "The same code reproducing every published term": run A — the run whose CRT directly
  yields the object — reproduces all 378; run B structurally cannot emit non-diagonal
  published terms (its width-28 column sweep produces only row-28 totals), and is
  instead validated by exact small-width gates, the width-20 validate, 27-cell agreement
  with run A, and the a(28) anchor. Judged within the rule's intent, since the criterion
  simultaneously demands a different decomposition.
- runA stamps log peak_rss_mb=0 (Windows RSS query artifact); runB_chunked.py contains
  dead code with a latent NameError (step_nomod's undefined base_only) unused by the
  production path.

confirmed_scope: The 27 integers T(28,k) for k = 1..27 of OEIS A210662 (monomer-dimer tilings of the k x 28 grid), constituting the table's next row — every cell new beyond the live 378-term triangular b-file, T(28,28) excluded as open PR #849's claim — are confirmed on the two-run basis of row-by-row width-k sweeps over 13 set-A primes and a width-28 column sweep over 13 disjoint set-B primes whose CRT reconstructions agree exactly on all 27 cells while reproducing all 378 published terms and the A028420 diagonal, and lie on the preregistered monomer-dimer growth trajectory (fitted W = 1.9318762 vs Finch's 1.9402139258, literal 1e-3 parenthetical unattainable at reachable n as disclosed).

context: subagent
pass: true
