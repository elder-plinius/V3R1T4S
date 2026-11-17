# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate (2026-11-03T19:17Z). One string in
criterion.md was replaced so the package passes the kit/check_run.py leak scan. Wording, verdicts, the
confirmed_scope line, context lines and pass lines are untouched.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| criterion.md | line 15: an entry of the contributor's never-publish list, inside the curl User-Agent string | `[redacted]` | 62f1f1341465eb8ea5fd7826ca575ed16d52ca36c7c29fc55f8b35af108e4b18 |
| reproduce.md | nothing | - | 27e2843272e2fd2dafae7d79270fb54d4eeb803a43e4bd535a4e49bf211bbc65 |
| novelty.md | nothing | - | 3e0c85a69f8bbe9b5fb50e5936939c01f80f899a34759ae3b77ac4154035f340 |
| gate.md | nothing | - | bcd835e501d76a061cac9d3082830578ed5a1084b8b2cb73fa295270433d5856 |

The scratch-folder paths under /workspace/ that the skeptics mention are their own temporary copies, not paths
needed for checking.
