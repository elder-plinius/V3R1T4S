# Novelty skeptic — run 2026-11-03-1625-nestconn
context: subagent (novelty)
claim: A326335(11) = 61987
working copy: /workspace/panel-nestconn-novelty/ (claim/ copied; live fetches saved alongside)
fetched: 2026-11-03 ~14:13 EST (America/New_York)

## Live OEIS entry (https://oeis.org/A326335/internal)
- %I #6 Jun 28 2019; %S 1,1,1,1,2,6,21,86,394,1974,10696 (n=0..10); %O 0,5; %K nonn,more -> keyword `more` present.
- No %H links, no extensions; comments/examples/Mathematica only go to a(6)/n<=5. "61987" occurs 0 times in the page.
- First missing index = 11. Matches claim.

## b-file (https://oeis.org/A326335/b326335.txt)
- "b-file synthesized from sequence entry", ends at `10 10696`. No term at n=11. "61987" absent.

## History (https://oeis.org/history?seq=A326335)
- Revisions #2..#6 only (Gus Wiseman Jun 27-28 2019, approved by Susanna Cuyler #6). No later edits, no pending/proposed draft. DATA never extended past 10696. "61987" absent.
  (/A326335/history returned "page not found"; the history?seq= form is the canonical one and was used.)

## Value searches (OEIS)
- `61987`: 5 results — A061987, A209399, A220933, A243426, A302318 (A-number/unrelated term hits; none is a set-partition/nesting sequence, none is A326335 or a duplicate of it).
- `seq:10696,61987`: "Sorry, but the terms do not match anything in the table."
- `seq:1974,10696,61987`: no match.
  -> No other OEIS entry contains the claimed continuation.

## V3R1T4S repo (origin/HEAD 7712cc8, fetched now)
- `git grep A326335` over origin/HEAD (TROPHY_CASE.md, known-knowns/, known-unknowns/, bank/ incl. targets.json and proposed/): 0 hits. A326335 is not a bank-named A-number, so not excluded.
- `61987` in TROPHY_CASE/bank: 0 hits (only coincidental digit substrings inside Thomson-problem coordinate files in known-knowns).
- GitHub issue/PR search (all states) for `A326335`, `A3263`, `61987`, `nestconn`: 0 results.
- Diffs of all 100 currently open PRs grepped for `A326335`: 0 hits.

## Other exclusions
- Not a near-repdigit/repunit prime-index sequence; Kamada clause N/A.

## Verdict
Term at first missing index n=11 of a live `more` sequence; value appears nowhere in entry, b-file, history (no pending draft), OEIS value search, or V3R1T4S trophy case/known-knowns/bank/PRs. Novelty holds (correctness not assessed by this seat).
pass: true
