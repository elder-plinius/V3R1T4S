# A DNA code with constant GC-content: A_4^GC(19,14,9) >= 44 (table: 38)

## What
The 44-word list in claim/objects/A4GC_19_14_9_M44.txt (sha256 8b28d53b...c1a1a) is a quaternary code of length 19 with exactly 9 G/C per word, all words distinct and minimum Hamming distance 14, so A_4^GC(19,14,9) >= 44, strictly above the unmarked value 38 in the copy of King's table in claim/data/dnacodes.html fetched 2026-10-25T10:17:08Z; post-2010 literature not checked here.

Caveats (from panel/gate.md): this result was first seen in an exploratory sweep (exploratory folder named by hand, started 08:51:32Z) and in an earlier formalization run whose CRITERION failed. This run re-froze a PREREG before regenerating. The null was resumed after an interruption (400 distinct seeds). SAMP 2011, Aboluion-Smith-Perkins 2012 and MS2 2009 primaries were not readable (PENDING STATUS CHECK).

## Check it yourself
`sh verify-it-yourself/run_checks.sh` -> last line `PASS` (Python 3 standard library, under a second on a laptop).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| King, A_4^GC(n,d,w) (GC only) | n=19, d=14, w=9 | 38 (unmarked) | https://rambutan.umassmed.edu/king/dnacodes.html | 2026-10-25T10:17:08Z |

## Not claimed
No optimality; no reverse-complement (GC,RC) property; nothing about other cells (other cells, such as (20,15), are separate submissions); superiority over post-2010 literature beyond the sources read is not confirmed.

## Credits
O. D. King and P. Gaborit (table, https://rambutan.umassmed.edu/king/dnacodes.html); King 2003, EJC 10 R33; Montemanni, Smith, Koul 2014; N. A. Aboluion 2011 thesis; Smith, Aboluion, Montemanni, Perkins 2011; Aboluion, Smith, Perkins 2012. Contributor: circusPulga (V3R1T4S run 2026-10-25-1017).
