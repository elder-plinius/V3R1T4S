# Panel Report — CRITERION

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: covering-designs-record
object: claim/design_94_13_5.txt (sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908)
confirmed_scope: An explicit (94,13,5) covering design in claim/design_94_13_5.txt (sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908) with 125,184 distinct 13-element blocks over {0..93}, exhaustively verified across all 54,891,018 5-subsets of a 94-set with zero uncovered 5-subsets, strictly improving on the Covering Repository plain (v,k,t) record of 129,203 (by 4,019 blocks) and the La Jolla Covering Repository record of 129,337 (by 4,153 blocks) for C(94,13,5).

## 1. Clause-by-Clause Audit Against Verbatim Success Criterion

Verification was performed independently by writing and executing `panel/criterion_work/verify_criterion.py` alongside `claim/author_checker_cover_check.py`.

1. **Block count and structure (`b blocks, each a k-subset of a v-set (no repeated points)`):**
   - `claim/design_94_13_5.txt` (`sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`) has `125,184` lines (`125,184` non-empty lines).
   - Every line parses as exactly `k = 13` distinct integers in `0..93` (`v = 94`), with zero repeated points within any block and `125,184` distinct sorted blocks (`0` duplicate blocks).
   - Point degree across the `94` points ranges from `min = 16,701` to `max = 20,220`, summing to `1,627,392 = 125,184 * 13`.

2. **Exhaustive $t$-subset coverage (`covering every t-subset (checked exhaustively)`):**
   - Total 5-subsets of `{0..93}`: $\binom{94}{5} = 54,891,018$. Each 13-block contributes $\binom{13}{5} = 1,287$ 5-subsets, for $125,184 \times 1,287 = 161,111,808$ total block-subset incidences.
   - Using an independent **lexicographic** ranking bijection (`lex_rank(c_0..c_4) = 54891017 - sum_{i=0..4} C(93 - c_i, 5 - i)`, verified at endpoints `lex_rank(0,1,2,3,4) = 0` and `lex_rank(89,90,91,92,93) = 54891017`, distinct from the colex ranking in `claim/author_checker_cover_check.py`), `panel/criterion_work/verify_criterion.py` computed exact coverage multiplicity across all `54,891,018` 5-subsets:
     - `covered = 54,891,018 / 54,891,018`, `uncovered = 0`.
     - Coverage multiplicity distribution: `min = 1`, `max = 461`, `mean = 2.935122` (`161,111,808 / 54,891,018`).
     - Histogram for counts `0..9`: `{0: 0, 1: 38203970, 2: 6751602, 3: 1597562, 4: 395750, 5: 682200, 6: 363732, 7: 506032, 8: 333634, 9: 1071020}`.
   - Running `claim/author_checker_cover_check.py 94 13 5 claim/design_94_13_5.txt` independently returned `blocks=125184`, `distinct=125184`, `uncovered=0`, `COVER_CHECK: PASS` (exit code `0`).

3. **Strict improvement over all live tables and repositories (`b is STRICTLY SMALLER (direction: min)`):**
   - **coveringrepository.com plain `(v,k,t)` table (`m = t` section):** `claim/cr_archive_vkt.txt` (`sha256 78bf5453858b476b90eeebd8ee8a35454e5f31866dd5f629934083ca0cd9bee3`, `9,629` lines) has at line `3648` the entry `94	13	05	05		129203`. Our `b = 125,184` is strictly smaller than `129,203` (by `4,019` blocks, or `3.111%`).
   - **La Jolla Covering Repository (LJCR live site & dmgordo/LJCR Zenodo records 19472830 / 19735294):** `C(94,13,5) = 129,337`. Our `b = 125,184` is strictly smaller than `129,337` (by `4,153` blocks, or `3.211%`).
   - **GitHub / arXiv over the last 6 months (including hobbyist repos such as `thebrockchain/covering-designs`):** Web searches across GitHub and arXiv for `(94,13,5)` covering designs found no competing bound or construction for `(94,13,5)` (`thebrockchain/covering-designs` covers small $t=4$ cells `C(28,13,4)` and `C(32,13,4)`).

4. **Parameter bounds ($v \le 99, k \le 25, t \le 8$):**
   - $v = 94 \le 99$ (True), $k = 13 \le 25$ (True), $t = 5 \le 8$ (True).

5. **Schonheim lower bound ($b \ge L(v,k,t)$):**
   - Iterated ceiling computation:
     - $L(90,9,1) = \lceil 90/9 \rceil = 10$
     - $L(91,10,2) = \lceil 91 \times 10 / 10 \rceil = 91$
     - $L(92,11,3) = \lceil 92 \times 91 / 11 \rceil = \lceil 8372 / 11 \rceil = 762$
     - $L(93,12,4) = \lceil 93 \times 762 / 12 \rceil = \lceil 70866 / 12 \rceil = 5906$
     - $L(94,13,5) = \lceil 94 \times 5906 / 13 \rceil = \lceil 555164 / 13 \rceil = 42705$
   - $b = 125,184 \ge 42,705$ (True).

6. **Same-day exhaustive check condition ($C(v,t) \le 5 \times 10^9$):**
   - $\binom{94}{5} = 54,891,018 \le 5,000,000,000$ (True; approximately `1.098%` of the threshold, running in a few seconds on a single CPU core).

## 2. Null Model Exemption & Checker Sensitivity / Deletion Controls

- **Why a statistical 400-control null test does not apply:** The claim is a deterministic, finite combinatorial certificate (`125,184` explicit blocks) verified exhaustively over the entire finite universe of `54,891,018` 5-subsets against a deterministic integer upper bound (`129,203`), with zero stochastic estimation or sampling variance.
- **1-Minimality (Irredundancy) & Deletion Controls:**
  - `panel/criterion_work/verify_criterion.py` counted the number of uniquely covered 5-subsets (`count == 1`) inside each of the `125,184` blocks. Exactly `0` blocks are redundant (`redundant_blocks = 0`): every single block in `claim/design_94_13_5.txt` uniquely covers between `15` (block `22173`: `[44, 45, 48, 51, 52, 54, 55, 56, 59, 60, 85, 90, 91]`) and `510` (block `24826`: `[0, 9, 18, 27, 36, 51, 63, 66, 67, 68, 71, 83, 92]`) 5-subsets.
  - **Deletion Control 1 (remove block `0`):** Block `0` (`[47, 48, 49, 50, 51, 60, 62, 65, 69, 71, 83, 85, 86]`) uniquely covers `425` 5-subsets. Deleting line 1 (`125,183` blocks, `sha256 acbec0887d73d1080d54553c72bbb03944237be6f7f4aafd3f57ff5e13187891`) causes both `panel/criterion_work/verify_criterion.py` and `claim/author_checker_cover_check.py` to report `uncovered=425` (`COVER_CHECK: FAIL 425 uncovered t-subsets`, exit code `1`).
  - **Deletion Control 2 (remove least-essential block `22173`):** Deleting block `22173` (`125,183` blocks) leaves `uncovered = 15` (strictly positive).

pass: true
