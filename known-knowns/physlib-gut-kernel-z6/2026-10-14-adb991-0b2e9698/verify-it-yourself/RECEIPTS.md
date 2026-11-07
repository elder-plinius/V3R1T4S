# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded 2026-10-14T07:27:17Z on the contributor's machine (Linux, 4 cores, 15 GB), PHYSLIB = a Physlib checkout at be0f21e5002d6d73b87f2055530c1e8bf7151546 built with Lean 4 v4.34.1. Machine paths of the checker's scratch folder are shown as [scratch].

## 1. The package as shipped (exit 0, 35 s)

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 0b2e9698935d6a53381d1015fdac67779ff1d6b9761358e79767391d12c1663d
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

## 2. Control: one digit of the object changed (exit 1, 26 s)

The middle ASCII digit of object/InclSMKer.lean (line 86) was changed from 2 to 1 in a copy, the same corruption repo/kit/check_run.py applies to text objects (it does not scan .lean files itself).

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 6d0748807d580a3f36a3d964a9c9ce23e80b37b78dddee2715e376a013c59187
spec compile: exit 0
candidate compile: exit 1
[scratch]/V3R1T4SClaim.lean:86:16: error: Invalid projection: Projections extract constructor fields for one-constructor inductive types. The expression
  h.left
has type `↑x.2.2 ^ 3 • ↑x.2.1 = 1` which has no fields.

problem: candidate does not compile cleanly
FAIL
```
