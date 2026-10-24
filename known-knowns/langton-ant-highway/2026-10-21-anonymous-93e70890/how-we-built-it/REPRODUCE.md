# REPRODUCE — run every check from this folder (Linux, gcc, python3, sh, awk, zcat, sha256sum)

All commands are run from the claim folder root. Scratch files go to work/ and binaries to bin/. Times are from a clean copy on an 8-vCPU Linux VM, single-threaded, nice 19.

## One command (about 1.5 min)
```
sh code/scripts/run_all.sh
```
It runs the steps below in order and ends with `RUN_ALL: PASS`.

| step | command | expected output (last line / key numbers) | time |
|---|---|---|---|
| build | `sh code/scripts/build.sh` | `built bin/lantx2 bin/lant4 bin/lant_ref` | 1 s |
| summaries | `python3 code/scripts/check_summaries.py` | `chunks 4096 masks 68719476736 CAP 68719476736 ... global max tcap 375545 at mask 40920836116`, `SUMMARIES: PASS` | <1 s |
| 4x4 | `sh code/scripts/check_4x4.sh` | `4x4: PASS (65536 lines identical)` (lantx2 vs lant2 output, columns mask tcap vx vy dir status) | 2 s |
| 5x5 slice | `sh code/scripts/check_5x5_slice.sh` | `5x5 chunk07: PASS (1048576 lines identical) sha256 a75f41cd2b52c87f95a07c8ae936dc614d1693863036ec913a359a5f3c336305` (same sha256 as chunk 07 in data/validation/lantx_5x5_all_chunks.log) | 25 s |
| hard cases | `sh code/scripts/check_hard.sh` | `hard cases 4096 mismatches 0`, `HARD: PASS` (each per-chunk maxtcap mask CAP with tcap equal to the summary) | 5 s |
| lant4 vs lantx2 | `sh code/scripts/check_lant4_small.sh [START END]` | `lant4 vs lantx2 [40920803348,40920868884): PASS (65536 lines identical)` | 4 s |
| sample units | `sh code/scripts/check_sample_blocks.sh [PASS CHUNK ...]` | default units (0,0) (1,777) (2,2439) (3,4095) each `IDENTICAL` to data/sample/sample_units.txt; `SAMPLE BLOCKS: PASS`. Any other unit: give its pass and chunk (1-2 s each). | 4 s |
| sample summary | `python3 code/scripts/check_sample_summary.py` | pure-Python recount of the hash selection in chunks 0 and 4095 equals the units' n (`[41799, 41742, 42009, 41903]`, `[41578, 42018, 41960, 41830]`); `sample masks 687234013 (1.000057% of 2^36) CAP 687234013; units over user chunk max: 0`; `SAMPLE SUMMARY: PASS` | 15 s |
| tamper | `sh code/scripts/tamper_tests.sh` | 8 tampered copies (4x4 tcap, 5x5 dir, missing chunk summary, UNCAP 1, maxtcap+1, sample linehash, sample max above chunk max, missing unit), each must make its check fail: `tamper tests detected: 8 of 8`, `TAMPER: PASS` | 36 s |

## Longer checks (optional)
- Full chunk C (2^24 masks): `sh code/scripts/rerun_full_chunk.sh C [THREADS]` prints the exhaustive run's summary line, then the sha256 of lant4's raw per-mask output (must equal the summary's sha256: `SHA256 MATCH`), then lantx2's line count, CAP count and maxtcap (must be 16777216, 16777216 and the summary's maxtcap). With 1 thread this took 16 min 39 s for chunk 4095 from a clean copy (lant4 ~10 min, lantx2 ~7 min; output in data/validation/fullchunk4095_cleancopy.txt: SHA256 MATCH, lantx2 16777216 CAP, maxtcap 213277 at 68707411148, equal to the summary). Chunks 0 and 2439 also gave SHA256 MATCH (data/validation/fullchunks.txt). It exceeds 8 minutes, so run it in the background (nohup ... &) if your environment limits command length.
- Any sample unit: `sh code/scripts/check_sample_blocks.sh P C`. All 16,384 units take about 5 CPU-hours.
- Any mask: `bin/lantx2 range 6 6 M M+1` and `bin/lant4 6 6 M M+1 2000000 1` (columns mask tcap vx vy dir [steps] STATUS). The global max: `bin/lantx2 range 6 6 40920836116 40920836117` prints `40920836116 375545 -2 2 1 CAP`.
- lantx2 negative tests: `bin/lantx2 range 4 4 0 1 9976` prints UNCAPTURED_WITHIN_CAP and `bin/lantx2 range 4 4 0 1 9977` prints `0 9977 -2 -2 3 CAP`. `bin/lantx2 plant 6 6 0 -210 -184` (black cell on the empty-grid highway at its step-20000 position) prints `0 20299 -2 -2 3 CAP` and `steps 21120`.
- Reference program for anything suspicious: `bin/lant_ref enumr 6 6 M M+1 CAP` (bigger cap allowed).

## Full exhaustive rerun (not done by this package; ~40 h on 24 threads)
`code/lant4pkg/scripts/run_chunks.sh` (see code/lant4pkg/README.md section 3), then compare each chunk_*.sum with data/user-chunk-sums/.
