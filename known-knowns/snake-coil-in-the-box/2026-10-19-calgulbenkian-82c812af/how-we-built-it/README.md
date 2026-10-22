# How the object was built (contributor text, unverified)

Source: the contributor's search workspace for the target snake-coil-in-the-box (Q9 to Q14), copied from the agent's read-only
snapshot of 2026-10-19. Local absolute paths were replaced by {WORKDIR}, {HOME} and {TMP}.

- `PREREG.md`: the run's pre-registration (target, definitions, baselines, attack plan).
- `RESULTS.md`: the agent's own results note for the whole run (all cells of the run, not only this one). Its claims are the
  contributor's; the checker in `verify-it-yourself/` and the panel files are the independent evidence.
- `fast_opt.c`: bitboard iterated local search and lifting program (modes ils_snake, ils_coil, ils_sym, lift_sym, lift_coil).
- `snake_coil_opt.c`, `snake_coil_opt2.c`, `lift_all_dims.c`: earlier optimiser and dimension-lifting programs.
- `verify_snake_coil.py`, `verify_snake.py`, `generate_summary.py`: the contributor's own verifier and summary scripts
  (not used by the panel; the panel wrote its own checks).

## This object

RESULTS.md section 4 lists this object as a second-generation equal-record witness (a 'drifted' file): fast_opt.c writes files named *_drifted_r{round}_Q{n}_{length}.txt during its iterated local search (ils_snake and ils_coil modes: neutral moves that keep the length, then a check for a longer path), starting from an earlier witness of the same cell (the seed). The seed is the author's earlier closed-PR object; it is not in this package.

## Commands

fast_opt usage (from fast_opt.c): `fast_opt ils_snake N ROUNDS SEED_FILE OUT_PREFIX` and `fast_opt ils_coil N ROUNDS SEED_FILE OUT_PREFIX`. The exact command line, round count and seed file that wrote this object were not recorded in the snapshot.

Build note: the C files are single-file programs (for example `cc -O3 fast_opt.c -o fast_opt`; the snapshot has no build script,
so this line is ours, not a recorded command).

## Not included

Third-party record files (the minortriad samples, the Caltech banks, other contributors' sequences) and the search seeds are
not copied; see `the-record-we-beat/` for the sources by name and link.
