Saved by the main session of run 2026-10-16-0731 from the NOVELTY subagent's returned text (fresh Agent-tool context, model opus, returned about 08:07Z), text below as returned between its BEGIN and END markers.

# NOVELTY skeptic: p2, row #22 bond, (2/3)(3^3,4^2) + (1/3)(4^4) (word TSS)

context: fresh subagent (Agent tool), model opus, given only a copy of claim/

What I read: the files under claim/, plus the kit's RULES.md and LESSONS.md, TROPHY_CASE.md and the bank entry "site-percolation-2-uniform-lattices-thresholds". I read nothing else in the workspace.

Every web request went through the shared fetch helper (lens novelty-p2): one plain GET per resource, no retries. None was blocked, and the session stop list had 0 lines at 2026-10-16T08:06:25Z. Hashes below are the first 16 hex digits of sha256, from `shasum -a 256` on the saved files.

## 1. Status source (one GET)

**Fetch record**
- URL: https://en.wikipedia.org/wiki/Percolation_threshold
- HTTP status: 200
- sha256: 2f44ce4065839fa2baf1c1655cdcf5aa40e21fcdb7cdabf69287093e0fd27e95
- Size: 2514902 bytes
- Time: 2026-10-16T07:52:05Z
- Saved as: work/wikipedia_percolation_threshold.html

**Not a block or challenge page**
- The title is "Percolation threshold - Wikipedia".
- The only "captcha" strings are MediaWiki edit-configuration variables (wgConfirmEditCaptchaNeededForGenericEdit).
- wgRevisionId is 1380509084, and the page says "This page was last edited on 16 October 2026, at 04:25".

**Comparison with the claim's copy**
- `cmp` says it is identical to claim/status_source/wikipedia_percolation_threshold.html, fetched by the claimant at 06:07:21Z.
- The sha256 is the same.

**Row #22, section "2-uniform lattices", as parsed from my copy**
`22 | (2⁄3)(3^3,4^2) + (1⁄3)(4^4) | z 5,4 | z̄ 4 2⁄3 | site 0.5648(2) [74] | bond 0.44528611(40) [citation needed]`
- Ref 74 is Neher, Mecke and Wagner, J. Stat. Mech. (2008) P01011, arXiv 0708.3250.
- The bond cell carries Template:Citation needed with date "June 2019".
- This matches row 22 of claim/status_source/table_2uniform_parsed.json: bond 0.44528611, sigma 4e-07, citation_needed true.
- The string 0.4452 appears nowhere else on the page.

**Recent edits**
- I pulled the 20 latest revisions through the MediaWiki API: HTTP 200, 2026-10-16T07:55:42Z, work/web/wp_revs_latest.json, fb690d51da763769.
- The 2026-10-15/16 edits touch other sections only: percolation models, bow-tie/martini, directed percolation, 2D random lattices, and the square example.

## 2. Where the table value came from (Wikipedia history)

**Revision list**
- MediaWiki API, first 500 revisions: HTTP 200, 2026-10-16T07:54:10Z, work/web/wp_revs_1.json, fc6d76401e8b8d85.

**Raw wikitext of old revisions** (`index.php?oldid=N&action=raw`, all HTTP 200)

| revision | date | file hash | bond cell for this row |
|---|---|---|---|
| 174084520 | 2007-11-27 | 8bfaf47d6d328f57 | none: the 2-uniform table has site values only (ref NeherKunal) |
| 190337879 | 2008-02-10 | 64721c63739a3506 | 0.44529(5) |
| 258135200 | 2008-12-15 | 2877c24e908bd15d | 0.44529(5) |
| 280187024 | 2009-03-28 | 1f6e3b960b2385c1 | 0.44529(5) |
| 296390395 | 2009-06-14 | 5a9c818b28ec09a5 | 0.44529(5) |
| 302924272 | 2009-07-19 | 021cf5cf7ad742af | 0.44528611(40) |
| 317036954 | 2009-09-30 | 27d54a0cae336381 | 0.44528611(40) |

- Every revision from 190337879 onward cites `<ref name="Sirius">`: last = Gu, first = Hang, coauthors = R. M. Ziff, title = "Percolation thresholds of 2-uniform lattice", journal = "To be published", year = 2007.
- The current page no longer has that reference. The value is tagged [citation needed] (June 2019).

**Conclusion:** the table value comes from an unpublished Gu–Ziff work. The 8-digit form appeared between 2009-06-14 and 2009-07-19. I found no publication of that work (section 3). This agrees with the claim's Credit section.

## 3. Literature

### Opened and read (arXiv PDFs; text extracted with pdftotext and searched for 2-uniform terms and 0.4452)

