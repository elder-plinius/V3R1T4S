# A_4^GC(10,7,5) >= 44: a DNA code with constant GC-content beating King's table (34)

## What
The 44 words in claim/gc_n10_d7_m44.txt form a length-10 quaternary code with exactly 5 G/C per word, all words distinct, and minimum plain Hamming distance 7, which strictly exceeds the unmarked entry 34^v for A_4^GC(10,7,5) in the GC (non-RC) table of claim/king_table_live_refetch.html (re-fetched 2026-10-19T16:38:28Z); post-2010 novelty is not covered.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS` (the line before it: `VALID size=44 table=34 BEATS`). Takes under a second on a laptop.

## Compared to
King's table of lower bounds for DNA codes with constant GC-content, https://rambutan.umassmed.edu/king/dnacodes.html,
first table, cell (n,d) = (10,7): 34 (superscript v), fetched 2026-10-19T17:06:28Z (HTTP 200). Details in the-record-we-beat/RECORD.md.
Also below Montemanni-Smith-Koul 2014 (Table 1: 34) and the Aboluion 2011 thesis (Table 10.69: 34).

## Not claimed
- Not optimal: no upper bound is claimed; the true maximum may be larger than 44.
- Only the plain GC-content table (Hamming distance only), not the GC,RC (reverse-complement) table.
- The search that found it was time-limited (600 s branch and bound over symmetric orbits). Rerunning it may give a different code; the claim is the object, which is checked deterministically.
- No claim about any other cell.

## Credits
- Oliver D. King, the table above, and "Bounds for DNA codes with constant GC-content", Electron. J. Combin. 10 (2003) R33, https://arxiv.org/abs/math/0306197 (the GC-content convention w = n/2 and the Plotkin-type bound used while exploring).
- Philippe Gaborit and Oliver D. King, "Linear constructions for DNA codes", Theoret. Comput. Sci. 334 (2005) 99-113.
- Roberto Montemanni and Derek H. Smith, the variable neighbourhood search value 34 in this cell (J. Math. Model. Algorithms 7 (2008) 311-326; MIC 2009), and Montemanni, Smith and Koul, LNMS 6 (2014) 167-175.
- Yeow Meng Chee and San Ling, "Improved lower bounds for constant GC-content DNA codes", IEEE Trans. Inf. Theory 54 (2008) 391-394.
- Niema Aboluion, PhD thesis (University of Glamorgan, 2011), and D. H. Smith, N. Aboluion, R. Montemanni and S. Perkins, Discrete Math. 311 (2011).
- Credit for this result: zubair_r (a V3R1T4S run).
