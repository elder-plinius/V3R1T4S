# Criterion skeptic report: secp256k1 scalar inversion, length 281

context: subagent (fresh context, own copy of claim/)

All file names below are relative to claim/. I read only that folder, used no network, and wrote my own checks outside it; the folder is unchanged (24 files, no new files).

confirmed_scope: object/chain.txt (sha256 b4c92140602faf399a6aad09073210f46b902351a6b7db3bfa1c848e06d4ce9b) is an addition chain, valid in exact integer arithmetic, of length 281 = 251 doublings + 30 other additions for E = N - 2 = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f (the secp256k1 scalar inversion exponent, d = 2), one step shorter than the shortest published chain for that exponent in the saved copies fetched on 2026-11-10 and 2026-11-12 (Brian Smith's 2026 chain of length 282 = 251 + 31 on additionchains.com; the other saved bars are Smith's 2017 page at 290, addchain results.md at Length 293 and Best Known 290, and TTaoGaming at 288), found by a search seeded from the dictionary of that published 282 chain, with which it shares 173 of its 282 values, and not shown to be optimal or independent of that chain.

## Verdict in one paragraph

The full success criterion is met for one cell (secp256k1 scalar inversion), not a partial win. The object is an explicit chain that I checked myself with exact integers; its length 281 is strictly less than every bar in the saved evidence, the lowest of which is a published chain of length 282 that I replayed myself. An exact search of my own shows that no chain built only from elements of the three published chains I could reconstruct (282, 288, 290) is shorter than 282, so the result is not subsumed by a composition of published chains. The result is a derivative of the published 282 chain (seeded from it, 61 percent of the values in common), which the claim says plainly; the criterion asks for strictly shorter, not for independence.

## Clause by clause

