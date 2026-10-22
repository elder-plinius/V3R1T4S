# How the object was built (the contributor's search code)

Everything in this folder is copied from the contributor's own snapshot (taken 2026-10-19), with absolute local paths replaced by {WORKDIR} and the C include lines written with quotes instead of angle brackets so that no angle-bracket token occurs. No other change was made.

Construction field of the object, in the contributor's words: "Full-space hitting-set extension (+1 cols) from [156,10,101]_4".

Files:
- `qc_search.c`: the contributor's first quasi-cyclic and quasi-twisted search (orbit and CRT lifting, then a coset-weighted Construction X tail search).
- `qc_hunt.c`: the later, wider version of the same search (all two-dimensional subspaces of the small base space, exhaustive lift scan).
- `q_smart_opt.c`: smart puncturing, full-space hitting-set column extension and column replacement over GF(q).

Commands: the snapshot does not record the command lines, seeds or parameter files that produced this particular object. The programs print their results to the terminal; the only invariant we can state is the one in the construction field above. The object itself is checked by the standalone checker in `verify-it-yourself/`, which does not need these programs.

PREREG.md: there is none. The snapshot holds no pre-registration for this search. The search was an open optimisation (find a generator matrix whose exact minimum distance beats the live lower bound), so the stopping rule is simply that the exact distance of the final matrix exceeds the table value.

Compile hint (an assumption, not a recorded command): `cc -O3 -o NAME NAME.c`.

Third-party data not copied: the snapshot parsed the live codetables.de bounds into a local table that these programs read. That table is not copied here; the live values are in `the-record-we-beat/`.
