# RECEIPTS: real output of sh verify-it-yourself/run_checks.sh

run at 2026-10-24T18:07:57Z (UTC), about 41 seconds on a laptop (Apple M4 Pro, Python 3.14)

```
47419363a41b203879fe8ae93035fe231852f01eb3081ad15c306a91d1e3298a u.txt
dbf5c154ad97f11abdefd3d7d9ff1fda723a49710e881124bc547299308a93fa v.txt
797187bb905b8ee0dd22f321b802a1009938e2b4905517c1ffa7c576749bfacb w.txt
== exact Brent-equation check (check_scheme.py)
format <18,19,19>, 3424 terms, every term with three nonzero factors, common denominator 352800, 42224004 Brent equations checked, 0 wrong
rank 3424 scheme for <18,19,19> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 342 entries of C differ from AB
trial 2: 0 of 342 entries of C differ from AB
trial 3: 0 of 342 entries of C differ from AB
PASS
PASS
```
