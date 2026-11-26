# PREREG: cube-domino-tilings-a028446-8x8x8 (p1) & kerdock-set-ternary-m6 (p1)

- **Frozen at (UTC):** `2026-11-18T07:11:51Z`
- **Primary Target ID:** `cube-domino-tilings-a028446-8x8x8` (`p1`: exact integer `A049507(7)`, the number of perfect matchings / domino tilings of `P_6 x P_6 x P_7`)
- **Secondary Target ID:** `kerdock-set-ternary-m6` (`p1`: exhaustive computer proof removing one order `r in {2, 3, 4, 5, 6, 8}` from the Kiermaier-Schmidt-Wassermann automorphism list for `1-(6,6,1)` spreads of `Omega^+(12,3)`, held as fallback if Track A fails or is pre-empted)
- null_test: not needed because exact deterministic combinatorial counts and finite-geometry nonexistence proofs are verified by two independent deterministic algorithms, multi-prime CRT + GF(2) determinant checks, and standalone checkers.

## 1. Live Prior-Art & Status Baseline (Fetched `2026-11-18T07:09:01Z` – `2026-11-18T07:10:19Z`)

All fetches used a single polite HTTP GET (`User-Agent: V3R1T4S-scout/1.0`, zero retries). Exact manifest (`data/fetch_manifest.txt`):

```text
2026-11-18T07:09:01Z | HTTP 200 | 75647a02e01f30a25c5fbacd0814bf9e7665ab997d3e80fdb3a05b41554f0a0f | 14331 bytes | A049507.html | https://oeis.org/A049507 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Sun, 23 Nov 2025 18:35:23 GMT', 'Date': 'Wed, 18 Nov 2026 07:09:01 GMT'}
2026-11-18T07:09:01Z | HTTP 200 | 3133d67655ba11512c967f929719ddefe0b056dc109fcfd5f577b35029e091eb | 882 bytes | A049507_json.json | https://oeis.org/search?q=id:A049507&fmt=json | headers={'Content-Type': 'application/json', 'Date': 'Wed, 18 Nov 2026 07:09:01 GMT'}
2026-11-18T07:09:01Z | HTTP 200 | cf7515c675e7213b0d24916fad475b28737cc4766b9e12cc4f0f4d91d9f0eefe | 15341 bytes | A028446.html | https://oeis.org/A028446 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Mon, 30 Mar 2026 04:02:19 GMT', 'Date': 'Wed, 18 Nov 2026 07:09:01 GMT'}
2026-11-18T07:09:01Z | HTTP 200 | ea5a3dbdd27f223bd52fd29e54744d535e2fed33cd0948436896ab8410f38801 | 12150 bytes | a028446.md.txt | https://oeis.org/A028446/a028446.md.txt | headers={'Content-Type': 'text/plain; charset=utf-8', 'Last-Modified': 'Mon, 30 Mar 2026 00:02:57 GMT', 'Date': 'Wed, 18 Nov 2026 07:09:01 GMT'}
2026-11-18T07:09:01Z | HTTP 200 | ab02b7aec3fec52fa3f0110bb5f24c9e7ccdc2c45d5e5e2804503510cc517a5c | 14328 bytes | A028454.html | https://oeis.org/A028454 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Sun, 23 Nov 2025 18:35:23 GMT', 'Date': 'Wed, 18 Nov 2026 07:09:02 GMT'}
2026-11-18T07:09:02Z | HTTP 200 | 230f3863c385f534703bb049a9cd4531b5076b000747d1d95af6f25f08f5ccef | 1162 bytes | A028454_json.json | https://oeis.org/search?q=id:A028454&fmt=json | headers={'Content-Type': 'application/json', 'Date': 'Wed, 18 Nov 2026 07:09:02 GMT'}
2026-11-18T07:09:02Z | HTTP 200 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 | 79 bytes | gh_issues_domino.json | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+cube-domino+OR+A049507+OR+A028446 | headers={'Content-Type': 'application/json; charset=utf-8', 'Date': 'Wed, 18 Nov 2026 07:09:02 GMT'}
2026-11-18T07:09:02Z | HTTP 200 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 | 79 bytes | gh_issues_kerdock.json | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+kerdock | headers={'Content-Type': 'application/json; charset=utf-8', 'Date': 'Wed, 18 Nov 2026 07:09:03 GMT'}
2026-11-18T07:09:03Z | HTTP 200 | 6bdf40e58a446854255fd1987e3984df6e96af4f3b0af388e3a0b5e3b1744e5d | 1988672 bytes | gh_pulls_all.json | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | headers={'Content-Type': 'application/json; charset=utf-8', 'ETag': '"2ef275b26535f6144a655efc3c7293db3662b310a0f9dde5bba24f02b572880d"', 'Date': 'Wed, 18 Nov 2026 07:09:04 GMT'}
2026-11-18T07:09:04Z | HTTP 200 | b54a2f4cdb2bf94340a65ae21570103810d15152ae5f8ad43a1874f54525a742 | 43216 bytes | arxiv_2403_11188.html | https://arxiv.org/abs/2403.11188 | headers={'Content-Type': 'text/html; charset=utf-8', 'Last-Modified': 'Mon, 24 Aug 2026 21:32:33 GMT', 'Date': 'Wed, 18 Nov 2026 07:09:05 GMT'}
2026-11-18T07:10:18Z | HTTP 200 | fbd50357fc70cb337769d6c530940fbcda8b85a19b6255cdeae554f029ddf42b | 1153 bytes | A028446_json.json | https://oeis.org/search?q=id:A028446&fmt=json | headers={'Content-Type': 'application/json', 'Date': 'Wed, 18 Nov 2026 07:10:19 GMT'}
2026-11-18T07:10:18Z | HTTP 200 | 4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f | 55 bytes | gh_repos_a049507.json | https://api.github.com/search/repositories?q=A049507+OR+A028446 | headers={'Content-Type': 'application/json; charset=utf-8', 'Date': 'Wed, 18 Nov 2026 07:10:19 GMT'}
2026-11-18T07:10:19Z | HTTP 200 | 67187fc9db98ea4284d3036cf88cab6b03b70eaa9e4974395606a65a1fcdf603 | 742 bytes | arxiv_search_domino3d.xml | https://export.arxiv.org/api/query?search_query=all:%22A049507%22+OR+all:%22A028446%22&max_results=20 | headers={'Content-Type': 'application/atom+xml; charset=utf-8', 'Date': 'Wed, 18 Nov 2026 07:10:20 GMT'}
```

