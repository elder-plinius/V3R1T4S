# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. They were scanned for absolute
machine-local paths (and the other leaks kit/check_run.py scans for); none were found, so nothing was replaced. All
four are byte-for-byte identical to the run's originals. Wording, verdicts and pass lines are untouched.

| file | replaced | sha256 of the run's original (= this copy) |
|---|---|---|
| reproduce.md | nothing | 01e9f8c514450c67c01b19b24b4d75d7026d42f547f2a7ff231706bc876c6c94 |
| novelty.md | nothing | bd6e262503273968d95b9911e743f009340e930fd64d7849a55c9f5c7541751f |
| criterion.md | nothing | bdfa54bf5d104fa1ea4a7df4ea70feee17501336999b9382838ed369c6e31cfd |
| gate.md | nothing | 9dd77d2ceaafa410da37bcc8aac38503aff013c224c17c28d09b753a23803887 |

A note on names: the panel text refers to the run's claim/ folder. In this package result/T11_22moves.txt is
object/T11_22moves.txt; code/pegcheck.py and code/pegsim2.c are verify-it-yourself/pegcheck.py and pegsim2.c;
code/beam3.c is how-we-built-it/beam3.c; fixtures/ is verify-it-yourself/fixtures/ (all byte-identical). data/ (the
OEIS and Bell page snapshots) is not shipped; its fetch record is the-record-we-beat/TABLE_SNAPSHOT.md. The reproduce
skeptic's own checker (reproduce_mycheck.py) is described in its file and not shipped; verify-it-yourself/check_peg.py
is a separate checker written for this package.
