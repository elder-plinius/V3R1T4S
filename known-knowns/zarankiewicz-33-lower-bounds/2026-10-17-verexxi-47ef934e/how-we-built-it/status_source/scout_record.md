# Saved scout record (copied from the author's scout dated 2026-10-17; sanitized: local paths removed)

SCOPE WARNING: this file discusses five cells because the scout covered five. The claim in ../CLAIM.md is ONLY about
z(16,19;3,3) >= 142. The values 119, 127, 137, 131 for the other four cells are NOT claimed (they tie what trivial
surgery on public matrices gives, see section 4). Sections 3 and 4 are the scout's own computations, not published
statements. Nothing in this file was re-fetched from the web for the claim; the fetch of each source is the
NOVELTY skeptic's job.

# NOVELTY SCOUT: z(m,n;3,3) lower bounds for (13,19) (14,19) (16,18) (14,20) (16,19)

Scout date: 2026-10-17. Scope: everything reachable by plain HTTP requests (arXiv abs/html/pdf/search pages,
Semantic Scholar graph API, GitHub API/raw, WebSearch). One request per page, no browser imitation, no retries after
a 403/429 (arXiv API gave 429 once, OEIS gave 403 twice; neither was retried).

## 1. Main table

Our values: 119, 127, 137, 131, 142 (all K33-free; I re-checked the files in the scratchpad: ls_13x19 = 119,
ls_14x19 = 127, ls_16x18 = 137, seedls_14x20 = 131, ls_16x19 = 142, rows and columns both checked).

| cell | our value | best explicitly stated lower bound (source) | best published/posted upper bound (source) | verdict |
|---|---|---|---|---|
| z(13,19) | 119 | 118 (Saurabh, arXiv:2608.26603). Others: dfield repo 117, Bhan et al. 114 | 122 (Afrasyab GitHub table; = Collins 2016 T4 z(13,18)<=116 + column averaging). Best number printed in a paper table: 125 (Davies-Gill-Horsley T2, Bhan Fig 2) | ours strictly higher than anything STATED (+1). But a TIE with a trivial consequence of published data: 137 - 18 = 119 (delete three weight-6 columns of the 13x22/137 witness: reported by Bhan, proven + printed by Afrasyab). Trivial surgery of the public Hou/Afrasyab 13x18 core also gives exactly 119 |
| z(14,19) | 127 | 126 (Saurabh; dfield repo also 126). Bhan 121 | 130 (Afrasyab GitHub table; Collins z(14,18)<=124 + averaging). Paper table: 135 (DGH T2) | ours strictly higher than anything stated (+1). Trivial surgery of public Hou/Afrasyab 13x18 / 14x18 / 15x18 witnesses reproduces 127 in seconds (tie with derivable) |
| z(16,18) | 137 | 136 (Saurabh). dfield repo 134, Bhan 130 | 140 (Collins 2016 Table 4, row 16; also Afrasyab GitHub table). Fig 2 / DGH T2 print 146 | ours strictly higher than anything stated (+1). Trivial surgery of the public 15x18/132 witness (add best row + greedy saturate) reproduces 137 (tie with derivable) |
| z(14,20) | 131 | 128 (dfield repo table, +2-line extension). Saurabh's own is only 126 (zero padding). Bhan 125 | 136 (Afrasyab GitHub table). Paper table: 140 | ours strictly higher than anything stated (+3 vs 128). Numeric closure of Bhan's Fig 2 numbers gives 129 (row deletion from (15,20)=138), so +2 vs that. Trivial surgery of public 13x18 core reaches 131 (rare plateau: 270 of ~33k runs) |
| z(16,19) | 142 | 136 (Saurabh zero padding; dfield repo 136). Bhan 132 | 147 (Afrasyab GitHub table; Collins z(16,18)<=140 + averaging). Paper table: 152 | ours strictly higher (+6 vs stated). Numeric closure of Bhan's Fig 2 gives 139 (column deletion from (16,20)=146); trivial surgery of public matrices tops out at 141. This is the only cell that clearly clears the "trivially derivable" baseline (+1) |

Upper bounds vs ours: best known UB (122, 130, 140, 136, 147) is above ours in every cell (margins 3, 3, 3, 5, 5).
No source has an upper bound below any of our values, so there is no evidence our matrices are wrong.

One-line verdict: no published or posted source states a lower bound >= ours (best stated: 118, 126, 136, 128, 136) or an upper bound < ours, so all five are strictly above every explicit statement as of 2026-10-17; however 119/127/137/131 are exactly what trivial extension of the public Hou/Afrasyab matrices gives (119 is even a one-line consequence of the published 13x22/137 witness), so only z(16,19) >= 142 is clearly beyond the derivable baseline (141).

