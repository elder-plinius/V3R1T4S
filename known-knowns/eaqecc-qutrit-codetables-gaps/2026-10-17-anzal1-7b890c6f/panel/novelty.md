context: subagent

# Novelty Skeptic Report — `eaqecc-qutrit-codetables-gaps` (`[[14, 3, 8; 5]]_3`)

## 1. Claimed Object and Target Summary
- **Claim file:** `claim/CLAIM.md`
- **Object file:** `claim/object/qutrit_14_3_8_5.json` (`sha256: 7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5`)
- **Target ID:** `eaqecc-qutrit-codetables-gaps`
- **Claimed parameters:** Pure entanglement-assisted qutrit quantum error-correcting code `[[14, 3, 8; 5]]_3` (`n = 14, k = 3, d = 8, c = 5, s = 16`) given by an explicit `16 x 28` symplectic generator matrix `S` over `GF(3)` and its `6 x 14` dual generator matrix `H9` over `GF(9)`.

## 2. Single Honest Fetch of the Primary Status Source
- **URL:** `https://eaqecc.codetables.de/qutrit.php`
- **Fetched (UTC):** `2026-10-17T05:40:20Z` (single request via `curl -sS -A "V3R1T4S/1.0"`, no retries)
- **HTTP status:** `200`
- **Saved file:** `claim/data/qutrit.php` (`sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`)
- **Table footer timestamp:** `Last change: 10.07.2025`

### Exact Cell Quote on the Live Table
For `(n=14, k=3, c=5)`, the live table `https://eaqecc.codetables.de/qutrit.php` lists:
```html
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[19,3,7;0]] from codetables.de">[[14,3,7-10;5]]<sub>3</sub></TD>
```
- **Live table value for `(n=14, k=3, c=5)`:** `7-10`, so `d_lower = 7, d_upper = 10`.
- **Claimed value:** `d = 8`.
- **Comparison:** `d = 8 > d_lower = 7` and `d = 8 <= d_upper = 10` (strict improvement of `+1` in minimum distance over the live table lower bound).

### Full `(n=14, k=3)` Cell and Neighboring Cells on the Live Table
All entries listed in the `(n=14, k=3)` cell of `https://eaqecc.codetables.de/qutrit.php`:
- `c = 0`: `[[14,3,5-6;0]]_3` (`from codetables.de`)
- `c = 1`: `[[14,3,6-7;1]]_3` (`increasing dimension of [[14,2,6;0]] from codetables.de`)
- `c = 5`: `[[14,3,7-10;5]]_3` (`reducing length of [[19,3,7;0]] from codetables.de`)
- `c = 6`: `[[14,3,8-11;6]]_3` (`subcode of [[14,4,8;6]] quantum shortening of [[16,2,10;6]] from arXiv:2207.05647`)
- `c = 7`: `[[14,3,9-11;7]]_3` (`increasing dimension of [[14,2,9;6]] from arXiv:2207.05647`)
- `c = 10`: `[[14,3,10-11;10]]_3` (`subcode of [[14,4,10;10]] quantum shortening of [[16,2,12;10]] increasing dimension of [[16,1,12;9]] from arXiv:2207.05647`)
- `c = 11`: `[[14,3,11-12;11]]_3` (`quantum shortening of [[15,2,12;11]] increasing dimension of [[15,0,12;9]] from arXiv:2207.05647`)

In addition to strictly improving `d_lower` at `(n=14, k=3, c=5)` from `7` to `8`, `[[14, 3, 8; 5]]_3` also strictly reduces the entanglement required for `(n=14, k=3, d=8)` from `c = 6` (`[[14,3,8-11;6]]_3`) to `c = 5`.

