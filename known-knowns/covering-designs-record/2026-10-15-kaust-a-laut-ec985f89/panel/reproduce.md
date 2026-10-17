role: REPRODUCE
context: subagent (fresh context that saw only claim/)

# Reproduction Audit for C(41, 12, 5) <= 2207

## 1. Scope and Fresh-Context Protocol
Only the files inside `claim/` were read:
- `claim/CLAIM.md`
- `claim/REPRODUCE.md`
- `claim/C41_12_5_2207blocks.txt`
- `claim/table_record/coveringrepository_download_archive_vkt.html`
- `claim/table_record/ljcr_zenodo_v1.2_C41_12_5.json`
- `claim/table_record/ljcr_github_C41_12_5.json`

All verification scripts and logs were written to `panel/work/reproduce/`.

## 2. Standalone Checker (`panel/work/reproduce/check_cover.py`) and Self-Test
Before running the commands in `claim/REPRODUCE.md`, an independent checker `panel/work/reproduce/check_cover.py` was written from the covering design definition and success criteria quoted in `claim/CLAIM.md` using only the Python standard library (`sys`, `hashlib`, `math`, `itertools`, `time`).

The checker validates:
1. Parameter bounds (`v <= 99`, `k <= 25`, `t <= 8`, and `C(v, t) <= 5e9`).
2. Exact block count `b` (and match with expected `b = 2207`).
3. Every line has exactly `k` integer tokens in `1..v` with no repeated points (`len(frozenset(pts)) == k`).
4. All `b` blocks are pairwise distinct (`len(set(blocks)) == b`).
5. Schonheim lower bound `L(v, k, t)` is computed from the iterated ceiling formula and `b >= L(v, k, t)` is verified.
6. Exhaustive `t`-subset coverage using two independent methods:
   - Union of all `C(k, t)` subsets generated from the `b` blocks, checking `len(covered_set) == C(v, t)` and recording multiplicity statistics (`min_multiplicity`, `max_multiplicity`).
   - Exhaustive iteration over all `C(v, t)` bitmasks, checking that every `t`-subset bitmask is a submask of at least one block bitmask.

### Self-Test Results (`panel/work/reproduce/selftest.txt`)
Command: `python panel/work/reproduce/check_cover.py --selftest`
- Valid Fano plane `(7, 3, 2)` with 7 blocks: **PASS** (`b = 7`, `unique_blocks = 7`, `schonheim_bound = 7`, `total_t_subsets = 21`, `covered_t_subsets = 21`, `uncovered_t_subsets = 0`, `min_multiplicity = 1`, `max_multiplicity = 1`).
- Negative 1 (missing block, 6 blocks): **PASS (detected FAIL)** (`Block count 6 is below Schonheim bound L(7,3,2) = 7`).
- Negative 1b (incomplete 7-block cover with 7 distinct blocks): **PASS (detected FAIL)** (`Uncovered 2-subsets: 2 of 21 (first missing: (1, 7))`).
- Negative 2 (repeated point `1 2 2`): **PASS (detected FAIL)** (`Line 1: repeated point in block [1, 2, 2]`).
- Negative 3 (out-of-range point `8 > 7`): **PASS (detected FAIL)** (`Line 1: point 8 out of range 1..7`).
- Negative 4 (out-of-range point `0 < 1`): **PASS (detected FAIL)** (`Line 1: point 0 out of range 1..7`).
- Negative 5 (duplicate block `4 2 1` duplicating `1 2 4`): **PASS (detected FAIL)** (`Duplicate blocks detected: 7 total vs 6 unique`).
- Negative 6 (wrong block size, 4 tokens): **PASS (detected FAIL)** (`Line 1: expected 3 tokens, got 4`).

## 3. Two Independent Runs on `claim/C41_12_5_2207blocks.txt`
Command (run twice):
`python panel/work/reproduce/check_cover.py claim/C41_12_5_2207blocks.txt 41 12 5 2207`

Outputs saved in `panel/work/reproduce/run1.txt` (87.152 s) and `panel/work/reproduce/run2.txt` (90.785 s) are identical in all verification fields:
- `file_bytes`: `74496`
- `sha256`: `ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa` (matches `claim/CLAIM.md` and `claim/REPRODUCE.md`)
- `params_in_range`: `v=41<=99 (True), k=12<=25 (True), t=5<=8 (True)`
- `v`: `41`, `k`: `12`, `t`: `5`
- `b`: `2207`
- `unique_blocks`: `2207`
- `schonheim_bound`: `1070` (`2207 >= 1070`, and `2207 >= 1121` LJCR lower bound)
- `total_t_subsets`: `749398` (`C(41, 5) = 749,398 <= 5e9`)
- `covered_t_subsets`: `749398`
- `uncovered_t_subsets`: `0`
- `min_multiplicity`: `1`
- `max_multiplicity`: `51`
- `RESULT`: `PASS`

## 4. Audit of `claim/REPRODUCE.md` and `claim/table_record/`
1. **Step 1 (SHA-256 hash)**:
   Running the command in `claim/REPRODUCE.md` output `ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa`, matching the claimed digest.
2. **Step 2 (Exhaustive coverage one-liner)**:
   The mathematical logic of Step 2 in `claim/REPRODUCE.md` is sound, though its inner generator expression `(m & sum(1<<p for p in T))==sum(1<<p for p in T) for m in M` recomputes `sum(1<<p for p in T)` twice per block inside the loop over `M` (roughly `1.5e9` bit-shifts across `749,398` subsets, taking over 19 minutes in pure CPython). Hoisting the `T` bitmask outside `for m in M` (as done in `panel/work/reproduce/check_cover.py`) completes the exact same bitmask check in ~87 seconds and confirms `blocks 2207 missing 0`.
3. **Step 3 (Schonheim bound)**:
   Verified `L(41, 12, 5) = ceil(41/12 * ceil(40/11 * ceil(39/10 * ceil(38/9 * ceil(37/8))))) = ceil(41/12 * ceil(40/11 * ceil(39/10 * ceil(38/9 * 5)))) = ceil(41/12 * ceil(40/11 * ceil(39/10 * 22))) = ceil(41/12 * ceil(40/11 * 86)) = ceil(41/12 * 313) = 1070`. `2207 >= 1070`.
4. **Step 4 (`claim/table_record/` verification)**:
   - `claim/table_record/coveringrepository_download_archive_vkt.html`: verified `171741` bytes, sha256 `85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17`, matching `claim/CLAIM.md`. The row for `(41, 12, 05, 05)` is `41\t12\t05\t05\t\t2244` (`2207 < 2244` by 37 blocks).
   - `claim/table_record/ljcr_zenodo_v1.2_C41_12_5.json`: lists `"size": 2245`, `"low_bd": 1121` (`2207 < 2245` by 38 blocks).
   - `claim/table_record/ljcr_github_C41_12_5.json`: lists `"size": 2429`, `"low_bd": 1121` (`2207 < 2429` by 222 blocks).

pass: true
