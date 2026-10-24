# Path sanitisation of the shipped scripts, including two hash-frozen ones

`kit/SUBMIT.md` forbids absolute user paths in a submission, and `kit/check_run.py` rejects any absolute home-directory string. The scripts in this directory were written against one machine, so each absolute
path was replaced by an environment-variable lookup with a relative default. The variables are documented in
`PATHS.md`.

**This is recorded because two of the rewritten files are hash-frozen in `PREREG.v4.md`.** A verifier
re-checking those hashes gets a mismatch, and the honest thing is to say why rather than let them wonder.

## The two frozen files

| file | sha256 frozen in `PREREG.v4.md` | sha256 as shipped here |
|---|---|---|
| `h10_build_teacher.py` | `df368571330b4db802496f99483616e6ed166d0b88ff1681d14537ae9fa546d6` | `a6b34fa5b68e203bf97e71181dca5af176096675aff611a51c4c11bf70d8165f` |
| `h10_teacher_threshold.py` | `312b0a8ef06cc27d76f170fc84225aadaaf7b0b0773078bad14248978f727d51` | `fe0a11788963ad0c11bcf49207c073e978b67cbcd53b28651d7c1138f4dd0f71` |

Both as-shipped values are printed in full above so a verifier can confirm that the file in hand is the file
described here, and `../../SHA256SUMS` carries them too.

**The complete diff, after masking the substituted path literals on both sides, is one line per file:**

```
h10_build_teacher.py:      3a4  > import os
h10_teacher_threshold.py:  2a3  > import os
```

That `import os` is required by the substitution itself. Independently confirmed by the verification panel,
which reconstructed both originals from text it had read before any cleanup and diffed them mechanically.
Every substantive constant is intact, including the >=30-measurement panel filter, `radius=2, fpSize=2048`,
the `maxsim >= 0.85` audit cutoff, the three leaked identifiers `{373989, 721951, 757444}`,
`torch.manual_seed(0)`, and the full 2048-1024-256-1 / Dropout(0.3) / AdamW(1e-3, weight decay 1e-4) /
25-epoch / batch-256 training schedule.

**Nothing but path strings changed in either file**: no logic, no constant, no hyperparameter, no threshold.
Both still compile, and both are byte-identical to the frozen versions everywhere except those path literals.

**The unmodified, hash-matching originals exist outside this package**, in the run directory the submission
was built from, and the four *other* artefacts frozen in `PREREG.v4.md` §1 — `potency_core.py`,
`potency_transfer_model.py`, `potency_core_fast.py` and `teacher_pred.csv` — are shipped **unmodified and
still match their frozen hashes exactly**, because they contained no absolute paths. Those four include the
entire model, which is what the frozen hashes exist to pin.

## Every file rewritten

`ablate_teacher.py`, `devharness.py`, `diagnostics.py`, `evaluate_with_drevalpy.py`, `h10_build_teacher.py`,
`h10_leak_audit.py`, `h10_teacher_threshold.py`, `leader_fold.py`, `make_splits_independent.py`,
`null_test.py`, `run_confirmatory.py`, `repro_seed42.sh`.

Each was restored from the original before substitution, each substitution was **parse-checked before being
written**, and every shipped `.py` file compiles under Python 3.12. An earlier attempt at this cleanup
produced invalid files and was reverted; the verification panel caught it, which is why the check is now
part of the procedure rather than an afterthought.

## What this does not fix

These scripts remain **the record of what was run, not a turnkey pipeline**: several still write their
outputs to paths relative to `OUT`/`PKG` that mirror the author's run layout, and reproducing Levels 2-4 of
`../RUN_IT_YOURSELF.md` means setting the variables in `PATHS.md` and reading the script first. Level 1 —
the verification that settles the claim — needs none of them and no environment variables at all.

## Two further files sanitised for the same reason

| file | sha256 before | sha256 as shipped | change |
|---|---|---|---|
| `PREREG.v2.md` | `29260e18f26ade3be18a95037c5af5e2c3458410905f6f1f457430b3126d5d52` | `2153aea543b0b35e583574c10ba809374357242a75c8bb22981e5ab533fa205b` | path anonymisation |
| `null_test.md` | `7d526b7725c65904c1112532481c12746b08d1466c6e5a82ec38bcdc63656fff` | `45010345f76ef4e5c5b7f3cdae76d090dec288ac691c7ebbc3c442554e84af35` | path anonymisation |

`PREREG.v2.md` is referenced by hash in `PREREG.v3.md`; the shipped copy therefore no longer matches that
reference, for the same reason as the two scripts above and with the same kind of change — an absolute path
replaced by a variable name, nothing else. The unmodified originals remain in the run directory outside this
package. `PREREG.md` itself is shipped unmodified and still matches its recorded hash.
