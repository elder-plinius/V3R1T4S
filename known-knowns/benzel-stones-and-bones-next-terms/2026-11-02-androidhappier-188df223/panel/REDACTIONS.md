# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. novelty.md, criterion.md and gate.md
are byte-for-byte identical to the run's originals. reproduce.md has one change, in the package copy only. On line 5,
the skeptic's scratch-copy path, an absolute path under the system temporary folder, is written as
`$TMPDIR/claim-reproduce-0316`, because kit/check_run.py's leak scan rejects absolute temporary-folder paths. Nothing
else changed. `diff` between the copy and the original shows only that token. Wording, verdicts and pass lines are
untouched.

| file | replaced | sha256 of the run's original | sha256 of this copy |
|---|---|---|---|
| reproduce.md | scratch path, line 5 | c035b9c58f5b12a3fa49866ecd44f0584663730efc3d6c1e4b86595b0472dd52 | see SHA256SUMS |
| novelty.md | nothing | ae54ea813ab069640806ebc6e4580b9c87a0d79da60340c196175175eecb25ad | same |
| criterion.md | nothing | daa0db4618a09b1a033cf6e330ab5e14f928f91813e1d2caa7f0a52d4a579fe9 | same |
| gate.md | nothing | 317ced32ba29840252f07a08da3812100e914dfdb042f0dfb7e6bdb2b0db0576 | same |

A note on names: the panel text refers to the run's claim/ folder (code/benzZQ.c, code/benzB64.c, result/...). This
package ships the same programs, byte-identical, in verify-it-yourself/ and how-we-built-it/, and the same result
files in object/evidence/ (result/A_final is object/evidence/A_final, and so on). The OEIS files under the run's
claim/data/ are not shipped (third-party pages). Their hashes are in the-record-we-beat/TABLE_SNAPSHOT.md. The
reviewers' own scratch programs (for example the reproduce skeptic's mycount.py) are described in their files. They
are not shipped.
