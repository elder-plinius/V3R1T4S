# NOTES zeng-replay (started 2026-10-31 ~17:35)

Paper facts (arXiv:2609.01284, read in full S7-S14): bodies D (r=1/2), regular Reuleaux triangle R3, regular Reuleaux pentagon R5 (width 1);
z=(x3,y3,psi5,x5,y5); core box [-0.08,0.08]^2 x [0,pi/5] x [-0.08,0.08]^2; far-field b3=0.190700, b5=0.194601; collar a0=0.08;
R3 collar [0.08,0.1907]x[0,pi/3], R5 collar [0.08,0.194601]x[0,pi/5]; tau=0.834; 6,747,165 records (2374 + 1029 + 6,742,989 core + metadata);
shards 773 files, 787,849,048 bytes, sha256 c5fdc18d...; author verifier = python-flint, "hours to tens of hours".
Paper methods per core leaf: INNER_POLYGON (interval shoelace), TEMPLATE_CONVEX_BOUND (turn margins + perturbation), TEMPLATE_MEAN_VALUE_SIMPLE_BOUND.

## Hypotheses (chance of "replay passes" / cost)
1. Certificate replays clean under literal outward-rounded interval arithmetic (p=0.75, cost: decoder+checker, hours).
2. Some leaves rely on author's perturbation bridge (decimal constants vs ideal pi/5, vertex radii) that a literal checker must reproduce by enclosing pi with an interval (p=0.5 matters; cheap).
3. Text/code mismatch (e.g. record count 6,747,165 vs sum of parts 6,746,... , leaf counts, method names) (p=0.5, cheap).
4. Template-convex rotation-index argument is weaker in code than in text (only turn-sign check, no index check) (p=0.3, medium).
5. Simple-template mean-value: derivative bound G_k only valid with sup |dS/dz_k|, code may use signed bound (p=0.15).
6. Coverage check in author's verifier compares floats/decimals not exact rationals (p=0.25, cheap to test by exact Fractions).
7. (outside field: database/log-structured storage) treat shards as an append-only log with a Merkle-like hash; verify shard hash and per-shard counts first; mismatch -> defect (p=0.2).
8. (outside field: compiler/SMT) replace trust by a proof-producing small kernel: one tiny interval kernel (Iv type with ulp widening) running over all leaves, controls via mutation testing (p=0.9, this is the plan).
9. (strange) Check whether the certificate leaves use mirror-symmetry-violating data (psi in [0,pi/5] but template built for reflected pentagon) by running the checker on psi mirrored boxes; if hull minimum is symmetric the leaf bound should still hold (p=0.1).
10. Speed: python-flint author verifier hours; C# double-based Iv ~ minutes (p=0.8 for >20x speed-up).

## Progress log (outcomes of the hypotheses; times)
- 17:33 download complete, md5 matches Zenodo (73b400c8...). Paper S7-S14 read fully; author's verifier read for FORMAT only (no code imported into my checker; python-flint used only for the optional author cross-check in a lens venv).
- H1/H8 (plan): own C# checker `code/ZengCheck` (Iv = binary64 interval, every + - * / sqrt widened 1 ulp; sin/cos by Taylor+remainder; sample-point tables from mpmath.iv outward-rounded, C# re-verifies membership).
- H3 (text/code mismatch): FOUND several (see report D1-D8). H6 (coverage in floats): author's coverage is exact Decimal (not floats) -> refuted, but boxes for geometry are re-read as floats (harmless since repr round-trips).
- H2 (bridge): author's verifier has NO perturbation-bridge code for pi/5, pi/3 (grep found none) although S14.3 claims one; my checker implements it (top-end boxes extended to the outward pi/n).
- H4 (rotation index): author checks turn margins only; I added an explicit rotation-index-1 certificate to the convex route.
- First full run (binary bin_final, 28 min, 2 threads): 2,354 of 6,742,989 core leaves failed to certify (11 shards), all "no certified template" with bound > 0.834: cause = my sample set contains one near-vertex point per Reuleaux set that the author's replay drops (python-flint `arb**2` of a ball containing 0 -> NaN -> point silently excluded) so polygons differ; polygons are knife-edge sensitive. Fix: second sample-set variant without those points (completeness heuristic only; every polygon is re-certified from scratch). With it the 11 shards pass with 0 failures.
- Final run: bin_final2 (sha in out/final2_binary_sha.txt) -> out/final2.jsonl.

## Final outcome of hypotheses (20:00)
1 (clean replay under literal interval arithmetic): CONFIRMED - ACCEPT, 6,746,392 leaves, 0 failing, 27 min 31 s on 2 threads.
2 (bridge for decimal vs ideal constants): CONFIRMED as a gap: shipped verifier has no bridge code (D2); closed in my checker.
3 (text/code mismatch): CONFIRMED, D1-D8 in report.md (none invalidating).
4 (rotation-index): author code relies on hull ordering (D6); mine certifies explicitly.
5 (mean-value sign/abs): refuted - author's derivative bound uses |.| (abs upper); mine too; 40 leaves cross-checked in mpmath.
6 (float coverage): refuted - author's coverage is exact Decimal; mine exact Int128/BigInteger.
7 (log/hash structure): shard-set hash only matches with 'shards/' prefix (D1); per-record hashes all good.
8 (small proof-kernel + mutation tests): done (Iv selftest 200k ops, 16 tamper controls, leaf cross-check in mpmath, Monte Carlo).
9 (mirror psi test): not run (no evidence needed; normalisation argued on paper L3).
10 (speed): CONFIRMED ~71x wall, ~250x CPU vs author's 117,852 s on 7 workers.
Resource log: <=2 busy threads at all times (the Python integrity job ran 1 thread concurrently with 1 checker thread; later 2 checker threads); RAM peak ~1.2 GB. No PIDs left running.
