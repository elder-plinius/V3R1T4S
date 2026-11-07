# Receipts

Run on the author's machine (macOS, Python 3.14.7), 2026-11-07T00:30:45Z, from this folder:

    $ sh verify-it-yourself/run_checks.sh
    {"v4": {"S": 35, "USABLE": 221, "frac": 0.1584, "wilson": [0.116, 0.212], "over264": 0.1326, "upper264": 0.2992, "listed_signal": 33, "listed_usable": 108, "unlisted_signal": 2, "fake_signal": 23, "fake_usable": 437, "fake_rate": 0.0526, "fake_worst_case": 0.0872}, "v5_sensitivity": {"S": 26, "USABLE": 188, "frac": 0.1383, "wilson": [0.096, 0.195], "over264": 0.0985, "upper264": 0.3864, "listed_signal": 24, "listed_usable": 86, "unlisted_signal": 2, "fake_signal": 11, "fake_usable": 407, "fake_rate": 0.027, "fake_worst_case": 0.0545}}
    PASS

Exit status 0, wall time under a second. "v4" is the headline map (object/map.csv); "v5_sensitivity" is the post-hoc
PREREG.v5 map (sensitivity-v5/map.csv).

Negative check: with one digit of object/land_listed.txt changed (the middle digit of the first file of object/ in
sorted order), the same command prints:

    {"v4": {"S": 35, "USABLE": 221, "frac": 0.1584, "wilson": [0.116, 0.212], "over264": 0.1326, "upper264": 0.2992, "listed_signal": 33, "listed_usable": 108, "unlisted_signal": 2, "fake_signal": 23, "fake_usable": 437, "fake_rate": 0.0526, "fake_worst_case": 0.0872}, "v5_sensitivity": {"S": 26, "USABLE": 188, "frac": 0.1383, "wilson": [0.096, 0.195], "over264": 0.0985, "upper264": 0.3864, "listed_signal": 24, "listed_usable": 86, "unlisted_signal": 2, "fake_signal": 11, "fake_usable": 407, "fake_rate": 0.027, "fake_worst_case": 0.0545}}
    mismatch: sha256 mismatch: object/land_listed.txt
    FAIL

Exit status 1.