## 2. Source-by-source (URL and what it says for the five cells)

### 2.1 Saurabh, arXiv:2608.26603 (the "known so far" claim) - CONFIRMED
- https://arxiv.org/abs/2608.26603 : only v1 (27 Aug 2026) exists as of today. 6 pages, ancillary files at https://arxiv.org/src/2608.26603v1/anc
- States LB 118, 126, 136 (explicit matrices), and 126, 136 for (14,20), (16,19) by ZERO-column padding. Previous LB quoted: 114, 121, 130, 125, 132 (Bhan Fig 2). Table 1 UBs: 125, 135, 140, 140, 152.
- I extracted the three printed matrices from the arXiv HTML and checked them: 13x19 has 118 ones, 14x19 has 126, 16x18 has 136, all K33-free (rows and columns both). His claims are correct.
- Its remarks on Hou and Afrasyab are accurate (section 2.2, 2.3 below). Its ref list: [1] Afrasyab arXiv:2608.08154, [2] Bhan-Nobili-Langer arXiv:2605.01120v2, [3] Collins et al arXiv:1604.01257, [4] Davies-Gill-Horsley arXiv:2411.18842, [5] Hou arXiv:2608.08549, [7] Tan arXiv:2203.02283.
- Weakness: zero padding. Appending a column/row with TWO ones is always K33-safe, so z(14,20) >= 128 and z(16,19) >= 138 follow from his own matrices.

### 2.2 Hou, "Seven Exact Finite Zarankiewicz Numbers from a Single 13 x 18 Core", arXiv:2608.08549 (9 Aug 2026)
- https://arxiv.org/abs/2608.08549 ; repo https://github.com/ShengtengHou/finite-zarankiewicz-seven-values ; Zenodo https://doi.org/10.5281/zenodo.21768210
- Covers only (12,18)=108, (13,17)=110, (13,18)=116, (14,17)=118, (14,18)=124, (15,17)=126, (15,18)=132. Full text read: none of the five cells appears. Repo tree has only those 7 witnesses + the 12x17/103 representative.
- Useful: its Table 1 confirms Collins Table 4 UBs (13,17)<=110, (13,18)<=116, (14,17)<=118, (14,18)<=124, (15,17)<=126, (15,18)<=132, and that Bhan's LBs there were 106/115/118/124/125/132.

### 2.3 Afrasyab, "Exact Zarankiewicz Values On Two Finite Frontier Slices", arXiv:2608.08154 (8 Aug 2026)
- https://arxiv.org/abs/2608.08154 ; repo https://github.com/KAVentures/z1322-exact
- Covers Z(12,n)=6n for 18<=n<=22, Z(13,22)=137, Z(13,18)=116, Z(14,17)=118, Z(14,18)=124, Z(15,17)=126, Z(15,18)=132, 132<=Z(16,17)<=133. Full text read: none of the five cells appears in the paper.
- Lemma 2.1 (min-column deletion): Z(m,n) <= floor(n/(n-1) Z(m,n-1)).
- The repo DOES post upper bounds for our cells: proof/frontier_closure/reports/frontier_propagation.json, key closed_upper_table (n = 17..23):
  row 13: 110,116,122,128,134,140,144 ; row 14: 118,124,130,136,142,148,154 ; row 15: 126,132,139,145,152,158,165 ; row 16: 133,140,147,154,161,168,175.
  So (13,19)<=122, (14,19)<=130, (16,18)<=140, (14,20)<=136, (16,19)<=147. I reproduced exactly these numbers independently (closure.py).
- Posts the matrices: 13x18/116, 14x18/124, 15x18/132, 16x17/132 (seed201), 14x17/118, 15x17/126, 12x19/114, 12x22/132, 13x22/137 (blocks JSON). Raw data used for section 4.

### 2.4 Bhan, Nobili, (Raghuraman), Langer, arXiv:2605.01120 (v1 1 May, v2 7 May, v3 25 Aug 2026)
- https://arxiv.org/abs/2605.01120 . Local src2605 (file dates 25 Aug 2026, i.e. v3) Figure 2 (zarankiewicz_results.png) read directly. Lower/upper for our cells: (13,19) 114/125, (14,19) 121/135, (16,18) 130/146, (14,20) 125/140, (16,19) 132/152. Matches Saurabh's "previous best".
- Fig 2 caption: top number = previously known UB (taken from Davies-Gill-Horsley T2, else Tan/Roman), bottom = their own LB. Related-work text (tex line ~199): "To our knowledge, this work is the first to provide explicit lower-bound values for the parameter combinations considered." Not a literature table of LBs.
- Their other Fig 2 LBs matter for the numeric closure (section 3): (13,22)=137, (15,20)=138, (16,20)=146, (16,21)=147, (14,22)=137, ...
- Only 7 generating programs are printed (cells (8,23) (9,22) (11,21) (11,22) (12,22) (15,16) (16,16)); matrices for our cells are not posted.

