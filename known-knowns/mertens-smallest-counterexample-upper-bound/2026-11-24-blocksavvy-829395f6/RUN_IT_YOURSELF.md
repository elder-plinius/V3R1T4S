# Run it yourself
Fresh shell, from this package folder. Needs python3 (>= 3.8). Standard library only for the default check.

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. The checker parses object/p1_certified_values.json, recomputes the 19-row comparison
with the printed excerpt under rounding and truncation, and requires the 19 (y, k, h) balls to match
verify-it-yourself/expected.json. Expect 8 mismatches under rounding, 6 under truncation, and corrections at
printed precision only for Table 2 rows 1, 4, 12 and 14.

To rebuild the certified values from zeros (optional, about 20 minutes on 3 cores, needs python-flint 0.9.0), see
how-we-built-it/COMMANDS.md. Definitions: how-we-built-it/CLAIM.md, taken from Kim-Nguyen (2.6) and (2.7).
