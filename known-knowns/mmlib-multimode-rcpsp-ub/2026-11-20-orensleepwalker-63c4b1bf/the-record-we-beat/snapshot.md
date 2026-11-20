# What these results are compared against

Status source (the bank's status_source): http://solutionsupdate.ugent.be/mrcpsp, fetched 2026-11-20T10:14:46Z, HTTP 200, page sha256 1124afbea346b1da102647427ce8c6a91edb286da7924e73c13f5c7575a083bf; it lists MMplus with 3,240 instances, 1,965 open.

Per-instance values (SolutionsUpdate dataset MMplus), fetched at the same time, HTTP 200:
- http://solutionsupdate.ugent.be/sites/default/files/datasets/MMplus_2.csv (sha256 f76dbba5f90f1cef0072ed1c488235aa426233b96d80cb84c1d3ad2d60494e86): LB value, UB value, UB ref.
- http://solutionsupdate.ugent.be/sites/default/files/datasets/MMplus_2_BKS.csv (sha256 21378ab18d8cd136d9dda24c7a186ecc09d0cacfbbd99a05533b14233c86f70d): best-known value per instance.
Re-fetched by the NOVELTY reviewer at 2026-11-20T10:41:46Z: byte-identical (panel/novelty.md).

Release: MMLIB GitHub release v2.1 (published 2026-06-23), asset MMLIB_v2_1.zip, sha256 4f6f5318fcbc01943ec74dfbf8b16afc25b65759963666f631d6cdd2f242fecd (equal to the digest GitHub publishes); its Excel 'MMLIB (Parameters and BKS).xlsx', sheet MMLIB+, column UB-lit.

The cells compared against, for each of the 30 instances, are in values.csv (Excel UB-lit is read from the release by the checker). UB holders by the dataset's reference list: 1 Coelho and Vanhoucke 2011; 5 Etminaniesfahani, Gu, Moslemi Naeni and Salehipour 2023; 7 Shichen Tian 2026; 8 mmlib.eu 2018 ('several authors').
