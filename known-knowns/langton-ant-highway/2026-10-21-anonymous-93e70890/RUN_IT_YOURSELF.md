# Run it yourself (from this folder, fresh shell; Linux/WSL with sh, gcc, python3, awk, zcat, sha256sum)

## Main check (~1.5-2 min)
```
sh verify-it-yourself/run_checks.sh
```
Expected: `object check: 0 problems ...`, then the claim checks (SUMMARIES, 4x4, 5x5 chunk07, HARD, lant4 vs lantx2, SAMPLE BLOCKS, SAMPLE SUMMARY, TAMPER, each PASS), `RUN_ALL: PASS`, and the last line `PASS`. The real output is in verify-it-yourself/RECEIPTS.md.

## Longer checks: work in a scratch tree laid out like the original claim
The main check builds this tree itself and deletes it afterwards. To keep one, run the reassembly part of run_checks.sh by hand, or:
```
mkdir -p ../w/code ../w/data/user-chunk-sums ../w/data/validation ../w/data/sample
cp -r verify-it-yourself/code/lantx2 verify-it-yourself/code/scripts ../w/code/; cp -r how-we-built-it/lant4pkg ../w/code/
cat object/chunk_sums/*.txt | awk '{for(i=1;i<NF;i++) if($i=="chunk"){c=$(i+1);break} f="../w/data/user-chunk-sums/chunk_" c ".sum"; print > f; close(f)}'
cat object/sample/sample_units.part*.txt > ../w/data/sample/sample_units.txt
cd ../w && sh code/scripts/build.sh
sh code/scripts/check_sample_blocks.sh 2 1234 3 99      # any (pass, chunk) units, 1-2 s each; all 16,384 units take about 5 CPU-hours
sh code/scripts/rerun_full_chunk.sh 77 4                 # a whole chunk (2^24 masks): lant4 output sha256 must equal the summary's (SHA256 MATCH); ~17 min with 1 thread
bin/lantx2 range 6 6 40920836116 40920836117             # the slowest mask: 40920836116 375545 -2 2 1 CAP
```

## Rebuilding the object (how-we-built-it/)
- Exhaustive run (~40 h on 24 threads): build with how-we-built-it/lant4pkg/build.sh, then `scripts/run_chunks.sh out6 6 6 24 lant4 <threads>` (lant4pkg/README.md section 3). Each chunk_<c>.sum must equal the line for chunk c in object/chunk_sums/.
- Independent sample: build how-we-built-it/lantx/lantx2.c, then run `lantx2 sample P W NW OUTDIR` for P = 0..3 (driver: how-we-built-it/sample-job/run_sample.sh). Each unit file must equal its line in object/sample/. lantx_v1.c is the version that ran the sample; it differs only in its stop rule near the cap (PREREG.v2.md).
