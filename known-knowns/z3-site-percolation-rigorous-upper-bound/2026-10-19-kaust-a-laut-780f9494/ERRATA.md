# Errata (cosmetic, found by the panel; the object is unchanged from what the panel checked)

1. object/code/cert/go.mod says `go 1.26.4` (the toolchain used), while the documents say Go >= 1.21. The source
   needs nothing newer than Go 1.21. With an older Go, either let Go fetch the toolchain (GOTOOLCHAIN=auto, the
   default) or change that line to `go 1.21` before building.
2. object/code/chain.py always ends with "given Campanino-Russo's p_c < 1/2 for link 1", even when a run starts at
   q1 = 501/1000 (which needs only p_c <= 1/2) or at another q. The certificates do not depend on that text; PROOF.md
   section 5 states the base correctly.
3. object/code/chain.py runs code/cert/cert.exe and the fixed arguments 3 3 3 6 6 (block 3x3x3, 6 workers, minimum
   size 6). On Linux or macOS build with `go build -o cert.exe .` (the name is arbitrary).
4. PROOF.md calls the finite checks "interval arithmetic" in section 4 and "exact arithmetic" in section 5: the laws
   are outward-rounded intervals and the final comparison is exact; both statements refer to that one procedure.
5. how-we-built-it/outputs/chainA_summary.txt: a line "[exited with code 1]" in the panel's copy came from the shell
   capture (tee could not open its log file at start), not from chain.py; every step exits 0 (chainA_log.txt).
   The copy here has that line removed.
6. "Site order" in the tie-break means increasing site index id = 9x + 3y + z (object/code/cert/main.go). Any
   deterministic rule giving a connected set or the empty set makes the proof work.
