role: CRITERION
context: subagent (fresh context that saw only claim/)

# CRITERION Panel Review — C(41, 12, 5) <= 2207

## 1. Independent Verification of the Covering Design Object
I wrote and executed an independent verification script (`panel/work/criterion/verify_criterion.py`) against the files in `claim/`:

- **File**: `claim/C41_12_5_2207blocks.txt`
- **Byte size**: `74,496` bytes
- **SHA-256**: `ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa` (matches `claim/CLAIM.md` and `claim/REPRODUCE.md`).
- **Structure**: Exactly `2,207` non-empty lines; every line parses to `12` strictly increasing integers in `{1, ..., 41}`; all `2,207` blocks are distinct `12`-subsets of `{1, ..., 41}` with no repeated points. Point frequencies across the 41 points range from `546` to `816`.
- **Exhaustive coverage check**: Using two independent methods — (a) enumerating all $\binom{12}{5} = 792$ 5-subsets of each of the 2,207 blocks (`1,747,944` block-subset incidences) and verifying every one of the $\binom{41}{5} = 749,398$ 5-subsets of `{1, ..., 41}` has positive multiplicity, and (b) testing all `749,398` 5-subset bitmasks directly against the `2,207` block bitmasks — every one of the `749,398` 5-subsets of `{1, ..., 41}` is covered at least once (`missing = 0`).
- **Coverage multiplicity distribution**: Minimum multiplicity `1` (`416,156` 5-subsets covered once, `123,015` covered twice, `58,495` covered 3 times, `61,738` covered 4 times, up to a maximum multiplicity of `51` on `3` 5-subsets).

## 2. Parameter Bounds, Schonheim Bound, and Tractability Clause
- **Parameter bounds**: `v = 41 <= 99`, `k = 12 <= 25`, `t = 5 <= 8` — all within the bank criterion limits.
- **Schonheim lower bound**:
  - $L(37, 8, 1) = \lceil 37 / 8 \rceil = 5$
  - $L(38, 9, 2) = \lceil 38 \times 5 / 9 \rceil = 22$
  - $L(39, 10, 3) = \lceil 39 \times 22 / 10 \rceil = 86$
  - $L(40, 11, 4) = \lceil 40 \times 86 / 11 \rceil = 313$
  - $L(41, 12, 5) = \lceil 41 \times 313 / 12 \rceil = 1070$
  - Our block count `b = 2207 >= 1070` (and `2207 >= 1121`, the LJCR `low_bd`), satisfying the lower-bound sanity check.
- **Same-day exhaustive check threshold**: $\binom{41}{5} = 749,398 \le 5 \times 10^9$.

## 3. Comparison Against Saved Table Records and Live Re-Fetch
- **Saved `coveringrepository.com` archive**: `claim/table_record/coveringrepository_download_archive_vkt.html` (`171,741` bytes, SHA-256 `85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17`) contains `9,490` plain `m = t` rows. The row `41 TAB 12 TAB 05 TAB 05 TAB TAB 2244` gives `2244`. Thus `2207 < 2244` (an improvement of `37` blocks).
- **Saved LJCR Zenodo v1.2 excerpt**: `claim/table_record/ljcr_zenodo_v1.2_C41_12_5.json` (SHA-256 `9a4710779c2f0eb4eb69e459c674090fc1090f503db6cb89cbd87548b7499dec`) gives `size = 2245`, `low_bd = 1121` (top entry: `2245` by Jan de Heer and Steve Muir, `2026-02-28 23:37:02`). Thus `2207 < 2245` (an improvement of `38` blocks).
- **Saved `dmgordo/LJCR` GitHub excerpt**: `claim/table_record/ljcr_github_C41_12_5.json` (SHA-256 `4823d4f04164f8469358917a9c3d4589e02b7a08ed8b4ba6c090ca808b10bc09`) gives `size = 2429`, `low_bd = 1121`. Thus `2207 < 2429` (an improvement of `222` blocks).
- **Live re-fetch of `https://dmgordon.org/covering-designs/` and `https://zenodo.org/api/records/19735294`**:
  - `https://dmgordon.org/covering-designs/` returned HTTP 200 (SHA-256 `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`), confirming it hosts no per-cell table and directs users to `coveringrepository.com` and Zenodo DOI `10.5281/zenodo.19472830`.
  - `https://zenodo.org/api/records/19735294` returned HTTP 200 for version `1.2` (`2026-04-24`), with `coverdata.json` (`8,319,503` bytes, `md5:b2c626b07f216aac830d344eff5ad523`) and `covers.json` (`4,191,522,340` bytes, `md5:bb59d977afd6724b32dcc187f68a229c`) unchanged.
- **Check of elementary neighbour bounds in the saved `coveringrepository.com` table**:
  - Monotonicity in $v$: $C(41,12,5) \le C(42,12,5) = 2421$
  - Point-padding: $C(41,12,5) \le C(40,11,5) = 2804$
  - Pascal split: $C(41,12,5) \le C(40,12,5) + C(40,11,4) = 1994 + 483 = 2477$
  - Monotonicity in $k$: $C(41,12,5) \le C(41,11,5) = 3060$
  - Monotonicity in $t$: $C(41,12,5) \le C(41,12,6) = 12399$
  - Average-degree derived bound (R7) from $C(42,13,6) = 8718$: $\lfloor 13 \times 8718 / 42 \rfloor = 2698$
  - None of the elementary bounds from table entries comes close to `2207` (the 2207-block design is obtained by taking a specific high-degree point in the 8735-block $C(42,13,6)$ cover in Zenodo v1.2, whereas the listed table entry for $C(41,12,5)$ is `2244`).

confirmed_scope: The file C41_12_5_2207blocks.txt (sha256 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa) is a valid (41,12,5) covering design with 2207 blocks covering all 749398 5-subsets of {1..41} (checked exhaustively), 37 fewer than the 2244 listed in coveringrepository.com (fetched 2026-10-15T23:10:40Z) and 38 fewer than the 2245 in LJCR Zenodo v1.2.
pass: true
