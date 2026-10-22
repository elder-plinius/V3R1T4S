# Panelist Report — REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Mandate & Quoted Definition

Per the REPRODUCE mandate:
> "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Quoted definition from `claim/CLAIM.md`:
> "OEIS `A089980` ($T(m, n) =$ number of independent sets / hard-square configurations on the $m \times n$ grid graph $P_m \times P_n$, read by antidiagonals $d = m + n$), complete antidiagonal **$d = 79$** (`80` entries $T(w, 79 - w)$ for $w = 0..79$, corresponding to b-file indices `n = 3160..3239`, determined by the `40` canonical widths $w = 0..39$ under $T(w, m) = T(m, w)$)."

Before inspecting `claim/author_checker_a089980_ad79.py`, `claim/hs_mod.py`, `claim/far.py`, or `claim/indep_transfer.py`, a standalone verification script (`indep_reproduce_a089980.py`) was written from scratch directly from the graph-theoretic definition of independent sets on $P_w \times P_m$ and executed against the saved artifact files in `claim/`.

## 2. File Integrity & SHA-256 Hashes Verified

All six claimed data files in `claim/` were checked for exact byte length and SHA-256 digest:

| File | Size (bytes) | SHA-256 | Status |
|---|---:|---|---|
| `claim/a089980_antidiag79.txt` | `15,242` | `918a1787709ce8d30985fe62d7cf067072f66d3edf34e5c99718541f3b7f0ed6` | Match |
| `claim/a089980_antidiag79.tsv` | `16,032` | `8f76c40e12a0b32548660ca69e1ae2eadd060a2b04fb39737363205e740a6c8e` | Match |
| `claim/residues_hs_mod.tsv` | `34,110` | `fd7afeceeca2989189406d1f5dac326f2fe561e6d5b5726952c73d2c63688f68` | Match |
| `claim/residues_far.tsv` | `34,498` | `bac0ba49cae99d2b8dbc5d3f2ba40b8e0f7204bad0ad76398c69b60d9c906107` | Match |
| `claim/antidiag79_indep_bigint.tsv` | `1,870` | `d69d90e4b286878a5e01a6aa1c29c89471c8f1890f50ecf16e45973c763662c3` | Match |
| `claim/b089980.txt` | `304,116` | `a28e1a8df3a08cf6881981e6288a61b0bad260be40cbd4ca58d08d53fbef2e32` | Match |

## 3. Independent Checker Results (Pre-Code-Inspection)

Running `indep_reproduce_a089980.py` completed in `5.33s` and verified:

1. **Format & Symmetry of Saved Tables:**
   - `claim/b089980.txt` contains `3,160` entries (`n = 0..3159`), covering complete antidiagonals $d = 0..78$.
   - `claim/a089980_antidiag79.txt` (`80` lines, `n = 3160..3239`) and `claim/a089980_antidiag79.tsv` (`80` rows, $w = 0..79, m = 79 - w$) match each other 100% in integer value and decimal digit count, and satisfy $T(w, 79 - w) = T(79 - w, w)$ for all $w = 0..79$, with $T(0, 79) = T(79, 0) = 1$ and $T(1, 78) = T(78, 1) = F(80) = 23416728348467685$.

2. **Brute-Force Subset Enumeration ($0 \le w, m \le 4$):**
   - Enumerating all $2^{wm}$ vertex subsets of $P_w \times P_m$ and filtering for subsets with no horizontal or vertical adjacency matched `claim/b089980.txt` at index $n = d(d+1)/2 + w$ ($d = w + m$) across all `25/25` grids (`0` mismatches).

3. **Independent Pure-Python Big-Integer Column-Transfer DP ($w = 0..14$):**
   - Constructing the valid column bitmasks $\{s \in [0, 2^w) : s \mathbin{\&} (s \ll 1) = 0\}$ of cardinality $F(w+2)$ and iterating compatible column transitions $u \mathbin{\&} v = 0$ in exact Python arbitrary-precision arithmetic recomputed `1,080` published cells ($w = 0..14, w + m \le 78$) against `claim/b089980.txt` and `15` new antidiagonal-79 cells ($w = 0..14, m = 79 - w$) against `claim/a089980_antidiag79.txt` in `1.06s` with `0` mismatches.
   - All `17` rows ($w = 0..16$) of `claim/antidiag79_indep_bigint.tsv` also matched `claim/a089980_antidiag79.txt` exactly.