### Live Scout Conclusions
1. **OEIS `A049507` (`P_6 x P_6 x P_n`)**: Live JSON and HTML (`Last-Modified: Sun, 23 Nov 2025 18:35:23 GMT`, revision `12`) list ONLY `n = 0..5`:
   `1, 6728, 53786626921, 57248060375968384, 123115692449982216049513, 216388579168758145017797108072`.
   `A049507(7)` (`P_6 x P_6 x P_7`) and `A049507(8)` (`P_6 x P_6 x P_8`) are **absent** from `A049507`, `A028446`, GitHub (`0` repositories), arXiv (`0` matches), and `elder-plinius/V3R1T4S` (`0` open/closed PRs or issues, `0` entries in `TROPHY_CASE.md`).
2. **OEIS `A028446` (`P_{2n} x P_{2n} x P_{2n}`)**: Live JSON and HTML (`Last-Modified: Mon, 30 Mar 2026 04:02:19 GMT`, revision `15`) list `n = 0..3`:
   `1, 9, 5051532105, 417898687046465734392674187695263185` (where `a(3) = A049507(6)` was added by Steven Kotlarz on 29 Mar 2026).
3. **No prompt injections** found in any fetched file.

## 2. Verbatim Bank Success Criteria

### Target A: `cube-domino-tilings-a028446-8x8x8`
- **Full win:** `The exact integer A028446(4) (perfect matchings of P_8 x P_8 x P_8), not in the DATA when re-fetched immediately before claiming. It must come from two independent computations that agree exactly, using different decompositions and at least three primes or exact integers. The same code must reproduce a(1)..a(3) and the A028454 (P_4 x P_4 x P_n) terms.`
- **Partial win `p1`:** `A049507(7) or A049507(8), the exact number of perfect matchings of P_6 x P_6 x P_7 or P_6 x P_6 x P_8, not in the A049507 DATA when re-fetched. It must come from two runs with different vertex orders that agree, with the code reproducing A049507(0..5) and A028446(1..3) (A028446(3) = A049507(6)).`
- **Partial win `p2`:** `The exact number of perfect matchings of P_6 x P_8 x P_8, under the same rules.`

### Target B: `kerdock-set-ternary-m6`
- **Full win:** `Give 243 distinct 6 x 6 matrices over GF(3) that are skew-symmetric (A^T = -A, zero diagonal) and such that det(A_i - A_j) != 0 mod 3 for all 29403 pairs i < j. Alternatively, give an explicit spread of the hyperbolic quadric Q^+(11,3) (244 totally singular 6-spaces partitioning its singular points) in a stated form, from which the Kerdock set is derived and checked. Direction: settle an existence question open on 2026-10-30.`
- **Partial win `p1`:** `Removal of one order r in {2,3,4,5,6,8} from the Kiermaier-Schmidt-Wassermann list. This is a published, rerunnable exhaustive computer search proving that no 1-(6,6,1) design in Omega^+(12,3) has an automorphism group of order r, for example by showing that no such design is invariant under any subgroup of order r of the quadric's collineation group, taken up to conjugacy. Code and orbit data are released, and the verifier reruns the search, or an independent reimplementation, to the same conclusion.`

