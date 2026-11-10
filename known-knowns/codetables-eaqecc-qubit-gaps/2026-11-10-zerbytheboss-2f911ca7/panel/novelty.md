# Skeptic Panel — NOVELTY

- context: fresh research subagent invoked with zero solver history (role: NOVELTY)
- target: `codetables-eaqecc-qubit-gaps` — cell `(n, k, c) = (19, 2, 9)` (`[[19, 2, 11; 9]]_2` vs live `[[19, 2, 10-17; 9]]_2`)
- object audited: `object/eaqecc_n19_k2_d11_c9.tsv`

## 1. Live Primary Table Re-Fetch (`PROVED-HERE`)

A single plain HTTP GET was issued in memory via Python `urllib.request` (`User-Agent: V3R1T4S-novelty-skeptic/1.0`, zero files written to disk) against Markus Grassl's primary binary EAQECC table:

- **URL**: <http://www.codetables.de/EAQECC/qubit.php>
- **UTC Fetch Window**: `2026-11-10T20:08:26Z` to `2026-11-10T20:08:34Z` (HTTP `Date` header: `Tue, 10 Nov 2026 20:08:33 GMT`)
- **HTTP Status**: `200` (`Server: Apache`, `Content-Type: text/html; charset=UTF-8`)
- **Payload Size**: `1,194,336` bytes (`111` lines; `7,752` `<TD ... class="EAQECC">` parameter entries across `2,144` `(n, k)` cells; zero prompt-injection text)
- **Page Footer Stamp**: `Last change: 10.07.2025`
- **Live SHA-256**: `c84dea1ab3b3657e268462019569f0bf6b3cb15872ae0675d47ae9ae62536e6a` (matches `the-record-we-beat/codetables_eaqecc_n19_k2_c9_snapshot.md` bit-for-bit)

Across all `2,144` `(n, k)` boxes in `qubit.php`, Grassl prints exclusively the Pareto step-points `c` (`0 <= c <= n - k`) at which `d_lower(n, k, c)` strictly increases (`0` monotonicity exceptions across all `7,752` entries, `PROVED-HERE`). Extracting the `(n = 19, k = 2)` box verbatim from line 50 of the live HTML yields every printed entry and the implied monotone step function across all `c = 0..18` (`c <= n - k = 17` is the algebraic maximum for `n = 19, k = 2`, since `rank(S Omega S^T) = 2c <= dim(S) = n - k + c`):

- `c = 0`: `[[19,2,6;0]]_2` (`bgcolor="#66ff00"`, `title="from codetables.de"`) -> effective `d_lower(19, 2, c) = 6` for `c in {0, 1}`.
- `c = 2`: `[[19,2,9-16;2]]_2` (`bgcolor="#ffff00"`, `title="using teleportation"`) -> effective `d_lower(19, 2, c) = 9` for `c in {2, 3, 4, 5, 6, 7, 8}`.
- `c = 9`: `[[19,2,10-17;9]]_2` (`bgcolor="#00ccff"`, `title="reducing length of [[28,2,10;0]] from codetables.de"`) -> `d_lower = 10`, `d_upper = 17` at `(19, 2, 9)`, and because no higher `c in {10..17}` entry appears in `(19, 2)`, the live table knows no `[[19, 2, >=11; c]]_2` code even for `c in {10..17}` (`effective d_lower = 10` for `c in {9..17}`).
- `c = 18`: algebraically infeasible (`c > n - k = 17`).

Conclusion of live table check (`PROVED-HERE`): Cell `(n, k, c) = (19, 2, 9)` is live and open with `[[19, 2, 10-17; 9]]_2` (`d_lower = 10`, `d_upper = 17`), so `d_EA = 11` strictly beats `d_lower = 10` (`10 < 11 <= 17`).

## 2. Propagation & Neighbouring-Cell Audit (`PROVED-HERE`)

### 2a. Live Neighbouring Cells (`n in 17..23, k in 1..5, c in 0..15`)

All explicit entries extracted from the live `qubit.php` HTML in the `(n in 17..23, k in 1..5, c in 0..15)` window (`PROVED-HERE`):

