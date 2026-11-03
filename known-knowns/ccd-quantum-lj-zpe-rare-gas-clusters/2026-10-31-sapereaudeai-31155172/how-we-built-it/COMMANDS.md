# How the object was built (exact commands, relative to a run folder)

Requirements: Python 3 with numpy (`requirements.txt`). `ljfast.py` is the fast evaluator that every search script
imports (pass its folder as `--tools`). `bars.tsv` comes from the table:

    python -I parse_table.py table.html table_rows.tsv
    # bars.tsv: minimum per (N, species) over the A/B/C rows of table_rows.tsv; columns N, species, bar, row

Calibration of the fast evaluator on the posted point files (from the table's own all.tar link,
http://www-wales.ch.cam.ac.uk/~florent/LJZPE/points/all.tar) gave 47 of 56 files matching all four columns to
5e-5. The 9 that miss are the ones the V3R1T4S bank entry lists as known mismatches.

The landscape chain that found the object (basin-hopping on the classical surface, Metropolis acceptance on E_Ne,
T = 0.4, 10 minutes, below-normal priority, numpy generator seed 12):

    OMP_NUM_THREADS=1 python -I bh_zpe.py --tools . --bars bars.tsv --n 38 --species Ne --minutes 10 --T 0.4 \
        --out out --rng 12 --seed points/38A --seed points/38B

It wrote `out/cand_N38_Ne_r12_Ne.xyz` (Newton-polished, 17-digit mantissas). The object here is that file with
its comment line replaced. A second, independent route reached the same minimum (same E_LJ to 12 digits): a
best-first walk along soft normal modes from 38A and 38B, ranked by E_Ne:

    OMP_NUM_THREADS=1 python -I softmode_walk.py --tools . --bars bars.tsv --points points --good good_labels.txt \
        --sizes 37,38,44 --species Ne --minutes 10 --out out --rng 24

The searches are stochastic. A rerun reaches its own minima, and how many steps run depends on wall-clock time.

Self-check (independent pair-loop gradient and finite-difference Hessian):

    python -I selfcheck.py ../object/N38_Ne.xyz -107.42431

`PREREG.md` is the run's pre-registration, frozen before any lens ran. No null test applies: the claim is an
explicit object checked by a deterministic checker against a table value.
