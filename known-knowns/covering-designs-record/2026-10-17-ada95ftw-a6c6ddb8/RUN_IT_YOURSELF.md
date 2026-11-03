# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
selftest: Fano covers (0 uncovered), Fano minus a block leaves 3 uncovered, L(7,3,2)=7, L(20,6,3)=64: OK
sha256 a6c6ddb8d095dc3818d1eb09a2a2342cfa3254b443799c213068aff07d2a4c6f object/C20_6_3_70blocks.txt
v=20 k=6 t=3 blocks=70 distinct=70 bad_lines=0 t_subsets=1140 uncovered=0 schonheim=64
VERIFIED C(20,6,3) <= 70
PASS
```
File format: object/C20_6_3_70blocks.txt has 70 lines, each one block of 6 distinct points from 1..20, separated by spaces.

Then compare: open https://coveringrepository.com/ in a browser, go to (v,k,t)-covering designs, and enter v=20, k=6, t=3 (it showed 71 on 2026-10-17). Also look up "C(20,6,3)" in https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json (size 71).

To rebuild the object, see how-we-built-it/README.md (needs ortools, pinned in how-we-built-it/requirements.txt). The rebuild gives an isomorphic copy, though not always the same labelling.
