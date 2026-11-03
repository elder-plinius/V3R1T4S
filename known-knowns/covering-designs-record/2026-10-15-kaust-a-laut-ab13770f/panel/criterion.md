role: CRITERION
context: subagent (fresh context that saw only claim/)
claim_id: C53_20_3
target: covering-designs-record
confirmed_scope: The file C53_20_3_34blocks.txt (sha256 ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e) contains 34 distinct blocks of size 20 over {1..53} that exhaustively cover all C(53,3) = 23426 3-subsets, which is one fewer than the 35 blocks listed for (53,20,3) in the coveringrepository.com plain table as fetched at 2026-10-15T23:10:40Z and in LJCR Zenodo v1.2 and dmgordo/LJCR GitHub coverdata.json.

# CRITERION Skeptic Panel Report for C53_20_3

## 1. Clause-by-Clause Bank Criterion Check

The bank criterion quoted in `claim/CLAIM.md` for `covering-designs-record` was checked independently using `panel/work/criterion/verify_criterion.py` (standard library Python, invoked via `python`).

1. **Block count, block size, point range, no repeated points**:
   - File: `claim/C53_20_3_34blocks.txt` (1926 bytes, sha256 `ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`).
   - Parsed 34 non-empty lines. Every line has exactly 20 space-separated integers (`all_len_20_list = true`), every parsed set has cardinality 20 (`all_len_20_set = true`, confirming no repeated points within any block), all 34 blocks are distinct (`distinct_blocks = 34`), and every point lies in `{1, ..., 53}` (`all_in_range = true`). Point degrees across the 34 blocks range from 12 to 16.

2. **Exhaustive coverage of all t-subsets**:
   - Total 3-subsets of `{1, ..., 53}`: `C(53,3) = 23426`.
   - Every one of the 23,426 triples is contained in at least one of the 34 blocks (`missing_triples = 0`).
   - Coverage multiplicity histogram across all 23,426 triples: 1x: 15,340; 2x: 4,285; 3x: 905; 4x: 2,532; 5x: 276; 6x: 63; 7x: 9; 8x: 3; 11x: 1; 12x: 5; 13x: 7 (sum = 23,426).

3. **Comparison against status sources and saved/re-fetched records (`b = 34` strictly smaller than every reference)**:
   - **coveringrepository.com plain `(v,k,t)` table (`m = t` section)**:
     - Saved snapshot `claim/table_record/coveringrepository_download_archive_vkt.html` (171,741 bytes, sha256 `85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17`, fetched 2026-10-15T23:10:40Z).
     - Contains 9,490 data rows formatted as `v TAB k TAB t TAB m TAB TAB blocks`, all 9,490 having `m = t` (plain covering designs).
     - The row for `(53, 20, 03, 03)` has block count `35`. Thus `34` is strictly less than `35`.
     - Live re-fetch of `coveringrepository.com` and the 6-month GitHub/arXiv sweep are delegated to the NOVELTY panelist to avoid Cloudflare rate limits.
   - **Live LJCR landing page (`https://dmgordon.org/covering-designs/`)**:
     - Re-fetched once via `curl.exe` with `User-Agent: V3R1T4S-research-agent (curl)`: HTTP 200 (9,191 bytes, saved in `panel/work/criterion/dmgordon_covering_designs.html`). Confirmed it serves no per-cell table directly and links to `coveringrepository.com` and the Zenodo archive (`19472830`).
   - **LJCR Zenodo v1.2 (`https://zenodo.org/api/records/19735294`)**:
     - Re-fetched metadata once via `curl.exe`: HTTP 200 (saved in `panel/work/criterion/zenodo_19735294.json`), confirming record `19735294` is version `1.2` (published `2026-04-24`) with `coverdata.json` (8,319,503 bytes, checksum `md5:b2c626b07f216aac830d344eff5ad523`).
     - Checked `claim/table_record/ljcr_zenodo_v1.2_C53_20_3.json`: entry `C(53,20,3)` has `size: 35` and `low_bd: 30`. Thus `34` is strictly less than `35`.
   - **dmgordo/LJCR GitHub `coverings/coverdata.json`**:
     - Checked `claim/table_record/ljcr_github_C53_20_3.json`: entry `C(53,20,3)` has `size: 35` and `low_bd: 30`. Thus `34` is strictly less than `35`.

4. **Parameter bounds, Schonheim lower bound, and laptop exhaustive check threshold**:
   - Parameter limits: `v = 53` (at most 99), `k = 20` (at most 25), `t = 3` (at most 8) — all satisfied.
   - Schonheim lower bound:
     - `L(51,18,1) = ceil(51/18) = 3`
     - `L(52,19,2) = ceil(52 * 3 / 19) = ceil(156/19) = 9`
     - `L(53,20,3) = ceil(53 * 9 / 20) = ceil(477/20) = 24`
     - `b = 34` is at least `24` (and at least `30`, the LJCR `low_bd`).
   - Same-day exhaustive check threshold: `C(53,3) = 23426` is at most `5e9` (exhaustive check finishes in ~0.05s).

5. **Monotonicity and neighbour-cell check**:
   - In the 9,490-row `coveringrepository_download_archive_vkt.html` table, we checked all cells `(v', k', 3)` with `v'` at least 53 and `k'` at most 20 (any such design with at most 34 blocks would imply `C(53,20,3)` is at most 34 by point deletion / block padding): zero such cells have value at most 34 (`subsuming_cells_v_ge_53_k_le_20_t_eq_3 = []`).
   - Specific neighbours in the table:
     - `C(54,20,3) = 35` (was the source of the previous 35-block construction for `(53,20,3)` in LJCR)
     - `C(53,19,3) = 37`
     - `C(52,20,3) = 31` (at most 34, consistent with monotonicity in `v`)
     - `C(53,21,3) = 30` (at most 34, consistent with monotonicity in `k`)
     - `C(52,19,3) + C(52,19,2) = 36 + 11 = 47` (at least 34)
     - `C(54,21,4) = 107`

pass: true
