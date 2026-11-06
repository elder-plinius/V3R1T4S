# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate (2026-11-03T17:44Z). Two strings in
novelty.md were replaced so the package passes the kit/check_run.py leak scan. Wording, verdicts, context lines and
pass lines are untouched.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| novelty.md | line 8: an entry of the contributor's never-publish list, inside the curl User-Agent string | `[redacted]` | 03d572e0e3ad5012ebde9676ca5a69857dd5acc0c181dcfd288cc55b89d65fd8 |
| novelty.md | line 39: the absolute path of the workspace | `[workspace]` | (same file) |
| reproduce.md | nothing | - | bfeb32f5f37ee3c4a58b99bb60411457060ada08d352bcd1e8652dc66d3c99c9 |
| criterion.md | nothing | - | 832145007467ca3e874aadabb12bd2bcb0b3da7144d2694259e48966c40ce233 |
| gate.md | nothing | - | e671fb78b4f8f4949b2bdf602ac19bb3732ec7e22f428d630f941cd4ac746e76 |

The run also holds criterion.v1.md, an earlier CRITERION vote (pass: true) that gave no confirmed_scope sentence; it
was superseded by a second fresh CRITERION vote (criterion.md here) and is not part of this package. The scratch-folder
paths under /workspace/ that the skeptics mention are their own temporary copies, not paths needed for checking.
