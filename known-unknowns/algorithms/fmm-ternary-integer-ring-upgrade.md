# Fast matrix multiplication: best-known rank with ternary/integer coefficients where only rational or complex schemes are known

⚡ **Algorithms** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Several best-known FMM ranks are attained only with coefficients outside {-1,0,1} or outside Z (denominators), so they do not run over GF(2) or rings without 1/2. Confirmed live 2026-10-08 from Perminov's status table (ZT / Z / Q columns): <2,4,5>: 33 / 33 / 32 (the Lille 2x4x5 rank-32 scheme uses 1/2 throughout); <3,4,7>: 64 / 64 / 63; <4,4,4>: 49 / 49 / 48 (uses 1/2, 1/4, 1/8; this format is handled by the moonshot entry's partial win, not here). Across the 680 formats up to 16x16x16 (2026-10-20): 297 rows have ZT > Q, 16 rows have ZT > Z (integer known, ternary not), and the repo's coefficient-set status is 383 ZT / 10 Z / 287 Q schemes. The June 2026 paper (arXiv:2606.02480) closed 84 such ring gaps; MerlijnW70 ternary batches merged 29 Sep and 2 Oct 2026 and a ZT 2x9x10:140 rediscovery on 30 Sep 2026 closed more; cloudroom-math schemes (matyasstoch, 9 Oct 2026) and near-optimal ZT schemes from mizopl (19 Oct 2026) changed the table again. Finding a ternary or integer scheme at the known Q rank (or any strictly lower ZT/Z rank that does not beat the overall best rank) is a citable 'ring upgrade' and exactly what the 2026 flip-graph tooling targets.

## What counts as a win

Success means an explicit bilinear scheme for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) != (4,4,4), whose coefficients all lie in {-1,0,1} (ternary, 'ZT') or all in Z (integer), with rank r such that (1) r is STRICTLY LESS (direction: min) than the 'ZT rank' (for a ternary claim) or the 'Z rank' (for an integer claim) listed for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md re-fetched live immediately before claiming; (2) r is GREATER THAN OR EQUAL to the minimum over the live ZT/Z/Q columns for that format and to the live fmm_sota.json rank, i.e. the scheme does NOT beat the overall best rank (a scheme that does is the catalogue target fmm-catalogue-small-format-rank, never both); (3) no scheme of rank <= r in the same coefficient class already exists in the live schemes/results/ZT (or /Z) directory of that repository or in https://github.com/MerlijnW70/fmm-schemes; (4) the Brent equations are verified exactly over Z with integer arithmetic (so the scheme is valid over every ring), not merely mod 2. Equalling the format's Q rank is the natural goal but any strict ZT or Z improvement satisfying (1)-(4) counts.

## Partial wins

- **p1:** A lifting milestone: for a format where the live ZT and Z columns both exceed the live Q column, an exactly verified scheme of rank equal to that Q rank with all coefficients in Z/4Z (or Z/p^2 for an odd prime p), i.e. a modular lift one step beyond GF(p) that is not yet an integer scheme, where no integer or ternary scheme of that rank exists in the live repository.
- **p2:** A verified negative result for a specific format with max(n,m,p) <= 5 where the live ZT column exceeds the live Q column (e.g. <2,4,5>: ZT 33 vs Q 32): a SAT/ILP encoding of 'rank <= Q rank over GF(2) (or with ternary coefficients)' together with a DRAT/LRAT-checked UNSAT certificate (checked by drat-trim or cake_lpr on this Mac), with the encoding re-derived and spot-checked by the skeptic. Recorded as a result, not claimed as a record.

## How a win is checked

