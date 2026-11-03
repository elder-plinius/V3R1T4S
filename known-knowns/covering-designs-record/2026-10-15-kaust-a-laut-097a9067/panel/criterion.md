# CRITERION skeptic verdict: C(61,25,3) <= 27

role: CRITERION
context: subagent (Claude Code Agent tool, fresh context that saw only claim/)

Scope of what I looked at. Locally I opened only the files in claim/ (CLAIM.md, REPRODUCE.md, C61_25_3_27blocks.txt, table_record/*) plus my own scripts and outputs. To decide the "re-fetched at verification time" clause I also sent plain read-only GET requests to the public comparison sources (coveringrepository.com, dmgordon.org, the zenodo.org API, the GitHub API and raw.githubusercontent.com). I did not search GitHub or arXiv for recent claims; that is the NOVELTY skeptic's job.

## Independent object check (my own script, standard library only, two exhaustive methods)

- sha256 of claim/C61_25_3_27blocks.txt: 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e (matches CLAIM.md).
- 1928 bytes, no CR bytes, trailing newline, 27 non-blank lines. Every token is a plain decimal integer.
- Every line has 25 tokens and 25 distinct values. No block repeats a point. The smallest point is 1 and the largest is 61, all 61 points appear, and the 27 blocks are pairwise distinct.
- All C(61,3) = 35990 3-subsets of {1..61} were enumerated.
  - Method 1 (union of the 3-subsets of each block): 35990 covered, 0 missing, none outside {1..61}.
  - Method 2 (every 3-subset tested against every block by bitmask): 0 missing, minimum multiplicity 1.

## Clause-by-clause (the criterion as quoted in claim/CLAIM.md)

1. "b blocks, each a k-subset of a v-set (no repeated points)": MET. b = 27, and each block is a 25-subset of {1,...,61}.

2. "covering every t-subset (checked exhaustively)": MET. All 35990 3-subsets are covered, checked two ways (above). This is a full enumeration, not a sample.

3. "b is STRICTLY SMALLER (direction: min) than EVERY one of the following":
   - 3a. coveringrepository.com plain (v,k,t) value (m = t section): MET on the claim's saved fetch.
     - claim/table_record/coveringrepository_download_archive_vkt.html has 171741 bytes and sha256 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17, both matching CLAIM.md.
     - I parsed all 9490 rows (format `v<TAB>k<TAB>t<TAB>m<TAB><TAB>blocks`). There were 0 nonstandard lines and 0 duplicate (v,k,t,m) keys. Every row has m = t, so the file is the plain table only and cannot be confused with the lottery (m < t) table.
     - The only row for (61,25,3) reads exactly `61<TAB>25<TAB>03<TAB>03<TAB><TAB>28`. 27 < 28.
     - Caveat: my own single plain re-fetch of https://coveringrepository.com/download_archive_vkt.aspx at 2026-10-15T23:16:56Z got HTTP 403, a Cloudflare "you have been blocked" page. I did not retry or try to get around the block. So this value rests on the claim's fetch at 2026-10-15T23:10:40Z (HTTP 200, same run, about 6 minutes before my attempt), not on an independent fetch of mine.
     - Consistency check of the saved file against the Zenodo LJCR v1.2 data I re-fetched myself: 9482 cells in common. On those cells the saved table is equal in 8270, smaller in 1212 and larger in 0. That fits a repository that contains LJCR plus later improvements.
   - 3b. Live LJCR value (https://dmgordon.org/covering-designs/): MET, re-fetched independently.
     - I re-fetched the page at 2026-10-15T23:18:26Z (HTTP 200). It has no per-cell values; it links to coveringrepository.com.
     - https://dmgordon.org/ljcr/ (fetched 2026-10-15T23:18:59Z, HTTP 200) says the covering-designs database "was frozen after March 1, 2026", that the AWS servers were shut down in August, and that the data stays on GitHub with a Zenodo mirror. The only live per-cell LJCR value is therefore the Zenodo dataset.
     - The concept DOI 10.5281/zenodo.10779736, linked from that page, resolves to record 19735294, "La Jolla Coverings Repository", version 1.2, published 2026-04-24. That is the same record the claim cites; record 19472830 is v1.1 of the same concept, and its versions/latest also redirects to 19735294.
     - I downloaded coverdata.json at 2026-10-15T23:18:02Z: 8319503 bytes, md5 b2c626b07f216aac830d344eff5ad523 (equal to Zenodo's listed checksum), sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87. That is identical to the sha256 recorded in claim/table_record/ljcr_zenodo_v1.2_C61_25_3.json.
     - Entry C(61,25,3): size 28, low_bd 22. The best improvement listed is "28, Simple construction from (60,24,3), LJCR, 2009-01-21". 27 < 28.
     - Reading note: I take "live LJCR value" to mean this frozen Zenodo data, because the LJCR site has retired its per-cell tables and names GitHub/Zenodo as the place the data now lives. I do not consider this a stretched definition, but it is a reading.
   - 3c. dmgordo/LJCR GitHub/Zenodo value: MET.
     - On GitHub, dmgordo/LJCR was last pushed 2022-12-19T18:10:24Z, which is also the last commit touching coverings/coverdata.json.
     - I downloaded that file at 2026-10-15T23:22:07Z: 6517686 bytes, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef. It has 8759 entries, maximum k = 24, no k = 25 entries and no C(61,25,3) entry. This matches CLAIM.md.
     - The GitHub side therefore gives no value for this cell. The Zenodo side gives 28 (see 3b). 27 < 28.
   - 3d. "each re-fetched at verification time": MET.
     - The claim records fetches between 2026-10-15T23:10:38Z and 23:12:39Z in the verification run, plus an earlier coveringrepository fetch at 16:35:57Z that it says returned the same bytes. I cannot check the earlier fetch, and nothing depends on it.
     - I re-fetched the LJCR/Zenodo/GitHub sources myself between 23:18 and 23:22Z, with identical results and hashes.
     - coveringrepository.com refused my client (3a), so that source was re-fetched by the claim only.

4. "beat any value found by grepping GitHub/arXiv for that (v,k,t) over the last 6 months, including unverified hobbyist claims": NOT ESTABLISHED BY claim/.
   - claim/ contains no evidence for this clause: no search log, no queries, no results.
   - The clause as written can be satisfied, since it is a checkable live search and nothing in claim/ contradicts it. But only the NOVELTY skeptic's search can settle it. My pass below depends on that search finding no value <= 27 for C(61,25,3) in the window.
   - Related evidence that I did check: a covering for any (v',k',t') with v' >= 61, k' <= 25 and 3 <= t' <= k' gives an upper bound on C(61,25,3). No such listed value is <= 27 in any of the three tables:
     - coveringrepository saved table: 2785 such rows, minimum 28 (the cell itself).
     - Zenodo v1.2: 2782 such entries, minimum 28.
     - GitHub 2022 file: 2420 such entries, minimum 32, at C(61,24,3).

5. "If a live table cannot be fetched, the claim is 'PENDING TABLE CHECK', not a record": not triggered by the claim's record, which has HTTP 200 for each source and saved bytes. My 403 from coveringrepository.com was a block on my client. I flag it so that someone can re-fetch independently.

6. Parameter range v <= 99, k <= 25, t <= 8: MET (61, 25, 3). k sits at the boundary but inside it. The cell is listed in the table, whose rows span v 4..99, k 3..25 and t 2..8.

7. b >= Schonheim L(v,k,t): MET. I computed it with exact integer arithmetic: ceil(59/23) = 3, ceil(60*3/24) = 8, ceil(61*8/25) = 20. So L(61,25,3) = 20, which agrees with REPRODUCE.md, and 27 >= 20. Also 27 >= 22, the LJCR low_bd. No sign of a bug.

8. "Same-day claim only if C(v,t) <= 5e9": MET. C(61,3) = 35990.

## Hidden quantifiers and stretched definitions

- **Right table section:** yes. Every row of the saved archive has m = t, and exactly one row is (61,25,3,*). For context, the (61,25,t) rows read: t=2: 9, t=3: 28, t=4: 90, t=5: 285, t=6: 1329, t=7: 5104, t=8: 20255.
- **Multiplicity:** this is a plain covering (lambda = 1, "at least one block"), per CLAIM.md's definition. The observed minimum multiplicity is 1. Nothing is stretched.
- **Tie presented as a record:** no. 27 < 28 strictly, against every source that has a value.
- **One cell:** yes, (61,25,3) only.
- **Subsumed:** no (see 4). Neighbouring cells in the saved table: (60,25,3) = 26, (62,25,3) = 29, (61,24,3) = 31, (60,24,3) = 28, (61,25,4) = 90. None implies 27 or less for (61,25,3).
- **Partial wins:** p1 and p2 are not claimed. The claim is for the full criterion.

## Null model

I agree that a null model does not apply. The object is an explicit set of blocks checked deterministically and exhaustively; there is no statistical inference.

## Residual dependencies (for the panel)

- (i) The GitHub/arXiv 6-month sweep in clause 4 is not in claim/; it is left to the NOVELTY skeptic.
- (ii) My own coveringrepository.com re-fetch was blocked (HTTP 403). That source's value of 28 rests on the claim's saved copy fetched at 2026-10-15T23:10:40Z, whose hash and row I checked.

confirmed_scope: The file C61_25_3_27blocks.txt (sha256 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e) is a (61,25,3) covering design with 27 blocks (all 35990 3-subsets of {1,...,61} checked exhaustively), one fewer than the 28 listed for (61,25,3) in the m = t coveringrepository.com archive as saved by the claim from its fetch at 2026-10-15T23:10:40Z and in the La Jolla Covering Repository Zenodo v1.2 coverdata.json as re-fetched at 2026-10-15T23:18:02Z.

pass: true
