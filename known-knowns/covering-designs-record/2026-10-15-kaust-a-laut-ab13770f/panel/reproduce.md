role: REPRODUCE
context: subagent (fresh context that saw only claim/)

# REPRODUCE Verdict for C(53,20,3) <= 34

## 1. Scope and Fresh-Context Protocol
- Inspected exclusively the files inside `claim/`:
  - `claim/CLAIM.md`
  - `claim/REPRODUCE.md`
  - `claim/C53_20_3_34blocks.txt`
  - `claim/table_record/coveringrepository_download_archive_vkt.html`
  - `claim/table_record/ljcr_zenodo_v1.2_C53_20_3.json`
  - `claim/table_record/ljcr_github_C53_20_3.json`
- All independent verification scripts and outputs were written to `panel/work/reproduce/`.

## 2. Standalone Verifier (`panel/work/reproduce/check_cover.py`)
Before executing the commands in `claim/REPRODUCE.md`, a standalone verifier (`panel/work/reproduce/check_cover.py`) was written from scratch using only the Python standard library and the mathematical definition quoted in `claim/CLAIM.md`:
- Parses each non-empty line as space-separated integers.
- Verifies that every block has exactly `k` integers, no repeated elements (`len(set(pts)) == k`), and every point lies in `1..v`.
- Verifies that the number of blocks equals `b` and that all `b` blocks are pairwise distinct (`len(set(raw_blocks)) == b`).
- Computes the Schonheim lower bound `L(v,k,t)` and checks `b >= L(v,k,t)`.
- Exhaustively iterates over all `C(v,t)` `t`-subsets of `{1..v}` using bitmask containment (`(block_mask & t_mask) == t_mask`) and verifies that `0` `t`-subsets are uncovered.

### Self-Tests on `(7,3,2)` Fano Plane
Executed `python panel/work/reproduce/check_cover.py --self-test`:
- **Valid `(7,3,2)` Fano plane (7 blocks)**: `PASS` (`v=7, k=3, t=2, b=7, unique_blocks=7, total_t_subsets=21, uncovered=0, schonheim_bound=7`).
- **Missing block (6 blocks)**: `FAIL` as expected (`Block count 6 is below Schonheim bound L(7,3,2) = 7`).
- **Uncovered subset with 7 distinct blocks**: `FAIL` as expected (`Uncovered 2-subsets: 2 / 21 (first: (1, 7))`).
- **Repeated point in a block (`1 2 2`)**: `FAIL` as expected (`Line 1: repeated point in block [1, 2, 2]`).
- **Out-of-range point high (`1 2 8`)**: `FAIL` as expected (`Line 1: point 8 out of range 1..7`).
- **Out-of-range point low (`0 2 4`)**: `FAIL` as expected (`Line 1: point 0 out of range 1..7`).
- **Duplicate block**: `FAIL` as expected (`Duplicate blocks detected: 7 total vs 6 unique`).

## 3. Independent Two-Run Verification of `claim/C53_20_3_34blocks.txt`
Executed `python panel/work/reproduce/check_cover.py claim/C53_20_3_34blocks.txt 53 20 3 34` twice (logged in `panel/work/reproduce/verify_output.txt`):
- **Run 1**:
  - `file_sha256: ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`
  - `RESULT: PASS | v=53 k=20 t=3 b=34 unique=34 total_t_subsets=23426 uncovered=0 schonheim_bound=24`
- **Run 2**:
  - `file_sha256: ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`
  - `RESULT: PASS | v=53 k=20 t=3 b=34 unique=34 total_t_subsets=23426 uncovered=0 schonheim_bound=24`
- **Determinism and Bounds**: Both runs produced identical output. Specifically:
  - SHA-256 matches `ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`.
  - Block count `b = 34`, all 34 blocks distinct, each containing 20 distinct integers in `1..53`.
  - All `C(53,3) = 23426` 3-subsets of `{1..53}` are covered (`0` uncovered).
  - Schonheim bound `L(53,20,3) = ceil(53/20 * ceil(52/19 * ceil(51/18))) = ceil(53/20 * ceil(52/19 * 3)) = ceil(53/20 * 9) = 24`; `b = 34 >= 24` (and `34 >= 30`, the LJCR lower bound).
  - Parameter constraints satisfied: `v = 53 <= 99`, `k = 20 <= 25`, `t = 3 <= 8`, `C(53,3) = 23426 <= 5e9`.

## 4. Verification of `claim/REPRODUCE.md` and `claim/table_record/`
- Ran the exact one-liners from `claim/REPRODUCE.md` inside `claim/`:
  - Command 1 (SHA-256): returned `ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e` (matches expected).
  - Command 2 (exhaustive check): returned `blocks 34 missing 0` (matches expected).
- Verified saved table records in `claim/table_record/`:
  - `claim/table_record/coveringrepository_download_archive_vkt.html`: `171741` bytes, SHA-256 `85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17`; row for `(53, 20, 03, 03)` is `53\t20\t03\t03\t\t35` (value `35`).
  - `claim/table_record/ljcr_zenodo_v1.2_C53_20_3.json`: records `"C(53,20,3)": {"size": 35, "low_bd": 30, ...}`.
  - `claim/table_record/ljcr_github_C53_20_3.json`: records `"C(53,20,3)": {"size": 35, "low_bd": 30, ...}`.
- Our verified block count `b = 34` is strictly smaller than `35`.

pass: true
