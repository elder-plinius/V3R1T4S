# PREREG — written 2026-11-05T00:48:25Z, i.e. AFTER the first computations of this run (calibration,
# pools, enumeration and the dom(Q11) <= 19 bound). Stated honestly; the criterion itself was fixed by the bank.

Criterion: verbatim in target.md (bank). Checker for any lower-bound claim: attempts/checker/code/check.py
(independent of every search program), validated on Lauri's published partitions (dom Q9=15, dom Q10=17,
idom Q11=18: PASS) and on a mutated grid (FAIL).
Lower bound (p1): a grid file whose check.py verdict is PASS for kind dom with K = 19 on n = 11 (or other open pairs).
Upper bound: the bank's literal criterion requires a DRAT/LRAT-checked UNSAT proof; our exhaustive-enumeration + exact
LP-dual argument (attempts/certificate) does NOT meet that literal requirement and is reported as mathematics, not as a
bank partial win.
null_test: not needed because the claims are explicit objects / exact certificates checked deterministically.
