# How we built it (cell LA)

The frozen system: classifier/PRIMARY (frozen 2026-10-18T19:14:05Z; code tree sha256 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051).

- entries/classifier/PRIMARY/code/: its frozen code (system.py with `train --manifest M --model-dir D` and `predict --model-dir D --family F --jobs J`); entries/classifier/FROZEN.md: the freeze record (sha256 of every code file and of the val-0.50 and test-0.40 result files); audit_test_P.txt: the harness's test-mode row-isolation audit; run_test_P.txt: the main session's test runs at P other than 0.40.
- tools/q15h.py: the harness (training manifest = the 10 surprise training-P.tsv files plus the development families; prediction one masked-language partition at a time). tools/check_freezes_040.py and tools/rank_040.py: eligibility and validation ranking (frozen_entries.md, ranking_040.md); tools/score_test_040.py: test scoring with the official scorer; the null-test tools; tools/make_object.py writes object/ from the result files.
- PREREG.md (frozen before any lens of the session started), selection.md (candidate fixed before any test gold was read), null_test.md (400 paired-permutation controls against Mockingbird-I1's predictions), the sealed_check logs (the entry retrained in a sandbox and every test partition predicted alone in its own process, byte-identical; sealed_check.py itself is not included).
Paths in these files that began with the workspace folder read WORKDIR.
