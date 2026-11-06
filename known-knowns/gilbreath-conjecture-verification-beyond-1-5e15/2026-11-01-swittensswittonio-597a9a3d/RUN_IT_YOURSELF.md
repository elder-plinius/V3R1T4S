# Run it yourself

Quick check (3-8 minutes, Python only): `sh verify-it-yourself/run_checks.sh` -> last line PASS.

Full recomputation (NVIDIA GPU, about 10 GB free VRAM, Python 3.10+ with `pip install numpy "cupy-cuda13x[ctk]"`; needs about 700 MB disk for depth.u16):
```sh
cd object/code
# self-test on a small window against primesieve (needs primesieve in PATH or edit the path in test_small.py): depths equal numpy, primes equal primesieve
python test_small.py
# the whole range (resumable: rerun the same command; state.json and carry.npy hold the checkpoint)
python run_range.py --out OUT
# outputs in OUT: depth.u16, clean1280.u8, windows.csv, chunk_first_primes.csv, selfverify.log, run.log (last line: DONE ...)
sha256sum OUT/depth.u16 OUT/clean1280.u8     # equal to object/RESULT.json
python verify_counts.py OUT 500 2            # needs primecount; prints 'mismatches 0'
```
Expected: windows 46,567, blocks 349,009,729, max depth 783, flagged 0, unclean (row 1280) 0. On an idle RTX 3080 about 0.2-0.3 s per window (about 3 h); the first run took 5.1 h of GPU time shared with other work.
How it works: object/code/gil_gpu.py (CUDA C kernels through NVRTC): k_big marks multiples of primes in [262144, 4.0e7] in a 2^30-byte odd-number flag array, k_small sieves the primes below 262144 in 64 KiB shared-memory tiles (primes 3..13 by a precomputed pattern), k_emit writes the primes; k_rows runs, for each block, all rows 1..1280 in shared memory (16-bit lanes while any value exceeds 255, then bytes with __vabsdiffu4), recording the first row whose owned entries are all in {0,2} and whether row 1280 is. run_range.py streams windows, carries the unprocessed tail (blocks need 1,537 extra primes) into the next window, and recomputes 4 blocks per 250 windows with numpy as an in-run check (selfverify.log).
