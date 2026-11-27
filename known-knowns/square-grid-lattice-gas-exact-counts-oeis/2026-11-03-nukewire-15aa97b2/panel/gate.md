status: CONFIRMED_PARTIAL
confirmed_scope: The 27 integers T(28,k) for k = 1..27 of OEIS A210662 (monomer-dimer tilings of the k x 28 grid), constituting the table's next row — every cell new beyond the live 378-term triangular b-file, T(28,28) excluded as open PR #849's claim — are confirmed on the two-run basis of row-by-row width-k sweeps over 13 set-A primes and a width-28 column sweep over 13 disjoint set-B primes whose CRT reconstructions agree exactly on all 27 cells while reproducing all 378 published terms and the A028420 diagonal, and lie on the preregistered monomer-dimer growth trajectory (fitted W = 1.9318762 vs Finch's 1.9402139258, literal 1e-3 parenthetical unattainable at reachable n as disclosed).

Gate notes (main session, after reading all three verdicts in full):
- Three fresh subagent contexts, each seeing only claim/; all three end
  `pass: true` with `context: subagent`; each did its own computation (own
  checker + two fresh primes; own live fetch + repo/web sweep incl. the OEIS
  column-sequences; own CRT + own DP + growth recompute).
- No downgrade triggers found: no hedging, no mismatch, scope no wider than
  evidence, exhaustive-modular basis stated, no bundled claims (k=28 excluded).
- Disclosed immaterialia carried into the package: "61-bit" primes are 62-bit
  (2^61 + offset; discipline 3(p-1) < 2^63 still holds); run B structurally
  emits only row-28 totals (validated instead by its gates, the width-20
  validate, 27/27 agreement, and the a(28) anchor — the criterion
  simultaneously demands a different decomposition); dead code in runB's
  unused memmap path; zeroed RSS log field; T(28,1)=F(29) trivially derivable
  from the OEIS entry's documented Fibonacci diagonal (1 cell of 27 that gains
  nothing; the row object is not reducible to trivial edits of published
  objects — NOVELTY's judgment, concurred).
- PREREG chain: v1 (11-01) + v2 (memory note) + v3 (constant-provenance
  correction, issued before the panel sat, no threshold touched; the
  criterion panelist independently verified the correction was genuine and
  material-free).
- Panel fetches are < 6 h old (08:38Z vs gate 10:4xZ); the b-file is
  byte-identical across the 11-01/11-02/11-03 fetches (sha256 05d85498…).
