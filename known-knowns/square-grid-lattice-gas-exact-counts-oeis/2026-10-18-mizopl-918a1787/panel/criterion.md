# Skeptic Panel Report — Role: CRITERION

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target: square-grid-lattice-gas-exact-counts-oeis
claimed_level: partial win p2 (OEIS A089980 complete antidiagonal d = 79, b-file indices n = 3160..3239)

## 1. Clause-by-Clause Criterion Audit

### 1.1 Main Target vs Enumerated Partial Win `p2`
- **Main `success_criterion`:** Requires the first unknown diagonal term $a(N)$ of `A028420`, `A006506`, or `A063443`. This run does not claim any of those three diagonal sequences and therefore does not meet the main target criterion.
- **Enumerated partial win `p2` (verbatim):**
  > "`p2`: A new row of an associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares m x n) extending the largest published m by one for all n up to the published range, same rules."
- **How `A089980` is tabulated and why antidiagonal $d = 79$ is the complete next row:**
  - OEIS `A089980` tabulates $T(w, m)$, the number of independent vertex sets (hard-square configurations) on the $w \times m$ grid graph $P_w \times P_m$, read by rising antidiagonals $d = w + m \ge 0$, with $w = 0, 1, \dots, d$ and b-file index $n(w, m) = d(d+1)/2 + w$.
  - In `claim/b089980.txt` (`304,116` bytes, `3,160` lines, `sha256: a28e1a8df3a08cf6881981e6288a61b0bad260be40cbd4ca58d08d53fbef2e32`), the published sequence covers $n = 0..3159$, which is the exact set of complete antidiagonals $d = 0..78$ ($\sum_{d=0}^{78} (d+1) = 79 \times 80 / 2 = 3160$).
  - Extending the published table by one complete row under the OEIS tabulation rule therefore requires all `80` entries of antidiagonal $d = 79$: $T(w, 79 - w)$ for $w = 0..79$ (`n = 3160..3239`). By grid transposition symmetry $T(w, m) = T(m, w)$ (verified with `0` mismatches across all `3,160` published entries of `claim/b089980.txt`), the `80` entries of $d = 79$ are determined by the `40` canonical widths $w = 0..39$.
  - No hidden quantifiers or stretched definitions are present: all `40` canonical widths $w = 0..39$ and all `80` symmetric entries `n = 3160..3239` are present in `claim/a089980_antidiag79.txt` (`15,242` bytes, `80` lines, `sha256: 918a1787709ce8d30985fe62d7cf067072f66d3edf34e5c99718541f3b7f0ed6`) and `claim/a089980_antidiag79.tsv` (`16,032` bytes, `81` lines, `sha256: 8f76c40e12a0b32548660ca69e1ae2eadd060a2b04fb39737363205e740a6c8e`).

### 1.2 Two-Run Independence Rule ("same rules")
- **Decomposition 1 (`claim/hs_mod.py`, `8,386` bytes, `sha256: d4f6a8fc22858bf4032020fb801b99baab30196dbf43c49487952b23a20d0dfb`):**
  - State encoding and sweep: cell-by-cell broken-profile DP with boustrophedon column alternation, factoring the frontier after row $k$ into $(A, B) \in V(k+1) \times V(w-k-1)$ with no cross-break constraint, ordered recursively MSB-first as $[0 + V(n-1)] \cup [10 + V(n-2)]$, reducing modulo $p$ every $32$ cells in `uint64`.
  - Saved residue table `claim/residues_hs_mod.tsv` (`34,110` bytes, header + `1,000` rows, `sha256: fd7afeceeca2989189406d1f5dac326f2fe561e6d5b5726952c73d2c63688f68`) uses `37` distinct 31-bit primes in $[2147482819, 2147483647] \subset (2^{30}, 2^{31})$.