- `n = 17`:
  - `(17, 1)`: `[[17,1,7;0]]`, `[[17,1,11-16;1]]`, `[[17,1,13-16;12]]`, `[[17,1,15-16;14]]`
  - `(17, 2)`: `[[17,2,6;0]]`, `[[17,2,8-14;2]]`, `[[17,2,10-15;9]]`
  - `(17, 3)`: `[[17,3,5-6;0]]`, `[[17,3,7-12;3]]`, `[[17,3,9-14;9]]`
  - `(17, 4)`: `[[17,4,5;0]]`, `[[17,4,6-9;3]]`, `[[17,4,7-12;8]]`, `[[17,4,8-13;9]]`
  - `(17, 5)`: `[[17,5,4-5;0]]`, `[[17,5,5-7;1]]`, `[[17,5,6-9;4]]`, `[[17,5,7-11;8]]`, `[[17,5,8-12;11]]`
- `n = 18`:
  - `(18, 1)`: `[[18,1,7;0]]`, `[[18,1,12-17;1]]`, `[[18,1,13-17;12]]`, `[[18,1,15-17;14]]`
  - `(18, 2)`: `[[18,2,6;0]]`, `[[18,2,8-15;2]]`, `[[18,2,10-16;9]]`
  - `(18, 3)`: `[[18,3,5-6;0]]`, `[[18,3,6-9;2]]`, `[[18,3,8-13;3]]`, `[[18,3,9-15;9]]`
  - `(18, 4)`: `[[18,4,5-6;0]]`, `[[18,4,6-9;2]]`, `[[18,4,7-13;7]]`, `[[18,4,8-13;8]]`, `[[18,4,9-14;11]]`
  - `(18, 5)`: `[[18,5,5;0]]`, `[[18,5,6-9;3]]`, `[[18,5,7-12;7]]`, `[[18,5,9-13;11]]`
- `n = 19`:
  - `(19, 1)`: `[[19,1,7;0]]`, `[[19,1,12-18;1]]`, `[[19,1,13-18;12]]`, `[[19,1,15-18;14]]`
  - `(19, 2)`: `[[19,2,6;0]]`, `[[19,2,9-16;2]]`, `[[19,2,10-17;9]]`
  - `(19, 3)`: `[[19,3,5-6;0]]`, `[[19,3,6-9;1]]`, `[[19,3,8-14;3]]`, `[[19,3,9-15;8]]`
  - `(19, 4)`: `[[19,4,5-6;0]]`, `[[19,4,6-9;1]]`, `[[19,4,7-12;4]]`, `[[19,4,8-14;7]]`, `[[19,4,9-15;11]]`
  - `(19, 5)`: `[[19,5,5-6;0]]`, `[[19,5,6-9;2]]`, `[[19,5,7-12;6]]`, `[[19,5,9-14;11]]`
- `n = 20`:
  - `(20, 1)`: `[[20,1,7;0]]`, `[[20,1,13-19;1]]`, `[[20,1,15-19;14]]`
  - `(20, 2)`: `[[20,2,6-7;0]]`, `[[20,2,10-17;2]]`
  - `(20, 3)`: `[[20,3,6-7;0]]`, `[[20,3,8-15;3]]`, `[[20,3,9-16;7]]`
  - `(20, 4)`: `[[20,4,6;0]]`, `[[20,4,8-13;4]]`, `[[20,4,9-16;11]]`
  - `(20, 5)`: `[[20,5,5-6;0]]`, `[[20,5,6-9;1]]`, `[[20,5,7-11;5]]`, `[[20,5,8-14;9]]`, `[[20,5,9-15;11]]`
- `n = 21`:
  - `(21, 1)`: `[[21,1,7;0]]`, `[[21,1,14-20;1]]`, `[[21,1,15-20;14]]`
  - `(21, 2)`: `[[21,2,6-7;0]]`, `[[21,2,7-11;1]]`, `[[21,2,10-18;2]]`
  - `(21, 3)`: `[[21,3,6-7;0]]`, `[[21,3,8-16;3]]`, `[[21,3,9-17;6]]`, `[[21,3,10-18;11]]`
  - `(21, 4)`: `[[21,4,6-7;0]]`, `[[21,4,8-14;4]]`, `[[21,4,10-17;11]]`
  - `(21, 5)`: `[[21,5,6;0]]`, `[[21,5,7-11;4]]`, `[[21,5,8-15;9]]`, `[[21,5,9-16;11]]`
