# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. The only change is that the
machine-local temporary-folder prefix of the skeptics' scratch copies was replaced so the package leaks no local paths
(kit/check_run.py leak scan). Wording, verdicts and pass lines are untouched; `diff` between a copy and its original
shows only this token.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| reproduce.md | nothing | - | 8414c5ce53e751bd72841b357310dd44711f951f0fb8f5833068ec53172ebff5 |
| novelty.md | the temporary-folder prefix of the novelty skeptic's claim copy (3 times, lines 3 and 15) | `[scratch]/` | 33c199c1adeeff6287b0117f25e16c7c86069d2736ddd3cdb718b444bc35e4e3 |
| criterion.md | the temporary-folder prefix of the criterion skeptic's claim copy (1 time, line 4) | `[scratch]/` | 23bf295d4105ce5ab9b6c4bb6717895dd0ec7e121d8305bfd89208e9753dfb84 |
| gate.md | nothing | - | 7641c438812707cea97d12874c43853c7bace28fa8f8a8b10af010ef58a7b852 |

In the panel text, claim/code/ and claim/result/ are the run's names for the files shipped here as object/code/ and
object/evidence/ (same bytes; object/VALUE.txt pins them). claim/data/ (the fetched OEIS pages) is not shipped
(third-party content); the-record-we-beat/TABLE_SNAPSHOT.md records its URLs, times and sha256.