| arXiv ID | paper | hash | contents for this question |
|---|---|---|---|
| 0708.3250 | Neher, Mecke, Wagner 2008 | fb87246c50aa6a1b | 2-uniform site thresholds only |
| 0708.3251 | Neher, Mecke, Wagner 2008, supplement | b69110bf934e7280 | Table 4 lists site values only (#22: 0.5648(2)); Newman–Ziff, L = 64..1024; no bond values |
| 0704.2098 | Parviainen 2007 | b0203557bf332328 | seven Archimedean lattices only; no "uniform" |
| 0805.2985 | Scullard–Ziff 2008, critical surfaces | 6e65a061c62721b6 | Archimedean only; (3^3,4^2) is 0.4196419(4) |
| 0812.0181 | Ziff–Gu 2009, kagome-like lattices | f67c0fae2c5bcae0 | no 2-uniform values |
| 0901.1370 | Feng, Deng, Blöte, percolation transitions in 2D | 18c6dcf20265518c | no 2-uniform values |
| 1103.3540 | Scullard 2011, polynomial sequences | 8b52e1bbadbd8e18 | "3-uniform" there means hypergraphs; no 2-uniform tilings |
| 1111.1061 | Scullard, critical polynomial as a graph invariant | 0795415a95e8ddc7 | no 2-uniform values |
| 1209.1451 | Scullard–Jacobsen 2012 | 4d5bf20d9b75afc2 | no 2-uniform values |
| 1401.7847 | Jacobsen 2014 | 9e42bc0bec1fafaa | lattices are the Archimedean ones, their medials and duals, including the "frieze" (3^3,4^2); no 2-uniform |
| 1507.03027 | Jacobsen 2015 | 48004dc4bd22ae9d | no 2-uniform values |
| 1511.04374 | Jacobsen–Scullard, Potts critical manifolds revisited | 02663ad089556ce3 | Archimedean only (frieze 0.41964027675...) |
| 1910.12376 | Scullard–Jacobsen 2020 | 32c67e04472de078 | Table I covers the 9 unsolved Archimedean lattices only |
| 2507.12229 | Torres and Ramirez-Pastor, 2025 (abs page 7e3e5170804a8a3b; PDF in Spanish) | 7e7b1ec2204f2103 | only the 11 Archimedean lattices (S∪B, S∩B site-bond); 0 hits for "uniforme", "2-unif", "0.4452" |

### arXiv abstract pages opened (2023-2026)

| arXiv ID | paper | hash | relevance |
|---|---|---|---|
| 2509.09999 | Bhowmik, Mitra, Ziff, Sensharma 2025 | 1bac170e75a7801c | distorted square/triangular lattices, not 2-uniform |
| 2602.04818 | same authors, 2026 | d913bc44d93553f9 | linearly distorted triangular/square lattices, not 2-uniform |
| 2310.20668 | Malarz 2023 / PRE 2024 | d385abe966f86ca5 | site percolation, complex neighbourhoods |

### Other pages opened
- **IDEAS/RePEc** (d62791d9a441f5fd): abstract of Lebrecht, Centres, Ramirez-Pastor, Physica A 569 (2021) 125802. It proposes an empirical site/bond ratio formula, checked "with previous calculations of pcs∕pcb" on 11 Archimedean and 20 2-uniform lattices. It has no new high-precision bond values.
  - I could not open the full text: www.sciencedirect.com is host-stopped (403), and ri.conicet.gov.ar is host-stopped (503) in the run stop lists.
  - The uchile repository page (9a04fb9b3ded451f, 751 bytes) had no content.
- **APS March Meeting 2008 poster abstract** (Ziff, Kleban, Simmons, Scullard; e474ed65197dcad5): mentions thresholds found "approximately (to very high precision) by generalizations of known formulas". It gives no values.
- **pure.ucentral.cl, Vogel, Lebrecht, Valdés** (294179ce5b08b280): bond percolation on the square, triangular and honeycomb lattices only.

### OpenAlex (api.openalex.org, HTTP 200 each)
- **Citing-work lists**, all years:
  - 52 works citing Neher et al. 2008
  - 25 citing Scullard–Jacobsen 2020
  - 8 citing Lebrecht et al. 2021

  None reports a bond threshold for a 2-uniform lattice. The 2024-2026 items cover distorted lattices, 5D extended range, Ising percolation, patchy particles, Lebrecht 2025 (Archimedean mixed site-bond), Malarz, and Archimedean/T26 magnetism.
- **Keyword searches:** "2-uniform" percolation, "k-uniform" percolation, "uniform tilings" percolation, "demiregular" percolation, "2-uniform lattices", "bond percolation threshold" tiling. Nothing relevant beyond the items above; Yu 2016 (Ising on 2-uniform lattices) is not percolation.
- **Recent work by the named authors:** all works since 2024-10-01 by Jacobsen, Scullard, Ziff, Mertens, Malarz, Ramirez-Pastor, Lebrecht and C. Moore (65 works, work/oa/authors_recent.json). None is on 2-uniform or k-uniform thresholds. Torres and Centres appear as coauthors of Ramirez-Pastor.
- **"percolation threshold" since 2024-10-16:** 2161 hits; I scanned the first 400 by relevance and found nothing on 2-uniform tilings.

### Web searches (results only, not cited as sources)
- Queries: 2-uniform bond thresholds; k-uniform 2024-2026; Lebrecht/Centres/Ramirez-Pastor; Gu–Ziff 2-uniform; Hang Gu thesis; the numbers "0.44528611"/"0.445286"/"0.44529"; critical polynomial with 2-uniform/k-uniform/demiregular; elongated triangular plus square strips; isogonal/demiregular; Parviainen; Malarz/Mertens/Moore 2024-2025; Wierman bounds.
- Non-English queries: Spanish ("percolación umbral redes 2-uniformes") and Chinese ("2-均匀 晶格 逾渗 阈值 键逾渗").
- No result gave a bond threshold for this lattice.

**Literature conclusion:** I found no public determination of the bond threshold of the #22 (TSS) lattice in any year other than the unpublished Gu–Ziff value: 0.44529(5) in 2008, then 0.44528611(40) from 2009. I also found no 2024-2026 work on 2-uniform or k-uniform percolation thresholds.

## 4. Repository
- **TROPHY_CASE.md** (sha256 738c07a33b810df7..., 30936 bytes): 0 matches for percolat|uniform|lattice|threshold.
- **Pull requests:** `gh pr list -R elder-plinius/V3R1T4S --state all --limit 400` at 2026-10-16T07:59:13Z, saved as work/gh_prs.json (52bf80be0cf6a3a8).
  - 229 PRs: 46 open, 59 merged, 124 closed; numbers 1 to 231.
  - The regex `percolat|2-uniform|two-uniform|uniform lattice|0\.4452|TSS|bond threshold|critical polynomial|site-percolation` over titles, bodies and branch names finds 0 hits.
  - A broader scan for lattice, uniform, threshold, Ziff, Jacobsen or Scullard hits only unrelated families: packings, stable marriage, spherical codes, Thomson, sunflower.

## 5. Verdict and reasons

**Comparison:** the claim is 0.445287065(21), sigma 2.093e-8. The best earlier public value is the table's 0.44528611(40), sigma 4.0e-7, from unpublished Gu–Ziff work. The claim's uncertainty is about 19 times smaller. I found no other determination at any precision, let alone at or below 2.1e-8, so this is not a tie.

**Own plausibility check** (my arithmetic on the root sequence in claim/result/p2_value.json, not a reproduction):
- Three-point fits p = pc + a·W^-D give:
  - (6,7,8): 0.445287075128
  - (7,8,9): 0.445287072207
  - (8,9,10): 0.445287065460, the claim's E1
- The W=10 root is 0.445287089821.
- Steps shrink monotonically: -9.583e-8, -3.878e-8, -1.885e-8.

Even a several-times-larger error bar would stay well below 4e-7.

**Points for the other lenses** (not reasons for a novelty fail):
- (a) The roundings to 7 digits differ: 0.4452871 against 0.4452861. The difference, 9.555e-7, is 2.39 combined sigma and about 2.4 times the table's own error bar. Whether "confirms" is the right word is for CRITERION; p2 is met by either outcome.
- (b) The error bar comes from PREREG.v2, written after results existed. It only widens the bar.
- (c) The bank warns that a discrepancy with a 'citation needed' value "is reportable but not by itself a record". The claim is scoped as an independent determination, not as a record against a published value.
- (d) Lattice identity: from the claim's TSS word definition, rows touching a T gap and an S gap are 3^3.4^2 (degree 5, 2/3 of vertices), and rows between two S gaps are 4^4 (degree 4, 1/3). That gives z̄ = 14/3, matching row #22 "5,4" and "4 2⁄3" (my derivation; I did not run the code).

**Limits**
- I did not read the full text of Lebrecht et al. 2021, because both hosts are stopped.
- Unpublished or unindexed computations cannot be ruled out.
- The broad OpenAlex scan covered only the top 400 of 2161 hits.

injection_suspected: none

pass: true