## 3. Check Against All 8 Table Propagation Rules
We checked all 3,888 entries of `claim/data/qutrit.php` to verify that `[[14, 3, 8; 5]]_3` is not implied by any of the 8 propagation rules used by Grassl and Luo et al. (`arXiv:2207.05647`, Section 6):
1. **Rule 1 — Lengthening (`[[n-1, k, d; c]]_3 -> [[n, k, d; c]]_3`):** Would require `[[13, 3, d >= 8; c <= 5]]_3`. On the live table, `(n=13, k=3)` has `[[13,3,7-9;5]]_3` (`d_lower = 7`) and `[[13,3,8-10;6]]_3` (`c = 6`).
2. **Rule 2 — Subcode (`[[n, k+1, d; c]]_3 -> [[n, k, d; c]]_3`):** Would require `[[14, 4, d >= 8; c <= 5]]_3`. On the live table, `(n=14, k=4)` has `[[14,4,7-9;5]]_3` (`d_lower = 7`) and `[[14,4,8-9;6]]_3` (`c = 6`).
3. **Rule 3 — Smaller distance (`[[n, k, d+1; c]]_3 -> [[n, k, d; c]]_3`):** At `(n=14, k=3, c <= 5)`, the largest `d_lower` is `7`.
4. **Rule 4 — More entanglement (`[[n, k, d; c-1]]_3 -> [[n, k, d; c]]_3`):** At `(n=14, k=3)` with `c <= 4`, the largest `d_lower` is `6` (`[[14,3,6-7;1]]_3`).
5. **Rule 5 — Puncturing (`[[n+1, k, d+1; c]]_3 -> [[n, k, d; c]]_3`):** Would require `[[15, 3, d >= 9; c <= 5]]_3`. On the live table, `(n=15, k=3)` has `[[15,3,8-11;5]]_3` (`d_lower = 8`, which punctures to `d = 7`) and `[[15,3,9-11;6]]_3` (`c = 6`).
6. **Rule 6 — Increasing dimension of a pure Hermitian-constructed code (`[[n, k-1, d; c-1]]_3 -> [[n, k, d; c]]_3`):** Preserves `c - k = 2` at `n = 14`. For `k < 3` at `n = 14`, the table has `[[14,0,7-9;2]]_3` (`d_lower = 7`) and `[[14,0,8-10;4]]_3` (`c - k = 4`, which gives `c = 7` at `k = 3`). Note that `[[14,2,8-11;2]]_3` (`bgcolor="#ffff00"`, `title="using teleportation"`) is an impure classical-teleportation scheme (`arXiv:2007.01249`), not a pure code from the Hermitian construction, so Rule 6 does not apply to it (and is never applied to `using teleportation` entries anywhere on `qutrit.php`).
7. **Rule 7 — Length reduction (`[[n+1, k, d; c-1]]_3 -> [[n, k, d; c]]_3`):** Would require `[[15, 3, d >= 8; c <= 4]]_3`. On the live table, `(n=15, k=3)` has `[[15,3,7-10;3]]_3` (`d_lower = 7`) and `[[15,3,8-11;5]]_3` (`c = 5`, which reduces to `c = 6` at `n = 14`).
8. **Rule 8 — Quantum shortening of a pure code (`[[n+1, k-1, d+1; c]]_3 -> [[n, k, d; c]]_3`):** Would require a pure `[[15, 2, d >= 9; c <= 5]]_3` code. On the live table, `(n=15, k=2)` has `[[15,2,6;0]]_3` (`d = 6`), `[[15,2,10-13;8]]_3` (`c = 8`), and the impure teleportation entry `[[15,2,9-12;2]]_3` (to which quantum shortening of pure codes does not apply).

