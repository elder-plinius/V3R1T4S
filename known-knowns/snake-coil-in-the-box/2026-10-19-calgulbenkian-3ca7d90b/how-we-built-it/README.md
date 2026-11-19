# How we built it

Contributor material, unverified. Copied from the contributor's snapshot (taken 2026-10-19T02:53:48Z) and sanitised: every absolute local path is replaced by {WORKDIR}, and usernames, emails and hostnames are removed. Compiled binaries and the contributor's own verifier scripts are not copied. Third-party datasets are not copied.

Files here:

- `PREREG.md`
- `RESULTS.md`
- `src/snake_coil_opt.c`
- `src/fast_opt.c`
- `src/snake_coil_opt2.c`
- `src/lift_all_dims.c`

`PREREG.md` is the run's pre-registration; `RESULTS.md` is the contributor's results log for all dimensions (section 4 covers the p3 witnesses).

## Commands

`snake_coil_opt` has the modes `lift_coil`, `lift_snake`, `drift_opt N IS_COIL SEED_FILE OUT_FILE` and `boost_coil`; compile and run per the header comments in the sources. The seed file, random seeds and exact command that produced this drifted sequence are NOT recorded in the snapshot.
