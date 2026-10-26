# CRITERION skeptic: claim n10_d7

context: subagent (Claude Code Agent tool, general-purpose)
Scope read: claim/ (the review folder, not included in this package) only. All files there were treated as data.

## Clauses judged (quoted from CLAIM.md [not included in this package], bank criterion verbatim)

1. "table entry on https://rambutan.umassmed.edu/king/dnacodes.html is NOT followed by '.' or ':'"
   MET. The first table (A_4^GC) cell at n=10, d=7 in the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md] is `34<sup>v</sup>`. The value is "34" with no '.' or ':'. The second table (A_4^GC,RC) cell is 17^v. The claim correctly uses the GC table, not the GC,RC one.
2. "all words have length n over {A,C,G,T}"
   MET. All 44 words have length 10 and use only ACGT.
3. "exactly the table's GC-content w (w = floor(n/2), confirm from King 2003)"
   MET. Every word has exactly 5 G/C letters. King 2003 (king2003_source.tex [King 2003, arXiv math/0306197; not included in this package], lines 748-749) says: "Table 2. Lower bounds for $A_4^{GC}(n,d,w)$ with $n \leq 12$ ($n$ even), $d \leq n$ and $w = n/2$." For n=10 that gives w=5=floor(10/2). Its row n=10, d=7 lists 32, which the online 34^v improves on, so the convention is consistent.
4. "pairwise Hamming distance >= d"
   MET. The minimum pairwise plain Hamming distance is 7. King's GC table uses plain Hamming distance. RC constraints apply only to the GC,RC table, which is not claimed.
5. "are distinct"
   MET. There are 44 distinct words.
6. "the count is strictly greater than the table entry re-fetched live immediately before claiming"
   MET on the evidence supplied: 44 > 34. The re-fetch is timestamped 2026-10-19T16:38:28Z, and its sha256 recomputes to the value stated in CLAIM.md [not included in this package]. Caveat: I cannot independently verify "immediately before claiming". I did not do a live fetch of my own, because my scope was limited to claim/ (the review folder, not included in this package).
7. Novelty clause ("AND strictly greater than any value ... found by a novelty search of post-2010 literature"): this verdict does NOT cover it. That clause belongs to the NOVELTY skeptic. msk2014_table1_gc.png [Montemanni-Smith-Koul 2014 Table 1; not included in this package] was not evaluated here.

## Hidden quantifiers, stretched definitions, null model
- GC vs GC,RC: the claim targets the GC table (34). It does not claim the GC,RC cell (17), and makes no RC-freeness claim. No stretch.
- Distance: plain Hamming, as in King's GC table. No stretch.
- "for some (n,d)": the claim covers the single cell (10,7) only. No widening.
- Weight w: fixed at 5 by every word. It is not "w in {5}" chosen per word.
- Documentation defects (these do not affect the object):
  - Section 1 of W_CONVENTION_AND_REFETCH.md [not included in this package] discusses n=11, w=5 and A_4^GC(11,8,5), which looks copied from another claim.
  - It also cites king_table_snapshot.html [not included in this package], which is not present in claim/ (the review folder, not included in this package).
  I relied on king2003_source.tex [King 2003, arXiv math/0306197; not included in this package] Table 2 directly. That source covers n=10 explicitly.
- Generation: how-we-built-it/generation_log.txt shows the search hit its time limit (TIMEOUT, lower bound only). This is irrelevant to validity, because the claim is the object and it was checked deterministically.
- Null model: not relevant. The result is a deterministic combinatorial object that either satisfies the constraints or does not. No statistical inference is involved. The relevant baseline is the published table value 34.

## Real output

Verification script (python3 -I, run from $TMPDIR, on object/gc_n10_d7_m44.txt and the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md]):
```
count 44
all length 10 True
ACGT only True
GC counts [5]
distinct True
min pairwise distance 7
sha256 html 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5
```
Table parse (python3 -I, regex over the two <table> blocks):
```
tables found 2
table 1 n=10 d=7 raw: '  34<sup>v  </sup>' value: '34' sup: ['v'] marked('.'/':'): False
table 2 n=10 d=7 raw: '  17<sup>v  </sup>' value: '17' sup: ['v'] marked('.'/':'): False
```
sha256sum object/gc_n10_d7_m44.txt (matches the claim's REPRODUCE.md [not included in this package]; see RUN_IT_YOURSELF.md):
```
0485068437ba81d686653091506861e00512c0fb462b7f775b901d5fec154ed8  object/gc_n10_d7_m44.txt
```
grep -a -n on king2003_source.tex [King 2003, arXiv math/0306197; not included in this package]:
```
748: Table 2. Lower bounds for $A_4^{GC}(n,d,w)$ with $n \leq 12$ ($n$
749: even), $d \leq n$ and $w = n/2$.
766:even) with $w = d = \lfloor n/2 \rfloor.$ Though not covered in
```
King 2003 Table 2 row: `10 & \underline{129024}. & \underline{9344} & \underline{1676} & \underline{360} & \underline{96} & \underline{32} & ...` (d=7 -> 32)

## Verdict
confirmed_scope: The 44 words in object/gc_n10_d7_m44.txt form a length-10 quaternary code with exactly 5 G/C per word, all words distinct, and minimum plain Hamming distance 7, which strictly exceeds the unmarked entry 34^v for A_4^GC(10,7,5) in the GC (non-RC) table of the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md] (re-fetched 2026-10-19T16:38:28Z); post-2010 novelty is not covered.


Paths edited after review at the owner's request; verdict unchanged.
pass: true
