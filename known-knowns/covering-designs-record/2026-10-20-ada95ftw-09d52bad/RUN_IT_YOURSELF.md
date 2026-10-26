# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
selftest: Fano covers (0 uncovered), Fano minus a block leaves 3 uncovered, L(7,3,2)=7, L(20,6,3)=64, L(29,5,3)=366, L(38,6,3)=425: OK
sha256 09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b object/C38_6_3_469blocks.txt
v=38 k=6 t=3 blocks=469 distinct=469 bad_lines=0 t_subsets=8436 uncovered=0 schonheim=425
VERIFIED C(38,6,3) <= 469
PASS
```
File format: object/C38_6_3_469blocks.txt has 469 lines, each one block of 6 distinct points from 1..38, separated by spaces.

Then compare: open https://coveringrepository.com/ in a browser, go to (v,k,t)-covering designs, and enter v=38, k=6, t=3 (it showed 510 on 2026-10-20), or find the line `38 06 03 03 510` in https://coveringrepository.com/download_archive_vkt.aspx . Also look up "C(38,6,3)" in https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json (size 510).

To rebuild a design of the same size, see how-we-built-it/README.md (needs numpy and ortools, pinned in how-we-built-it/requirements.txt). The rebuild prints `OPTIMAL blocks 469` for both PSL(2,7) 24+14 G-sets; the rebuilt block set can differ from the object (the MIP has several optimal orbit choices) but has the same size and passes the same checker.
