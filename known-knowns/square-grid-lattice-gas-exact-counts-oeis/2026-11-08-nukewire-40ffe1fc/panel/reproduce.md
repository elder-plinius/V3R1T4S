# REPRODUCE round 3 — independent panel verdict (A210662 row 29, k=12..28)

context: subagent

Panelist wrote their own checker from the definition (no code taken from the
author's verify_claim.py; different DP formulation: per-column transfer with
protrusion bitmask and per-outgoing-mask aggregated big-int counts, vs the
author's cell-by-cell scanline). Checker: `my_reproduce_checker.py` in this
folder; raw outputs: `run_w15_a.txt` / `run_w15_b.txt` (two identical runs).
Claim folder read as data only; nothing from it was executed.

Definition used (quoted from claim/OEIS): T(n,k) = number of monomer-dimer
tilings of the k x n grid (each cell covered by a 1x1 monomer or half of a
1x2 domino, exact cover) = number of matchings of the k x n grid graph.

## Results (all from command output)

STEP 1 — own exact big-integer DP (widths 1..15; width-12 sweep builds in 1.3 s):
- Hand anchors from the definition: T(1,1)=1, T(2,2)=7, T(3,3)=131. PASS.
- Mandated: all 78 published b-file cells with n <= 12 reproduced exactly. PASS.
- Bonus: ALL 300/378 published cells with k <= 15 reproduced exactly
  (b-file parsed as i = n(n-1)/2 + k, rows n=1..27, 378 terms, contiguous).
- Mandated claimed cell: T(29,12) recomputed exactly = 17833870010668294976688555661192891203867165074825503358766291806872648413869260880082005168053765
  (98 digits) — matches row29.json. Bonus exact: T(29,13), T(29,14), T(29,15)
  (106/114/123 digits) also match row29.json. 4 claimed cells now verified by
  pure exact DP, 13 of 17 only via CRT.
- Disclosed-not-claimed cells T(29,1..11) also match my DP (context file).
- Row-28 anchors T(28,k), k <= 15 match my DP exactly.
- Bonus: every residue of BOTH sets for k <= 15, j = 1..29 equals my exact
  value mod p — 19,140 direct (p,k,j) checks. PASS.

STEP 3 — primes / disjointness / bounds:
- Residue files parse to complete 22 x 28 x 29 grids (22 primes, k=1..28,
  j=1..29, unique (p,k,j), all r in [0,p)); the files' "# k=28 skipped"
  stamps are stale — the k=28 blocks are present for all 22 primes.
- All 44 moduli pass my deterministic Miller-Rabin, bases 2,3,5,7,11,13,17,
  19,23,29,31,37 (deterministic < 3.3e24 > 2.31e18 here). PASS.
  A: 22 primes in [2305843009216693979, 2305843009216695229];
  B: 22 primes in [2305843009316693969, 2305843009316694877].
- Sets disjoint. PASS.
- Per-set modulus 1343 bits (~10^404) each; 3^(29*28) = 1287 bits, so the
  bound holds for every claimed k=12..28 (margin 56 bits at the worst k=28);
  each claimed value also checked < 3^(29k). PASS.

STEP 2 — CRT (my own implementation), each set separately:
- runA: all 17 claimed T(29,k), k=12..28 reconstructed exactly (22 residues
  each, full-product modulus). PASS.
- runB: same, all 17 exact. PASS.
- j=28 column equals the row-28 object (PR #960) for all 27 covered k, from
  each set separately. PASS.
- ALL 378 published b-file cells — including the wide ones T(27,27) (207
  digits), T(27,26), T(26,26) — reconstructed exactly by CRT from EACH set
  (per-cell modulus > 3^(nk) verified). PASS.

STEP 4 — informational (not a gate): per-site growth T(29,k)^(1/(29k))
rises monotonically 1.903082 (k=12) -> 1.913584 (k=20) -> 1.918102 (k=28),
bracketing the published T(27,27)^(1/729) = 1.916873; consistent with the
known ~1.94 square-lattice monomer-dimer trend, no anomaly.

Determinism: full checker run twice (run_w15_a.txt vs run_w15_b.txt); all
computed lines byte-identical (only wall-clock timings differ); both runs end
RESULT: PASS, exit code 0.

Total: 18/18 check groups passed; ~19,600 individual verifications.

## Caveats honestly stated
- 13 of the 17 claimed cells (k=16..28) are beyond my exact big-int reach;
  for those the evidence is: both residue sets independently CRT to the
  claimed values under moduli exceeding the rigorous 3^(29k) bound, and the
  same residue tables reproduce all 378 published OEIS cells and the whole
  j=28 column exactly, and match my exact DP mod p for every cell with
  k <= 15 (which includes j=29, i.e. the claimed-regime pipeline itself).
- Novelty/absence from published sources was NOT re-checked by me (out of
  scope for this reproduction panel); I verified the mathematics only.

pass: true
