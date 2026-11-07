# Publication-candidate reproduction

Command from the candidate root: `sh verify-it-yourself/run_checks.sh` (Git for Windows shell). Actual captured output:

```text
{"complement_pairs": 0, "elapsed": 17.1056166, "found": false, "leaves": 1702800, "masks": 1571472, "n": 10, "nodes": 91726677, "peak_working_bytes": 577544192, "q": 90, "status": "COMPLETE"}
PASS
```

Exit status: 0. This recompiles the unchanged independent program and completes the entire domain. No calibration case was rerun for publication preparation.

A separate copy had the middle numeric character in object/DECISION.json changed using the upstream mechanical checker's corruption rule. Actual output:

```text
ValueError: unexpected certificate counts
FAIL
```

Exit status: 1. This is an explicit rejection, not a timeout or compilation failure. Both copies are retained locally. These are directly executed scientific checks; they do not assert that the complete upstream package command has yet run.