## 4. Literature Search (Last 24 Months, 2024–2026)
We searched arXiv and recent coding-theory literature from 2024–2026 for qutrit EAQECCs, `GF(9)` Hermitian-hull codes, and `GF(3)` symplectic-hull codes:
- **Y. Li, M. F. Ezerman, S. Li et al., "Generalized Extended Codes with Applications in Entanglement-Assisted Qubit and Qutrit Codes", `arXiv:2607.02170` (July 2026)** and its supplementary repository (`yanglimath/SI-EAQECCs-from-GECs`, `SI-EAQECCs_Table_V_ternary.tsv` and `SI-EAQECCs_Table_VII_literature_equal.tsv`): This paper compares against `https://eaqecc.codetables.de/qutrit.php` (accessed June 15, 2026) and all recent literature improvements, reporting 14 new/improved qutrit EAQECCs for `7 <= n <= 25` (`[[7,1,7;6]]_3`, `[[8,0,8;6]]_3`, `[[8,1,8;7]]_3`, `[[13,3,7;4]]_3`, `[[17,2,15;15]]_3`, `[[18,2,16;16]]_3`, `[[19,2,17;17]]_3`, `[[19,3,15;16]]_3`, `[[21,2,18;19]]_3`, `[[22,2,19;20]]_3`, `[[23,2,20;21]]_3`, `[[24,2,21;22]]_3`, `[[25,2,22;23]]_3`, `[[25,3,20;22]]_3`) plus 5 qutrit EAQECCs from 2024–2025 literature (`[[7,0,7;5]]_3`, `[[7,2,5;3]]_3`, `[[9,0,9;7]]_3`, `[[15,2,13;13]]_3`, `[[16,2,14;14]]_3` from Cao–Li–Zhu *IEEE Trans. Inf. Theory* 71(10):7649–7669, Oct 2025; Liu–Li–Shi *Adv. Math. Commun.* 19(2):588–603, 2025; Li–Li–Guan–Song *Int. J. Theor. Phys.* 63(9):221, 2024; and Li–Zhu *Discrete Math.* 347(2):113760, Feb 2024). None of these 19 qutrit codes has `n = 14` or implies `[[14, 3, 8; 5]]_3` via propagation rules (note that `[[13, 3, 7; 4]]_3` has `d = 7`).
- **K. Abdukhalikov, S. Gupta, and D. Ho, "Hull Variation in Symplectic Linear Codes", `arXiv:2610.15535` (Oct 2026):** Studies symplectic hull variation under monomial/GL-equivalence and gives graph-based self-dual examples at lengths `2n in {12, 20, 24, 30}`; no length `n = 14` (`2n = 28`) code or `[[14, 3, 8; 5]]_3` code is constructed.
- **J. Fan, W. Cheng, G. Luo, Z. Li, and M. Cao, "Entanglement-assisted concatenated quantum codes: Parameters and asymptotic performance", `arXiv:2501.04921` (Jan 2025):** Constructs binary concatenated EAQECCs (`q = 2`); no qutrit (`q = 3`) codes are constructed.
- **H. Matsui and K. Kaneko, "Entanglement-assisted quantum error-correcting codes via quasi-cyclic codes with complementary duals", *Des. Codes Cryptogr.* 93:3575–3591 (2025)** and **Y. Li and S. Zhu, "On symplectic hulls of linear codes and related applications", *J. Appl. Math. Comput.* 70(3):2603–2622 (2024):** Neither constructs `[[14, 3, d >= 8; c <= 5]]_3` or a `[14, 6, 8]_9` Hermitian self-orthogonal code.
- **G. Luo, M. F. Ezerman, M. Grassl, and S. Ling, `arXiv:2207.05647` / *Quantum Inf. Process.* 23:4 (2024):** Lists only `[[14, 8, 3; 0]]_3`, `[[14, 5, 6; 3]]_3`, `[[14, 2, 9; 6]]_3`, and `[[14, 0, 14; 12]]_3` at `n = 14` in Table 2.

## 5. Check of `TROPHY_CASE.md`, `known-knowns/`, and Pull Requests
- **`TROPHY_CASE.md` and `known-knowns/`:** Checked all 53 rows of `TROPHY_CASE.md` and all 18 directories in `known-knowns/`. There are no entries for `eaqecc-qutrit-codetables-gaps` or qutrit EAQECCs.
- **Pull requests on `elder-plinius/V3R1T4S`:** Checked the latest 100 pull requests (`gh pr list --repo elder-plinius/V3R1T4S --state all --limit 100`) as well as targeted searches for `eaqecc`, `qutrit`, and `codetables`. Existing `codetables` PRs concern `codetables-qubit-upper-bounds-n101-256` and `codetables-binary-linear`; there are zero open, merged, or closed pull requests on `eaqecc-qutrit-codetables-gaps` or `[[14, 3, 8; 5]]_3`.

## 6. Verdict
The claimed pure qutrit EAQECC `[[14, 3, 8; 5]]_3` strictly beats the live table lower bound `d_lower = 7` (`7-10`) at `(n=14, k=3, c=5)` on `https://eaqecc.codetables.de/qutrit.php`, is not implied by any propagation rule from known table or literature entries, and does not appear in the last 24 months of literature, `TROPHY_CASE.md`, `known-knowns/`, or any pull request on `elder-plinius/V3R1T4S`.

pass: true
