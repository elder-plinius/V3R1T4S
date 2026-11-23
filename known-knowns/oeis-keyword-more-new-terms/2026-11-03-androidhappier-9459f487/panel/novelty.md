# Panel vote: NOVELTY skeptic, run 2026-11-03-1625-capconn

context: subagent (novelty)
claim under review: A326336(11) = 70472 (first missing index n = 11)
scope: novelty / prior-disclosure / exclusion only. I did not check that the count is correct (that is REPRODUCE's job). I ran no programs, and I did not read the other panel votes, the GATE, the criterion files, or the reproduce outputs. The claim dir was copied to /workspace/panel-capconn-novelty/claim, and the raw fetches are in /workspace/panel-capconn-novelty/f_*.html.

## Live OEIS fetches (curl, Tue Nov 3 2026, 15:28:43–15:28:56 EST)
| URL | result | sha256[:16] |
|---|---|---|
| https://oeis.org/A326336?fmt=text | DATA 1, 1, 1, 1, 2, 7, 24, 100, 458, 2279, 12270 (n = 0..10); OFFSET 0,5; KEYWORD nonn,more; STATUS approved. No EXTENSIONS. The only LINK is "Table of n, a(n) for n=0..10". 70472 does not appear anywhere on the page (0 occurrences). | 7580af1a387906b0 |
| https://oeis.org/A326336/b326336.txt | "b-file synthesized from sequence entry", lines 0..10, last line "10 12270". 70472 does not appear. | c1111d16bc01d67e |
| https://oeis.org/history?seq=A326336 | Revisions #1 through #6, all by Gus Wiseman or Susanna Cuyler between Jun 27 and Jun 28 2019. The latest is #6, approved Fri Jun 28 21:14:48 EDT 2019. There is no pending or proposed draft, and 70472 does not appear (0 occurrences). | 430bf39c94810d35 |

So the first index not in DATA or the b-file is n = 11, and that matches the claim. The keyword 'more' is present on the live entry.

## OEIS value searches (same session)
- `70472` gives 1 result, A070472 "a(n) = n^3 mod 7". Its terms are only 0, 1 and 6, with period 7. The hit comes from the A-number string "A070472" matching the query, not from a term value. **This is a coincidence and has nothing to do with A326336.** No sequence anywhere in OEIS has 70472 as a term.
- `12270,70472` returns "Sorry, but the terms do not match anything in the table."
- `2279,12270,70472` also returns no match.
- `A326336` returns 6 results: the entry itself and its cross-referencing siblings (A326330, A326335, A326337, A099947, …). The prior-term-plus-70472 searches above show that none of them carries 70472.

The value 70472 is therefore missing from the entry's comments, links and extensions, from its edit history including drafts, and from OEIS search. No prior disclosure was found.

## V3R1T4S repo and GitHub
- Local repo `repo/` (HEAD 9a0d19a, 5 behind) and `git grep origin/main` after fetching (up to 7712cc8, which adds the proposed targets #492/#764/#765/#776). I searched TROPHY_CASE.md, known-knowns/*, known-unknowns/*, bank/targets.json and bank/proposed/* for `A326336`, `capconn` and the word `70472`. None of them hit. The only matches were numeric substrings inside unrelated float/certificate object files and the word "capturing" in unrelated prose. **A326336 is not named in any other bank entry or in any proposed entry**, so the bank exclusion does not apply.
- GitHub elder-plinius/V3R1T4S issues and PRs: searches for `A326336`, `70472` and `capconn` each returned 0 results. To make sure the search was working, I ran a control query `OEIS` on PRs, which returned 75 PRs. None of the first 30 bodies contains "A3263" or "70472". There is no open claim PR or bank proposal that collides with this one.
- A global GitHub code search for `A326336` returned only hex or ID noise from unrelated repos, and none of the result text contains 70472.

## Disclosure note (not prior art)
The local, unpublished outbox package `outbox/2026-11-03-[redacted]-17262752` is the nestconn claim for A326335(11) = 61987. Its program output tables (RUN_IT_YOURSELF.md and how-we-built-it/outputs/*.txt) print the A326336 column, which includes 70472 at n = 11. This is the same team's own computation, not external prior art, and the PR searches above show it has not been published. Packaging should still be coordinated: if nestconn is published first, its outputs will reveal 70472 before this claim is filed. This does not change the novelty verdict. A326336 is a separate A-number with its own cell.

## Verdict
The claimed term is at the first missing index of a live 'more' entry and was not found on the entry, in its history or drafts, in any OEIS value search, in the V3R1T4S bank or proposals, in TROPHY_CASE or known-knowns, or in V3R1T4S GitHub issues or PRs. The only hit on bare 70472 (A070472) matches the A-number string and has nothing to do with A326336.

pass: true