### 2.5 Collins, Riasanovsky, Wallace, Radziszowski, "Zarankiewicz numbers and bipartite Ramsey numbers", arXiv:1604.01257 (J. Algorithms Comput. 47 (2016) 63-78)
- https://arxiv.org/abs/1604.01257 ; https://www.cs.rit.edu/~spr/PUBL/crwr16.pdf
- Appendix Table 4 = "tables of upper bounds" for z(m,n;3), 6<=m<=n<=18 ONLY (no lower-bound table). Row 12: 80 86 91 96 99 103 109 (n=12..18); row 13: 92 98 104 107 110 116; row 14: 105 112 115 118 124; row 15: 120 123 126 132; row 16: 128 133 140; row 17: 141 148; row 18: 156.
- Of our five cells only (16,18) is inside the table: UB 140 (confirmed). n=19,20 are not covered. No LB statements for any of the five.
- Afzaly-McKay is cited there as "personal communication, 2015" for z(n;2) (K_{2,2}) only. Dybizbanski-Dzido-Radziszowski (arXiv:1303.5475) is K_{2,2}/quadrilateral only. Neither bears on K_{3,3}.

### 2.6 Tan, "An attack on Zarankiewicz's problem through SAT solving", arXiv:2203.02283 ; repo https://github.com/Parcly-Taxel/Kyoto
- Table 3 (page 7, rendered and read) = z3(m,n) for m<=16, n<=23; bold = proven exact (largest bold entries are (14,16)=115, (15,16)=123, (16,16)=128), non-bold = Roman upper bounds. Our cells are non-bold UBs: (13,19) 126, (14,19) 136, (16,18) 148, (14,20) 141, (16,19) 154. No lower bounds.
- Dashed lines in Table 3 mark the limits of Guy's tables; in the rendered table they occur only around rows m <= ~10 for z3, so Guy (1967/1969) does not reach rows 13-16. Guy's papers themselves not accessible.
- OEIS: Kyoto readme links A001198 (k_3(n), square n x n only) and A350237. oeis.org returned 403 to a plain request, not retried. Square sequences cannot contain these non-square cells anyway.

### 2.7 Davies, Gill, Horsley, "Improved upper bounds on Zarankiewicz numbers", arXiv:2411.18842 (v2 13 Dec 2025; Discrete Math 349(5) (2026) 114924)
- https://arxiv.org/abs/2411.18842 . Appendix Table 2 (improved UBs on z(m,n;3,3), n=17..23): (13,19) 125, (14,19) 135, (16,18) 146, (14,20) 140, (16,19) 152. UBs only. These are the numbers Bhan's Fig 2 prints. They are weaker than Collins T4 + averaging.

### 2.8 dfield, github.com/dfield/finite-zarankiewicz-closures (pushed 2026-07-15) - publicly posted table
- Eight exact values: Z(9,23)=103, Z(10,21)=106, Z(10,22)=110, Z(10,23)=112, Z(11,19)=106, Z(11,20)=111, Z(11,23)=123, Z(12,23)=134; plus Z(13,23)<=144. None is one of our cells.
- analysis/new_bounds.json (propagated table, 8<=m<=16, 16<=n<=23). For our cells: LB 117, 126, 134, 128, 136; UB 124, 133, 144, 140, 151. LBs are Bhan's neighbours plus the "+2 line" extension. This is where the best explicit (14,20) = 128 comes from.