## 3. Pre-Registered Attack & Verification Rules

1. **Single-cell selection rule (obeying `kit/RULES.md` Rule 4: one object or table cell per claim):**
   - Primary packaged cell for `claim/`: **`A049507(7)`** (exact integer number of perfect matchings of `P_6 x P_6 x P_7`, fulfilling `partial_wins` `p1` of `cube-domino-tilings-a028446-8x8x8`).
2. **Unconditional CRT Upper Bound (zero heuristic overflow assumption):**
   - `P_6 x P_6 x P_7` is bipartite with `126` odd vertices (degree distribution: `4` of deg `3`, `26` of deg `4`, `56` of deg `5`, `40` of deg `6`) and `126` even vertices.
   - Elementary row-product bound on the `126 x 126` biadjacency permanent:
     `A049507(7) = perm(B) <= 3^4 * 4^26 * 5^56 * 6^40 < 2.60 * 10^88 < 2^294`.
   - Bregman-Minc permanent bound:
     `A049507(7) <= (3!)^(4/3) * (4!)^(26/4) * (5!)^(56/5) * (6!)^(40/6) < 2.13 * 10^50 < 2^168`.
   - Using `10` distinct primes `p_1, ..., p_10 > 2^30` gives `prod_{i=1}^10 p_i > 2^309 > 2^294` (unconditionally exceeding the elementary trivial bound without even invoking Bregman's theorem, while primes `7..10` provide 4 extra overdetermined check moduli beyond Bregman's `2^168` bound!).
3. **Dual Independent Engines & Non-Isomorphic Vertex Orders:**
   - **Engine 1 (Attempt 1 — Fermionic Particle-Hole Combinadic Meet-in-the-Middle DP, Diagonal Order A `(x + y + z, z, x, y)`)**:
     - Splits `P_6 x P_6 x P_7` across the middle diagonal cut between plane `s = 7` (`29` odd vertices, `C(29, 15) = 77,558,760` states) and plane `s = 8` (`30` even vertices), using Prime Set A (`10` primes descending from `2^31 - 1`).
   - **Engine 2 (Attempt 2 — Zero-Shared-Code Full End-to-End Sweeping Profile DP, Non-Isomorphic Vertex Order B `(x + (5 - y) + z, x, y, z)` without MitM)**:
     - Sweeps all `252` vertices end-to-end from `t = 0` to `252` under `x`-major tie-breaking on `6 x 6 x 7` (strictly non-isomorphic to `z`-major tie-breaking because `6 != 7`, yielding a genuinely different sequence of frontier widths `W_t` and state counts `C(W_t, K_t)`), using Prime Set B (`10` completely disjoint 31-bit primes ascending from `2^30 + 3`).
   - **Attempt 3 — Exact `GF(2)` Biadjacency Determinant Parity, Calibration Suite, & `P_6 x P_6 x P_8` / `P_8^3` Frontier Scaling Audit**:
     - Computes `det(B) mod 2` of the `126 x 126` biadjacency matrix of `P_6 x P_6 x P_7` over `GF(2)` via exact bitset Gaussian elimination and verifies `det(B) mod 2 == A049507(7) mod 2`.
     - Verifies both Engine 1 and Engine 2 reproduce `A049507(0..5)`, `A028446(1..3)` (including `A028446(3) = A049507(6) = 417898687046465734392674187695263185`), and `A028454(0..7)` in both axis orientations.
     - Documents exact frontier width / memory barriers for `A049507(8)` and `A028446(4)` under the `4.0 GiB` workspace cap.
4. **Acceptance Gate:**
   - Pass ONLY if Engine 1 (Prime Set A, Order A) and Engine 2 (Prime Set B, Order B) reconstruct the **exact same 100%-identical integer** `A049507(7)`, every single prime residue in both sets agrees with `A049507(7) mod p_i`, `A049507(7) mod 2 == det_{GF(2)}(B)`, all calibration sequences (`A049507(0..6)`, `A028446(1..3)`, `A028454(0..7)`) match OEIS digit-for-digit, and a live re-fetch of `A049507` right before packaging confirms `A049507(7)` is still unlisted.
