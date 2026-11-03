# Criterion skeptic report: cover-57-14-3-b108
context: Claude Code subagent, fresh context

Target: covering-designs-record. Cell: C(57,14,3). Object: object/C_57_14_3_b108.json, 108 blocks. Hashes in the contributor's hash list were checked from inside the package folder: all OK.

## My own checks (its output is not shipped in this package)
I wrote my own script (not the author's). It reads the blocks and checks: 108 blocks; every block has exactly 14 distinct integers within 1..57; the 108 blocks are pairwise distinct as sets; the union of their 3-subsets has 29260 members, equal to C(57,3) = 29260, so every 3-subset of {1..57} is covered (exhaustive, not sampled); the Schonheim bound L(57,14,3), computed recursively with exact integer ceilings, is 90.

## Clause by clause
- b blocks, each a k-subset of a v-set with no repeated points, covering every t-subset, checked exhaustively: met (above).
- Parameters within v <= 99, k <= 25, t <= 8: met (57, 14, 3).
- b at least the Schonheim bound: met. 108 >= 90.
- Same-day claim only if C(v,t) <= 5e9: met. C(57,3) = 29260.
- b strictly smaller than the live coveringrepository.com plain (v,k,t) value (m = t section), re-fetched at verification time: NOT MET / cannot be decided. The only record of the value 109 (Franco Atzeni, 14/02/2025, lower bound 90) is the author's own form-post snapshot from 2026-10-17 about 22:41Z (HTTP status not recorded; the-record-we-beat/README.md says the orchestrator did not fetch it and has no form-post fetch for this cell). It is a day old and was not taken at verification time. My own attempts: one plain GET of the coveringrepository.com systems page at 2026-10-18T14:24Z returned HTTP 200 (811713 bytes, sha256 46eb77ac...896e) but holds no (57,14,3) row (the table needs a form post); one plain GET of the same page with query k=14, t=3, m=3 returned HTTP 403 and was not retried. So I could not re-fetch the primary table value either. Per the criterion text this is 'PENDING TABLE CHECK', not a record.
- b strictly smaller than the live LJCR value (the dmgordon.org covering-designs page): NOT MET as stated. The orchestrator's fetch of that page (2026-10-18T13:46:58Z, HTTP 200) is a prose page with no table of values; it says coveringrepository.com holds the newer improvements. So the 'live LJCR value' is not shown by that page.
- b strictly smaller than the dmgordo/LJCR GitHub and Zenodo value: met on the saved snapshots only. Argon's saved copy of the GitHub cover data file gives 110 (de Heer and Muir, 2013-09-05); Zenodo v1.2 (record 10.5281/zenodo.19735294) gives 109 (Atzeni, 2025-02-14); 108 < 109 and < 110. These were Argon's files from 2026-10-17, not re-fetched by the orchestrator, and the folder does not show that v1.2 is the newest Zenodo version. The extracted entries are in the-record-we-beat/ljcr_zenodo_entries_57_14_3.json.
- Must also beat any value found by grepping GitHub and arXiv for that (v,k,t) over the last 6 months, including hobbyist claims: only partly shown. The folder records Argon's copy of the thebrockchain README (no (57,14,3)), the orchestrator's copy of Wynand van Staden's records list (no (57,14,3) row; v=57 rows only for k = 9, 12, 16) and three coveringrepository.com latest-improvements pages (300 rows, all dated 18/10/2026, none for (57,14,3)). No arXiv search and no wider GitHub search is recorded, and the latest-improvements pages say nothing about earlier dates.
- Comparison set is every source the criterion lists: NOT MET at verification time, because the coveringrepository.com value (the primary one) and the LJCR value were not re-fetched live by anyone, and the grep over GitHub and arXiv is incomplete.

The object itself is a correct covering with 108 blocks. Whether 108 is below every live value cannot be confirmed from this folder, and the criterion says an unfetched table makes the claim PENDING.

confirmed_scope: The 108 blocks in object/C_57_14_3_b108.json are 14-subsets of {1..57} that cover all 29260 3-subsets (checked exhaustively here) and 108 is at least the Schonheim bound 90; that 108 is strictly below the current coveringrepository.com value was not confirmed, only a one-day-old author snapshot of 109.

pass: false
