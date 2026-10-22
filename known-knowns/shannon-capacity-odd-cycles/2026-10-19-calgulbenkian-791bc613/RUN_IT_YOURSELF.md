# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only, no network):

```sh
sh verify-it-yourself/run_checks.sh
```

The script first checks every file in object/ against SHA256SUMS and prints FAIL if one differs. Then it runs the checker on the schedule and the rules, runs two negative controls (a corrupted table and a changed input, both must be rejected) and prints a RESULT line and then ALL CHECKS PASS. Expected last line: ALL CHECKS PASS. Expected RESULT line:

```
RESULT C23 d=2928 M_digits=3088 bound=11.33455800536622830135329115399285797338312702840016 headline_margin_vs_bpz_lean=+0.00000008261171015172020100791294991706509008814509 all_records_beaten=True time=18.6s
```

The checker alone:

```sh
python3 -I verify-it-yourself/shannon_check.py object the-record-we-beat
```

What it does: (1) compares the label separation relation (22 ordered pairs) with Definition 4 of Tandon's paper; (2) checks Definition 6 for every substitution table and terminal code the schedule uses; (3) recomputes the integer M and the degree d from object/schedule.json, starting from the base seven-family vector taken from the BPZ Lean data; (4) compares them with the contributor's file; (5) computes the certified 50-digit floor of M^(1/d) and compares it by exact integer arithmetic with the records in the-record-we-beat/records.json. It also recomputes the Lean repository's own integer from the Lean schedule as a known-answer test.

Rebuilding the object: it is a recursion, not a list of words; object/schedule.json is the whole object. The search that found it cannot be reproduced from this package (see how-we-built-it/README.md).
