# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` (run from the claim folder).

```
sha256 matches INDEX.csv (6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539)
== calibration: the Ma-Tang 14-set must give s = 8 (and be a (4,5)-set)
n=14 bad_4_subsets=0 relations=12 s_branch_and_bound=8 s_exhaustive_2^n=8 ratio=4/7 n_multiple_of_14=True ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== object: n = 21, s = 12 by branch-and-bound and by exhaustive enumeration of all 2^21 subsets
n=21 bad_4_subsets=0 relations=19 s_branch_and_bound=12 s_exhaustive_2^n=12 ratio=4/7 n_multiple_of_14=False ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== negative control: a copy with one element moved to break the (4,5)-property must FAIL
negative control rejected as expected: n=21 bad_4_subsets=1 relations=16 s_branch_and_bound=14 s_exhaustive_2^n=14 ratio=2/3 n_multiple_of_14=False r
ALL CHECKS PASS
```


## Run of 2026-10-18 with the ILP added (orchestrator)

Command: PY=.venv python sh verify-it-yourself/run_checks.sh

    sha256 matches INDEX.csv (6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539)
    == calibration: the Ma-Tang 14-set must give s = 8 (and be a (4,5)-set)
    n=14 bad_4_subsets=0 relations=12 s_branch_and_bound=8 s_exhaustive_2^n=8 ratio=4/7 n_multiple_of_14=True ratio<4/7=False ratio==4/7=True ratio>=9/17=True
    PASS
    == object: n = 21, s = 12 by branch-and-bound and by exhaustive enumeration of all 2^21 subsets
    n=21 bad_4_subsets=0 relations=19 s_branch_and_bound=12 s_exhaustive_2^n=12 ratio=4/7 n_multiple_of_14=False ratio<4/7=False ratio==4/7=True ratio>=9/17=True
    PASS
    == second exact method: ILP (pulp + CBC; needs PY with pulp installed)
    ILP: n=14 relations=12 status=Optimal s(A)=8 returned_subset_is_sidon=True PASS
    ILP: n=21 relations=19 status=Optimal s(A)=12 returned_subset_is_sidon=True PASS
    == negative control: a copy with one element moved to break the (4,5)-property must FAIL
    negative control rejected as expected: n=21 bad_4_subsets=1 relations=16 s_branch_and_bound=14 s_exhaustive_2^n=14 ratio=2/3 n_multiple_of_14=False r
    ALL CHECKS PASS


## Run in this package folder, 2026-10-18 (packager)

Command: `PY=python-with-numpy-and-pulp sh verify-it-yourself/run_checks.sh` (exit 0)

```
sha256 matches INDEX.csv (6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539)
== branch-and-bound and exhaustive enumeration: Ma-Tang 14-set calibration (must give s = 8)
n=14 bad_4_subsets=0 relations=12 s_branch_and_bound=8 s_exhaustive_2^n=8 ratio=4/7 n_multiple_of_14=True ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== branch-and-bound and exhaustive enumeration: object, n = 21, s = 12
n=21 bad_4_subsets=0 relations=19 s_branch_and_bound=12 s_exhaustive_2^n=12 ratio=4/7 n_multiple_of_14=False ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== ILP (needs pulp)
ILP: n=14 relations=12 status=Optimal s(A)=8 returned_subset_is_sidon=True PASS
ILP: n=21 relations=19 status=Optimal s(A)=12 returned_subset_is_sidon=True PASS
== negative control: a copy with elements moved to break the (4,5)-property must FAIL
negative control rejected as expected: n=21 bad_4_subsets=1 relations=16 s_branch_and_bound=14 s_exhaustive_2^n=14 ratio=2/3 n_multiple_of_14=False r
methods that ran: branch-and-bound, exhaustive enumeration, ILP ran
ALL CHECKS PASS
```

### Same run with a python3 that has no pulp (the ILP is skipped, the rest runs)

Command: `PY=/usr/bin/python3 sh verify-it-yourself/run_checks.sh` (exit 0)

```
sha256 matches INDEX.csv (6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539)
== branch-and-bound and exhaustive enumeration: Ma-Tang 14-set calibration (must give s = 8)
n=14 bad_4_subsets=0 relations=12 s_branch_and_bound=8 s_exhaustive_2^n=8 ratio=4/7 n_multiple_of_14=True ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== branch-and-bound and exhaustive enumeration: object, n = 21, s = 12
n=21 bad_4_subsets=0 relations=19 s_branch_and_bound=12 s_exhaustive_2^n=12 ratio=4/7 n_multiple_of_14=False ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== ILP (needs pulp)
ILP SKIPPED: the python package pulp is not installed for /usr/bin/python3 (pip install pulp); the other methods ran above
== negative control: a copy with elements moved to break the (4,5)-property must FAIL
negative control rejected as expected: n=21 bad_4_subsets=1 relations=16 s_branch_and_bound=14 s_exhaustive_2^n=14 ratio=2/3 n_multiple_of_14=False r
methods that ran: branch-and-bound, exhaustive enumeration, ILP skipped
ALL CHECKS THAT RAN PASS (ILP skipped: install pulp to run the criterion's second method)
PASS
```
