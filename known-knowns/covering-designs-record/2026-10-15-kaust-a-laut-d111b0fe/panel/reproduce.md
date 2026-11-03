# REPRODUCE skeptic verdict: C85_24_3

role: REPRODUCE
context: subagent (Claude Code Agent tool, fresh context that saw only claim/)

## Definition (quoted from claim/CLAIM.md)

> A (v,k,t)-covering design is a collection of k-element subsets (blocks) of {1,...,v} such that every t-element subset
> is contained in at least one block. C(v,k,t) is the minimum number of blocks.

Claimed object: `C85_24_3_76blocks.txt`, v = 85, k = 24, t = 3, b = 76, stated sha256
d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53. Claimed comparison: best known value 77.

## Method

I read only CLAIM.md, then wrote my own checker from the definition, using only the Python standard library
(`work/reproduce/my_checker.py`, sha256 6fca46bf394eb470a8511943f9391264e2f3b04975824ccf4281438cb131f3bf, Python 3.14.4).
I wrote it before opening REPRODUCE.md. It checks:
- the file parses, with no empty lines and no CR bytes, and the block count equals the expected b;
- every block has exactly k entries, all distinct, all integers in 1..v;
- the blocks are pairwise distinct as sets;
- an EXHAUSTIVE coverage check over all C(v,t) t-subsets of {1..v} (itertools.combinations, no sampling), done
  two independent ways: (A) mark every t-subset of every block and count the unmarked t-subsets of {1..v};
  (B) test each t-subset against every block bitmask, which also records cover multiplicity;
- the Schonheim bound L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)) with L(v,k,1) = ceil(v/k), in exact integer arithmetic
  (ceil(a/b) = -(-a//b)), and that b >= L;
- that C(v,t) <= 5e9.

## Checker self-test (output saved in work/reproduce/tests_output.txt, sha256 f7eec699...d671d010)

| fixture | params / expected b | exit | result |
|---|---|---|---|
| Fano plane, 7 blocks | (7,3,2), b=7 | 0 | PASS: uncovered 0 (both methods), distinct 7 of 7, Schonheim 7 |
| Fano with one block removed | (7,3,2), b=7 | 1 | FAIL: block_count 6, uncovered 3 [(3,5),(3,6),(5,6)] |
| same, b=6 | (7,3,2), b=6 | 1 | FAIL: uncovered 3, 6 < Schonheim 7 |
| last block {3,5,6} changed to {3,5,1} | (7,3,2), b=7 | 1 | FAIL: uncovered 2 [(3,6),(5,6)] |
| repeated point {3,5,5} | (7,3,2), b=7 | 1 | FAIL: blocks_with_repeated_point 1 |
| out-of-range point {3,5,8} | (7,3,2), b=7 | 1 | FAIL: blocks_with_out_of_range_point 1, max_point 8 |
| duplicate block {1,2,3} | (7,3,2), b=7 | 1 | FAIL: distinct_blocks 6 of 7 |

Last line: `ALL_TESTS_BEHAVED_AS_EXPECTED: True`.

## My checker on the claimed object

Command: `python my_checker.py claim/C85_24_3_76blocks.txt 85 24 3 76`, run twice with exit code 0 both times.
This is the full output (work/reproduce/my_run1.txt):

```
file_sha256: d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53
file_bytes: 5283
file_has_CR: False
empty_lines: 0
parse_errors: 0
params: v=85 k=24 t=3
block_count: 76 (expected 76) -> True
blocks_wrong_size: 0 []
blocks_with_repeated_point: 0 []
blocks_with_out_of_range_point: 0 []
min_point: 1 max_point: 85
distinct_blocks: 76 of 76 -> True
points_used: 85 of 85
C(v,t): 98770 ; <= 5e9 -> True
methodA_t_subsets_enumerated: 98770
methodA_uncovered: 0
methodB_t_subsets_enumerated: 98770
methodB_uncovered: 0 []
methodB_min_cover_multiplicity: 1 max: 21
schonheim_L(v,k,t): 54 ; b >= L -> True
RESULT: PASS
```

- The sha256 of `C85_24_3_76blocks.txt` (hashlib) is d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53.
  It matches CLAIM.md.
- Determinism: my_run1.txt and my_run2.txt are byte-identical. Both have sha256
  a538ed47b070545740578625071ad6c3e9d4d7a4277ede905f1419cfe8ac28c2.
- Line check: `grep -c .` gives 76 non-empty lines, and `awk '{print NF}' | sort | uniq -c` gives `76 24`.
- Schonheim by hand: ceil(83/22) = 4, ceil(84*4/23) = ceil(336/23) = 15, ceil(85*15/24) = ceil(1275/24) = 54.
  So 76 >= 54, and 76 is also >= the LJCR low_bd 61 given in the excerpts.

## Author's REPRODUCE.md commands (run from inside claim/, output in work/reproduce/author_reproduce_output.txt)

```
step1:
d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53
step2:
blocks 76 missing 0
step2_exit=0
step3:
ceil(83/22)= 4 ceil(84*4/23)= 15 ceil(85*15/24)= 54
```

These agree with my checker on all points: the hash, 76 blocks, 0 uncovered of the 98770 3-subsets, and a Schonheim
bound of 54. Step 4 (a live fetch) is outside this role, which has no web access. Instead I checked the saved copy
below.

## Saved comparison files (table_record/)

- `table_record/coveringrepository_download_archive_vkt.html`: 171741 bytes, sha256
  85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17. Both match CLAIM.md. The content is a tab-separated
  table with CRLF line endings and 0 lines that are not rows.
  - `grep -n "$(printf '^85\t24\t03\t')"` gives exactly one row, line 8775: `85	24	03	03		77`
    (`cat -A`: `85^I24^I03^I03^I^I77$`).
  - A Python parse finds one row with (v,k,t,m) = (85,24,3,3), and its value is 77. This matches CLAIM.md.
- `table_record/ljcr_github_C85_24_3.json` (sha256 dec67330...39816d9): `"C(85,24,3)": {"size": 77, "low_bd": 61, ...}`.
  Its best improvement is `["77", "Simple construction from (86,24,3)", "LJCR", "2009-01-21 20:09:11"]`. Source field:
  dmgordo/LJCR coverings/coverdata.json, last commit 2022-12-19. This matches CLAIM.md.
- `table_record/ljcr_zenodo_v1.2_C85_24_3.json` (sha256 80d957a1...4073774a): `"C(85,24,3)": {"size": 77, "low_bd": 61, ...}`,
  with the same improvement list. Source field: Zenodo record 19735294, LJCR v1.2, 2026-04-24. This matches CLAIM.md.

So all three saved sources give 77 for C(85,24,3), and the claimed b = 76 is strictly smaller than each of them.

## Concerns (none affects this role's checks)

- The two JSON files are excerpts that the claimant wrote out. The full coverdata.json files they cite, with their
  sha256 values, are not saved in claim/, so I cannot verify those source hashes. I checked only that the excerpts say
  what CLAIM.md says.
- I did not judge freshness against the live tables or the 6-month GitHub/arXiv grep that the success criterion
  requires. CLAIM.md lists no GitHub/arXiv grep result, so another panel role has to cover that part.
- I found no mismatch, missing object or non-determinism.

pass: true
