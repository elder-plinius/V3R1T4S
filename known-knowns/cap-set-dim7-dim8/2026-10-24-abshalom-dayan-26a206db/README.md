# A cap of 1104 points in F_3^9 (cap-set-dim7-dim8, partial win p1)

## What
The file cap_1104_n9.txt (sha256 26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e) is an affine cap of 1104 distinct points in F_3^9, with no three distinct points summing to 0 mod 3, verified exhaustively over all 608,856 pairs; 1104 is strictly larger than every F_3^9 cap size found on 2026-10-24 in the sources p1 names as the panel read them (1082 from the FunSearch notebook and from doubling Edel's 541-cap in PG(8,3), no n = 9 value in X-evolve Table 2 or OEIS A090245, none in arXiv titles and abstracts) and than the unrefereed 1084 of Noirsys/capset, so it meets partial win p1 for dimension 9 and does not meet the main n = 7 or 8 criterion.

Note: the sentence above is the confirmed_scope in panel/gate.md, where the words "and by an exact Fourier count"
were removed after the gate (in both places): the code for that count is not shipped, and the shipped check (verify-it-yourself/capcheck.py) is the
exhaustive pair check.

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's claim folder and work folders. There,
cap_1104_n9.txt is object/cap_1104_n9.txt, CLAIM.md is README.md, REPRODUCE.md is RUN_IT_YOURSELF.md and
checker/capcheck.py is verify-it-yourself/capcheck.py. The FunSearch 512-cap inputs/record_512_n8.txt is not shipped
(how-we-built-it/fetch_512.py downloads it), nor are inputs/verify_structure.py and sources/funsearch-cap_set.ipynb.
Work files and folders named there (for example panel/.work/, mychk/, novelty-fetch/, criterion_fetch/,
criterion_check.py and criterion_extra.py) are not shipped.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERDICT: CAP size 1104 n 9`). Python 3 standard library only; about
5 seconds on a laptop.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Edel's cap table, with the doubling construction (Mukhopadhyay 1978; Theorem 1 of the Bierbrauer-Edel survey) | PG(8,3), so AG(9,3) = 2 x 541 | 541, so 1082 | http://www.yvesedel.de/Matritzen/CAPs/CAPMatIndex.html | 2026-10-24T20:07:59Z and 20:28:35Z |
| FunSearch notebook (Romera-Paredes et al.) | largest known cap set for n = 9 | 1082 | https://raw.githubusercontent.com/google-deepmind/funsearch/main/cap_set/cap_set.ipynb | 2026-10-24T16:41:19Z and 20:18:29Z |
| X-evolve (bank status source), Table 2 | n = 3..8 only | no n = 9 value | https://arxiv.org/html/2508.07932 | 2026-10-24T20:04:23Z |
| OEIS A090245 | exact maxima | through n = 6 only | https://oeis.org/A090245 | 2026-10-24T20:07:27Z |
| Noirsys/capset (unrefereed GitHub repository, created 2026-10-23) | c(9,3) | 1084 | https://github.com/Noirsys/capset | 2026-10-24T20:17:02Z and 20:26:56Z |

1104 > 1084 > 1082. Fetch records, hashes and the extracted cells are in the-record-we-beat/.

## Not claimed
- Nothing for n = 7 or n = 8 (the target's main criterion): the two 512-point slices only tie the FunSearch record.
- Not an optimality claim for n = 9 (arXiv:2601.16917 quotes the upper bound 2070).
- No claim about projective caps in PG(8,3). No point reflection x -> t - x maps the set to itself (overlap at most
  512 of 1104 over all 3^9 values of t), so it is not affinely equivalent to any doubled projective cap and implies
  nothing about PG(8,3).
- No claim about F_3^10. The same lens built a 2368-point cap in F_3^10 from this one, below the published 2432
  (2 x Edel's 1216-cap in PG(9,3)); it is not part of this package.
- "Nothing at 1104 or above was published" rests on the searches listed in panel/novelty.md and panel/criterion.md;
  journals outside arXiv and the MinT database (unreachable on 2026-10-24) were not searched exhaustively.

## Credits
- B. Romera-Paredes et al., "Mathematical discoveries from program search with large language models", Nature 625,
  468-475 (2024) (FunSearch): the 512-cap of F_3^8 that forms two slices of this cap, and the 1082 statement
  (https://github.com/google-deepmind/funsearch).
- Y. Edel and J. Bierbrauer: cap tables, the 541-cap of PG(8,3) behind the 1082, and the survey that states the
  doubling construction as Theorem 1 (http://www.yvesedel.de/).
- A. C. Mukhopadhyay, "Lower bounds on m_t(r,s)", J. Combin. Theory Ser. A 25 (1978) 1-13: the doubling construction.
- A. R. Calderbank and P. C. Fishburn; F. Tyrrell ("New lower bounds for cap sets", arXiv:2209.10045): slice-frame
  (extendable collection) constructions of this kind.
- Karapetyan and Karapetyan (arXiv:2601.16917; CSIT 2023, doi:10.51408/csit2023_30): cap-set bounds for nearby
  dimensions, and the n = 9 upper bound 2070 that they quote.
- Zhai et al., X-evolve (arXiv:2508.07932); OEIS A090245.
- Noirsys/capset (https://github.com/Noirsys/capset): the 1084 claim of 2026-10-23, compared against.
- Google OR-Tools CP-SAT (the exact 80-point slice).
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
