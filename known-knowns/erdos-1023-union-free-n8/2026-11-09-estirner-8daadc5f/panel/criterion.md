# CRITERION skeptic verdict
context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
verdict time (date -u): 2026-11-09T13:30:56Z
injection_suspected: none

## What the criterion literally requires

The success criterion quoted in CLAIM.md (bank repo commit 06b61ea) asks for:

1. an explicit list of at least 80 distinct nonempty subsets of {1..8};
2. no member S equals the union of the other members contained in S, for every S, covering unions of any number of other members;
3. a size that exceeds every value in the live OEIS A347025 entry, its comments, links and history (re-fetched just before claiming), and any value found in a fresh literature check (direction max, strictly above 79);
4. at most 89 sets (more than 89 contradicts Loo's bound and means a bug).

The claim asks for the full criterion, not an enumerated partial win.

## Object (clauses 1 and 4)

- object/union_free_n8_80.txt (sha256 8daadc5f6c94a0b0e2364d01cfb9db7931fff7e815d182b329dc4b5cd3293560): pure ASCII, one comment line, then 80 data lines. A strict parse (each line must match `[1-8]( [1-8])*`, no repeated element within a line) accepts all 80 lines.
- 80 members, all distinct, all nonempty, all inside {1..8}. Size profile: 2 of size 2, 15 of size 3, 63 of size 4. This matches CLAIM.md.
- 80 <= 89, so the Loo bug flag does not apply. I recomputed Loo's upper bound min_h a(h) + 2^h a(8-h) with a(0..7) = 0, 1, 2, 4, 7, 13, 24, 44 and got 89 (h = 1).

## Definition against the OEIS entry (clause 2)

I fetched https://oeis.org/A347025 once (2026-11-09T13:28:00Z, HTTP 200). Title: "Maximum size of a family of nonempty sets on n elements such that no set is a union of some others."

- Empty set: excluded by "nonempty" in both the OEIS title and the criterion. The object has no empty member.
- Empty union (zero other members): its union is the empty set, which never equals a nonempty S. Not a loophole.
- One other member, and members equal to S: a union of one other member T is T itself, and T differs from S because the members are distinct. A duplicate member would make the family a multiset, and the distinctness check rejects that.
- Singletons: a singleton {x} could only be the union of members equal to {x}, so the same distinctness argument applies. The object has no singletons anyway.
- The entry's own PROG (Michael S. Branicky) tests a family by ORing every r != s with r a subset of s and comparing the result with s. That is exactly the reduction in tools/check_union_free.py and REPRODUCE.md, so the claim uses the entry's own definition and test.
- Why the reduction is equivalent: any subcollection of other members whose union is S must use only members contained in S. The union U of all other members contained in S contains every such sub-union and is itself contained in S. So some subcollection has union S exactly when U = S.

## Checks run

- python3 tools/check_union_free.py object/union_free_n8_80.txt 8 80. Output: calibration a(1..4) = [1, 2, 4, 7]; members 80, distinct True, nonempty subsets of {1..8} True, union-free True; size profile {2: 2, 3: 15, 4: 63}; last line PASS. The script's union test uses strict T < S and deduplicates through set(F), so a duplicate is caught only by its separate distinctness test. A mutation with a duplicated member does print FAIL, so the combined script handles it.
- I also wrote an independent standard-library brute force that does not use the reduction. For every member S, it enumerates every nonempty subcollection of the other members contained in S and compares the union with S. Result: 0 violations. The reduction gives 0 violations too. No member contains more than 2 other members.
- I ran the same literal subcollection brute force over all families on {1..n}, n = 1..4. It gives 1, 2, 4, 7, which matches the OEIS DATA, so the literal reading reproduces the sequence.
- Mutation tests: adding {2,4,5,6} (= {2,4} union {5,6}) makes both checks fail. A duplicated member makes both fail. Removing {2,4} (79 sets) makes the contributor's script print FAIL against the bound 80.

## The bar (clause 3) and hidden quantifiers

- The fetched entry has n = 8 information in two places. The first is the comment "a(7) >= 44, a(8) >= 79, a(9) >= 144, a(10) >= 270; ... - Jon E. Schoenfield, Apr 04 2022". The second is Schoenfield's Apr 05 2022 formula. I recomputed that formula and got 4, 7, 13, 24, 44, 79, 144, 270 for n = 3..10, so it gives 79 at n = 8. DATA stops at a(7) = 44 (William Blair, Jun 2026). No other value for n = 8 appears in the entry body, comments, formula, example or extensions. 80 exceeds 79.
- "Exceed every value": read literally over all numbers on the page, this clause would include the a(9) and a(10) bounds and Loo's upper-bound formula, and no n = 8 family can exceed those. The only coherent reading is every n = 8 lower-bound or witness value. Under that reading the live bar is 79, as table/status_record.md states. My page hash (469984560e40...) differs from the claimant's (71e3c73b...). The footer carries a live timestamp and sequence count, so the hashes would differ anyway, and the n = 8 content agrees with table/status_record.md.
- History: I fetched the first history page once (https://oeis.org/history?seq=A347025, 2026-11-09T13:30:38Z, HTTP 200). It shows revisions #102 to #111 (Jun 11 to Sep 27 2026), which are only the Süskind comment, a reference and status changes. None of them holds an n = 8 value. Older revisions #1 to #101 sit on further pages, which I did not fetch.
- Links: I did not fetch the linked documents. table/status_record.md says the Blair repository holds an n = 8 witness of size 60. Loo's lower-bound formulas from the entry give binomial(8,4) = 70 and max_h a(h) + a(8-h) + 1 = 46, both below 79. The NOVELTY skeptic covers the full content of the links and the fresh literature check. This verdict does not certify them.

## Null models

- All 70 four-sets (a Sperner antichain) give 70. Loo's split bound gives 46. Schoenfield's construction gives 79. The object has 80, so it beats the published lower bound.
- The object is not padded and is not the trivial antichain. It uses 63 of the 70 four-sets plus 17 smaller sets. It is maximal: no further nonempty subset of {1..8} can be added while keeping the property (checked over all 255 subsets).

## Literal finding

The object meets clauses 1, 2 and 4 literally, and two independent methods confirm it. Clause 3 holds against the live entry body and comments (79) and against the most recent history page. The linked documents' contents, older history pages and the fresh literature check are outside what I verified. This is a full-criterion claim, not a partial win, and nothing in the entry subsumes it.

confirmed_scope: object/union_free_n8_80.txt lists exactly 80 distinct nonempty subsets of {1..8} (2 of size 2, 15 of size 3, 63 of size 4) in which no member equals the union of any nonempty subcollection of the other members (the OEIS A347025 property, equivalently no member equals the union of all other members it contains), confirmed by the contributor's script and by an independent brute force, so its size exceeds by one the bar a(8) >= 79 (Jon E. Schoenfield, Apr 2022), the only n = 8 value in the live OEIS A347025 entry body and comments as fetched 2026-11-09T13:28:00Z.
pass: true
