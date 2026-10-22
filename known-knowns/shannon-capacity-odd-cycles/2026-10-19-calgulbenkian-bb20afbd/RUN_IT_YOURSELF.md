# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only, no network, single thread):

```sh
sh verify-it-yourself/run_checks.sh
```

The script first checks every file in object/ against SHA256SUMS and prints FAIL if one differs. Then it runs the checker on the schedule and the rules (separation property of every table and code, exact recomputation of M and d, exact comparison with the records), four negative controls (a corrupted table, a changed input, a corrupted base set, a wrong certificate value; each must be rejected), and the further checkers: the base gadget G5 (every axiom, exhaustive), the BPZ Lean C7 schedule as a known answer, a set-level test of the composition rules on explicit vertex sets, box-level axioms at dimension 15 and 30, and the certificates C1 to C4 re-derived from their definitions. It prints the RESULT lines and then ALL CHECKS PASS. It takes about 2 to 3 minutes. Expected last line: ALL CHECKS PASS. Expected first RESULT line:

```
RESULT C7 d=560 M_digits=288 bound=3.25883477557614484751818055569792750605282670056114 headline_margin_vs_tandon_d500=+0.00000215522287853839664150388745206844743910623919 all_records_beaten=True time=0.1s
```

The main checker alone:

```sh
python3 -I verify-it-yourself/shannon_check.py object the-record-we-beat
```

The real output of a full run is in verify-it-yourself/RECEIPTS.md. The written derivation that the schedule is valid under Tandon's Lemma 1 and Theorem 1 is verify-it-yourself/DERIVATION.md; the panel's written re-derivation of the theorems is in panel/criterion.md.

Rebuilding the object: it is a recursion, not a list of words; object/schedule.json is the whole object. The search that found it cannot be reproduced from this package (see how-we-built-it/README.md). The 560-dimensional set (about 10^287 words) is not enumerated.
