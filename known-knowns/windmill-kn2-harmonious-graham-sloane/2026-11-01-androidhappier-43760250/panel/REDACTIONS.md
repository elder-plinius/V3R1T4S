# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. reproduce.md, criterion.md and
gate.md are byte-for-byte identical to the run's originals. novelty.md has one change, in the package copy only.
The skeptic's scratch-folder path, an absolute path under the system temporary folder, is written as
`$TMPDIR/claim-novelty-2341`, because kit/check_run.py's leak scan rejects absolute temporary-folder paths. Nothing
else changed. `diff` between the copy and the original shows only that token. Wording, verdicts and pass lines are
untouched.

| file | replaced | sha256 of the run's original | sha256 of this copy |
|---|---|---|---|
| reproduce.md | nothing | 3dbadeb11b3b95c6fa3e2e108555c36b41ddace5ecd2558895307eeff829660b | same |
| novelty.md | scratch path, line 5 | 047bbcc2e4e10be1c2bfb59687de2b80ad5a0338862faea4513d39e6321f42b9 | see SHA256SUMS |
| criterion.md | nothing | 9a6ea1b0868382e62a9f714e016bc7d605e1fa04c724ed134159275971933f22 | same |
| gate.md | nothing | 65fd62039266528e42ca8800981ca534b10619c19824b973fabb4f9a2a462d8e | same |

A note on names: the panel text refers to the run's claim/ folder (checkers/wsearch.c, checkers/mitm.py, result/...).
This package ships the same programs, byte-identical (same sha256 as the run's claim/SHA256SUMS.txt), in
verify-it-yourself/ and how-we-built-it/, and the same result files in object/evidence/ (result/DECISION.txt is
object/evidence/run_DECISION.txt). The reviewers' own scratch programs are described or inlined in their files.
They are not shipped separately.
