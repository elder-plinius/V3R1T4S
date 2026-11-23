# Panel copies: redactions

The four panel files (reproduce.md, novelty.md, criterion.md, gate.md) are byte-for-byte copies of the run's panel/
files, made after the gate. Nothing was redacted: they contain no absolute workspace paths (the reproduce skeptic
mentions only that it worked in a private temporary folder, without naming the path).

| file | replaced | sha256 of the run's original | sha256 of this copy |
|---|---|---|---|
| reproduce.md | nothing | c023d71306607e6dbc255f19a4b047fc96c1ac81ca99cd8a5f14afacd45064bd | same |
| novelty.md | nothing | 0a00546b70675350ae75d427c6ad9a6fb2ee80f753e7fdc128ba8971245a5acf | same |
| criterion.md | nothing | f864fb81961ace6f8ca4ef9eb56be097f89c5b557254f7d9d90c6298ba0db174 | same |
| gate.md | nothing | 582a2691f08893a69de7977b941e8440ffb24eaf64fac4f191b4a6058f6cbcba | same |

A note on names: the panel text refers to the run's claim/ folder. result/T12_25moves.txt is this package's
object/T12_25moves.txt; code/pegcheck.py and code/pegsim2.c are in verify-it-yourself/; code/beam3.c is in
how-we-built-it/; fixtures/ is verify-it-yourself/fixtures/ (all byte-identical). The run's claim/data/ pages are not
shipped (third-party pages); their hashes are in the-record-we-beat/TABLE_SNAPSHOT.md. The reviewers' own scratch
checkers are described in their files and are not shipped.
