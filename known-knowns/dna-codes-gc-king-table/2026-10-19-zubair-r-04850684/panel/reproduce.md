# REPRODUCE skeptic: claim n10_d7

context: subagent (Claude Code Agent tool, general-purpose)

Scope: only files under claim/ (the review folder, not included in this package). All paths below are relative to claim/ (the review folder, not included in this package).

## Definition checked (quoted)
From CLAIM.md [not included in this package], success criterion (verbatim from the bank):
> "a checker confirms all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2), confirm from King 2003), pairwise Hamming distance >= d, are distinct, and the count is strictly greater than the table entry re-fetched live immediately before claiming"

Here n=10, d=7, w=floor(10/2)=5. King 2003 (king2003_source.tex [King 2003, arXiv math/0306197; not included in this package], sha256 efcafba5...c5423), remark after Table 2:
> "lower bounds for $A_4^{GC}(n,d,w)$ are given for $4 \leq n \leq 20$ ($n$ odd or even) with $w = d = \lfloor n/2 \rfloor.$"
and line 748: "Table 2. Lower bounds for $A_4^{GC}(n,d,w)$ with $n \leq 12$ ($n$ ..." (even n, w = n/2). For n=10, w=5 is unambiguous.

## 1. Independent checker (written from the definition before opening verify-it-yourself/check_gc_code.py or how-we-built-it/blockcyc.c)
Written in a temporary directory outside claim/ (the review folder, not included in this package), run as `python3 -I mycheck.py object/gc_n10_d7_m44.txt`. It also checks closure under
the map rot(x) = x[1:5]+x[0] + x[6:10]+x[5] (Z_5 rotating both 5-coordinate blocks simultaneously) and its inverse, and counts orbits.
Real output:
```
count 44
all length 10: True
alphabet ACGT: True
GC=5 each: True
distinct: True
min pairwise distance: 7 >=7: True
closed under Z5 block rotation: True
orbits: 12 sizes: [1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5]
closed under inverse rotation: True
bytes 484 lines 44
```
All six required properties hold: length 10, ACGT, exactly 5 G/C, distinct, all pairwise distances >= 7 (minimum exactly 7, all C(44,2)=946 pairs checked exhaustively), 44 words.
Orbit structure 4x1 + 8x5 = 44 matches how-we-built-it/generation_log.txt ("max_weight_clique=44 orbits=12").

## 2. Table value from the live re-fetch
Parsed the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md] with an HTMLParser script (table index taken from the preceding <h3>). Output:
```
0 'Lower bounds for A4GC(n,d,w):'
1 'Lower bounds for A4GC,RC(n,d,w):'
header: ['n\\d', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
row n=10: ['10', '10622m', '2016v', '504x', '116c', '34v', '16.l', '5.l', '4.p', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
cell (10,7) text: '34v'
value 34 marker '' sup v
```
Raw HTML row from the FIRST (GC, not GC,RC) table:
`<tr><td> <b>10</b> </td><td>  10622<sup>m  </sup></td><td>  2016<sup>v  </sup></td><td>  504<sup>x  </sup></td><td>  116<sup>c  </sup></td><td>  34<sup>v  </sup></td><td>  16.<sup>l  </sup></td><td>  5.<sup>l   </sup></td><td>  4.<sup>p  </sup></td>...`
Cell (n=10, d=7) = 34, superscript v, no '.' or ':'. 44 > 34.
sha256 of the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md] = 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5, matching CLAIM.md [not included in this package].

## 3. Author's checker (as in the claim's REPRODUCE.md [not included in this package]) and hash
```
$ python3 -I verify-it-yourself/check_gc_code.py object/gc_n10_d7_m44.txt 10 7 34
VALID size=44 table=34 BEATS
exit 0
$ sha256sum object/gc_n10_d7_m44.txt
0485068437ba81d686653091506861e00512c0fb462b7f775b901d5fec154ed8  object/gc_n10_d7_m44.txt
```
Output equals the expected line; hash equals the stated sha256. Reading verify-it-yourself/check_gc_code.py afterwards: it implements the same
definition (w = n//2, ACGT, exact GC count, distinctness, all pairs >= d). Both checkers run three times gave byte-identical
combined output (sha256 3b1857a0...22b5 each time): checking is deterministic.

## 4. Orbit-union statement
CLAIM.md [not included in this package]: "Z_5 rotating each of the 2 blocks of 5 consecutive coordinates simultaneously ... The code is a union of G-orbits."
Confirmed: the code is closed under that map and its inverse; it splits into 12 orbits (4 fixed points, e.g. CCCCCAAAAA and
GGGGGTTTTT, plus 8 full orbits of size 5).

## 5. Reproducibility / non-determinism declaration
The object is a fixed file with a stated hash, and its verification is exhaustive and deterministic; reproducibility is judged on
that and it passes. The generator was not re-run (not required: the claim is the object). The declaration in CLAIM.md [not included in this package] and
the claim's REPRODUCE.md [not included in this package] that regeneration is time-limited (600 s branch and bound, log shows "TIMEOUT: lower bound only, not exhaustive")
and, with OpenMP dynamic scheduling, may yield a different code or size is honest and consistent with how-we-built-it/generation_log.txt. It is
sufficient because no claim rests on regeneration: the generator is only provenance, and the code is stated to be a lower bound,
not an optimum.

## Notes (not blocking for this check)
- W_CONVENTION_AND_REFETCH.md [not included in this package] is partly stale: it speaks of n = 11 and A_4^GC(11,8,5), evidently copied from another claim. Its
  King 2003 quote and the re-fetch hash are still correct and apply here; for n = 10 w = 5 is forced anyway.
- Log timing (search 16:29:42Z-16:42:02Z, re-fetch 16:38:28Z) is consistent with "re-fetched immediately before claiming".
- msk2014_table1_gc.png [Montemanni-Smith-Koul 2014 Table 1; not included in this package], cell (10,7): V = 34, B = 32, both below 44 (novelty beyond this is for the other skeptics).


Paths edited after review at the owner's request; verdict unchanged.
pass: true
