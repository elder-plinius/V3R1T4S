# C85_24_3 - criterion skeptic verdict

role: CRITERION
context: subagent (Claude Code Agent tool, fresh context that saw only claim/)

Inputs: the files in claim/ (CLAIM.md, REPRODUCE.md, C85_24_3_76blocks.txt, table_record/*). Own code and output are in the
criterion work folder: verify_criterion.py -> verify_output.txt, crosscheck.py -> crosscheck_output.txt, and
refetch/ (skeptic-side re-fetches, logged in refetch/FETCH_LOG.txt). Python 3.14.4, standard library only, run with -I.
Verification started 2026-10-15T23:28:17Z.

## Clause-by-clause (bank entry covering-designs-record, as quoted verbatim in CLAIM.md)

1. "b blocks, each a k-subset of a v-set (no repeated points)": MET.
   C85_24_3_76blocks.txt is 5283 bytes, LF only (0 CR bytes), sha256 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53
   (matches CLAIM.md). Strict parse: 76 lines, 0 blank lines, every line exactly 24 integer tokens, no repeated point within any
   line, all points in 1..85, 0 parse problems. 76 distinct blocks. All 85 points are used (min 1, max 85).

2. "covering every t-subset (checked exhaustively)": MET.
   I ran two independent exhaustive checks over all 98770 = C(85,3) 3-subsets of {1..85}. (a) A bitmask intersection of the
   per-point block-incidence masks for every triple gives 0 uncovered, minimum multiplicity 1 and maximum 21. (b) The union of
   all 3-subsets of every block covers 98770 of 98770 triples, with 0 uncovered and 0 invalid. "Covering" has its standard
   meaning (every t-set lies in at least one block), as in the CLAIM.md definition and on dmgordon.org. No higher multiplicity
   is required.

3. "b is STRICTLY SMALLER (direction: min) than EVERY one of the following": MET for all three sources (76 < 77; not a tie).
   - coveringrepository.com plain (v,k,t) value (m=t section): table_record/coveringrepository_download_archive_vkt.html has
     sha256 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17 and 171741 bytes, both matching CLAIM.md. It is
     tab-separated text with no HTML markup: 9490 data rows, 0 non-data non-blank lines and 0 duplicate keys. Every row has
     t = m, so the file is the plain section only and holds no lottery (t != m) rows that could be confused with it. Known
     values confirm the column order v,k,t,m: (4,3,2)=3, (7,3,2)=7, (9,3,2)=12. The only row for the cell is line 8775,
     exactly `85<TAB>24<TAB>03<TAB>03<TAB><TAB>77`, i.e. 77.
     Consistency cross-check: every cell of the re-fetched LJCR Zenodo v1.2 coverdata.json (9482 cells) and of the GitHub
     coverdata.json (8759 cells) is in this file, and none has a coveringrepository value larger than the LJCR value. This
     matches dmgordon.org's statement that coveringrepository.com contains all LJCR coverings plus more recent improvements.
   - The live LJCR value at dmgordon.org/covering-designs/: my re-fetch (HTTP 200, page "Site last updated 2026-09-03")
     confirms the claim's statement that the page shows no per-cell values. Its "This database" link is concept DOI
     10.5281/zenodo.10779736, whose versions/latest resolves to record 19735294, "La Jolla Coverings Repository", version 1.2,
     published 2026-04-24. That is the same record the claim uses; the claim reached it through record 19472830, which I did
     not fetch. Its coverdata.json has C(85,24,3) size 77, low_bd 61, so 76 < 77. Reading "the live LJCR value" as the value
     in the database the live LJCR page links to is the natural reading, and I accept it.
   - dmgordo/LJCR GitHub coverings/coverdata.json: re-fetched. The latest commit touching the file is 2022-12-19 (459bcaf247bd).
     C(85,24,3) size 77, low_bd 61, so 76 < 77.
   The claim's excerpt files table_record/ljcr_zenodo_v1.2_C85_24_3.json and table_record/ljcr_github_C85_24_3.json are
   exactly equal to the C(85,24,3) entries in my re-fetched files.

4. "It must also beat any value found by grepping GitHub/arXiv for that (v,k,t) over the last 6 months": NOT ESTABLISHED BY
   claim/, and NOT DECIDED HERE. claim/ contains no record of such a search (no queries, dates or results). The clause can be
   satisfied: it holds as long as no value <= 76 for C(85,24,3) turns up in that search. Deciding it is the NOVELTY skeptic's
   live search, and my pass does not cover this clause.

5. "each re-fetched at verification time" / "If a live table cannot be fetched, the claim is 'PENDING TABLE CHECK'": MET, with
   one caveat.
   CLAIM.md records fetches made during this run on the same day: coveringrepository.com archive at 2026-10-15T23:10:40Z
   (HTTP 200, saved and hash-verified above), dmgordon.org at 23:10:44Z and Zenodo at 23:12:39Z. So the live table was
   fetched, not missing.
   My own re-fetches: dmgordon.org returned HTTP 200 at 23:28:42Z. Zenodo coverdata.json at 23:29:59Z is byte-identical to
   the recorded sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87, and its md5 matches Zenodo's own
   checksum. GitHub coverdata.json at 23:30:17Z is byte-identical to the recorded sha256
   0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef.
   Caveat: coveringrepository.com refused my plain request with HTTP 403 (a Cloudflare "you have been blocked" page) at
   23:28:41Z, for both the download archive and the home page. I did not try to get around the block. The coveringrepository
   value of 77 therefore rests on the claimant's in-run fetch (saved copy, hash-verified, consistent with both LJCR sources),
   not on an independent skeptic-side re-fetch. The final report should say so.

6. "v <= 99, k <= 25, t <= 8": MET (85, 24, 3).

7. "b must be at least the Schonheim bound L(v,k,t)": MET. Exact integer recursion L(v,k,t) = ceil(v*L(v-1,k-1,t-1)/k)
   gives L(83,22,1) = 4, L(84,23,2) = 15 and L(85,24,3) = 54. 76 >= 54, and also 76 >= the LJCR low_bd of 61. Nothing
   suggests a bug.

8. "Same-day claim only if C(v,t) <= 5e9": MET. C(85,3) = 98770, and the exhaustive check above ran to completion.

## Hidden quantifiers, stretched definitions, subsumption

- Table section: the comparison uses the (85,24,3,3) plain row. The saved file contains only t = m rows, so the lottery
  (v,k,t,m) table cannot be the source.
- Tie presented as a record: no. 76 is strictly less than 77 in all three sources.
- One cell only: yes, C(85,24,3). Partial wins p1 and p2 are not claimed; this is judged against the full criterion.
- Same-cell subsumption: the saved table has no duplicate or second row for (85,24,3,3).
- Implied-bound subsumption: I checked whether any listed value already implies C(85,24,3) <= 76 by a standard
  construction. None does.
  - Monotonicity (C(v,k,t) <= C(v',k',t') for v' >= 85, k' <= 24, t' >= 3) gives a minimum of 77 from the coveringrepository
    file, the Zenodo file and the GitHub file alike. In each case that minimum is the cell itself.
  - Neighbouring values in the saved table: C(86,24,3) = 77, C(84,24,3) = 73, C(85,23,3) = 82, C(85,25,3) = 68,
    C(84,23,2) = 19.
  - The combining bound C(84,24,3) + C(84,23,2) is 73 + 19 = 92.
  - The best direct-product split computed from table values is 99.
  - C(84,24,3) = 73 <= 76 and C(85,25,3) = 68 <= 76 are consistent with the new design and contradict nothing.
- Null model: I agree it does not apply. The object is explicit and was checked deterministically and exhaustively, so no
  statistical inference is involved.

## Result

Every clause I can decide from claim/ plus my own checks is met literally. The exception is clause 4 (the GitHub/arXiv
6-month search), which claim/ does not evidence and which belongs to the NOVELTY skeptic. Clause 5 carries the caveat that
coveringrepository.com blocked my independent re-fetch.

confirmed_scope: The file C85_24_3_76blocks.txt (sha256 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53) is a (85,24,3) covering design with 76 blocks, covering all 98770 3-subsets of {1..85} as checked exhaustively, which is one fewer than the 77 listed for (85,24,3) in the coveringrepository.com plain table as fetched by the claimant at 2026-10-15T23:10:40Z and in the LJCR Zenodo v1.2 and dmgordo/LJCR GitHub coverdata.json files as re-fetched at 2026-10-15T23:29:59Z and 23:30:17Z.

pass: true
