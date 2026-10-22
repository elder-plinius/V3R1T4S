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

RESULTS.md section 3.3: the Q13 symmetric coil of length 2886 (half period 1443) came from a four-stage cascade: symmetric local search 2870 to 2878, then lifting the Q12 coil of length 1454 into Q13 (1454 to 2882), then `ils_sym 13 15` on the 2882 file, which found the +4 step to 2886 in round 6. The file is results/best_sym13_from2882_Q13_2886.txt.

## Commands

fast_opt usage (from fast_opt.c): `fast_opt ils_sym N ROUNDS SEED_FILE OUT_PREFIX` and `fast_opt lift_sym N_IN MAX_DETOURS SEED_FILE OUT_PREFIX`. RESULTS.md quotes `ils_sym 13 15` and `ils_sym 12 12`. The seed files (the author's earlier closed-PR objects and the lifted intermediates) are not in this package, and the full command lines of the run that wrote this object were not recorded in the snapshot.

Build note: the C files are single-file programs (for example `cc -O3 fast_opt.c -o fast_opt`; the snapshot has no build script,
so this line is ours, not a recorded command).

## Not included

Third-party record files (the minortriad samples, the Caltech banks, other contributors' sequences) and the search seeds are
not copied; see `the-record-we-beat/` for the sources by name and link.
