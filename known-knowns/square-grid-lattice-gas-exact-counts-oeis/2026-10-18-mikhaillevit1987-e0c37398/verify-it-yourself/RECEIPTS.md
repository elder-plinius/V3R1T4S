# Receipts (real output of `sh verify-it-yourself/run_checks.sh`, 2026-10-18, Python 3.10, Windows Git sh)

```
== sha256 of the object
e0c37398f08f335e03cc8f76222b70ac3f351f7475fd6508f1367b1e4db17385
== checker on the object (must be VALID)
claimed a(16) = 2781781827849835218619790131266486746689884618378 (49 digits)
independent row transfer matrix, n = 1..9: match
author mode A (claim/checker ice.rs, full symmetry)        moduli ok, product 2^247, residues match
author mode B (ice.rs, reversed sweep, shifts only)        moduli ok, product 2^243, residues match
skeptic own checker, dihedral+complement, set A            moduli ok, product 2^311, residues match
skeptic own checker, rotations only, set B                 moduli ok, product 2^311, residues match
author ice.rs mode A on skeptic fresh primes, set F        moduli ok, product 2^247, residues match
runs that alone determine a(16) (modulus > 2^272): 2
VALID
== checker on a corrupted copy (last digit changed; must be INVALID)
corrupted copy rejected
PASS
exit code 0
```
