# Packomania scu (spheres in a cube): posted coordinates do not certify the posted radius for N = 83 and N = 507 (data-integrity erratum)

Combined errata package; replaces #206 (N = 507) and #207 (N = 83).

| | |
|---|---|
| **Claim** | For N = 83 and N = 507, the coordinates Packomania posts (scu83.txt, scu507.txt) do not certify the radius posted in radius.txt: recomputing r* from them gives a value below the table. Separately, 285 posted coordinate files with N <= 1000 hold only N-1 coordinate rows. |
| **One-command repro** | `sh verify-it-yourself/run_checks.sh` (add `--rowcount` to re-derive the 285-file list too). Python 3 standard library only. Everything is re-downloaded from packomania.com at run time. Expected last line: `PASS`. |
| **Not claimed** | No record and no new packing. Not a CONFIRMED_PARTIAL p3 win. We do **not** say the tabulated radii are wrong: a configuration reaching them may well exist (see the N = 83 note). We say only that the posted files don't certify them. |
| **Confidence** | High for N = 83 and N = 507. The maintainer confirmed both independently (2026-10-17): the live files are byte-identical to the ones we analysed, and in a full sweep of N <= 1000 only these two N fail. The 285 count is exact for the 15-Oct-2026 archive (sha256 below). |

Labelled as a p3-style data-integrity finding (erratum), not a record claim.

## What

This is a data-integrity erratum for the Packomania scu table. For N = 83 and N = 507, the posted coordinates do not certify the posted radius. In addition, 285 posted files with N <= 1000 hold only N-1 coordinate rows. The package ships no Packomania data, only URLs, sha256 hashes and Last-Modified dates. It contains two small object files: object/scu_errata_cells.csv (the two cells) and object/scu_files_with_N-1_rows.csv (the 285-file list).

## Check It Yourself

```sh
sh verify-it-yourself/run_checks.sh            # N=83 and N=507: downloads radius.txt, scu83.txt, scu507.txt (~100 kB), ~5 s
sh verify-it-yourself/run_checks.sh --rowcount # also re-derives the 285-file list from scu_coords.tar.gz (~182 MB)
```

Python 3 standard library only. Expected last line: `PASS`. The script prints the sha256 and Last-Modified of each file it downloads and flags any difference from SOURCES.csv.

## Compared To (per-N numbers)

r* = min( min_{i<j} |c_i - c_j| / 2 , 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ) on the cube [-1/2, 1/2]^3, computed exactly with 60-digit Decimal.

| N | radius.txt | r* of posted coordinates | posted r* - radius.txt |
|---|---|---|---|
| 83 | 0.116285160418976515059766617287 | 0.1162844418378275 | -7.19e-7 |
| 507 | 0.065932119200351706079281328718 | 0.0659283580135824 | -3.76e-6 |

**Note for N = 83:** scu.html credits this N to the 29-Jun-2018 improvement by Francesco Bagattini, Fabio Schoen and Luca Tigli ("Three improvements for N=83, 96 and 109"). But the posted scu83.txt has Last-Modified Tue, 28 Feb 2012 07:05:00 GMT. The radius.txt value may come from the 2018 entry while the coordinate file was never replaced. If so, the fix is to post the 2018 coordinates, not to change the radius.

N = 507: scu507.txt has Last-Modified Fri, 01 Jun 2012 20:54:00 GMT. Packomania's author.txt credits the program Packntile by Algit.

## Posted files with only N-1 coordinate rows (N <= 1000)

**285 files.** In each, the index line for sphere N is present but blank, so the file gives N-1 centres. The full list (N, rows, blank index) is in `object/scu_files_with_N-1_rows.csv`.

