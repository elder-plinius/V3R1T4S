# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. The only change is that
machine-local paths were replaced so the package leaks no local paths (kit/check_run.py leak scan). Wording, verdicts and
pass lines are untouched.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| novelty.md | the absolute path of the workspace's kit repository clone | `[workspace]/repo` | bb75c7e17a6f56ffd82ea5b7ec24de3351d99241ceba56baec0dc9e63dae68ba |
| reproduce.md | the scratch-folder path of the reproducer's claim copy | `[scratch]/repro/claim` | 308e036a86d7a63a984f73e98327b981e55b183f4366c1440cd79be1ef92f297 |
| criterion.md | nothing | - | e284498d34a4d67f864c8d13d77214dd21e5e5ab622253fda52b9129c33373a6 |
| gate.md | nothing | - | f5f86cc3dc821fb65722f2375ab9f8415b801e1934e5a3f78a98f6c00f17e8c8 |
