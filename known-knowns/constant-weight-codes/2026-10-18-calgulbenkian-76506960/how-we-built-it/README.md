# How the object was built

Contents of this folder, copied from the contributor's search snapshot (read-only):

- `cwc_search.c`: the search program (C, POSIX threads). Co-blocking cluster large-neighbourhood search with an exact bit-parallel maximum-independent-set repair; coordinates are relabelled in descending order of ones-frequency in the seed code first. Its command line, from the source: `cwc_search seed_txt n d w out_results_dir [rounds] [kb] [rmax] [clusters] [max4] [plateau_frac] [seed] [max_seconds] [switch_kb4_round]`; the seed file is a code in the same 0/1-per-line format as `object/`.
- `PREREG.md`: the run's pre-registration (all goals of the run; this package is one cell of its Goal C).
- `RESULTS.md`: the run's results file (all cells of the run, including cells that are not part of this package).

For this cell (A(54,8,7), target size 4205): the seed was the code already listed in Brouwer's table (live value 4193, label Pl), or, where the contributor had an earlier unmerged record for the cell, that record (see README.md, Filing history).

Exact commands: the snapshot does **not** record the compile command, the seed file used for this cell, or the argument values (rounds, kb, rmax, clusters, max4, plateau_frac, seed, time limit) of the run that produced this object. PREREG.md and RESULTS.md describe the method only. The snapshot's results/codes_search/ folder holds intermediate improvements of this cell with sizes 4205. The search is randomised and time-limited, so rerunning it will not necessarily reproduce this object; the object is checked on its own by `verify-it-yourself/`. To build the program one would compile the single source file with a C compiler and `-pthread` (an assumption; the snapshot gives no build line).

Not copied, because they are third-party data or the contributor's own verifier, which the panel did not use: the saved copy of Brouwer's table page (https://aeb.win.tue.nl/codes/Andw.html), the seed codes under the snapshot's ref/ folder (from the merged V3R1T4S bigger-codes family, https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/bigger-codes), the compiled binary, and the contributor's verifier script.