- **Decomposition 2 (`claim/far.py`, `12,863` bytes, `sha256: db0e4d373637178f234a4fd10c49ee7c4ac05a699fddd7f975a47d821a476647`):**
  - State encoding and sweep: whole-column transfer operator $g(s) = \sum_{t \ \& \ s = 0} f(t)$ computed via a $w$-pass butterfly over the Fibonacci trie where suffixes are S-ranked by first bit and prefixes are P-ranked by last bit (reversed-string S-rank, exploiting reversal symmetry $g(\text{rev } s) = g(s)$), reducing once per column step (or branch-free conditional subtraction in `uint32` for $w \ge 33$).
  - Saved residue table `claim/residues_far.tsv` (`34,498` bytes, header + `1,027` rows, `sha256: bac0ba49cae99d2b8dbc5d3f2ba40b8e0f7204bad0ad76398c69b60d9c906107`) uses `38` distinct 30-bit primes in $[1073740933, 1073741789] \subset (0, 2^{30})$.
- **Decomposition 3 (`claim/indep_transfer.py`, `8,232` bytes, `sha256: 19268839e70bfdd6f88fba93fde4889f03c0843ad07242bc02f0914539f14777`):**
  - Explicit compatibility-list column transfer in pure-Python arbitrary-precision integers (no modular arithmetic, no CRT) for $w = 0..16$, saved in `claim/antidiag79_indep_bigint.tsv` (`1,870` bytes, header + `17` rows, `sha256: d69d90e4b286878a5e01a6aa1c29c89471c8f1890f50ecf16e45973c763662c3`).
- **Independent verification results:**
  - Deterministic Miller-Rabin primality verified for all `37` primes in `claim/residues_hs_mod.tsv` and all `38` primes in `claim/residues_far.tsv`.
  - Prime-set intersection: `0` shared primes ($\max P_{\text{far}} = 1073741789 < 2^{30} = 1073741824 < 2147482819 = \min P_{\text{hs\_mod}}$).
  - Rigorous CRT bound: for every width $w \in \{0, \dots, 39\}$ and $m = 79 - w$, the CRT modulus product $M_{\text{crt}} = \prod p_{\text{crt}}$ strictly exceeds the hard upper bound $F(w+2)^m \ge T(w, m)$ by at least `1.28` bits in `hs_mod` (`23.88` bits at $w = 39$) and at least `0.86` bits in `far` (`17.88` bits at $w = 39$).
  - Held-out check prime: on all `40/40` widths in `hs_mod` and all `40/40` widths in `far`, the CRT-reconstructed integer $X_w$ satisfies $X_w \bmod p_{\text{check}} = r_{\text{check}}$.
  - Exact agreement: `40/40` widths agree to the last decimal digit between `hs_mod` and `far` (up to `279` digits at $T(38, 41)$ and $T(39, 40)$), and `17/17` widths $w = 0..16$ agree with `claim/antidiag79_indep_bigint.tsv`.

### 1.3 Reproduction Rule ("with the same code reproducing every published term ... exactly")
- Both `claim/hs_mod.py` and `claim/far.py` compute all $m = 0..79-w$ in a single column sweep per width $w$, reproducing all $\sum_{w=0}^{39} (79 - w) = 2380$ published cells $(w, m)$ with $w + m \le 78$ across $w = 0..39$ (covering all `3,160` entries of `claim/b089980.txt` by symmetry) with `0` mismatches.
- Independent verification confirmed:
  1. Brute-force subset enumeration on $P_w \times P_m$ for all $25$ grids $0 \le w, m \le 4$: `25/25` match `claim/b089980.txt`.
  2. Pure-Python exact big-integer column transfer for $w = 0..10$, $m \le 78 - w$: `814/814` published cells match `claim/b089980.txt` with `0` mismatches, and all `11` new cells $T(w, 79 - w)$ match `claim/a089980_antidiag79.txt`.
  3. `claim/far.py selftest`: reproduces all `975` published cells for $w = 0..12$ in exact big-integer arithmetic (`0` mismatches), verifies P-rank reversal against the direct bitwise definition on random vectors for $w = 1..10$, and verifies modular vs exact agreement on $w \in \{9, 12, 16\}$.
  4. Live fresh-prime sweeps at $p = 999999937$ (outside both prime sets) on $w \in \{12, 16, 18\}$ for all $m = 0..79-w$: `hs_mod.py` and `far.py` agree identically on every published cell (`m < 79 - w`) and on the new $d = 79$ cell (`m = 79 - w`, yielding `845241495` at $w = 12$, `831304054` at $w = 16$, and `292738096` at $w = 18$), and `p = 1000000007` at $w = 16, m = 63$ yields `309266150`, matching $T(16, 63) \bmod p$.

