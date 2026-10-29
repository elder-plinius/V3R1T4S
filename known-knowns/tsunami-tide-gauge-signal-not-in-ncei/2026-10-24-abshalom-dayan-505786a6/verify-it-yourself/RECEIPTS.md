# Receipts

Run on the author's machine (macOS, Python 3.14.7), 2026-10-24T22:08:13Z, from this folder:

    $ sh verify-it-yourself/run_checks.sh
    {"S": 26, "USABLE": 188, "frac": 0.1383, "wilson": [0.096, 0.195], "over264": 0.0985, "upper264": 0.3864, "listed_signal": 24, "listed_usable": 86, "unlisted_signal": 2, "fake_rate": 0.027, "fake_worst_case": 0.0545}
    PASS

Exit status 0, wall time under a second.

Negative check: with one digit of object/land_listed.txt changed (the middle digit of the first file of object/ in
sorted order), the same command prints:

    {"S": 26, "USABLE": 188, "frac": 0.1383, "wilson": [0.096, 0.195], "over264": 0.0985, "upper264": 0.3864, "listed_signal": 24, "listed_usable": 86, "unlisted_signal": 2, "fake_rate": 0.027, "fake_worst_case": 0.0545}
    mismatch: sha256 mismatch: object/land_listed.txt
    FAIL

Exit status 1.
