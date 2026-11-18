# PREREG: hypercube-q8-perfect-matchings (p2/p1) & hypercubic-percolation-1-over-d-series-next-term (p2)

- **Frozen at (UTC):** `2026-11-18T05:59:03Z`
- **Primary Target ID:** `hypercube-q8-perfect-matchings` (`p2`: exact residue `A005271(8) mod p` for prime `p >= 3` via Sylow `p`-subgroup fixed points, plus `p1` folded 8-cube tractability probe)
- **Secondary Target ID:** `hypercubic-percolation-1-over-d-series-next-term` (`p2`: proven closed formula for the `binom(d, e-3)` coefficient of the bond perimeter polynomial `D_e(q)`, removing tasks `(9, 12)` and `(11, 14)` from Mertens-Moore Table 9)
- null_test: not needed because (all claims are deterministic exact combinatorial/algebraic counts and closed-form theorems certified by two independent zero-shared-code implementations with deterministic PASS/FAIL checkers; neither statistical estimation nor heuristic scoring is claimed).

## 1. Live Prior-Art & Status Baseline (Fetched `2026-11-18T05:59:03Z` window)

All fetches used a single polite HTTP GET with `User-Agent: V3R1T4S-Research-Scout/1.0`. Exact manifest (`data/fetch_manifest.txt`):

```text
2026-11-18T05:50:21Z | HTTP 200 | 57485a625af607e78a38e8e107b4f9c70da8d17f47932f18706277987b38d821 | 20862 bytes | A005271.html | https://oeis.org/A005271 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Sat, 30 May 2026 20:39:47 GMT', 'Date': 'Wed, 18 Nov 2026 05:50:22 GMT'}
2026-11-18T05:50:22Z | HTTP 200 | f709375e16328959c0a589dd0abd90daeff8e248a086725c0cbdaea34efd640c | 4641 bytes | A005271_json.json | https://oeis.org/search?q=id:A005271&fmt=json | headers={'Content-Type': 'application/json', 'Date': 'Wed, 18 Nov 2026 05:50:22 GMT'}
2026-11-18T05:50:22Z | HTTP 200 | c8da5b8d8f3bc4cb02ecf4eb925199c32b1e1e8404b4a8eb9c889fd640fab23d | 128 bytes | b005271.txt | https://oeis.org/A005271/b005271.txt | headers={'Content-Type': 'text/plain', 'Date': 'Wed, 18 Nov 2026 05:50:22 GMT'}
2026-11-18T05:50:22Z | HTTP 200 | bc91cc026b365f35199b3138ff06b91f489c85d493d2a5edefc81f91fef31df7 | 37500 bytes | arxiv_9801061.html | https://arxiv.org/abs/math/9801061 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Mon, 24 Aug 2026 21:05:54 GMT', 'Date': 'Wed, 18 Nov 2026 05:50:22 GMT'}
2026-11-18T05:50:22Z | HTTP 200 | 90f03436a0fffd90851c8fbe9f4b4ee045c396950f20c23c696defa532119d16 | 41441 bytes | arxiv_1805_02701.html | https://arxiv.org/abs/1805.02701 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Wed, 14 Nov 2018 14:49:22 GMT', 'Date': 'Wed, 18 Nov 2026 05:50:23 GMT'}
2026-11-18T05:50:22Z | HTTP 200 | c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf | 1024677 bytes | arxiv_1805_02701_src.tar.gz | https://arxiv.org/e-print/1805.02701 | headers={'Content-Type': 'application/gzip', 'Last-Modified': 'Wed, 11 Aug 2021 02:40:49 GMT', 'ETag': 'CNvC0974p/ICEAE=', 'Date': 'Wed, 18 Nov 2026 05:50:23 GMT'}
2026-11-18T05:50:23Z | HTTP 200 | 809405d5d4879a9ce4c4754fdadf47ecbef6f085bb8f6661aea7fed1866ccfd5 | 2343343 bytes | wikipedia_percolation_threshold.html | https://en.wikipedia.org/wiki/Percolation_threshold | headers={'Content-Type': 'text/html; charset=UTF-8', 'Last-Modified': 'Tue, 17 Nov 2026 19:35:31 GMT', 'Date': 'Wed, 18 Nov 2026 05:50:24 GMT'}
2026-11-18T05:50:25Z | ERROR The read operation timed out | - | 0 bytes | arxiv_search_q8_matchings.xml | https://export.arxiv.org/api/query?search_query=all:%22A005271%22+OR+(all:%22perfect+matchings%22+AND+all:%22n-cubes%22)&max_results=30
2026-11-18T05:50:45Z | ERROR The read operation timed out | - | 0 bytes | arxiv_search_perimeter_poly.xml | https://export.arxiv.org/api/query?search_query=all:%22perimeter+polynomial%22+AND+all:%22percolation%22&max_results=30
2026-11-18T05:52:04Z | HTTP 200 | fc9fdb22603e1a5e39806553d5121a85ff84716b7d9521f65ef474dea0727695 | 1103 bytes | A220904_json.json | https://oeis.org/search?q=id:A220904&fmt=json
2026-11-18T05:52:04Z | HTTP 200 | 4c0a09817df5d01b0553c8e04010c2cc110578eaded0c3bacd5cc004335bbeef | 765 bytes | A112311_json.json | https://oeis.org/search?q=id:A112311&fmt=json
2026-11-18T05:52:04Z | HTTP 200 | 6c55f75f3a7384892f3ef56137ebe35de3eceefd398f734a5aef04c65a71dc99 | 2745 bytes | A045310_json.json | https://oeis.org/search?q=id:A045310&fmt=json
2026-11-18T05:52:05Z | HTTP 200 | febdbe70f494683b919967df1a71aa616b83dbb8bccf2ef4e80458939cfb6d2a | 3060 bytes | propp_9801061_src.tar.gz | https://arxiv.org/e-print/math/9801061
2026-11-18T05:52:54Z | ERROR HTTP Error 403: Forbidden | - | 0 bytes | pettersson_2015_thesis.pdf | https://aaltodoc.aalto.fi/bitstream/handle/123456789/17688/isbn9789526063652.pdf?sequence=1
2026-11-18T05:52:55Z | HTTP 200 | 3301370a76b1270cb83aaa2ad4c311a834291147ca39484504e91873d878b4ed | 19212 bytes | arxiv_1705_03688_src.tar.gz | https://arxiv.org/e-print/1705.03688
2026-11-18T05:52:55Z | HTTP 200 | fc92325ab88a7926dbec579119a31f761a23ea3193c3fe3c0237b2405d80da76 | 40570 bytes | arxiv_1806_08067.html | https://arxiv.org/abs/1806.08067
```

