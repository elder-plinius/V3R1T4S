# Panel Report — REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Quoted Definition and Claim

From `claim/CLAIM.md`:

- **Claim**:
  "the file design_94_13_5.txt is a (94,13,5) covering design with 125184 blocks, strictly fewer than the coveringrepository.com (v,k,t) archive value 129203 and the LJCR value 129337 for C(94,13,5)."

- **Success criterion (verbatim from `claim/CLAIM.md`)**:
  "Success means b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively), where b is STRICTLY SMALLER (direction: min) than EVERY one of the following, each re-fetched at verification time: the live coveringrepository.com plain (v,k,t) value (m=t section, https://coveringrepository.com/), the live LJCR value (https://dmgordon.org/covering-designs/), and the dmgordo/LJCR GitHub/Zenodo value. It must also beat any value found by grepping GitHub/arXiv for that (v,k,t) over the last 6 months, including unverified hobbyist claims (e.g. thebrockchain/covering-designs: C(28,13,4) <= 53, C(32,13,4) <= 95). If a live table cannot be fetched, the claim is 'PENDING TABLE CHECK', not a record. Parameters must be within v <= 99, k <= 25, t <= 8, and b must be at least the Schonheim bound L(v,k,t); going below it means a bug. Same-day claim only if C(v,t) <= 5e9, so the exhaustive coverage check runs on a laptop; larger cases are logged as 'PENDING chunked exhaustive check' and claimed only after that full check completes."

## 2. Independent Checker Construction and Self-Tests

Before inspecting `claim/author_checker_cover_check.py`, a standalone exhaustive checker `panel/reproduce_work/indep_reproduce_check.py` was written directly from the mathematical definition of a $(v, k, t)$ covering design:

1. **Parameter & Schonheim bound derivation**:
   - Checks $1 \le t \le k \le v$, $v \le 99$, $k \le 25$, $t \le 8$, and $\binom{v}{t} \le 5 \times 10^9$.
   - Re-derives the recursive Schonheim lower bound $L(v,k,t) = \lceil \frac{v}{k} L(v-1, k-1, t-1) \rceil$ with $L(v-t, k-t, 0) = 1$:
     - $L(90, 9, 1) = \lceil 90 / 9 \rceil = 10$
     - $L(91, 10, 2) = \lceil 91 \times 10 / 10 \rceil = 91$
     - $L(92, 11, 3) = \lceil 92 \times 91 / 11 \rceil = \lceil 8372 / 11 \rceil = 762$
     - $L(93, 12, 4) = \lceil 93 \times 762 / 12 \rceil = \lceil 70866 / 12 \rceil = 5906$
     - $L(94, 13, 5) = \lceil 94 \times 5906 / 13 \rceil = \lceil 555164 / 13 \rceil = 42705$
2. **Block structural validation**:
   - Verifies that every block has exactly $k = 13$ tokens, all integers in `0..93`, with no repeated points inside any block, and that all $b = 125184$ canonical sorted blocks are mutually distinct.
3. **Exhaustive coverage check**:
   - Allocates a `uint8` array of length $\binom{94}{5} = 54,891,018$ (~54.9 MB).
   - Maps every $5$-subset $(x_0, x_1, x_2, x_3, x_4)$ in increasing order ($0 \le x_0 \lt x_1 \lt x_2 \lt x_3 \lt x_4 \lt 94$) to its unique colexicographic combinadic rank $\sum_{j=0}^{4} \binom{x_j}{j+1} \in \{0, \dots, 54891017\}$.
   - Iterates over all $\binom{13}{5} = 1287$ index 5-tuples within a 13-block across all $125,184$ blocks ($125184 \times 1287 = 161,111,808$ subset incidences) and marks each rank as covered.

### Self-Test Results (Positive & Negative Controls)

Executed automatically at the start of `panel/reproduce_work/indep_reproduce_check.py`:

- `[SELF-TEST 0]` Combinadic bijection check on $\binom{9}{4} = 126$: verified that the 126 4-subsets map bijectively to `0..125` (`PASS`).
- `[SELF-TEST 1]` Positive control — Fano plane $(7,3,2)$ with $b = 7$ blocks: `uncovered=0`, `L=7` (`PASS`).
- `[SELF-TEST 2]` Negative control — 6-block incomplete Fano plane: `uncovered=3`, below Schonheim bound (`PASS`, rejected).
- `[SELF-TEST 3]` Negative control — 7-block incomplete design (7th block replaced by `[0, 1, 2]`): `uncovered=2` (`PASS`, rejected).
- `[SELF-TEST 4]` Negative control — 8-block design with duplicate block `[0, 1, 3]`: `distinct=7 != b=8` (`PASS`, rejected).
- `[SELF-TEST 5]` Negative control — block `[6, 0, 0]` with repeated point: rejected (`Block 6 has repeated points: [6, 0, 0]`).
- `[SELF-TEST 6]` Negative control — block `[6, 0, 7]` with out-of-range point `7` for $v=7$: rejected (`Block 6 has point 7 out of range 0..6`).

## 3. Independent Verification of `claim/design_94_13_5.txt` (Two Deterministic Runs)

Command executed twice:
```
python3 panel/reproduce_work/indep_reproduce_check.py 94 13 5 claim/design_94_13_5.txt
```

Output from Run 1:
```
file_sha256=e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908
params=(94,13,5)
lines=125184
blocks=125184
distinct_blocks=125184
schonheim_bound=42705
total_t_subsets=54891018
covered=54891018
uncovered=0
elapsed_sec=2.482
peak_rss_mb=162.50
INDEP_CHECK: PASS
```

Output from Run 2:
```
file_sha256=e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908
params=(94,13,5)
lines=125184
blocks=125184
distinct_blocks=125184
schonheim_bound=42705
total_t_subsets=54891018
covered=54891018
uncovered=0
elapsed_sec=2.652
peak_rss_mb=160.27
INDEP_CHECK: PASS
```

Both runs are deterministic and identical in all counts and hashes, completing in ~2.5–2.7 seconds with ~0.16 GB peak RSS.

## 4. Inspection and Execution of Author's Checker & Saved Table Archive

After completing the independent checker and both runs, `claim/author_checker_cover_check.py` was inspected and executed as specified in `claim/REPRODUCE.md`:

```
python3 claim/author_checker_cover_check.py 94 13 5 claim/design_94_13_5.txt
```

Output:
```
file=claim/design_94_13_5.txt sha256=e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908 v=94 k=13 t=5
blocks=125184
distinct=125184
base=0
schonheim=42705
C_v_t=54891018
uncovered=0
COVER_CHECK: PASS
```

Saved archive `claim/cr_archive_vkt.txt` verification:
- `sha256`: `78bf5453858b476b90eeebd8ee8a35454e5f31866dd5f629934083ca0cd9bee3` (matches `claim/CLAIM.md`).
- Row for `(94, 13, 5)` (`m = 5`): `94	13	05	05		129203`.
- The claimed block count $125,184$ is strictly smaller than the `coveringrepository.com` value $129,203$ (by $4,019$ blocks) and strictly smaller than the LJCR value $129,337$ (by $4,153$ blocks), while satisfying $125,184 \ge L(94, 13, 5) = 42,705$.

pass: true
