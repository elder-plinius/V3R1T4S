# How the object was built

Contributor text, unverified. Everything here is copied from the search agent's workspace snapshot (read-only) with local paths replaced.

## Files

- `sc_opt.c`: the search code (only change from the snapshot: the usage string's angle-bracket placeholders were written with braces). Riemannian L-BFGS on the log-sum-exp smoothing of the maximum pairwise inner product, with a continuation in the sharpness beta (30 up to 3e10), tangential basin-hopping kicks, and a final sharp polish. Standard C, no dependencies.
- `PREREG.md`: the preregistration written before the run (target, goals A, B and C, method).
- `RESULTS.md`: the agent's results row for (d=29, N=60), trimmed on 2026-10-27 to this row, with its minimal angle corrected and its links to unshipped files removed. The object is in `../object/`.

## Commands

Build: `cc -O3 -o sc_opt sc_opt.c -lm`

Usage of the solver (from its source): `./sc_opt {d} {N} {in_file|RANDOM} {out_file} [restarts] [noise_amp] [seed]`, defaults 5 restarts, noise 0.005, seed from the clock. The input file holds one point per line, comma separated.

Not recorded in the snapshot: the exact command lines, restart counts, noise amplitudes and seeds that produced each object. A comparison with the posted coordinates shows the run for this row started from them (same point order, each point moved by 0.013 to 0.021; see `../HOW_WE_FOUND_IT.md`). The snapshot's own account (`RESULTS.md`) says the objects were produced by `sc_opt.c` and then normalised by a separate 50-digit mpmath script, with the coordinates written to 30 significant digits; that script is not included here. The shipped objects are the final polished files, so the claim does not depend on re-running the search; re-running it will not reproduce the same files without the seeds.

The checker `../verify-it-yourself/check_sc.py` is written from the definition and is independent of the search code and of the polishing script.

## Data not copied

The table pages and the posted coordinate files of spherical-codes.org were used as inputs by the agent. They are third-party data and are not copied here: https://spherical-codes.org/ , https://spherical-codes.org/plain . The PREREG hashes of those two pages are from the agent's earlier fetch and differ from the later fetch recorded in `../the-record-we-beat/` because the live table changed in between.
