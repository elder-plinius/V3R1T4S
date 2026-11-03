# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
selftest: Fano covers (0 uncovered), Fano minus a block leaves 3 uncovered, L(7,3,2)=7, L(20,6,3)=64, L(29,5,3)=366, L(35,5,3)=658, L(36,5,3)=756: OK
sha256 f7a9401c9fc3e6db6721b7eee490dbad8a7cb95bf6a9e8d0de9bcf7851da6b23 object/C36_5_3_812.txt
v=36 k=5 t=3 blocks=812 distinct=812 bad_lines=0 t_subsets=7140 uncovered=0 schonheim=756
VERIFIED C(36,5,3) <= 812
PASS
```
File format: object/C36_5_3_812.txt has 812 lines, each one block of 5 distinct points from 1..36, separated by spaces.

Then compare: open https://coveringrepository.com/systems.aspx in a browser, choose V=36, K=5, T=3, M=3 and press Search (it showed 821 on 2026-10-20), or find the line `36 05 03 03 821` in https://coveringrepository.com/download_archive_vkt.aspx . Also look up "C(36,5,3)" in https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json and in the Zenodo LJCR v1.2 coverdata.json (size 821 in both).

To rebuild the object, see how-we-built-it/README.md (needs numpy and ortools, pinned in how-we-built-it/requirements.txt). The rebuild gives the same 812 blocks in about 13 s (on 2026-10-20 the output file was byte-identical to object/C36_5_3_812.txt).
