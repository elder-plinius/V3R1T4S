# Novelty skeptic -- run 2026-11-03-2004-ldsemi
context: subagent (novelty)
date: 2026-11-03 ~16:20 America/New_York (EST). Fresh fetches, raw copies in panel/novelty_fetch/.
claim: A331783(21) = 10950456. Count NOT verified here (out of role).

## A331783 live entry (oeis.org/search?q=id:A331783&fmt=text, /A331783/internal)
- %I #6 Feb 02 2020; DATA a(1..20) ends 4242226; %K nonn,more; %O 1,3; no %E extensions; no %H links besides default table.
- Comments/examples/crossrefs contain no a(21) and no 10950456 (grep count 0).
## b-file (/A331783/b331783.txt)
- Synthesized from entry, n=1..20, last line "20 4242226". n=21 absent.
## History (/history?seq=A331783)
- Revisions #1-#6, all Gus Wiseman / Susanna Cuyler, Jan 25 - Feb 02 2020. No pending draft, no later edits; "editing" strings are only historical STATUS changes. 10950456 absent.
## OEIS value search
- "10950456": No results. "4242226,10950456": No results. (fmt=data page: "Sorry, but the terms do not match anything in the table.")
## Sibling leakage
- A316473 (locally disjoint rooted trees, non-semi-identity): %I #18 Feb 14 2026; a(21)-a(25) from R. P. P. McKone, Feb 13 2026 (a(21)=15732029). Its b-file (n=1..25), history (#7-#18), and McKone's a316473.py.txt (661 lines) contain no A331783 reference and no 10950456. Different sequence/values; no leakage.
- A316471 (identity version): %I #6 Jul 2018, DATA to a(20)=214490, keyword more; b-file n=1..20; history 2018 only; no 10950456. No leakage. (Separate locdisj run not consulted.)
## Web search (2026)
- "10950456" hits: unrelated -- A188270 b-file index 1055 (different sequence, not an OEIS term-search hit), US patent 10950456, a Zenodo record id. number.house mirror of A331783 shows only a(1..20).
- No 2026 extension of A331783 found anywhere.
## V3R1T4S repo (origin/main 7712cc8, fetched now)
- git grep A331783 / 10950456 / "semi-identity" / "locally disjoint": no hits in TROPHY_CASE.md, known-knowns, known-unknowns, sealed-envelopes, news, bank/targets.json, bank/proposed. (Raw "331783" substrings only inside unrelated codetables cert JSON digits.)
- Not a bank-excluded A-number.
- GitHub PR/issue search repo:elder-plinius/V3R1T4S for "A331783", "10950456", "locally disjoint": 0 results.

## Verdict
No prior occurrence of a(21) or the value 10950456 in the entry, b-file, history (incl. drafts), OEIS search, sibling entries, web, or repo/PRs. n=21 is the first missing index. Novelty holds.

pass: true
