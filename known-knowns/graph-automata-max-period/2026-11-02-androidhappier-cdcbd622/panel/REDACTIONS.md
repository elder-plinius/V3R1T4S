# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. The only change is that one
machine-local scratch-folder path was replaced so the package leaks no local paths (kit/check_run.py leak scan).
Wording, verdicts and pass lines are untouched; `diff` between a copy and its original shows only this token.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| reproduce.md | the temporary-folder path of the reproducer's helper files (1 time, line 17) | `[scratch]/` | 93e7eb6d96c41aa356de6b8f6050fa2a52c485d9f3535bdfa9e2cb3cdbad7591 |
| novelty.md | nothing | - | b0af97e713285b26351523e50e90e8fa68ed88bad03fcab60a709a01532d2aa5 |
| criterion.md | nothing | - | 10d37689dd4b8adb6fcc3163d586cd4cbc72c41a962a471214a0c7a36da1e433 |
| gate.md | nothing | - | 3bafa11c3cac0753d71bd4b6bc4a68b6ba1beef97172c3a9117c33d75f305911 |

In the panel text, claim/code/ and claim/result/ are the run's names for the files shipped here as object/code/ and
object/evidence/ (same bytes; object/VALUE.txt pins them).
