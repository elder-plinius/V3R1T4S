# CRITERION skeptic: C(36,5,3) <= 812

Inputs: only claim/C36_5_3_812/ (CLAIM.md, REPRODUCE.md, check_cover.py, object/, table/). I wrote my own checker and fetch scripts in a separate scratch folder, outside claim/. All times are UTC.

## Clause-by-clause

1. **b blocks, each a k-subset of a v-set, no repeated points.** PASS. My checker (written from the definition, using Python tuples rather than the author's bitmask code) found: object/C36_5_3_812.txt has 812 non-empty lines, each holding 5 distinct integers in 1..36. There are 0 bad blocks and 812 distinct blocks (no duplicates). All 36 points are used, with point degrees from 107 to 119. sha256 f7a9401c...51da6b23 matches CLAIM.md.
2. **Covers every t-subset, checked exhaustively.** PASS. I enumerated all C(36,3) = 7140 triples and 0 are uncovered. Coverage multiplicities: 6356 triples covered once, 588 twice, 196 three times (980 excess coverings in total).
3. **Strictly below the live coveringrepository.com plain (v,k,t) value (m = t section).** PASS: 812 < 821.
   - Fetched download_archive_vkt.aspx once at 2026-10-20T23:15:17Z with a non-browser UA ("V3R1T4S-skeptic/1.0"): HTTP 200. The row reads "36 05 03 03 821". The file's sha256 is identical to table/coveringrepo_archive_vkt.txt.
   - Also ran the live systems.aspx search (GET, then the Search POST for V=36 K=5 T=3 M=3) at 2026-10-20T23:15:54Z, same UA: HTTP 200. Blocks 821, lower 756, "Creator: Anastasios Tampakis", 01/01/2009.
4. **Strictly below the live LJCR value.** PASS: 812 < 821.
   - Fetched dmgordon.org/covering-designs/ once: HTTP 200. The page lists no per-cell values. It points to the dmgordo GitHub/Zenodo data and to coveringrepository.com.
   - The legacy page ljcr.dmgordon.org show_cover.php failed with a TLS error on a single attempt. It is the same data as item 5.
5. **Strictly below the dmgordo/LJCR GitHub/Zenodo value.** PASS: 812 < 821.
   - Fetched raw coverings/coverdata.json from GitHub dmgordo/LJCR (main) once: HTTP 200, 6,517,686 bytes. Entry C(36,5,3): size 821, low_bd 756. Improvement history: 821 Tampakis 2009-01-01; 871 Dambmann SA; 889 "Simple construction: combined (35,5,3) and (35,4,2)"; ...
   - I did not fetch Zenodo separately. Zenodo v1.2 (2026-04-24) is the snapshot of the same dataset.
6. **Beats any value from a 6-month GitHub/arXiv grep, including hobbyist claims.** PASS (no competing claim found).
   - GitHub search API, issues and repos created or pushed after 2026-04-20, for "C(36,5,3)" and "36,5,3 covering": 0 hits.
   - Shallow-cloned and grepped every recently pushed covering-design repo: TheEslabonGroup/covering-designs, thebrockchain/covering-designs, hectorfarahani/covering-designs, Meliwat/covering-hunt, WynandVStaden/covering-design-records, vibemathing/...covering-designs. None has any (36,5,3) entry, and there are no file names matching 36_5_3. The only 36-point hits were other cells (e.g. C(36,5,2,3), C(36,8,5,5)).
   - arXiv API, abs:"covering designs", sorted by date, entries since 2026-04-20: none mention (36,5,3).
   - Web search for "C(36,5,3)": only the LJCR/coveringrepository listings of 821.
   - Limitation: unauthenticated GitHub code search is unavailable, so the grep covers repo/issue search plus the cloned repos, not all code.
7. **Parameter limits v <= 99, k <= 25, t <= 8.** PASS: (36,5,3).
8. **b >= Schonheim bound L(v,k,t).** PASS. I recomputed it: ceil(34/3) = 12, ceil(35*12/4) = 105, ceil(36*105/5) = 756. 812 >= 756, so the result is not below the bound and there is no bug indication. 756 is also the listed lower bound.
9. **Same-day claim only if C(v,t) <= 5e9.** PASS: C(36,3) = 7140.

## Subsumption / null-model checks
- **One-point extension of the C(35,5,3) record.** Current C(35,5,3) is 732 (coveringrepository archive) or 733 (GitHub coverdata.json). Adding a point costs C(35,4,2) = 105 blocks, so this route gives 837 or 838. 812 beats that.
- **Not structurally a one-point extension.** For every point p, the blocks avoiding p (693 to 705 of them) do NOT form a C(35,5,3).
- **Two-part sum/product constructions.** I tried every split 36 = a + b using current table values: C(a,5,3) + C(b,5,3), plus the cheapest mixed-triple terms (C(a,ka,2) x C(b,5-ka,1), C(a,5-kb,1) x C(b,kb,2), and the joint C(a,3,2) x C(b,2,2) or C(a,2,2) x C(b,3,2)). The best result was about 837 (split 1+35); the next was 883 (2+34).
- **Other neighbours give no smaller bound.** Deleting points from C(37,5,3) = 886 gives nothing better, and C(36,5,2) = 66 gives no usable shortcut.
- **Not a trivial corollary.** coveringrepository.com, which also lists derived/sum coverings, still shows 821 live. The 821 record has stood since 2009.
- **Possible structured construction.** Point degrees fall into orbit-like classes (14 points of degree 107, 14 of degree 119, 8 of degree 112), which suggests one. That does not affect validity.
- **Conclusion.** 812 is not subsumed by any standard construction I checked.
- **Minor note for the author.** The GitHub coverdata.json lists C(35,5,3) = 733 while the coveringrepository archive lists 732. This is irrelevant to this cell.

confirmed_scope: The 812 blocks in claim/object/C36_5_3_812.txt form a valid (36,5,3) covering design (all 7140 triples covered, 812 distinct 5-subsets of {1..36}), so C(36,5,3) <= 812, which is strictly below the value 821 listed on 2026-10-20 by coveringrepository.com (archive and live search) and by dmgordo/LJCR GitHub coverdata.json, and above the Schonheim bound 756.
context: subagent (fresh executor, saw only claim/)
pass: true
