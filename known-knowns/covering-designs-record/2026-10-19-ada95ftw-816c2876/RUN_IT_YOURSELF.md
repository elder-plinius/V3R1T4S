# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
selftest: Fano covers (0 uncovered), Fano minus a block leaves 3 uncovered, L(7,3,2)=7, L(20,6,3)=64, L(29,5,3)=366: OK
sha256 816c287640bc50f50a87d27707aaae2c77ff99c1580a07336a594d3b94a56bbb object/C29_5_3_399blocks.txt
v=29 k=5 t=3 blocks=399 distinct=399 bad_lines=0 t_subsets=3654 uncovered=0 schonheim=366
VERIFIED C(29,5,3) <= 399
PASS
```
File format: object/C29_5_3_399blocks.txt has 399 lines, each one block of 5 distinct points from 1..29, separated by spaces.

Then compare: open https://coveringrepository.com/ in a browser, go to (v,k,t)-covering designs, and enter v=29, k=5, t=3 (it showed 413 on 2026-10-19). Also look up "C(29,5,3)" in https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json (size 413).

To rebuild the object, see how-we-built-it/README.md (needs ortools, pinned in how-we-built-it/requirements.txt). The rebuild gives the same set of 399 blocks (line order may differ).