- `n = 22`:
  - `(22, 1)`: `[[22,1,7-8;0]]`, `[[22,1,14-21;1]]`, `[[22,1,15-21;14]]`
  - `(22, 2)`: `[[22,2,7-8;0]]`, `[[22,2,11-19;2]]`
  - `(22, 3)`: `[[22,3,6-7;0]]`, `[[22,3,9-17;3]]`, `[[22,3,11-19;11]]`
  - `(22, 4)`: `[[22,4,6-7;0]]`, `[[22,4,7-11;3]]`, `[[22,4,8-15;4]]`, `[[22,4,10-17;11]]`
  - `(22, 5)`: `[[22,5,6-7;0]]`, `[[22,5,7-11;3]]`, `[[22,5,8-13;5]]`, `[[22,5,9-16;11]]`
- `n = 23`:
  - `(23, 1)`: `[[23,1,7-9;0]]`, `[[23,1,15-22;1]]`
  - `(23, 2)`: `[[23,2,7-8;0]]`, `[[23,2,12-20;2]]`
  - `(23, 3)`: `[[23,3,6-8;0]]`, `[[23,3,7-12;2]]`, `[[23,3,10-18;3]]`, `[[23,3,11-20;11]]`
  - `(23, 4)`: `[[23,4,6-7;0]]`, `[[23,4,7-11;2]]`, `[[23,4,8-12;3]]`, `[[23,4,10-18;11]]`
  - `(23, 5)`: `[[23,5,6-7;0]]`, `[[23,5,7-11;2]]`, `[[23,5,8-14;5]]`, `[[23,5,9-17;11]]`

### 2b. Exhaustive Check of EAQECC Propagation Rules (Grassl-Huber-Winter `arXiv:2207.05647` / Brun-Devetak-Hsieh)

