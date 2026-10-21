# Run it yourself

All commands run from this package folder in a fresh shell. Python 3.8+ required.
`verify-it-yourself/check.py` is standard-library only; the full n=15 recomputation below needs numpy.

## 1. The fast standalone check (~70 s, stdlib)

```
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. This brute-forces the definition (n=1..3), reproduces published terms
n=1..10 with an independent pure-Python transfer matrix, and CRT-reconstructs the n=15 value from
object/residues.txt (with the CRT-bound and prime-disjointness checks). If numpy is installed it also
recomputes one n=15 residue from scratch.

## 2. Reproduce every published term n=1..14 (~35 s, needs numpy)

```
cd how-we-built-it
python3 reproduce.py          # checks against https://oeis.org/A054759/b054759.txt (sha256 26a83711...); do NOT use python3 -I
```
Expected: each n=1..14 prints `OK`, final line `RESULT: ALL MATCH`.

## 3. The full two-run computation of a(15) (~12 min, needs numpy)

```
cd how-we-built-it
python3 n15.py
```
Expected: `RUN_A CRT value` and `RUN_B CRT value` both equal
`4310182149988584261406143524214457416387448`, `AGREE: True`, and
`RUN_A modulus (220 bits) > a*2^64 (206 bits)? True`.
RUN_A uses a forward vertex encoding + closed-form entry with 11 primes just below 2^20; RUN_B uses a
reversed encoding + explicit-walk entry with 12 DISJOINT primes just below 2^19. The two agree digit
for digit.

## 4. Independent self-break (~5 s, stdlib)

```
cd how-we-built-it
python3 break.py ../object/residues.txt
```
(The residues file is `object/residues.txt` in this package.) `break.py` does a full edge-orientation
brute force (n=1..3), an independent non-sector transfer matrix (n=1..8), independent CRT of the
recorded residues, and prints the growth-clause numbers literally.

## How the object was rebuilt
`object/a054759_15.txt` is the integer; `object/residues.txt` holds the 23 (run, prime, residue) rows
whose CRT reconstructs it. Rebuild from scratch with step 3.
