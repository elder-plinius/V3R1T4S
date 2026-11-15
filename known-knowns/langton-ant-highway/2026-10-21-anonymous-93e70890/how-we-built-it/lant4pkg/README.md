# Langton's ant — exhaustive 6x6 search package

Fast CPU solver (multithreaded, 12-core friendly) and a CUDA version of the exhaustive "all 2^36 starting patterns in a 6x6 box"
search, byte-for-byte compatible with the original single-threaded `lant2.c` (kept as `ref/lant_ref.c`).

**Honest status.** CPU solver: built, tested, verified byte-identical to the reference (see "What is verified").
CUDA solver: **written but never compiled or run** (the machine it was written on has no nvcc / GPU). The *kernel code is the
same `lant_run()` function* as the CPU solver, and a CPU "emulation build" of the CUDA program was verified identical to the
reference, so the algorithm is checked; the CUDA-specific glue (allocation, launch, memory) is untested. Verify it on your GPU
with `scripts/verify.sh lant_cuda` before trusting any result.

## 1. The problem, exactly
* Box: W x H cells (here 6 x 6 = 36 cells). A starting pattern is a 36-bit mask; bit `b` (0..35) is cell
  `(x,y) = (b % W - (W-1)/2, b / W - (H-1)/2)`, i.e. for 6x6 x,y in -2..3. Bit set = cell starts black (value 1). All other cells are white (0).
  All 2^36 = 68,719,476,736 masks are enumerated (`0 .. 2^36-1`).
* The ant starts at (0,0) **facing direction 0 (north)**. Because every pattern is run with the ant facing north, the four rotations of
  the ant's heading are already covered by the four rotated patterns; this is the only symmetry reduction that is valid.
  Mirror images are **not** equivalent (they swap R and L), and for even boxes (5x6, 6x6) the box is not rotation-invariant about the ant's cell,
  so no further reduction is used. (An orbit-dedup experiment gave only ~1.2x and is not included.)
* Rule (as in `lant2.c`): on cell value g: `d = (d + 1 + 2*g) & 3`, flip the cell, move one step. Direction d: 0:(0,+1) 1:(+1,0) 2:(0,-1) 3:(-1,0).
  (g=0: turn +1, g=1: turn +3; this is a fixed chirality.)
* **Highway detection.** From step t >= 104 a step is "periodic" if the direction equals the direction at t-104 and the displacement over
  the last 104 steps is one of (±2,±2). A run of consecutive periodic steps that keeps the *same* displacement is tracked; every time
  the run length reaches a multiple of 312 (3 periods) the program tests the certificate below, scanning start steps s from the earliest
  not-yet-tested one up to t-104.
* **Capture certificate C(s)** (what "captured" means): displacement over [s, s+104] is (vx,vy) = (±2,±2) with equal direction at s and s+104;
  let P = set of cells visited an odd number of times during steps s..s+103. Then for every translate k = 0,1,2,… the 104-step pattern
  (cells visited, shifted by k·(vx,vy)) is compared: grid value at cell c must equal (grid value at c+(vx,vy)) XOR P(c+(vx,vy)), checked for
  k = 0,1,… until the translate lies completely outside the bounding box of everything visited/initialised (in x or in y). If all comparisons pass the
  grid ahead of the ant is in the periodic highway configuration forever (the usual exact "the ant builds a highway" certificate).
  `T_cap` = the first s for which C(s) holds. The run continues until the cap (2,000,000 steps, `+104`) if never captured.
