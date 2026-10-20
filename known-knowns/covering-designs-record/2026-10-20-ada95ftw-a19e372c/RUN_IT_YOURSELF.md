# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
selftest: Fano covers (0 uncovered), Fano minus a block leaves 3 uncovered, L(7,3,2)=7, L(20,6,3)=64, L(29,5,3)=366, L(35,5,3)=658: OK
sha256 a19e372c3611962126c615fd73a79e8c023e2f7369b38aa29f12ca00e2181149 object/C35_5_3_713blocks.txt
v=35 k=5 t=3 blocks=713 distinct=713 bad_lines=0 t_subsets=6545 uncovered=0 schonheim=658
VERIFIED C(35,5,3) <= 713
PASS
```
File format: object/C35_5_3_713blocks.txt has 713 lines, each one block of 5 distinct points from 1..35, separated by spaces.

Then compare: open https://coveringrepository.com/systems.aspx in a browser, choose V=35, K=5, T=3, M=3 and press Search (it showed 732 on 2026-10-20), or find the line `35 05 03 03 732` in https://coveringrepository.com/download_archive_vkt.aspx . Also look up "C(35,5,3)" in https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json (size 733) and in the Zenodo LJCR v1.2 coverdata.json (size 732).

To rebuild the object, see how-we-built-it/README.md (needs numpy and ortools, pinned in how-we-built-it/requirements.txt). The rebuild gives the same set of 713 blocks (line order may differ), in about 15 s.
