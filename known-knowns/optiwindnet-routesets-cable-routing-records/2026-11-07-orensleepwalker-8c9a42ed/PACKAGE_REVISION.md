# Package revision (2026-11-07, before any filing)
This package was revised locally on 2026-11-07T13:59:40Z, before it was ever filed. The claimed object, its panel reports and its gate are unchanged (object/ and panel/ are byte-identical to the original; the exact original package is preserved in the author's run archive).
Changes:
1. INDEX.csv and the-record-we-beat/record.md: the status-fetch time and record-JSON hash had been copied by the package builder from an older run (2026-11-06T11:19:22Z, 8045297b...). They now give this run's actual fetch: 2026-11-07T08:26:34Z, HTTP 200, record JSON sha256 a1eb5479cd7a9ccde50311ad180aa7451d9ddefe70c23f253759299713637bad, plus the novelty reviewer's own fetch time (2026-11-07T09:06:24Z).
2. README.md: the novelty re-check date read 2026-11-06; corrected to 2026-11-07T09:06:24Z.
3. how-we-built-it/: lns_branched_original.py is the exact script that ran. lns_branched.py differs from it only in the import path of checks.py (now the same folder), so it runs from this package; replay instructions use it.
