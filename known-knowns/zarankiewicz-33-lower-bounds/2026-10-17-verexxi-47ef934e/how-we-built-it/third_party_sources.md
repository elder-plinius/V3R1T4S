# Third-party files (not copied into this package)

These files belong to other people. They were used by the scripts in this folder and were removed from the package; this table says
where each came from and the sha256 it must have. `python fetch_third_party.py` downloads them to the place the scripts expect
(baseline/wit/ and status_source/), checks every sha256 and stops on the first mismatch. Machine-readable copy: third_party_sources.json.
Nothing in verify-it-yourself/ needs any of them.

| file (relative to how-we-built-it/) | URL | sha256 |
|---|---|---|
| baseline/wit/z12_19_114_witness_verified.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/z12_18_21/data/z12_19_114_witness_verified.csv | 58d70937690d5f8d06cbf948a8d6193619cc0cdbb1fbc58cee9187b2710d15a9 |
| baseline/wit/z12_22_132_witness_verified.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/z12_18_21/data/z12_22_132_witness_verified.csv | cdbe85e5bb25f6c1caeab8120862a8c46350ce7f4c0a94d43bc0e850316e16dc |
| baseline/wit/z13_18_116_witness.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/data/z13_18_116_witness.csv | 2e096d73bc4571b497dd32613196062cde5170752e2bcbbc02b2ee7b496cfa18 |
| baseline/wit/z14_17_118_witness.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/data/z14_17_118_witness.csv | e7dae839eaf41b0d3c0e88359bc77cb43c285586a500cb7fa9f6e2e546283d6a |
| baseline/wit/z14_18_124_witness.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/data/z14_18_124_witness.csv | 7ab12773f1673ac5c87f9d9fc87221a8a566da35a815b63231e3469b74677429 |
| baseline/wit/z15_17_126_witness.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/data/z15_17_126_witness.csv | 3ce1435a34501a38be14aab9dd68b719b84f8e24220f9ccef81615515fa16e2e |
| baseline/wit/z15_18_132_witness.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/data/z15_18_132_witness.csv | ce4a324e5f65e464649f79426c72cfb2dca098093555826ce0c51e2ad095d690 |
| baseline/wit/z16_17_132_witness_seed201.csv | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/data/z16_17_132_witness_seed201.csv | 28140fe0d4aeb0ad3a85d352da8884cbe432629c2f82ac3a08fd405314d893ec |
| baseline/wit/z13_22_137_blocks.json | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/data/z13_22_137_blocks.json | 2bed49d7d128bc64cce1ab06dad45e37a1c5a33c9f929cbd328c3c1c6a41fcc0 |
| status_source/gh_frontier_propagation.json | https://raw.githubusercontent.com/KAVentures/z1322-exact/main/proof/frontier_closure/reports/frontier_propagation.json | d97267968b917a91fb34ff9bc3fb35c7eaf1753c7b888d9294b0bfef43ef0b22 |
| status_source/df_new_bounds.json | https://raw.githubusercontent.com/dfield/finite-zarankiewicz-closures/main/analysis/new_bounds.json | 5e81604e93be9794db9f17e8256edf1c31bcea5b353f5ce9eb12db404221e11f |
| status_source/df_extended.json | https://raw.githubusercontent.com/dfield/finite-zarankiewicz-closures/main/analysis/extended_results.json | 8bd98d0425193857672f209b5b60322b0281be2362ad008d1e905ff949639971 |
| baseline/wit/sau_13x19_118.txt | https://arxiv.org/html/2608.26603v1 | ab88b1ffcc0f135f75b7ba97318cdda00153db44093e6f70756b346af78fd0e0 |
| baseline/wit/sau_14x19_126.txt | https://arxiv.org/html/2608.26603v1 | 4ada525626b73ad6b0aca6236217fb803d220c1299294db15461e87875db9fee |
| baseline/wit/sau_16x18_136.txt | https://arxiv.org/html/2608.26603v1 | 5c3f131995b144d6b7609830ab687231e819bae780c129eaf6f730355bdd1bda |

## Saurabh's three matrices (arXiv:2608.26603 v1, Appendix A)
The page https://arxiv.org/html/2608.26603v1 prints each matrix in a `pre` block (class `ltx_verbatim`), one row per line, characters 0 and 1.
The first three such blocks, in page order, are 13 x 19 (118 ones), 14 x 19 (126 ones) and 16 x 18 (136 ones). The script takes the lines of
each block and writes them to a text file (rows joined by newlines, one final newline); the sha256 above is of that text file. The scout's
saved copy of the page had sha256 d1f6e36952103e36504d5591d20250d7facb6592a9d9a8d418d755af7813be90 (informational; the script checks the extracted matrices).

## Verification
- All 15 URLs were fetched with fetch_third_party.py on 2026-10-17T16:36Z; every file matched its sha256 above (output: ALL THIRD-PARTY FILES OK).
- The GitHub URLs use the branch `main` (no commit SHA recorded); the sha256 pins the content, so if a repository later changes a file the script stops with a mismatch.
