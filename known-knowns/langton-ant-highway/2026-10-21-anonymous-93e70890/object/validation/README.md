# Validation data
- enum4_lant2.txt: all 65,536 4x4 masks, lant2 output (mask tcap vx vy dir steps STATUS), box convention o=(k-1)//2: bit b -> (b%4-1, b//4-1).
- enum5_chunk07_lantc.gz: 5x5 masks [7340032, 8388608), lant.c output (bit b -> (b%5-2, b//5-2)).
- lantx_5x5_all_chunks.log: lantx vs lant.c on all 32 chunks of 2^20 5x5 masks (all IDENTICAL; per-chunk sha256 of lantx lines). The other 31 lant.c chunks are not shipped (300 MB).
- negtests.txt: lantx2 negative tests (METHOD.md section 1).
- lant4_vs_lantx2.txt: lant4 (1 thread) vs lantx2 per-mask, three 2^20 ranges, all IDENTICAL.
- fullchunks.txt: chunks 0 and 2439 rerun with lant4 (sha256 equal to the exhaustive run's) and lantx2 (all CAP, same maxtcap).
- fullchunk4095_cleancopy.txt: chunk 4095 rerun from a clean copy of this package with code/scripts/rerun_full_chunk.sh 4095 1 (SHA256 MATCH; lantx2 all CAP, maxtcap 213277).
