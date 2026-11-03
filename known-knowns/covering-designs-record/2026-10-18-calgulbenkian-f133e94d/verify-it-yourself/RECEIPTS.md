# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` (run from the claim folder).

```
sha256 matches INDEX.csv (f133e94dd68370e1e8001f34d0f021032948f2380962a71e8a4d80b15bee0803)
== check_covering.py: every 3-subset of the 57-set lies in some block
C(57,14,3) b=108 blocks_ok=True covered=29260/29260 PASS sha=f133e94dd68370e1
== schonheim.py
Schonheim L(57,14,3) = 90; blocks b = 108; b >= L: True; parameters within v<=99,k<=25,t<=8: True
SCHONHEIM PASS
== negative control: a copy with one block removed (and b adjusted) must FAIL the coverage check
negative control rejected as expected: C(57,14,3) b=107 blocks_ok=True covered=29192/29260 FAIL sha=515a97be11f66b5a
ALL CHECKS PASS
```


## Run in this package folder, 2026-10-18 (packager)

Command: `PY=python-with-numpy-and-pulp sh verify-it-yourself/run_checks.sh` (exit 0)

```
sha256 matches INDEX.csv (f133e94dd68370e1e8001f34d0f021032948f2380962a71e8a4d80b15bee0803)
== check_covering.py: every 3-subset of the 57-set lies in some block
C(57,14,3) b=108 blocks_ok=True covered=29260/29260 PASS sha=f133e94dd68370e1
== schonheim.py
Schonheim L(57,14,3) = 90; blocks b = 108; b >= L: True; parameters within v<=99,k<=25,t<=8: True
SCHONHEIM PASS
== negative control: a copy with one block removed (and b adjusted) must FAIL the coverage check
negative control rejected as expected: C(57,14,3) b=107 blocks_ok=True covered=29192/29260 FAIL sha=515a97be11f66b5a
ALL CHECKS PASS
```