| Clause of the criterion | Met? | What I observed |
|---|---|---|
| E is one of the eight listed exponents N - d | yes | The section "secp256k1 (Bitcoin) Scalar Inversion" of table/results.md prints d = 2 and N-d = fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f; I compared it programmatically with N - 2 from the SEC 2 value of n: equal. results.md has exactly eight sections with a Best Known row. |
| Explicit chain 1 = a_0, ..., a_L = E | yes | object/chain.txt: two header lines, 281 step lines, a_0 = 1, last element equals E. sha256 matches CLAIM.md. |
| Every a_i = a_j + a_k with j, k < i, exact integers | yes | My own script (Python integers, written without the claim's checker) confirms all 281 steps use strictly earlier indices; elements are strictly increasing and distinct. The claim's checkers/run_checks.sh also ends in CHECK: PASS and PASS. |
| Length strictly less than Smith's live page | yes, on the saved copy | table/smith.html prints "Total length: 290 = 253 doubles + 37 adds" for this exponent. I transcribed that chain from the page and replayed it: 290 steps, ends at E. |
| Strictly less than addchain's doc/results.md | yes, on the saved copy | Length 293, Best Known 290. |
| Strictly less than any shorter chain published elsewhere, searched for and cited | yes, within the stated search | table/LargeChains.html (additionchains.com, "updated 2 November 2026") lists secp256k1 scalar inversion at 282 = 251 + 31, credited to Brian Smith (2026). I replayed table/secp256k1-scalar-inverse-example.txt: 283 values, 282 steps, every value a sum of two earlier ones, ends at E, 251 doublings. 281 < 282. table/tt_secp256k1_288.json replays to 288 = 253 + 35 for the same exponent. table/COMPARATORS.md cites the library and paper search and lists what was not checked. |
| Best valid composition of published objects is in the bar | yes, see below | My exact search over the union of the values of the 282, 288 and 290 chains gives a minimum of 282. |
| States whether the candidate is a composition, with components and rule | yes | CLAIM.md: not a composition, seeded from the published 282 chain; it lists the dictionary values kept, dropped and added. I confirmed each number (27 seed values below 2^21, 30 in ours, 24 common, 3 dropped, 6 new). |
| Unmerged pull requests are not bars | yes | The only one mentioned (293 for this cell) is not used as a bar and is higher anyway. |

## Hidden quantifiers and stretched definitions

- **Length counted the same way on both sides.** Ours: 281 step lines, the starting 1 not counted. The published 282: 283 values, so 282 steps; the page itself says "the number of lines minus one is the chain length". Smith 2017: 290 = 253 + 37, which my replay reproduces. No off-by-one in favour of the claim.
- **Same exponent on both sides.** All four replayed chains (281, 282, 288, 290) end at the same integer E. The page table/LargeChains.html also shows a 281 for NIST P-256 scalar inversion; that is a different exponent and plays no role here.
- **Doublings.** 251 doublings whether counted from the index pairs (j = k) or from values (twice an earlier element). Two steps (11 and 27) are not star steps; both are valid.
- **"Live" pages.** I could only check saved copies. table/FETCHES.txt records each bar fetched on 2026-11-10 and again on 2026-11-12 with identical hashes; the sha256 of every saved file matches table/RECORD.md. Whether anything shorter appeared after 2026-11-12T18:20Z, or exists in a place not searched, is outside the evidence.
- **"Published elsewhere" coverage.** Honest and limited. The claimant raised the bar from the bank's 290 to 282 on its own evidence, which works against the claim. Limits stated in table/COMPARATORS.md: code search on default branches only; several libraries by code search only; no private code, mailing lists or social media. The page says Smith supplied a collection and that the downloadable example is of "the shortest supplied length", so 282 is the shortest in that collection; only one example of it is public.
- **Seed disclosure.** Plain and in the first paragraph of CLAIM.md. rebuild/search_init.txt and baseline/seed_dictionary.txt are identical and equal exactly the 27 values below 2^21 of the published chain (I compared).
- **How much is new.** 173 of our 282 values also occur in the published 282 chain. Shared: steps 0 to 9, 11 to 19, 21, 22, 24, 25, the whole stretch 29 to 157 (bit lengths 21 to 146, which is the ladder and the start of the main line), and the last 21 steps, 261 to 281 (bit lengths 238 to 256). New: 6 dictionary values and the main line from step 158 to 260. CLAIM.md mentions the shared top ladder but not the shared final 21 steps; that is an understatement of the overlap, not an error in the claim.
- **Trivial edit.** baseline/one_edit.txt scores the seed and 662 single edits of its dictionary (delete one value, insert one sum of two values, replace one value by one sum); the best is 282. I re-ran it in a separate copy and got the same histogram (282:11 283:183 284:150 285:3 308:1 309:37 310:229 311:49). What it shows: no single dictionary edit of that family reaches 281 under that evaluator. What it does not show: the evaluator is a beam search, not an exact minimum, and edits of two or more values or edits of the chain itself are not covered. The actual change is 3 values removed and 6 added.
- **Composition of published chains.** I built the union of all values of the published 282, 288 and 290 chains (602 values) and ran an exact branch-and-bound for the shortest chain for E that uses only those values. Result: 282, search exhausted in about a second (56,213 nodes). Sanity checks of the solver: each chain alone gives its own length (282, 288, 281), and the union with our chain added gives 281. So no gluing, splicing or mixing of pieces of those three chains gives 281 or less, and our chain is not such a mix: 105 of its values (99 of them above 2^22) are in none of the three. Not covered: compositions that need new elements, the explicit addchain 293 chain (only its length is saved), and the other library chains that table/COMPARATORS.md reports as 290 or 293 (I could not open them).
- **Rebuild.** The command in REPRODUCE.md rebuilt a chain from the 30-value dictionary that is byte-identical to object/chain.txt.
- **Minor record inconsistency, not material.** rebuild/search.log reports the seed dictionary at cost 284 at the start, while the baseline scores the same dictionary at 282; the two runs use different beam widths (256 and 2048). This concerns the search record only, not the object or the bar.

## Null models

A statistical null model does not apply: the claim is one explicit object checked exactly, not a measured effect. The relevant nulls are structural and both come out against a cheap explanation: the one-edit neighbourhood of the seed (best 282, reproduced) and the best chain inside the union of published chains (282, my own exact search).

## Full criterion or partial win

Full success criterion for one cell, secp256k1 scalar inversion. p1 does not apply (not one of the twelve field exponents). p2 does not apply (the length is lower, not equal with fewer additions); as a side fact the chain also has one addition fewer than the 282 chain at the same 251 doublings.

## What this pass does not cover

- Optimality: nothing here bounds the true minimum; the page itself records a lower bound of only 9 small steps against the 26 used here.
- Independence: the chain is seeded from and largely shares structure with Brian Smith's 2026 chain; credit for the ladder and most of the dictionary belongs there.
- Anything published after the saved fetches of 2026-11-12, or in places the claimant lists as not searched.
- No tool-guard block and no HTTP 401, 403 or 429 occurred; I made no network request.

pass: true
