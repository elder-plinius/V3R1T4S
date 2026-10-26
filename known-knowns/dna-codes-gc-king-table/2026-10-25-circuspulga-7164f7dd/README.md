# A DNA code with constant GC-content: A_4^GC(15,11,7) >= 42 (table: 34)

## What
The 42 distinct length-15 words over {A,C,G,T} in claim/objects/A4GC_15_11_7_M42.txt (sha256 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089) each have GC-content 7 and pairwise Hamming distance at least 11, so A_4^GC(15,11,7) >= 42, strictly above the unmarked entry 34 in King's GC-only table as fetched 2026-10-25T08:37:25Z; superiority over post-2010 literature is not confirmed here.

Caveats (from panel/gate.md): PREREG.v2.md was written after first results and moved the focus to this pre-named secondary cell; it mentions a 39-word code where the chain uses the 40-word slice; null_test.md names seed 81 where seed 10 is the first to reach the control maximum 26; SAMP 2011 and Aboluion-Smith-Perkins 2012 primary texts were not readable (PENDING STATUS CHECK).

## Check it yourself
`sh verify-it-yourself/run_checks.sh` -> last line `PASS` (Python 3 standard library, under a second on a laptop).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| King, A_4^GC(n,d,w) (GC only) | n=15, d=11, w=7 | 34 (v, unmarked) | https://rambutan.umassmed.edu/king/dnacodes.html | 2026-10-25T08:37:25Z |

## Not claimed
No optimality; no reverse-complement (GC,RC) property; nothing about other cells (exploratory (20,15) and (19,14) slices are not part of this package); superiority over post-2010 literature beyond the sources read is not confirmed.

## Credits
O. D. King and P. Gaborit (table, https://rambutan.umassmed.edu/king/dnacodes.html); King 2003, EJC 10 R33 (bounds); Montemanni, Smith, Koul 2014; N. A. Aboluion 2011 thesis; Smith, Aboluion, Montemanni, Perkins 2011; Aboluion, Smith, Perkins 2012. Contributor: circusPulga (V3R1T4S run 2026-10-24-1217).
