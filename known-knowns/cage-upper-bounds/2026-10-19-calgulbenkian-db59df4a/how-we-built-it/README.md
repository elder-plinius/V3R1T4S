# How we built it

Contributor material, unverified. Copied from the contributor's snapshot (taken 2026-10-19T02:53:48Z) and sanitised: every absolute local path is replaced by {WORKDIR}, and usernames, emails and hostnames are removed. Compiled binaries and the contributor's own verifier scripts are not copied. Third-party datasets are not copied.

Files here:

- `RESULTS.md`
- `mixed_bicay_general.c`
- `mixed_bicay_sa256.c`
- `mixed_bicay_sa256_small.c`

There is no PREREG.md for the cage run in the snapshot. `RESULTS.md` is the contributor's results log for six mixed-cage constructions; only the row for [2,9;6] belongs to this package.

## Commands

The sources compile with `clang -O3 -march=native -pthread FILE.c -o FILE` and take an output directory as their first argument. Which of the three solvers produced this particular graph, and the arguments used, are NOT recorded in the snapshot. The generators the log gives for this graph: BiCay(Z_147; S, A0, A1) with S = [0, 1, 47, 82, 86, 116, 124, 131, 134], A0 = [6, 91], A1 = [27, 80].
