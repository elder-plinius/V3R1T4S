# RECEIPTS: real output of sh verify-it-yourself/run_checks.sh (2026-10-21, 8-vCPU Linux VM, 1 thread; real 1m27s)
```
object check: 0 problems; recomputed {'chunks': 4096, 'masks': 68719476736, 'captured': 68719476736, 'uncap': 0, 'oob': 0, 'max_tcap': 375545, 'max_tcap_mask': 40920836116, 'contiguous': 'yes', 'sample_units': 16384, 'sample_masks': 687234013, 'sample_cap': 687234013, 'sample_max_tcap': 271692, 'sample_max_tcap_mask': 61493184540, 'sample_units_over_chunk_max': 0, 'hard_cases': 4096, 'hard_cases_equal': 4096}
== code/scripts/build.sh
built bin/lantx2 bin/lant4 bin/lant_ref
   (1 s)
== python3 code/scripts/check_summaries.py
chunks 4096 masks 68719476736 CAP 68719476736 (2^36 = 68719476736) global max tcap 375545 at mask 40920836116
SUMMARIES: PASS
   (0 s)
== code/scripts/check_4x4.sh
4x4: PASS (65536 lines identical)
   (1 s)
== code/scripts/check_5x5_slice.sh
5x5 chunk07: PASS (1048576 lines identical) sha256 a75f41cd2b52c87f95a07c8ae936dc614d1693863036ec913a359a5f3c336305
   (25 s)
== code/scripts/check_hard.sh
hard cases 4096 mismatches 0
HARD: PASS
   (4 s)
== code/scripts/check_lant4_small.sh
lant4 vs lantx2 [40920803348,40920868884): PASS (65536 lines identical)
   (4 s)
== code/scripts/check_sample_blocks.sh
unit pass 0 chunk 0: IDENTICAL (pass 0 chunk 0 n 41799 CAP 41799 UNCAP 0 OOB 0 maxtcap 107010 maxtcap_mask 14946136 sumtcap 173075090 steps 205095104 linehash fb7b57a2c860097f)
unit pass 1 chunk 777: IDENTICAL (pass 1 chunk 777 n 41971 CAP 41971 UNCAP 0 OOB 0 maxtcap 96579 maxtcap_mask 13042022687 sumtcap 182438356 steps 214631104 linehash 234e93da2c254d89)
unit pass 2 chunk 2439: IDENTICAL (pass 2 chunk 2439 n 41777 CAP 41777 UNCAP 0 OOB 0 maxtcap 150778 maxtcap_mask 40921964037 sumtcap 195780518 steps 227850432 linehash a7caafef1dee3fdf)
unit pass 3 chunk 4095: IDENTICAL (pass 3 chunk 4095 n 41830 CAP 41830 UNCAP 0 OOB 0 maxtcap 111973 maxtcap_mask 68715098667 sumtcap 203031001 steps 235138624 linehash 667c4518195103ce)
SAMPLE BLOCKS: PASS
   (5 s)
== python3 code/scripts/check_sample_summary.py
chunk 0 python selection counts per pass [41799, 41742, 42009, 41903] (units: ['41799', '41742', '42009', '41903'])
chunk 4095 python selection counts per pass [41578, 42018, 41960, 41830] (units: ['41578', '42018', '41960', '41830'])
sample masks 687234013 (1.000057% of 2^36) CAP 687234013; units over user chunk max: 0
SAMPLE SUMMARY: PASS
   (12 s)
== code/scripts/tamper_tests.sh
tamper 1 detected: 4x4: FAIL (1 differing lines)
tamper 2 detected: 5x5 chunk07: FAIL (1 differing lines)
tamper 3 detected: SUMMARIES: FAIL
tamper 4 detected: SUMMARIES: FAIL
tamper 5 detected: HARD: FAIL
tamper 6 detected: SAMPLE BLOCKS: FAIL
tamper 7 detected: SAMPLE SUMMARY: FAIL
tamper 8 detected: SAMPLE SUMMARY: FAIL
tamper tests detected: 8 of 8
TAMPER: PASS (every tamper detected)
   (35 s)
RUN_ALL: PASS
PASS
```