* **Output** (one line per mask, same as `lant2`): `mask tcap vx vy dir steps STATUS`
  * `CAP` — certificate found at step `tcap`; (vx,vy)= 104-step displacement, dir = heading; `steps` = step at which the run stopped.
  * `UNCAPTURED_WITHIN_CAP` — no certificate within 2,000,000 steps. **This is the interesting outcome** (a candidate counterexample to
    "every 6x6 start ends in a highway"), though almost certainly just a long transient; it must be re-run with a larger cap (`ref/lant_ref enumr 6 6 M M+1 CAP`) and examined by hand.
  * `OUT_OF_BOUNDS` — the reference's 8192x8192 grid was left (treat like UNCAPTURED; re-run with a bigger grid).
  * `WINDOW_OVERFLOW` — **only produced by the fast solvers** when the ant came within 16 cells of the edge of their 1024x1024 window.
    This is not a result: `scripts/fixup.sh` (called automatically by `run_chunks.sh` and `verify.sh`) re-runs that single mask with the reference program.
    (On the 6x6 samples tried — 5 x 40,000 masks plus the verify ranges — there were 0 overflows.)
* A finite search over 6x6 is evidence, not a proof about all starts (the open conjecture is that *every* finite start ends in a highway).

## 2. Build (Linux; Windows: use WSL2 — the scripts are POSIX sh/awk; native Windows is not supported)
```
./build.sh            # builds ref/lant_ref, lant4 (CPU), lant_cuda_emu (CPU emulation of the GPU kernel), and lant_cuda if nvcc exists
./build.sh sm_86      # arch for nvcc; sm_86 = RTX 3090 (default). Needs gcc, sh, awk, sha256sum, gzip.
nvcc -O3 -arch=sm_86 -Isrc -o lant_cuda src/lant_cuda.cu     # manual CUDA build
```
Windows + CUDA under WSL2 works with the NVIDIA WSL driver; on native Windows the display driver's ~2 s kernel watchdog (TDR) will kill the long
kernel — use WSL2 or a headless Linux box, and use small chunks (`CHUNK_LOG2` 18–20) for the GPU.

## 3. Run
```
scripts/verify.sh lant4 12          # 1. verify first (about 10 s)
scripts/run_chunks.sh out6 6 6 24 lant4 24          # full 6x6 run; chunk = 2^24 masks (4096 chunks); 24 threads on a 9900X (12C/24T)
scripts/run_chunks.sh out6 6 6 20 lant_cuda 16384   # GPU variant: THREADS = persistent GPU threads (each uses ~261 KB VRAM → 16384 ≈ 4.3 GB)
```
`run_chunks.sh OUTDIR [W H CHUNK_LOG2 ENGINE THREADS MAX_MINUTES]` is **resumable**: a chunk is complete only when `OUTDIR/chunk_<c>.sum` exists
(written last, atomically). Kill it any time (Ctrl-C, reboot) and re-run the same command; finished chunks are skipped.
`touch OUTDIR/STOP` stops after the current chunk. `MAX_MINUTES` makes it stop after a time budget. Per chunk you get
`chunk_<c>.sum` (counts of CAP / UNCAPTURED / OOB, max tcap and its mask, number of distinct (vx,vy,dir) classes, number of overflow fixups, sha256 of the full chunk output)
and `chunk_<c>.noncap` (every non-CAP line — **this is what to look at**). The full per-mask output is not kept (about 70 GB) unless `KEEP_FULL=1` (gzipped).
Direct use: `./lant4 W H START END CAP [THREADS]` (END exclusive; output to stdout), same for `./lant_cuda`.
Memory: lant4 uses ~1 MB per thread; the GPU ~261 KB per GPU thread plus 32 bytes per mask of the launch range (so keep chunks ≤ 2^22 masks on the GPU).

### Reporting results
After the run: `cat out6/ALL.sum` (regenerated at the end of each invocation) and `cat out6/chunk_*.noncap`. Report: total chunks complete (must be 4096 for 6x6 at L=24);
sum of CAP/UNCAP/OOB; the list of every non-CAP mask (hex or decimal) with its line; the maximum `tcap` and its mask; the number of distinct highway classes;
the engine, CPU/GPU model, thread count, wall time and commit/hash of this package; and the sha256 lines (`chunk_*.sum`) so results can be cross-checked on another machine.
If any non-CAP mask appears, re-run it with the reference and a larger cap before claiming anything.

