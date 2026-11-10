# How a(16) was computed

Needs rustc and Python 3. From this folder:

    rustc -O ice.rs -o ice            # ice.exe on Windows
    ./ice A 16 6 4611686018427387847 4611686018427387817 4611686018427387787 4611686018427387761
    ./ice B 16 6 2305843009213693951 2305843009213693921 2305843009213693907 2305843009213693723

`ice MODE N THREADS PRIME...` (MODE is A or B) prints one `prime residue` line per prime. A = left-to-right cell sweep with
symmetry reduction (shifts, reflection, global reversal); B = right-to-left sweep with the dual recursion, shifts
only. CRT of either run's residues gives the value. `drive.py LO HI THREADS` ran both modes for n = LO..HI and wrote
`results.jsonl` (it expects the original run layout: `primes.txt` and `data/b054759.txt` two levels up).
`primes.py` checks the primes (deterministic Miller-Rabin).

Timings on 6 logical CPUs at idle priority: n = 16, A ~5 min, B ~17 min; n = 17, A 1128 s, B 4429 s.

Independent method for n = 15 (whole-row transfer matrix split by flux sector, dense float64 products mod primes
below 2^19, no shared code):

    python sector_trace.py 15 524287 524269 524261      # 625 s; residues 301866 292953 237113

`PREREG.md` (n = 16) and `PREREG.v2.md` (extension to n = 17) were written before the runs.