Load the candidate as U, V, W matrices (Perminov's JSON format, 'Scheme File Formats' in the README). Assert every coefficient is in {-1,0,1} (ternary claim) or in Z (integer claim). Verify the Brent equations exactly with integer arithmetic: for all i,j,k,l,s,t, sum_r U_r[i,j] V_r[k,l] W_r[s,t] = [j==k][i==s][l==t] (mind the file's index convention; permute axes if it stores the transposed product). Count r after removing zero terms. Re-fetch Perminov's README (all three columns) and the ZT/Z directories, fmm_sota.json, the Lille per-format page and the MerlijnW70 repo; confirm condition (2) (r does not beat the overall best rank) and condition (3) (no existing scheme of rank <= r in the same coefficient class). For p1, verify the Brent equations modulo the stated modulus. For p2, re-run the DRAT checker on the certificate. Seconds to minutes on this Mac for formats up to 16x16x16.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md>

## Sources

- <https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md>
- <https://github.com/dronperminov/FastMatrixMultiplication>
- <https://github.com/dronperminov/ternary_flip_graph>
- <https://github.com/MerlijnW70/fmm-schemes>
- <https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md>
- <https://fmm.univ-lille.fr/2x4x5.html>
- <https://fmm.univ-lille.fr/4x4x4.html>
- <https://fmm.univ-lille.fr/3x4x7.html>
- <https://arxiv.org/abs/2606.02480>
- <https://arxiv.org/abs/2603.02398>
- <https://arxiv.org/abs/2506.13242>
- <https://arxiv.org/abs/2603.18699>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Ternary flip-graph search started from the known Q scheme after clearing denominators: multiply through by 2^k, reduce mod a prime, run flips in GF(p) to find a rank-equal scheme with small coefficients, then lift to Z by Hensel lifting / rational reconstruction and verify exactly.
- Direct ternary flip graph (dronperminov/ternary_flip_graph) seeded from the nearest ZT scheme of rank r+1 for the target format, running 'reduction' moves with coefficient constraint {-1,0,1}; parallel walks on 10 cores with restarts.
- Change of basis: a Q scheme with denominators 2^k is sometimes equivalent under invertible sparse basis changes (A -> PAQ etc.) to an integer scheme; search the orbit of the 48-term 4x4x4 scheme and the 32-term 2x4x5 scheme under the isotropy group with lattice-reduction-style pruning for an integral representative.
- SAT/ILP in GF(2) for <2,4,5> rank 32 (the F2 rank is 33): if a GF(2) rank-32 scheme exists, try lifting; if a short UNSAT proof emerges, that is a separate (non-claimed here) negative result worth recording.
- Meta flip graph: search a bigger format (e.g. <2,4,10>, <4,4,8>) in ternary coefficients and peel zero slices to recover ternary schemes of the smaller target format.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Verifying only mod 2 and claiming an integer scheme: a ternary scheme must satisfy the Brent equations over Z exactly (signs matter), otherwise it is a GF(2) scheme only.
- Perminov's table columns are the best ranks found in that coefficient set; 'Q rank' already includes schemes with 1/2. A scheme with coefficients in {-2,...,2} is 'Z', not 'ZT'; label the claim precisely.
- Duplicate work: the repository adds rediscoveries weekly (ZT 2x9x10:140 on 30 Sep 2026; MerlijnW70 batches on 29 Sep and 2 Oct 2026). Re-fetch README, CHANGELOG and the ZT/Z directories at verification time; a scheme already present is not a win.
- Index-convention errors (row-major vs column-major, which factor is transposed) make a correct scheme look wrong or a wrong scheme look right under a permuted test; verify against the explicit symbolic product A*B.
- If the new ternary/integer scheme also beats the overall best rank, it is the catalogue target's win, not this one; never claim the same scheme under two targets.
- <4,4,4> is excluded here: a ternary/integer rank-48 scheme for 4x4 is partial win p1 of the moonshot entry fmm-4x4x4-rank47-3x3x3-rank22.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/algorithms/fmm-ternary-integer-ring-upgrade.md
```

Already set up? Say `run V3R1T4S on fmm-ternary-integer-ring-upgrade`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `fmm-ternary-integer-ring-upgrade`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