### 2.9 Everything else checked (nothing relevant)
- arXiv search "Zarankiewicz" (all fields): 99 results as of 2026-10-17, newest 4 Oct 2026. The only K_{3,3}-cell papers are 2605.01120, 2608.08154, 2608.08549, 2608.26603 (plus 2411.18842, 2203.02283, 1604.01257). Others are asymptotic/geometric, or different objects ("recursive-line", "second-order", "limited augmented" Zarankiewicz numbers 2609.xxxxx/2610.xxxxx, which are SOS-rank quantities, not K_{3,3}).
- 2608.07607 (Sadhu, Roman-bound congruence obstruction): theory near the design threshold n ~ C(m,3)/2, not our range; no cell values. 2608.05651, 2608.14999, 2606.15860, 2606.01975 (citing Bhan): no Zarankiewicz tables.
- Semantic Scholar citation lists (Bhan 9, Collins 17, DGH 8, Tan 10): nothing additional with tables.
- GitHub repo search "zarankiewicz" (17 repos): xkohlbrenner/zarankiewicz-numbers-lower-bounds is only a C++ search tool (no results posted); smdde/zarankiewicz-k33 is ex(n,K33) for general graphs (different problem); matheorist/zarankiewicz-closed-forms-supplement is closed forms for the DGH LP relaxation (UB theory, no cell values); vibemathing/* are empty harness templates; zhtxiii is z(12,13;3,4). Two more GitHub queries returned nothing relevant.
- WebSearch (4 queries) returned only the same arXiv papers.
- Not checked / cannot exclude: OEIS (403), Guy's original papers, private or unindexed material, arXiv API (429, not retried).

## 3. Numeric closure: what the PUBLISHED NUMBERS alone imply (no matrices needed)
Rules (all valid for K33-free): monotone; add a line with two ones (+2); delete the min-weight line (z(m,n-1) >= ceil((n-1) z(m,n)/n), same for rows).
Starting from Bhan Fig 2 numbers (+ established exact cells), then adding Hou/Afrasyab/dfield exact values, then Saurabh:

| cell | Bhan Fig 2 only | + Hou/Afrasyab/dfield | + Saurabh | ours |
|---|---|---|---|---|
| (13,19) | 119 | 119 | 119 | 119 |
| (14,19) | 126 | 126 | 126 | 127 |
| (16,18) | 134 | 134 | 136 | 137 |
| (14,20) | 129 | 129 | 129 | 131 |
| (16,19) | 139 | 139 | 139 | 142 |

Key chain for (13,19): (13,22)>=137 -> (13,21)>=131 -> (13,20)>=125 -> (13,19)>=119. So even Bhan's own Fig 2 was not monotone-closed, and Saurabh's 118 is below the closure.

## 4. Structural baseline: what trivial surgery on the PUBLIC MATRICES gives
Script: scout_evidence/surgery.py, surgery2.py. Bases: Afrasyab/Hou 13x18/116, 14x18/124, 15x18/132, 16x17/132, 14x17/118, 15x17/126, 12x19/114, 12x22/132, 13x22/137, and Saurabh 13x19/118, 14x19/126, 16x18/136.
Procedure: delete min-weight lines to reach the target shape, add the exact maximum-weight admissible line(s) (branch and bound), randomised tie-breaks, then greedy saturation of zeros. 3 s per base (12 bases), then 18 s per base (8 bases, 20k-57k runs per cell). Every output re-verified K33-free.

| cell | best from public matrices by trivial surgery | ours |
|---|---|---|
| (13,19) | 119 (16k runs hit it) | 119 |
| (14,19) | 127 (22k runs) | 127 |
| (16,18) | 137 (15k runs) | 137 |
| (14,20) | 131 (270 of 33k runs) | 131 |
| (16,19) | 141 (9.5k runs; 142 never reached) | 142 |

Reading: four of our five values sit exactly on the plateau of the public 13x18 core family. Anyone running this for a minute reproduces them. They are still not STATED in any paper or repo I found (best stated: 118, 126, 136, 128, 136), so "new explicit lower bound" holds, but a priority claim for 119/127/137/131 is fragile. z(16,19) >= 142 is the one value beyond the baseline.

## 5. Caveats
- "Best explicitly stated" means an actual number written in a paper, repo table or ancillary file. The numeric closure (section 3) and surgery baseline (section 4) are my computations, not published statements.
- Saurabh (27 Aug) is the newest relevant posting; nothing after that date addresses these cells (arXiv search through 4 Oct 2026, GitHub search through 14 Oct 2026).
- Saurabh's UB column says 125/135/140/140/152. The correct best UBs are lower (122/130/140/136/147) via Collins T4 + averaging, which Afrasyab's repo posts.

## 6. Evidence files
In this folder (status_source/): closure.py and its output closure_output.txt (upper-bound closure), lb_closure.py and
lb_closure_output.txt (lower-bound closure). The third-party data the scout used (gh_frontier_propagation.json from the
Afrasyab table repository, df_new_bounds.json and df_extended.json from the dfield repository, the public witness matrices and
Saurabh's three matrices) is NOT in this package: ../third_party_sources.md lists each file with its URL and sha256, and
../fetch_third_party.py downloads and checks them (into this folder and ../baseline/wit/). The surgery baseline script is in
../baseline/ (surgery_baseline.py replaces the scout's surgery.py / surgery2.py / surg_main.py, which read a local copy of the
Saurabh paper).