### Literature Scout Findings (Frozen Before Compute)
1. **OEIS `A005271`** (`https://oeis.org/A005271`, HTTP 200, SHA-256 `57485a625af607e78a38e8e107b4f9c70da8d17f47932f18706277987b38d821`, last modified `2026-05-30`):
   - Lists `a(1)..a(7)` = `1, 2, 9, 272, 589185, 16332454526976, 391689748492473664721077609089`, keyword `nonn,hard,more,nice`.
   - `a(8)` is unknown, and **no odd-prime modular congruences (`mod 3`, `mod 5`, `mod 7`) for `a(8)` appear anywhere** in OEIS `A005271`, `A220904`, `A045310`, Propp (`arXiv:math/9801061`, which gives only Lovasz's parity `a(n) == n mod 2` via coordinate reflections), Ostergard & Pettersson (*Order* 30, 2013), or subsequent citing literature (2013-2026), nor in `TROPHY_CASE.md` of `V3R1T4S`.
2. **Mertens & Moore (2018)** (`https://arxiv.org/abs/1805.02701`, TeX source SHA-256 `c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf`) & **Wikipedia Percolation Threshold** (`https://en.wikipedia.org/wiki/Percolation_threshold`, HTTP 200, SHA-256 `809405d5d4879a9ce4c4754fdadf47ecbef6f085bb8f6661aea7fed1866ccfd5`):
   - Both high-dimension series still end at `119077/96 sigma^-6` (site) and `4855/12 sigma^-6` (bond).
   - Closed-form perimeter-polynomial coefficient families in `D_e(q)` are published only through `binom(d, e)`, `binom(d, e-1)`, and `binom(d, e-2)` (Mertens & Moore 2018, Theorems 4-6; site polycubes through `binom(d, n-1)` and `binom(d, n-2)` in Luther & Mertens 2017, `arXiv:1705.03688`). No closed formula for `[binom(d, e-3)] D_e(q)` has been published (2018-2026).

## 2. Verbatim Bank Success Criteria

### Target A: `hypercube-q8-perfect-matchings`
- **Full win:** `Success means the exact integer A005271(8), the number of perfect matchings of Q8, computed by two independent methods (different algorithm or decomposition, and different moduli or exact arithmetic) that agree exactly. The code must reproduce A005271(1..7), including Ostergard-Pettersson's n = 7 value. The live OEIS entry must still lack it.`
- **Partial win `p1`:** `The exact number of perfect matchings of the folded 8-cube (Q7 plus its antipodal matching; 128 vertices, 8-regular, bipartite). This equals the number of perfect matchings of Q8 invariant under the antipodal map. It must come from two independent methods that agree. The code must also reproduce the analogous counts for folded 4-, 5- and 6-cubes computed by brute force, plus A005271(1..7) in plain-cube mode. Literature check: the value must not already be published.`
- **Partial win `p2`:** `A005271(8) modulo a prime p >= 3 obtained by any method other than computing the full count (for example by counting matchings fixed by a Sylow p-subgroup of Aut(Q8), for p in {3, 5, 7}). A second independent implementation must agree, and the method must reproduce A005271(7) mod p.`

### Target B: `hypercubic-percolation-1-over-d-series-next-term`
- **Partial win `p2`:** `A proven closed formula for the next coefficient family of the bond perimeter polynomial D_e (the binom(d, e-3) coefficient, extending Mertens-Moore's Theorems 4-6 for binom(d, e), binom(d, e-1), binom(d, e-2)), or the analogous site formula with perimeter. It must remove one of the enumeration tasks in their Table 9 and be checked by computer against brute-force counts for small e and d.`

## 3. Pre-Registered Attack & Verification Rules

### Track A (`hypercube-q8-perfect-matchings` `p2`)
1. **Single-cell selection rule (frozen prior to compute, obeying Rule 4 "One object or table cell per claim"):**
   - Primary packaged cell for `attacks/discovery-q8-matchings-percolation/claim/`: **`A005271(8) mod 5`** via the cyclic Sylow `5`-subgroup `P_5 = <(0 1 2 3 4)> <= S_8 <= Aut(Q_8)` of prime order `5`, reporting BOTH the exact fixed-point integer `|Fix_{M(Q_8)}(P_5)|` and the residue `A005271(8) mod 5`.
   - Rationale frozen a priori: `5^1 || |Aut(Q_8)| = 2^15 * 3^2 * 5 * 7`, so `P_5` is a cyclic Sylow `5`-subgroup of prime order `5` (direct Cauchy/Burnside congruence `A005271(n) == |Fix(P_5)| (mod 5)` with zero subgroup-lattice inclusion-exclusion), and unlike `P_7` (which has `|Fix_{M(Q_7)}(P_7)| = 0`), `P_5` produces strictly positive non-trivial fixed-point counts on `Q_6`, `Q_7` (`A005271(7) mod 5 = 4`), and `Q_8`.
   - Across our three attempts in `work/attempts/`, we will ALSO compute exact fixed-point counts for `p = 7` (`P_7 = <(0 1 2 3 4 5 6)>`) and `p = 3` (`P_3 = <(0 1 2), (3 4 5)> ~ C_3 x C_3` and `H_1 = <(0 1 2)>`), verifying internal consistency (`|Fix(H_1)| == |Fix(P_3)| mod 3` on `Q_6, Q_7, Q_8`).
2. **Dual Zero-Shared-Code Engines & Calibration Gates:**
   - **Engine A1 (C99 / Python Orbit-Quotient Weighted Bipartite Permanent + Full-Cube Gray-Code Glynn Permanent):**
     - Must reproduce `A005271(1..6)` = `1, 2, 9, 272, 589185, 16332454526976` in full-cube permanent mode.
     - Must compute exact integer `|Fix_{M(Q_n)}(P)|` via stabilizer-stratified orbit-quotient weighted bipartite permanents and reproduce `A005271(6) mod p` and `A005271(7) mod p` for `p in {3, 5, 7}`.
   - **Engine A2 (Zero-Shared-Code Direct `2^n`-Vertex Hypercube Bitmask DP in Pure Python Stdlib):**
     - Operates directly on the `2^n`-vertex graph `Q_n` (`256`-bit integer vertex masks for `Q_8`) WITHOUT using quotient matrices or permanents: steps through uncovered vertices `u` of `Q_n`, branches over uncovered hypercube neighbors `v` of `u`, applies the group action `g in P` directly to edge `{u, v}` on `Q_n`, checks zero vertex collisions in `Q_n`, and counts valid `P`-invariant `2^{n-1}`-edge perfect matchings of `Q_n` via exact memoized bitmask DP.
     - **PASS gate:** Engine A1 and Engine A2 must output the **exact same integer** `|Fix_{M(Q_n)}(P_5)|` for every `n = 5, 6, 7, 8`, and `|Fix_{M(Q_n)}(P_5)| mod 5` must match `A005271(n) mod 5` (`0, 1, 4` for `n = 5, 6, 7`).

### Track B (`hypercubic-percolation-1-over-d-series-next-term` `p2`)
1. **Constructive Proof + Zero-Fitting Derivation:**
   - Prove that every bond animal of size `e` proper in `e - 3` dimensions has `v in {e, e+1}` and derive `[binom(d, e-3)] D_e(q)` from first principles via exhaustive enumeration of minimal excess-axis core configurations and Mertens-Moore Lemma 1 (`k n^{n-k-1}`), first validating the theorem-prover by re-deriving Theorems 4, 5, and 6 (`k = 0, 1, 2`) from scratch with zero free parameters.
2. **Independent Brute-Force & Published-Data Gate:**
   - Must match 100% of brute-force bond-animal counts `G_{e,t,v}^{(k)}` on `Z^d` for small `(d, e)` from an independent zero-shared-code lattice-animal enumerator AND match 100% of `[binom(d, e-3)] D_e(q)` in Mertens & Moore Appendix A for ALL `e = 4, 5, 6, 7, 8, 9, 10, 11` (`8` independent degrees of check beyond the core size!), then evaluate `[binom(d, 9)] D_{12}(q)` and `[binom(d, 11)] D_{14}(q)` removing Table 9 tasks `(9, 12)` (`4.5` years) and `(11, 14)` (`133,800` years).