## 4. What is verified (measured on the build machine, 8-vCPU Xeon, no GPU)
`scripts/verify.sh <engine>` compares the engine's output (after overflow fixups) against `ref/lant_ref enumr` byte for byte:
all of 4x4 (65,536 masks), all of 5x5 masks 0..32767 plus 20,032 more, 5x6: 120,700 masks in 3 places, 6x6: 80,000 masks in 4 places (all 11 comparisons identical)
— for **`lant4`** and for **`lant_cuda_emu`** (the CUDA kernel source executed on the CPU). The window-overflow fallback was exercised separately by compiling with a tiny window
(`-DWINLG=6`, 2105 overflow lines out of 3000 masks) and the fixed-up output was identical to the reference. The resumable runner was tested with an interrupted/resumed 4x4 run.
**Not verified:** the CUDA build (`lant_cuda`) — never compiled; correct results on the GPU are unproven until `scripts/verify.sh lant_cuda` passes on your machine. 
The 5x5 and 5x6 comparisons are samples, not complete enumerations (a complete 5x5 equality check was NOT done).

## 5. Speed — honest numbers
Measured here (Xeon 8 vCPU, shared; 6x6, 40k–400k masks from the middle of the range; mean ~4,900 steps/mask):
| program | time per mask |
|---|---|
| reference `lant2.c`, 1 thread | 31.0 µs |
| `lant4`, 1 thread | 29.5 µs (**only ~1.05x**) |
| `lant4`, 5 threads | 6.2 µs wall/mask (4.75x scaling) |
The single-thread core is **not meaningfully faster** than the original: the time is dominated by the ant's steps plus the periodic certificate scans, and my attempts
(flat-index ring buffer, 1-bit planes, lazy bounding box, vectorised bbox, 4-ants-per-thread interleaving) gave at most ~5%. The real gain is: it is multithreaded with dynamic load balancing, in-order output,
chunking/resume, an overflow-safe small window (cache friendly), and a GPU kernel. Nothing like the 1.65x "4 ants interleaved" microbenchmark carried over to the full algorithm.
Full 2^36 search extrapolation: 2^36 x 29.5 µs ≈ 2.0 million core-seconds ≈ 23.5 core-days on this Xeon. 
* **Ryzen 9 9900X (12 cores)**: ≈ 2.0 days at this Xeon's per-core speed on 12 cores; if a Zen 5 core is 1.5–2x faster per thread and SMT helps a bit, **expect roughly 1–1.5 days** (an extrapolation, not a measurement). Use 24 threads.
* **RTX 3090**: **no estimate is possible** (never run). Each ant is a long chain of dependent random memory accesses and warps diverge heavily (ants run 400 to >100,000 steps), so a naive one-thread-per-ant kernel may well
  be no faster than the 12-core CPU. Time the GPU on a 2^18-mask chunk first (`time ./lant_cuda 6 6 34359738368 34360000000 2000000 16384`) and compare with `lant4`.
* Best plan: verify, time one chunk on both engines, then split the chunk range between them with separate output dirs, e.g. `C0=0 C1=3000 scripts/run_chunks.sh outA 6 6 24 lant4 24` and `C0=3000 C1=4096 scripts/run_chunks.sh outB 6 6 24 lant_cuda 16384` (for the GPU a smaller CHUNK_LOG2 such as 20 is safer; then the chunk numbers change, so keep both engines on the same CHUNK_LOG2).

## 6. Files
`src/lant_core.h` shared single-ant core (+ the CPU interleaved engine) · `src/lant4.c` CPU driver · `src/lant_cuda.cu` CUDA driver / kernel / emulation build · `ref/lant_ref.c` original `lant2.c` ·
`scripts/{verify,run_chunks,fixup}.sh` · `build.sh`.