4. **Independent Chinese Remainder Theorem (CRT) Reconstruction & Determinism:**
   - Both `claim/residues_hs_mod.tsv` (`1,000` rows across $w = 0..39$) and `claim/residues_far.tsv` (`1,027` rows across $w = 0..39$) were reconstructed twice to verify determinism (`hs_rec1 == hs_rec2` and `far_rec1 == far_rec2`).
   - Deterministic Miller-Rabin primality testing confirmed all `37` moduli in `claim/residues_hs_mod.tsv` (range $[2147482819, 2147483647] \subset (2^{30}, 2^{31})$) and all `38` moduli in `claim/residues_far.tsv` (range $[1073740933, 1073741789] \subset (0, 2^{30})$) are prime.
   - The two prime sets have `0` shared primes ($\max P_{\text{far}} = 1073741789 \lt 2^{30} \lt 2147482819 = \min P_{\text{hs\_mod}}$).
   - For every width $w = 0..39$ in both tables, the product $M$ of `crt`-role primes strictly exceeds the theoretical upper bound $F(w+2)^{79-w}$, and the reconstructed integer $X \in [0, M)$ satisfies $X \bmod p_{\text{check}} = r_{\text{check}}$ on the held-out check prime (`40/40` widths pass in `hs_mod`, `40/40` widths pass in `far`).
   - Across all `40` canonical widths $w = 0..39$ (and all `80` symmetric entries `n = 3160..3239`), the CRT reconstructions from `claim/residues_hs_mod.tsv`, `claim/residues_far.tsv`, `claim/a089980_antidiag79.txt`, and `claim/a089980_antidiag79.tsv` agree 100% character-for-character.
   - Specifically, the central peak entry at $w = 39, m = 40$ (b-file index `3199`, `279` digits) is verified as:
     `254735682081189541344081503360736788844774937958504869716096214590338245178492823863429255507628678700444558564935870046594368781174025731139175661159108554557238150761113808065611962133371021250718485742976243397588856426972383225337965855119190243350002187880478598136326595377`

5. **Independent Split-Horizon Broken-Profile DP Modulo Fresh Primes:**
   - An independent lexicographically ranked split-horizon broken-profile DP written from scratch in `indep_reproduce_a089980.py` was run modulo two fresh primes outside both tables (`p1 = 1000000007` for $w = 0..22, m = 79 - w$ and `p2 = 3037000493` for $w = 0..18, m = 79 - w$) in `4.11s`.
   - Every residue matched `claim/a089980_antidiag79.txt` modulo `p1` and `p2` with `0` mismatches (e.g. $T(16, 63) \bmod 1000000007 = 309266150$ and $T(22, 57) \bmod 1000000007 = 532732411$).

6. **Entropy-Constant Consistency Check:**
   - At $(w, m) = (39, 40)$, $T(39, 40)^{1/1560} = 1.5082225930$ (excess $+0.005175$ above Baxter's hard-square entropy constant $\kappa = 1.5030480825$), monotonically decreasing from $d = 78$'s central entry $T(39, 39)^{1/1521} = 1.5082890104$ (excess $+0.005241$), consistent with the $O(1/w)$ free-boundary perimeter contribution on open grids.

## 4. Inspection & Execution of Author Code

After completing independent verification, the four Python scripts in `claim/` were inspected and executed:
- **Code Independence Verified:**
  - `claim/hs_mod.py` implements an MSB-first recursive `[0+V(n-1), 10+V(n-2)]` boustrophedon cell-by-cell broken-profile DP over `uint64` arrays with lazy reduction every `RED = 32` cells and 31-bit primes descending from $2^{31} - 1$.
  - `claim/far.py` implements a whole-column Fibonacci-trie butterfly transform (`transfer` / `transfer32`) converting suffix S-ranks to reversed prefix P-ranks (`P_k = P_{k-1}.0 | P_{k-2}.01`) using 30-bit primes descending from $2^{30} - 1$.
  - `claim/indep_transfer.py` implements pure-Python exact arbitrary-precision full-column bitwise pattern transfer (`s & sp == 0`) plus a dictionary-based cell-by-cell broken-profile cross-check for small $w$.
- **Execution of `claim/author_checker_a089980_ad79.py` and `claim/far.py selftest`:**
  - `author_checker_a089980_ad79.py` passed all checks `(A)`–`(D)` (`25/25` brute-force grids, `814` published cells for $w = 0..10$, `17/17` big-int rows in `claim/antidiag79_indep_bigint.tsv`, `40/40` CRT reconstructions and check primes in both tables, and live fresh-prime check $T(16, 63) \bmod 1000000007 = 309266150$), printing `PASS`.
  - `far.py selftest` reproduced all published cells for $w = 0..12$ (`0` mismatches), verified the P-rank reversal identity and random-vector transfer definition for $w = 1..10$, and verified modular vs exact agreement on $w \in \{9, 12, 16\}$ across primes `[1073741789, 1073741783, 1073741741]`, printing `SELFTEST: PASS`.
- Temporary scratch working directory was removed so `panel/` contains only panelist reports.

pass: true
