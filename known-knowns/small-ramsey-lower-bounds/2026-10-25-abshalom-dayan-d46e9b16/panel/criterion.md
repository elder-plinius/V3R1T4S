context: headless claude -p session (claude-opus-5-5, effort high), fresh, started inside a copy of claim/ .

# CRITERION skeptic verdict: partial win p1, R(3,3,14) >= 267

Verdict: the object meets partial win p1 literally. The main success criterion is not claimed and is not met: it is about a two-colour R(s,t) graph certified by B&B plus an UNSAT proof, and this object is a 3-colouring.

## Object
`shasum -a 256 object/R_3_3_14.txt` gave
`d46e9b167a93492eb02cabc1d2d9f81c975ea68698cb55944a4afac2463034ba  ../object/R_3_3_14.txt`, which matches CLAIM.md.
The header line is `circulant 266 3`, so N = 266 and N+1 = 267.

## Clause by clause (p1)

1. **"explicit edge colouring of K_N with no monochromatic forbidden clique in each colour"**: met.
   I wrote my own checker (work/check.py, sha256 60ee5da16634d3e73a099d7469d984302acd56b2dbb7b9c4c04b778f548c6b9d) from the
   stated file format before reading verify_circ.py. It checks that the distances 1..265 are partitioned (every distance gets
   exactly one colour). It counts triangles in colours 1 and 2 directly. For colour 3 it runs a CaDiCaL SAT search with a
   sequential-counter cardinality constraint: the clique is shifted to contain 0, and then split by orbits of the multipliers
   that preserve colour 3, with orbits already covered excluded. Output (work/k14.log):
   ```
   colour 1 degree 43
   colour 2 degree 50
   colour 3 degree 172
   colour 1 triangles through 0: 0
   colour 2 triangles through 0: 0
   multipliers preserving colour 3: [1, 265]
   orbit representatives in S3: 86
   ...
   colour 3 K14-free: True
   exit 0
   ```
   All 86 orbit subproblems were UNSAT (`grep -c "K12-clique: False"` = 86, `grep -c "K12-clique: True"` = 0).
   The degrees sum to 43+50+172 = 265 = N-1.
   - Null model / positive control: the same code with K=13 finds a K13 in colour 3, and the code re-checks it edge by edge
     (work/k13.log): `WITNESS K13: [0, 2, 5, 28, 31, 78, 81, 187, 190, 235, 247, 249, 264]`, `colour 3 K13-free: False`.
     So the SAT encoding is not vacuous, and colour 3 is tight at 14.
2. **"verified exhaustively"**: met by two independent exhaustive methods. The first is my SAT/UNSAT run above. The second is
   the author's bitset branch and bound, verify_circ.py, which I ran after my own check. Its output (work/author_check.log):
   ```
   colour 1: degree 43, no K_3 (no K_2 among the neighbours of 0, exhaustive)
   colour 2: degree 50, no K_3 (no K_2 among the neighbours of 0, exhaustive)
   colour 3: degree 172, no K_14 (no K_13 among the neighbours of 0, exhaustive)
   N 266 colours 3 forbidden 3,3,14
   proves R(3,3,14) >= 267
   PASS
   exit 0
   ```
3. **"N+1 strictly above the best lower bound in DS1"**: met. At 2026-10-25T08:37:01Z I fetched the DS1 PDF once: HTTP 200,
   585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc. Its text reads
   `revision #18: April 24, 2026`. In §6.1.2, Table XIb, the row for k = 3 reads
   `30 45 61 85 103 129 150 174 194 217 242 269 291` for m = 4..16, so the m = 14 entry is 242 [ExT]. 267 > 242.
   - Hidden quantifier "best lower bound in DS1" (implied bounds): DS1 says that some bounds are only *implied* by §6.2
     (for example "261 ≤ R(3,3,15) ... implied by 6.2.g"). The only general §6.2 inequality that applies to this cell is
     6.2.g: R(3,k,l) ≥ 4R(k,l−1) − 3. With DS1 Table Ia, R(3,13) ≥ 61 (lower-bound row `40 47 53 61 67 74` for l = 10..15),
     which gives 4·61 − 3 = 241 < 242. Even the R(3,13) upper bound of 68 could only give 269, and that would require
     R(3,13) = 68, which nobody has established. 6.2.h needs four or more colours. So no DS1-implied bound reaches 267.
   - Not subsumed: DS1 Table Ia lists R(5,14) ≥ 267 [Kuz] (row k = 5 upper line `43 59 80 101 133 149 183 203 233 267 275`
     for l = 5..15). That matches the stated (5,14) provenance of colour 3. But R(5,k) bounds do not imply R(3,3,k) bounds,
     because a K5-free graph need not split into two triangle-free graphs, and DS1 lists no such inequality. The split is
     new content, and the checks above verify it.
4. **"and any newer arXiv paper for that multicolour cell"**: met as far as a metadata search can show. I sent two arXiv API
   queries, newest first:
   - all:Ramsey AND (multicolor/multicolour/three colors/three-color/3-color/lower bounds): fetched 2026-10-25T08:37:45Z,
     HTTP 200, 300 entries, 2018-09-13 .. 2026-10-21, sha256 74931a2c….
   - all:Ramsey AND (circulant/cyclic/Exoo/small Ramsey/Radziszowski): fetched 2026-10-25T08:39:00Z, HTTP 200,
     86 entries, sha256 11948c0a….

   No entry since April 2026 gives a lower bound for R(3,3,14). The closest are:
   - arXiv:2609.28455, R(3,3,k) = Θ(k³/log²k), asymptotic only.
   - arXiv:2608.18769, R(3,n) bounds for 24 ≤ n ≤ 49 only, so R(3,13) and the 6.2.g bound are unchanged.
   - arXiv:2610.12122, R(6,8) and R(8,10).
   - arXiv:2608.18169, R(4,20).

   One general web search for "R(3,3,14)" Ramsey lower bound found only Exoo–Tatarevic 2015 (233 → 242).
   Limitation: arXiv metadata search cannot rule out a paper that mentions this cell only in its full text.

## Scope
- The claim is about R(3,3,14) only. Permutations of the arguments are the same number, so "that multicolour cell" is
  unambiguous.
- The direction is max and strict: 267 > 242 by 25.
- The off-by-one convention is right: the colouring is on K_266, which gives N+1 = 267.
- The win is genuine for p1. It does not satisfy the main criterion, which is two-colour.

confirmed_scope: The circulant 3-colouring of K_266 in object/R_3_3_14.txt (sha256 d46e9b16…34ba) has no monochromatic K_3 in colours 1 and 2 and no K_14 in colour 3, verified exhaustively by a SAT/UNSAT search and by the author's branch and bound, so R(3,3,14) ≥ 267, which is strictly above DS1's (April 24, 2026) bound of 242 and above every bound for this cell that I found on arXiv up to 2026-10-21 (titles and abstracts only).

pass: true