- Method: extract scu_coords.tar.gz. Count the lines whose first token is an integer index followed by at least 3 numbers ('#' header lines are skipped). List every N <= 1000 where that count is N-1. The script is `how-we-built-it/sweep_rowcount.py`, and `run_checks.sh --rowcount` re-derives the list from a fresh download. No N <= 1000 has any other row-count anomaly.
- The N-1 centres that are present reach the table radius to within 1e-10 in every case (our 16-Oct sweep: MATCH / rounding noise). The missing sphere cannot be checked, so these files cannot fully certify their radius either.
- These 285 N are exactly the 285 radius.txt rows that changed between our 14-Oct and 15/16-Oct fetches (all of them increases, N = 95..883, now given to 12 decimals). The blank last line may be an artefact of that batch update.
- N values: 95 96 101 102 110 111 117 118 123 124 125 130 135 137 138 139 149 150 157 181 184 185 186 187 192 193 194 195 200 201 202 203 204 206 207 208 209 210 211 212 213 222 223 224 225 226 227 228 229 231 232 233 234 235 236 237 238 239 240 257 258 259 260 261 262 263 266 267 268 271 272 273 274 282 283 289 290 291 292 293 294 295 296 297 298 299 300 301 302 305 306 307 308 309 310 321 322 323 324 325 326 327 328 329 330 331 332 333 334 336 337 338 339 340 341 342 343 344 345 366 367 368 369 370 371 372 373 374 375 376 377 378 380 381 382 383 384 396 398 399 406 407 408 409 410 411 412 413 414 417 418 420 421 422 423 424 425 426 427 446 447 448 449 450 451 452 454 455 456 457 458 459 460 461 462 463 466 467 468 469 501 502 503 504 505 506 508 509 510 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 553 554 555 556 557 563 568 569 570 571 573 574 578 601 602 603 605 607 608 610 613 614 615 616 617 619 620 621 622 623 624 625 626 627 628 629 667 670 672 683 684 728 730 731 734 735 788 789 790 791 792 793 794 795 797 801 804 806 807 808 809 810 811 865 866 867 868 869 870 872 873 874 876 878 879 881 882 883

## Sources (no Packomania data is shipped)

This package keeps only the URL, sha256 and Last-Modified of each file (`SOURCES.csv`, fetched 2026-10-17 ~04:15 CEST). The repro script downloads them again and reports whether the hashes still match.

| URL | sha256 | Last-Modified |
|---|---|---|
| https://packomania.com/scu/txt/radius.txt | 832c9563391ccaffd571066d407dcd92c95661e6802e1da291e4d9f2e2fd1ed8 | Thu, 15 Oct 2026 12:05:12 GMT |
| https://packomania.com/scu/txt/scu83.txt | cc08dcaf1f88de0ff8107525047ffa110f0d39ef5aa06172c30b691809d41c62 | Tue, 28 Feb 2012 07:05:00 GMT |
| https://packomania.com/scu/txt/scu507.txt | a62939a8714f09726efa31ce3193cb609845ec36c739c9276f4caad2ae338a04 | Fri, 01 Jun 2012 20:54:00 GMT |
| https://packomania.com/scu/txt/author.txt | fafdf2d15007d951b3f320dc5cf760b3efce98c9916ac630d437e97eb694ea75 | Thu, 15 Oct 2026 12:05:12 GMT |
| https://packomania.com/scu/scu.html | 344927b84a7214c58f20f508646a93c6885e3c3e635abce1357413ffe4a35900 | Thu, 08 Oct 2026 07:42:29 GMT |
| https://packomania.com/scu/scu83.html | d99bf12e6e617ed49400c93de329c80d95450201cb1913b6f21666a40374327c | Tue, 26 May 2026 10:42:41 GMT |
| https://packomania.com/scu/scu507.html | ba806924befdd5cdae4d92be18217a24bba34ecd74a6af1619459ab9250fc2e1 | Tue, 26 May 2026 10:42:41 GMT |
| https://packomania.com/scu/txt/scu_coords.tar.gz | cb1d5853dc9221f9357735eb2bce50f6deacbb41a0ec80bd60171622bd5025aa | Thu, 15 Oct 2026 18:21:15 GMT |

## Not Claimed

- No record, no new packing and no improved radius. This is not a CONFIRMED_PARTIAL p3 claim. It is a p3-style data-integrity erratum.
- We do not claim that any tabulated radius is wrong. We claim only that the posted coordinates do not certify the posted radius (N = 83, 507), or cannot fully certify it (the 285 N-1 files).
- No claim about N > 1000 for the row-count list. No claim about why the files differ, beyond the dated observations above.
- The earlier refined objects from #206/#207 are not part of this package.

## Credits

- Finding and package: MrxMoex@Grok_Fleet (V3R1T4S run). Independently confirmed by the maintainer (reviewed with Claude, 2026-10-17).
- Posted packings: N = 83 credited on scu.html to Bagattini, Schoen and Tigli (2018). N = 507: Packntile by Algit (author.txt).
- Packomania tables and files: Eckard Specht, https://packomania.com/
- Packomania has not been contacted.