### 1.4 Growth / Entropy Constant Analysis
- Baxter's hard-square entropy constant is $\kappa = 1.5030480825\dots$
- On finite $w \times m$ grids with free (open) boundaries, vertices on the perimeter $2(w + m)$ have fewer neighbors, creating a positive finite-size boundary excess of order $O(1/w)$ in $T(w, m)^{1/(wm)}$:
  - At $d = 77$ central cell $(38, 39)$ ($N = 1482$): $T(38, 39)^{1/1482} = 1.5083589266$ (excess $+0.005311$ above $\kappa$).
  - At $d = 78$ central cell $(39, 39)$ ($N = 1521$): $T(39, 39)^{1/1521} = 1.5082890104$ (excess $+0.005241$ above $\kappa$).
  - At $d = 79$ central cell $(39, 40)$ ($N = 1560$): $T(39, 40)^{1/1560} = 1.5082225930$ (excess $+0.005175$ above $\kappa$).
- The excess decreases monotonically toward $\kappa$ at the expected $O(1/w)$ open-boundary rate. As documented in `claim/CLAIM.md`, open-boundary grids at $w \le 40$ have $O(1/w) \approx 5.2 \times 10^{-3} > 10^{-3}$, which is a structural property of finite open-boundary hard-square grids and is stated transparently in `confirmed_scope`.

### 1.5 Perturbation / Corruption Controls (Null Models)
- **Control 1 (1-digit perturbation of claimed output):** Changing the final digit of $T(39, 40)$ (`n = 3199`) from `7` to `8` in a temporary copy of `claim/a089980_antidiag79.txt` caused `claim/author_checker_a089980_ad79.py` to fail immediately with `returncode = 1` (`AssertionError`).
- **Control 2 (1-residue perturbation in `hs_mod` CRT prime):** Incrementing one CRT residue at $w = 39$ by $+1 \bmod p$ in a temporary copy of `claim/residues_hs_mod.tsv` caused `claim/author_checker_a089980_ad79.py` to fail immediately with `returncode = 1` (`AssertionError: hs_mod check prime failed at w=39`).
- **Control 3 (1-residue perturbation in `far` check prime):** Incrementing the held-out check residue at $w = 39$ by $+1 \bmod p$ in a temporary copy of `claim/residues_far.tsv` caused `claim/author_checker_a089980_ad79.py` to fail immediately with `returncode = 1` (`AssertionError: far check prime failed at w=39`).

## 2. Confirmed Scope

confirmed_scope: The complete 80-entry antidiagonal d = 79 (b-file indices 3160..3239, canonical widths w = 0..39 peaking at the 279-digit T(39, 40) = 254735682081189541344081503360736788844774937958504869716096214590338245178492823863429255507628678700444558564935870046594368781174025731139175661159108554557238150761113808065611962133371021250718485742976243397588856426972383225337965855119190243350002187880478598136326595377) of OEIS A089980 in claim/a089980_antidiag79.txt (sha256 918a1787709ce8d30985fe62d7cf067072f66d3edf34e5c99718541f3b7f0ed6) is confirmed under partial win p2's two-run rule (40/40 widths agreed between MSB-first boustrophedon broken-profile DP modulo 37 primes in (2^30, 2^31) and LSB-first butterfly column-transfer DP modulo 38 disjoint primes in (0, 2^30), plus exact big-integer column transfer on w = 0..16, all 40/40 held-out check primes passing) and reproduction rule (0 mismatches across all published cells d <= 78 in claim/b089980.txt); at (39, 40), T(39, 40)^(1/1560) = 1.5082225930 vs Baxter's hard-square constant 1.5030480825 (open-boundary finite-size gap +0.005175, monotonically decreasing from +0.005241 at (39, 39) and +0.005311 at (38, 39)).

pass: true