Every non-catalytic propagation rule (`KNOWN` definitions from M. Grassl, F. Huber, and A. Winter, *IEEE Trans. Inf. Theory* 68(6), 3920-3950, 2022, <https://arxiv.org/abs/2207.05647>; T. A. Brun, I. Devetak, and M.-H. Hsieh, *Science* 314, 436-439, 2006, <https://arxiv.org/abs/quant-ph/0610092>) was audited globally across all `7,752` cells of `qubit.php` (`PROVED-HERE`):

1. **Puncturing (`[[n+t, k', d'; c']]_2 -> [[n, k, >= d' - t; c]]_2` for `t >= 1, k' >= 2, c' <= 9`)**:
   - At `t = 1..4`: `(20, 2, 2)` gives `10 - 1 = 9`; `(21, 2, 2)` gives `10 - 2 = 8`; `(22, 2, 2)` gives `11 - 3 = 8`; `(23, 2, 2)` gives `12 - 4 = 8`.
   - Across the entire `n = 20..64` table with `k' >= 2, c' <= 9`, `max(d_lower(n', k', c') - (n' - 19)) = 9 < 11`. Zero cells imply `d >= 11`.
2. **Subcode, Ebit-Increase, Teleportation & Length Reduction**:
   - *Subcode (`[[19, k', d'; c']]_2 -> [[19, 2, >= d'; 9]]_2` for `k' >= 3, c' <= 9`)*: Best at `n = 19` is `(19, 3, 8)` with `d_lower = 9 < 11`.
   - *Ebit trading / teleportation (`[[19 + t, 2 + t, d'; c' - t]]_2 -> [[19, 2, >= d'; c']]_2`)*: For `t = 1`, `(20, 3, c' <= 8)` has max `d_lower = 9` (`(20, 3, 7)`); for `t = 2`, `(21, 4, c' <= 7)` has max `d_lower = 8` (`(21, 4, 4)`); across all `t >= 1`, zero cells reach `d >= 11` with `c' + t <= 9` and `k' - t >= 2`. (Note: catalytic reduction `[[n, k, d; c]] -> [[n, k-1, d; c-1]]` is explicitly excluded by the non-catalytic setting of `qubit.php`, and even `(19, 3, 10)` has live `d_lower = 9 < 11`.)
   - *Length reduction (`[[19 + t, k' >= 2, d'; c']]_2 -> [[19, 2, >= d'; c' + t]]_2`)*: Moving `t` qubits from sender to receiver without losing logical dimension `k` requires the isotropic radical `H_0 = S cap S^{perp_s}` to project onto a full `2t`-dimensional symplectic space on those `t` coordinates. Across all `2,286` length-reduction cells in `qubit.php`, the parent has `c' = 0`; for `19 <= n' <= 28` (`t <= 9`), `max d_lower(n', >=2, 0) = 10` at `[[28, 2, 10; 0]]_2` (in fact `d_lower(n', 2, 0) = 10` for all `28 <= n' <= 35`). Meanwhile, the `c' = 2` classical-teleportation codes `[[22, 2, 11-19; 2]]_2` (`from [22, 4, 11]_2`) have purely `Z`-type radical `H_0 = {(0 | z) : z in C^{perp}}`, so on every coordinate `dim_GF2(proj_i(H_0)) <= 1 < 2`; shortening `S^{perp_s}` at a coordinate imposes an `X`-constraint on `C` and drops `k` from `2` to `1` rather than increasing `c`.
   - *Pure-code quantum shortening (`[[19 + t, 2 - t, d'; c' <= 9]]_2 -> [[19, 2, >= d' - t; c']]_2`, valid only when pure to `d'`)*: At `t = 2` (`(21, 0, c' <= 9)`), max `d_lower = 12` (`[[21, 0, 12-16; 9]]_2`), giving `12 - 2 = 10 < 11`. At `t = 1` (`(20, 1, c' <= 9)`), `c' = 0` gives `7 - 1 = 6`, while `[[20, 1, 13-19; 1]]_2` (`using teleportation` of `[20, 2, 13]_2`) is highly degenerate (`d(S cap S^{perp_s}) = 2`), so quantum shortening does not apply (which is why Grassl's own table lists `(19, 2, 1)` effective `d_lower = 6`, not `12`).
3. **Lengthening / Ancilla-Padding & Ancestor Audit (`[[19 - 2s, 2, >=11; 9 - s]]_2` and `GF(4)` Griesmer Bound)**:
   - Live effective `d_lower` values on all ancestor cells (`s = 1..4`, both at `c' = 9 - s` and `c' = 9`):
     - `s = 1`: `(17, 2, 8)` has effective `d_lower = 8` (from `[[17,2,8-14;2]]`); `(17, 2, 9)` has `[[17,2,10-15;9]]` (`d_lower = 10`); `(18, 2, 9)` has `[[18,2,10-16;9]]` (`d_lower = 10`).
     - `s = 2`: `(15, 2, 7)` has effective `d_lower = 8` (from `[[15,2,8-12;2]]`); `(15, 2, 9)` has `[[15,2,10-13;9]]` (`d_lower = 10`).
     - `s = 3`: `(13, 2, 6)` has effective `d_lower = 6` (from `[[13,2,6-10;2]]`); `(13, 2, 9)` has `[[13,2,8-11;9]]` (`d_lower = 8`).
     - `s = 4`: `(11, 2, 5)` has `[[11,2,6-9;5]]` (`d_lower = 6`); `(11, 2, 9)` has effective `d_lower = 6`.
   - Globally across all `n' <= 18, k' >= 2, c' <= 9` in `qubit.php`, the maximum `d_lower` is `10` (from `[[15, 2, 10-13; 9]]_2`), never `11`.
   - **Direct `GF(4)` Griesmer & Residual Non-Existence Audit on `[11 + 2 l', 2 + l']_4` for `l' in {0, 1, 2, 3}` (`PROVED-HERE`)**:
     Using `g_4(kappa, d) = sum_{j=0}^{kappa - 1} ceil(d / 4^j)` at `d = 11`:
     - `l' = 0` (`[11, 2]_4`, Hermitian LCD): `g_4(2, 11) = 11 + 3 = 14 > 11` (Griesmer max `d = 8`). Impossible.
     - `l' = 1` (`[13, 3]_4`, `1`-hull): `g_4(3, 11) = 11 + 3 + 1 = 15 > 13` (Griesmer max `d = 9`). Impossible.
     - `l' = 2` (`[15, 4]_4`, `2`-hull): `g_4(4, 11) = 11 + 3 + 1 + 1 = 16 > 15` (Griesmer max `d = 10`). Impossible.
     - `l' = 3` (`[17, 5]_4`, `3`-hull): `g_4(5, 11) = 11 + 3 + 1 + 1 + 1 = 17 = n` (`g_4(5, 12) = 18 > 17`), so Griesmer alone allows `d = 11` with equality, **but a classical `[17, 5, 11]_4` code does not exist**: any `[17, 5, 11]_4` code contains a weight-`11` codeword (`11 < 44/3`), whose residual code on the remaining `17 - 11 = 6` coordinates is a `[6, 4, d']_4` code with `d' >= 11 - floor(33/4) = 3`; yet a `[6, 4]_4` code has a `2 x 6` parity-check matrix over `GF(4)`, and because `|PG(1, 4)| = (4^2 - 1)/(4 - 1) = 5 < 6`, either a column is zero (`d' = 1`) or two columns are `GF(4)^*`-proportional (`d' <= 2`), a contradiction (`d_max([17, 5]_4) = 10`).
   - **Direct Irreducibility Check on `object/eaqecc_n19_k2_d11_c9.tsv` (`PROVED-HERE`)**: Inspecting the `26 x 38` stabilizer matrix `S` directly confirms that `S` contains `0` vectors of symplectic weight `1` and `0` vectors of symplectic weight `2`, every coordinate `i in {0..18}` has full `4`-element Pauli projection in `S^{perp_s}`, and puncturing `S^{perp_s}` at **any** single coordinate `i in {0..18}` drops `d_EA` strictly from `11` to `10` (`[10, 10, ..., 10]`). Thus `object/eaqecc_n19_k2_d11_c9.tsv` is not a lengthening, ancilla-padding, or trivial edit of any shorter code.

## 3. Literature & V3R1T4S Check (`KNOWN` & `PROVED-HERE`)

### 3a. V3R1T4S Repository & Pull Requests (`PROVED-HERE`)

- `TROPHY_CASE.md` (53 rows across 6 families + 2 commitments) and `known-knowns/` contain **zero** entries for `codetables-eaqecc-qubit-gaps` (the only EAQECC directory in `known-knowns/` is `eaqecc-qutrit-codetables-gaps` for ternary `q = 3` codes).
- Querying all open, closed, and merged pull requests on `elder-plinius/V3R1T4S` (`gh pr list --state all` for `codetables-eaqecc-qubit-gaps`, `eaqecc`, `entanglement`, and `qubit.php`) returns `0` pull requests on `codetables-eaqecc-qubit-gaps` (all `18` EAQECC pull requests in repository history target `eaqecc-qutrit-codetables-gaps` over `GF(3)`).

### 3b. Literature & 2024-2026 Preprint Audit (`KNOWN` sources inspected directly)

1. **Y. Li, S. Zhu, and M. Shi (July 2026)**, *"Generalized Extended Codes with Applications in Entanglement-Assisted Qubit and Qutrit Codes"*, <https://arxiv.org/abs/2607.02170> (and supplementary tables at <https://github.com/yanglimath/SI-EAQECCs-from-GECs>): Constructs 267 binary EAQECCs for `n <= 40` via Hermitian hulls of generalized extended codes over `GF(4)`. At `n = 19`, the only binary entries are `[[19, 3, 13; 16]]_2` (`c = 16 > 9`) and `[[19, 12, 5; 7]]_2` (`d = 5`); across all 267 binary codes in the paper and repository, the highest distance propagating unconditionally to `(19, 2, 9)` is `8` (`[[18, 5, 8; 9]]_2`, `[[20, 5, 8; 9]]_2`).
2. **J.-H. Baek et al. (Oct 2026)**, *"Researcher-in-the-loop Evolutionary Discovery of entanglement-assisted quantum code families"*, <https://arxiv.org/abs/2610.41183> (and Magma verification archive at <https://github.com/LeGenAI/llm_guided_EAQECC_search/tree/arxiv-v1>): Proves the `k = 1` family `[[n, 1, n - 1; n - q - 1]]_q` (at `q = 2, n = 19`, `[[19, 1, 18; 16]]_2`, which has `k = 1` and `c = 16`) and releases 68 explicit `q = 2` code records, all with `n <= 14` (and `d <= 9` for all `k >= 2`).
3. **K. Abdukhalikov, D. Ho, and R. M. Shat (Sept 2026)**, *"New distance bounds for one-generator quasi-cyclic codes with applications to Hermitian LCD codes and entanglement-assisted quantum codes"*, <https://arxiv.org/abs/2609.31300>: Constructs quaternary Hermitian LCD codes yielding maximal-entanglement `[[n, k, d; n - k]]_2` codes of lengths `n >= 21` and `c >= 13` (smallest entry `[[21, 7, 11; 14]]_2`).
4. **R. Zengin and M. E. Koroglu (June 2026)**, *"QEC and EAQEC Codes from Hermitian Sums and Hulls of Cyclic Codes over `F_2 x (F_2 + v F_2)`"*, <https://arxiv.org/abs/2606.02137>: Matrix-product LCD constructions at lengths `n in {36, 60, 84, 108, 204, 252}` with `c >= 24`.
5. **Prior Hermitian-hull, algebraic-geometry, and unitary constructions (`KNOWN`)** — K. Guenda, S. Jitman, and T. A. Gulliver (*Des. Codes Cryptogr.* 86, 121-136, 2018), C. Galindo, F. Hernando, R. Matsumoto, and D. Ruano (*Quantum Inf. Process.* 18:116, 2019), G. Luo, L. Sok, M. F. Ezerman, and S. Ling (*IEEE Trans. Inf. Theory* 70(7), 4889-4904, 2024), R. Liu, S. Li, and M. Shi (*Adv. Math. Commun.* 19(2), 588-603, 2025, `n <= 13` quaternary hull building-up), and M. Mam, M. F. Ezerman, S. Ling, and L. Sok (*Quantum Inf. Process.* 24:178, 2025, quadratic-residue circulant unitary matrices): Web and arXiv searches confirm **no** published or claimed `[[19, 2, >=11; <=9]]_2` binary EAQECC.

### 3c. Why Classical Non-Degenerate Hermitian-Hull Searches Miss This Code (`PROVED-HERE`)

Under the trace-Hermitian / symplectic correspondence (`KNOWN`, Brun-Devetak-Hsieh 2006; Guenda-Jitman-Gulliver 2018), an `[[n, k, d; c]]_2` code at `(19, 2, 9)` comes from a `26`-dimensional stabilizer space `S` (`[19, 13]_4` code `C`) whose symplectic dual `S^{perp_s}` has `GF(2)`-dimension `n + k - c = 12` (`[19, 6]_4` dual `C^{perp_H}`) and isotropic radical `H_0 = S cap S^{perp_s}` of `GF(2)`-dimension `n - k - c = 8` (`l = 4` quaternary Hermitian hull `Hull_H(C)`).

Standard classical Hermitian-hull theorems and computer searches (`Guenda-Jitman-Gulliver 2018`, `Liu-Li-Shi 2025`, `Li-Zhu-Shi 2026`, `Abdukhalikov-Ho-Shat 2026`) certify quantum distance via the **non-degenerate (pure) bound** `d_EA >= d_s(S^{perp_s}) = d_H(C^{perp_H})`, taking the minimum weight over all `4,095` nonzero vectors of `S^{perp_s}` without quotienting out the `255` nonzero isotropic stabilizer vectors in `H_0 = S cap S^{perp_s}`. In `object/eaqecc_n19_k2_d11_c9.tsv`, exact enumeration of `S^{perp_s}` (`PROVED-HERE`) gives:

- **Isotropic radical `S cap S^{perp_s}` (`256` vectors)**: weight distribution `(0: 1, 4: 6, 8: 21, 10: 12, 12: 48, 14: 84, 16: 60, 18: 24)` -> minimum nonzero weight `d(S cap S^{perp_s}) = 4` (`39` nonzero stabilizer vectors of weight `< 11`).
- **Logical cosets `S^{perp_s} \ S` (`3,840` vectors)**: weight distribution `(11: 192, 12: 528, 13: 408, 14: 1152, 15: 552, 16: 528, 17: 360, 18: 96, 19: 24)` -> exact non-catalytic minimum distance `d_EA = 11`.

Because `d(S^{perp_s}) = 4 < 11 = d_EA`, every classical non-degenerate Hermitian-hull filter evaluates the underlying `[19, 6]_4` dual code as having classical minimum distance `4` (worse even than the unassisted `[[19, 2, 6; 0]]_2` code) and discards it immediately. Furthermore, in any pure `[19, 6, >=11]_4` candidate with a `4`-dimensional Hermitian hull `H_0`, Hermitian self-orthogonality over `GF(4)` forces every codeword of `H_0` to have even Hamming weight, which would require `H_0` itself to be a `[19, 4, >=12]_4` code simultaneously with all `3,840` coset vectors having weight `>= 11`; exploiting degeneracy (`d(H_0) = 4` while `wt(S^{perp_s} \ S) >= 11`) bypasses that bottleneck cleanly.

## Verdict

The explicit degenerate EAQECC `[[19, 2, 11; 9]]_2` in `object/eaqecc_n19_k2_d11_c9.tsv` strictly improves the live `codetables.de` lower bound `d_lower = 10` (`[[19, 2, 10-17; 9]]_2`, re-fetched `2026-11-10T20:08:34Z`, HTTP `200`, SHA-256 `c84dea1ab3b3657e268462019569f0bf6b3cb15872ae0675d47ae9ae62536e6a`), is not implied by any propagation rule from any cell in the live table or recent 2024-2026 literature, and has no prior match in `TROPHY_CASE.md`, `known-knowns/`, or `V3R1T4S` pull requests.

pass: true
