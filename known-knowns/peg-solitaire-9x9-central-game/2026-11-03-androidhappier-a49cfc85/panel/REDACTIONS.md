# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. gate.md is byte-for-byte identical
to the run's original. reproduce.md, novelty.md and criterion.md each have one change, on line 3 (the `context:`
line), in the package copy only: the skeptic's scratch-folder path, an absolute path under the system temporary
folder, is written as `$TMPDIR/panel1321-reproduce`, `-novelty` or `-criterion`, because kit/check_run.py's
leak scan rejects absolute temporary-folder paths. Nothing else changed; `diff` against the original shows only
that token. Wording, verdicts and `pass: true` lines are untouched.

| file | replaced | sha256 of the run's original | sha256 of this copy |
|---|---|---|---|
| reproduce.md | scratch path, line 3 | 56baf77300bd3435f9661022ad64e3f96d6d5a4d0242bf9b2bf115f11cb2321b | see SHA256SUMS |
| novelty.md | scratch path, line 3 | 139794d80891d83352b6a1078f7412b811afa6493c0323254085a1f3d2615a39 | see SHA256SUMS |
| criterion.md | scratch path, line 3 | 7f948248a4044117eaa859ec61981f13fbb0c15260e0762aa3f9bd9b41f16a1a | see SHA256SUMS |
| gate.md | nothing | 1ea9b5fd6375e56b29d8daf07ae22e2caec1f30b47d63e18537477deff0d0232 | same |

A note on names: the panel text refers to the run's claim/ folder (claim/result/sol31.txt, claim/code/check9.py,
claim/code/replay9.c, claim/fixtures/, claim/data/). This package ships the same programs and fixtures
byte-identical in verify-it-yourself/ and how-we-built-it/, and the object as object/sol31.txt. The third-party
pages named there (claim/data/*.html, the Maye GIF) are deliberately NOT shipped; the-record-we-beat/TABLE_SNAPSHOT.md
records their URLs, fetch times, HTTP status and sha256 instead.
