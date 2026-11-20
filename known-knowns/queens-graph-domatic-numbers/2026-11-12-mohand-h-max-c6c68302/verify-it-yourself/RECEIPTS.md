# Receipts

Output of `sh verify-it-yourself/run_checks.sh` (exit code 0):

```
certificate sha256 c6c683024171c1fc2a95a3f8699d1d353f358c603c555fcd743941f15b67e13d OK
enc1 manifest sha256 OK
  enc1: encoder 196686 clauses, base formula 163030 clauses (sha256 of its DIMACS text e08e926ce30272fa64f0524d5d0325ae1c0d1f5390b6cd16bd54e6a6c87dda3f)
  enc1: 680 formulas rebuilt (34 per class, 20 classes); 680 equal to the manifest (sha256), recorded as VERIFIED and composed as described; 0 not; 0 manifest lines without a rebuilt formula; 4s
  REGEN enc1: PASS
enc1 chain formulas and base formula rebuilt from the generator: OK
enc2 manifest sha256 OK
  enc2: encoder 170805 clauses, base formula 160850 clauses (sha256 of its DIMACS text 30a7518ba31872fb8a1dbd962f4eaa855b19428fd9a0e87ee53e03d1876e37ce)
  enc2: 680 formulas rebuilt (34 per class, 20 classes); 680 equal to the manifest (sha256), recorded as VERIFIED and composed as described; 0 not; 0 manifest lines without a rebuilt formula; 4s
  REGEN enc2: PASS
enc2 chain formulas and base formula rebuilt from the generator: OK
PASS
```
