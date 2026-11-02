# A364417(20) = 225354012176304818: stones-and-bones tilings of the (20,37)-benzel (Propp, Problem 16)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Two independently written exact frontier-DP programs (benzZQ.c and benzB64.c) each give A364417(20) = 225354012176304818, a value absent from the OEIS A364417/A364416 DATA, b-file and draft as re-fetched 2026-11-02 01:40 ET, and benzZQ.c (but not benzB64.c) reproduces every published term A364416(3..20) and A364417(3..19).

Propp (arXiv:2206.06472) defines the (a,b)-benzel as the set of unit hexagonal cells lying inside a certain hexagon
with sides a and b, and counts its tilings by five prototiles: two "stones" (three mutually adjacent cells) and
three "bones" (three collinear cells, one per direction). T113(a,b) is the number of tilings that may use all five.
OEIS A364416(n) = T113(n,2n-4) and A364417(n) = T113(n,2n-3), offset 3. A364417 was known to a(19) =
20915277691567206 (Propp, Apr 25 2024). This folder adds the next term:

    A364417(20) = T113(20,37) = 225354012176304818

The object is object/VALUE.txt (sha256 188df22331bd9b546e473501977f50e762690706bf28a3fad4cd04e7bf712445). It states
the value, the two runs that produced it, the published terms used as controls, and pins the sha256 of every saved
run output (object/evidence/) and of the programs shipped in verify-it-yourself/.

How the number was obtained (details: how-we-built-it/BUILD.md):
- Program A (benzZQ.c) builds the region from the (i,j,k) inequalities and sweeps lines i = const. Program B
  (benzB64.c) builds the region from the complex-plane hexagon vertices and Euclidean tile distances, and sweeps
  lines k = const ascending, then i descending. Each has its own hash table and its own feasibility search.
- Both are exact frontier dynamic programs with unsigned 64-bit counts. Every addition is overflow-checked, and an
  overflow voids the result. Both reported overflow 0.
- Pruning is sound. A frontier state is dropped only when a complete exact-cover search proves that the next rows
  cannot be covered. A search that hits its node limit keeps the state.
- Run A was stopped once (SIGTERM, declared) and resumed from its own checkpoint at t=210. Resuming was tested on
  (16,28), where it gives A364416(16). Run B ran once, without interruption. A reviewer's fresh rerun of B gave the
  same value and the same peak state count (panel/reproduce.md).
- Controls: benzZQ.c reproduces every published term A364416(3..20) and A364417(3..19). benzB128.c (benzB64.c with
  128-bit counts) reproduces A364416(3..18) and A364417(3..18). A definition-level exact-cover counter with no
  transfer matrix (indep_check.py) reproduces n = 3..11.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: about 1 minute on 8 cores. Requirements: Python 3 (standard
library only), plus a C compiler with OpenMP (gcc or clang with -fopenmp). Without the compiler, step 4 is skipped.
The script checks the hash of object/VALUE.txt against INDEX.csv and every pinned file. It checks that the saved
n = 20 runs of both programs and all saved published-term runs agree with VALUE.txt. It recounts n = 3..11 from the
definition, and it reruns both n = 20 programs fresh on every published term up to n = 14 (set NMAX=16 for more).
Real output: verify-it-yourself/RECEIPTS.md.

Recomputing the new term itself takes about 40 minutes per program on 7 threads, with about 3.5 GB peak memory each.
Do not run both at once on a 16 GB machine. The commands are in RUN_IT_YOURSELF.md, section 3.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A364417, DATA, b-file and draft | a(20) | absent (DATA, b-file end at a(19) = 20915277691567206; draft: no pending changes) | 225354012176304818 | 2026-11-02T05:49:16Z (claim); 2026-11-02T06:40:30Z (novelty panel); 2026-11-02T07:41:24Z (gate); 2026-11-02T07:44:48Z (packaging; draft fetch failed, see snapshot) |
| OEIS A364416 (bank status source), DATA | a(20) (control) | 87817595880192684 | reproduced by benzZQ.c | same fetches |

URLs: https://oeis.org/A364417 (text form https://oeis.org/search?q=id:A364417&fmt=text) and https://oeis.org/A364416.
The fetch record (times, HTTP status, headers, hashes, extracted cell) is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A364417(20). A364416(21), the weighted sequences A364418 and A364438, and Propp's Problem 16 in
  general (a formula or the 2-adic pattern) are not claimed.
- This is an exact computer enumeration, not a proof by hand or a formal certificate. The value rests on two
  programs written separately in the same run that agree exactly. They share the general method: frontier DP plus
  pruning that cannot change the count.
- "The same code reproduces every published term" holds for Program A (benzZQ.c) only. Program B's published-term
  runs used benzB128.c, which differs from benzB64.c only in count width and hash load factor. B was not run for
  A364416(19), A364416(20) or A364417(19) (panel/criterion.md, caveats).
- The panel did not rerun Program A at n = 20. It reran Program B at n = 20 (same value) and checked A's saved logs,
  its rebuild and its checkpoint resume. run_checks.sh does not recompute n = 20.
- The claim text (how-we-built-it/claim_run.md) was written before the last two A reproductions, A364417(19) and
  A364416(20), finished. Both finished with matching values before the panel and the gate.
- Novelty is as recorded in panel/novelty.md. A deleted Zenodo record about benzel problems could not be read. Its
  abstract describes computations far below this size.

## Credits

- James Propp: benzels, stones-and-bones tilings and Problem 16 (Trimer covers in the triangular grid: twenty
  mostly open problems, arXiv:2206.06472): https://arxiv.org/abs/2206.06472. Propp also contributed A364417 a(15)-a(19)
  and the later A364416 terms in the OEIS.
- The OEIS entries we compared against and used as controls: https://oeis.org/A364417 and https://oeis.org/A364416
  (The OEIS Foundation, https://oeis.org).
- J. H. Conway and J. C. Lagarias, Tiling with polyominoes and combinatorial group theory (J. Combin. Theory Ser. A
  53 (1990) 183-208): the tiling invariant tried, and set aside, as a pruning rule during the run.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
