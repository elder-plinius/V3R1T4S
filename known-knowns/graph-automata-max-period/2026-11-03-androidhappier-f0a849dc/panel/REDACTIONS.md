# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. The only changes replace
machine-local path prefixes so the package leaks no local paths (kit/check_run.py leak scan). Wording, verdicts and
pass lines are untouched; `diff` between a copy and its original shows only these tokens.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| reproduce.md | nothing | - | 99f3c5f438a72e39e831cba4b717025618141032116bd7ae9430913242f73762 |
| novelty.md | the temporary-folder prefix of the novelty skeptic's claim copy (1 time, line 3); the absolute workspace prefix of the read-only repo checkout (1 time, line 3) | `[scratch]/`; `[workdir]/` | 289e23dc86d0e335a63ad976a6b23f3abbfee81048f009c528e454e5158e894e |
| criterion.md | the temporary-folder prefix of the criterion skeptic's claim copy and of its own simulator (2 times, line 3) | `[scratch]/` | 270ea97105ccdc2e3fb084bb2bc76dcfe24064e359daa327611c9b4daac0e0dd |
| gate.md | nothing | - | 15216db8070c2570ef6c9d2bdbb77d9155cfe2521c4ea7dd2e4390ea07cca238 |

In the panel text, claim/code/ and claim/result/ are the run's names for the files shipped here as object/code/ and
object/evidence/ (same bytes; object/VALUE.txt pins them). claim/tools/geng (the nauty 2.8.8 binary) is pinned by
sha256 in object/VALUE.txt but not shipped (third-party binary). claim/data/ (the fetched OEIS pages) is not shipped
(third-party content); the-record-we-beat/TABLE_SNAPSHOT.md records its URLs, times and sha256.
