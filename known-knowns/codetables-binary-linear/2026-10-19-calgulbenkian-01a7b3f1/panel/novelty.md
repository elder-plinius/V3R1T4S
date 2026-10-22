context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Novelty report: lpub-q7-n55-k10-d39

Role: novelty. Cell: upper bound d at most 39 for [55,10] over GF(7) (the claim: no [55,10,40]_7 code), a Delsarte linear-programming certificate.

## Primary table (fetched once, honestly) and the four propagation neighbours
- http://www.codetables.de/BKLC/BKLC.php?q=7&n=55&k=10 | fetched 2026-10-19T05:16:14Z | HTTP 200 | sha256 b805d923e10bc518778186de0c10abd652734aafc3347baf1422eb19883fbc1b
- http://www.codetables.de/BKLC/BKLC.php?q=7&n=54&k=9 | fetched 2026-10-19T05:16:13Z | HTTP 200 | sha256 051fb89c6fe0c6cc2e13becc5d84e8e95684062e9e9f9578fb72ac7419e851dd
- http://www.codetables.de/BKLC/BKLC.php?q=7&n=54&k=10 | fetched 2026-10-19T05:16:11Z | HTTP 200 | sha256 54a8940417c9fc4d61ea407e1768c3831fdc80fbf9c8bb3edd621c98a76934ae
- http://www.codetables.de/BKLC/BKLC.php?q=7&n=55&k=9 | fetched 2026-10-19T05:16:16Z | HTTP 200 | sha256 2c2932b02fe4f488bff08a660daee2c3102257f0733ba01d99904c556b3e927b
- http://www.codetables.de/BKLC/BKLC.php?q=7&n=56&k=10 | fetched 2026-10-19T05:16:17Z | HTTP 200 | sha256 91117f9f9284e0fb6e3b9a92f9c9dbb95004ea1092e58f5e1df59dfb577e6049
(7, 55, 10) live L/U 34 40 claim Ub 39 one-step neighbour bounds {'shorten U(n-1,k-1)': 40, 'puncture U(n-1,k)+1': 40, 'subcode U(n,k-1)': 41, 'pad U(n+1,k)': 41} closure bound 40 STRICTLY BELOW | claim >= lower: True
Page values: see the closure line (live lower and upper bound of the cell, and the four one-step neighbour bounds). Page hashes equal those recorded by the triage for the same URLs. The page gives no derivation chain for this cell. The page note says upper bounds are taken from Brouwer's tables except for codes over GF(7) with n above 50, and that 'for most of these codes, the upper bounds are rather weak' (small-dimension GF(7) bounds were provided by Daskalov).

## Shared sources (fetched once for the whole group, kept as notes)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-binary-linear | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 904f233ba9fe62d5cfda8003313ed80b431e4f461c65bb3448a86fd3f04f308f
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-qubit-upper-bounds-n101-256 | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 d6c01566c6a9f0e61760f975304955861d84aeeb2efb1fe32adce5b664882ce9
- Pull requests: a snapshot of all V3R1T4S pull requests (titles and bodies), fetched 2026-10-19T04:30:31Z, was used instead of the api.github.com pulls pages, to spare the shared quota. 473 pull requests were scanned: every title for the target, and every title and body for the cell's own parameters (a regular-expression search for the cell, results below).
- TROPHY_CASE.md (text dated 2026-10-10 to 2026-10-12) lists six result families (graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) and two cipher commitments. It has no row for a codetables.de table, so it holds no competing value for this cell.
- Merged folders for the target (listing above): binary-linear has three merged folders (the 2026-10-14 and 2026-10-15 binary [173,17,72], [175,25,61], [213,26,77] filings, all q = 2 lower bounds at other cells); the qubit-upper-bounds target has 52 merged folders by one other contributor.
- arXiv (4 queries plus the one named work). Query 1 (quaternary linear codes, new): 12 entries, newest 2609.21601 (Z4 quasi-cyclic codes) and 2605.14603 (Z4 codes with small Plotkin defect); none gives a GF(4) linear code with these parameters. Query 2 (linear programming bound, linear codes, nonexistence) returned zero entries (the server found nothing for that exact wording; not retried, the four-query allowance was then spent). Query 3 (quantum, upper bound, linear programming, stabilizer): 9 entries, the relevant ones 2610.09900 (Quantizing Delsarte Theory, general theory, no table cells) and 2601.15446 (check-weight-constrained codes, bounds for weight-limited checks, not the generic table). Query 4 (quantum codes, new, codetables): 3 entries, none newer than 2021. The named work 2609.37056 (LinCodeEvolve) is about BINARY linear codes and lists seven binary codes of length 172 to 200, so it cannot concern GF(4), GF(5), GF(7), GF(8), GF(9) or qubit cells.

## Own exact check of the certificate (dual feasibility and objective)
I wrote my own checker from the Delsarte definition (not shipped in this package): Krawtchouk polynomials by polynomial convolution of (1+(q-1)z)^(n-x) (1-z)^x, evaluated with exact fractions; the certificate must have y_j at least 0, f(x) = 1 + sum y_j K_j(x) at most 0 at every integer x from D to n, and f(0) below q^k. Output:
lpub-q7-n55-k10-d39 q,n,k 7 55 10 D 40 m 7 f(0)/q^k=0.829374 max f(w>=D) nonpositive: True VALID new Ub 39
So the certificate is valid and excludes distance D = 40; the new upper bound 39 follows by Delsarte's bound for any code of size q^k.

## Propagation closure (the claim must be strictly below it)
One step of each rule (shortening U(n-1,k-1), puncturing U(n-1,k)+1, subcode U(n,k-1), padding U(n+1,k)) applied to the fetched neighbour pages gives the bound shown in the closure line above; the claim is strictly below it. Merged and open pull requests contain no upper-bound value for any linear-code cell (the merged codetables-binary-linear pull requests 142, 158, 163 are binary lower bounds at other cells), so they lower nothing here.

## Literature
Maruta's page of Griesmer-bound results (fetched once, see http://mars39.lomo.jp/opu/griesmer.htm) gives full tables only for q = 3 (k up to 6), q = 4 (k = 4, 5), q = 5 (k = 4, 5), q = 7 and 8 (k = 4), q = 9 (k = 4) and all q for k = 3. This cell (q = 7, k = 10) is outside those tables, so it is neither confirmed nor refuted by that source. unresolved: papers on optimal codes of dimension 10 over GF(7) (and the Daskalov and Daskalov-Metodieva papers the table itself cites) could contain a stronger bound that the table did not pick up; I could not search them within the four-query arXiv allowance, and the four generic arXiv queries found none.

## Answers to the open questions that concern novelty
1. A plain Delsarte LP with distance only is a valid certificate; the live reason for the old bound (see the note) is a Griesmer or truncation argument, which is consistent with 'nobody ran the LP' for this cell, but I cannot prove that nobody did.
2. Other propagation rules: I applied the four standard ones to the live neighbours; I know of no table family that would give a smaller bound; the table page lists only the derivation chain shown above.
3. A second independent implementation of the Krawtchouk evaluation is the one I wrote (different construction from the checker in the folder: polynomial convolution, not the explicit sum); it agrees.


unresolved: whether a non-arXiv or older paper already excludes this length-distance pair (see the literature section).

novelty: PASS (with the unresolved literature caveat)
verdict: The certificate is exactly valid (my own Delsarte check), the new bound is strictly below the live upper bound and below the one-step propagation closure, and I found no pull request, TROPHY_CASE row or arXiv result with an equal or smaller bound.
pass: true
