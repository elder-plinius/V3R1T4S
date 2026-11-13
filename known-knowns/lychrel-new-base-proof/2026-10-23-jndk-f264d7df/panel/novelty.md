# Novelty skeptic verdict: lychrel-new-base-proof, base 13 (updated)

context: subagent (Claude Code Agent tool, fresh context)

Claim under test: a Lychrel number exists in base 13 (134-digit seed, 10 affine run-length templates). The result is novel
only if no Lychrel number has already been proven to exist in base 13. This verdict covers novelty only. Whether the
proof is correct is for the other skeptics.

novelty: CONFIRMED. Base 13 is not a proven Lychrel base in any source reachable at verification time, and no prior or
competing base-13 proof was found.

This update follows a coordinator follow-up. It closes two gaps from my first verdict: the full 2023 paper, and the open
PRs.

## Status page fetch (one fetch, honest client)

- URL: https://en.wikipedia.org/wiki/Lychrel_number
- client: one plain `curl -s -A "V3R1T4S-research-agent" -w '%{http_code}'`, no retries
- fetch time (date -u): 2026-10-23T22:36:25Z
- HTTP status: 200
- sha256: e574eb9d22306bccc3cbdc8bf2f597e5d8543e64d9ac183b9521b7ecdbd95270 (206694 bytes; saved as
  panel-work-b13/novelty/mine/wikipedia_lychrel_novelty.html)
- revision: wgRevisionId 1376703229, "last edited on 25 September 2026, at 19:28". The sha256 matches the author's earlier
  fetch in status/STATUS.md, so it is the same revision. I did not use the author's copy as my fetch.
- quoted list of proven bases (section "Other bases"): "Lychrel numbers have been proven to exist in the following bases:
  11, 17, 20, 26, and all powers of 2."
- base 13 appears on the page only in the table of the smallest *possible* Lychrel number per base: "13 | 12CA (2701)".
  That is a candidate, not a proof.
- Result: base 13 is NOT listed as proven on the status page at verification time.

## Literature and other sources searched

- "On the Construction of Some Lychrel Numbers", R. S. Kuitché, Research Square preprint rs-2659802 v1
  (doi 10.21203/rs.3.rs-2659802/v1, 2023):
  - Source: the full 30-page PDF from https://assets-eu.researchsquare.com/files/rs-2659802/v1/3abe4ea916f8c04c44cb883f.pdf.
    It was supplied by the coordinator in panel-work-b13/novelty/extra/. Its receipt says fetched 2026-10-20T10:16:28Z,
    HTTP 200. I recomputed the sha256 myself: c5130873a5d82c3577ac52d7a9a1ec94a7dce1017d9ce2dededa13a87f64dac7, which
    matches the receipt. I read all pages.
  - Content: every lemma, proposition and corollary is stated for "base b (3 <= b <= 10)". The abstract says "we answer
    this question by proposing in bases between 3 and 10 some mathematical approaches ... notably in base 4 and base 10".
  - The only Lychrel number it constructs is in base 4 (a = 255 = 3333 in base 4; section 4, Case 1). Base 10 gets only
    candidates ("Here we have not been able to exhibit a Lychrel number despite all our effort").
  - It cites proofs in "the bases 2, 11, 17 or 26".
  - Base 13 never appears, and it claims nothing beyond bases 3 to 10.
- ResearchGate copy of that paper (369073006): returned HTTP 403 on my first and only attempt. Not retried, and no longer
  needed now that the full text was read.
- OEIS A060382 (WebFetch; page says it was last modified October 23 2026): a(13) = 2701. Comment: "Only a(2) is proved,
  all the others are conjectured." No base-13 proof.
- OEIS A023108 / A088753 (search results): base-10 kin and seed lists only; nothing on base 13.
- MathPages, David Seal's January 1996 post (MathPages page at www.mathpages.com, file dseal.htm, via WebFetch): gives sporadic non-palindromic
  solutions for bases 4, 11, 17, 20, 26 only. Base 13 is not included.
- MathPages "Digit Reversal Sums Leading to Palindromes" (search snippet): mentions "a few sporadic examples in bases other
  than powers of 2, as shown by David Seal". Nothing on base 13.
- p196.org (math_solutions page, WebFetch; FAQ via search): no base-specific proofs; base 13 not mentioned.
- Wikipedia Talk:Lychrel_number (WebFetch): no discussion of new proofs in base 13 or any other new base.
- Kuitché, "Lychrel Numbers in Base 10: A Probabilistic Approach", Adv. Pure Math. 14(8), Aug 2024 (SCIRP, WebFetch):
  probabilistic argument for base 10; it cites proofs in "the bases 2, 11, 17 or 26". Base 13 is not mentioned.
- mizopl, "Mechanical Template-Closure Proofs of Lychrel Numbers in Bases b = 50, 98, and 146", Zenodo preprint
  10.5281/zenodo.23468033, 19 Oct 2026, plus GitHub repo (WebFetch): claims new proofs for bases 50, 98, 146 only.
  It states that the proven bases before it were powers of two and {11, 17, 20, 26}. 13 appears only as a factor of 26.
- dew-web/lychrel-self-similar (GitHub, 2026, WebFetch): a computer-assisted base-9 Lychrel family. It never mentions
  base 13.
- Dozenal wiki "Lychrel number" (search snippet): its proven-base list is written in dozenal ("E, 15, 18, 22" in base 12,
  which is 11, 17, 20, 26 in decimal). No base-13 proof.
- arXiv: the direct search https://arxiv.org/search/?query=Lychrel&searchtype=all says "Sorry, your query for all: Lychrel
  produced no results." My earlier attempt was a malformed author-search URL that returned 404; this is the correct
  search page, not a retry of a block. Web searches for 2024-2026 reverse-and-add proofs found only unrelated palindrome
  papers and arXiv 2012.02524 (a survey with a base-2 example only).
- CANUM 2024 abstract (Mahiddini): numerical experiments only, no proofs.
- MathOverflow "Status of the 196 conjecture?" (K. O'Bryant answer, 26 Dec 2012, cited by Wikipedia): the fetch tool could
  not reach mathoverflow.net, and per instructions it was not retried. It is a 2012 source, outside the 24-month window,
  and is one of the references behind the Wikipedia list quoted above. I do not count it as blocking.
- Repo TROPHY_CASE.md (pinned repo): no entry mentions Lychrel, palindrome, reverse-and-add or base 13.

## Open-PR check (github.com/elder-plinius/V3R1T4S)

- First read: the PR list page, read-only (WebFetch). It reports 306 open PRs. The 25 shown (#599 to #632) include no
  Lychrel, palindrome or base-13 PR.
- Second read, a different page explicitly allowed by the coordinator: the filtered search
  https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+is%3Aopen+lychrel (query shown on the page: "is:pr is:open
  lychrel"). It shows "Open 1". The one match is #517, "Claim: lychrel-new-base-proof CONFIRMED_SOLUTION (Lychrel numbers
  proven in bases b = 50, 98, 146 + Kuitche 2023 audit)", opened Oct 19, 2026 by mizopl.
- It covers bases 50, 98 and 146, not base 13, so there is no prior or competing open PR for base 13.
- A PR about base 13 that never uses the word "lychrel" would escape this search. That is implausible for this target id,
  whose name itself contains "lychrel".

## Remaining unreached sources and why they do not block

- MathOverflow 2012 answer: it predates the 24-month window, Wikipedia cites it among the references for its proven-base
  list, and no later source attributes a base-13 proof to it.
- ResearchGate: its copy is superseded by the full Research Square PDF.

Every source I could reach that lists proven bases agrees: powers of 2 and {11, 17, 20, 26}, with self-published 2026
claims adding 9, 50, 98 and 146. None includes 13.

## Verdict

Base 13 is not 2^k, not in {11, 17, 20, 26}, and not listed as proven on the Wikipedia status page at
2026-10-23T22:36:25Z (HTTP 200, revision 1376703229). It is also absent from the 2023 construction paper (bases 3 to 10
only), from all 2024-2026 literature found, from TROPHY_CASE.md, and from open PRs (the only Lychrel PR, #517, is for
bases 50, 98 and 146). A proof in a base with no previously proven Lychrel number strictly extends what is known, so this
is not a tie. Novelty passes, conditional on the proof itself being correct, which is the other skeptics' check.

pass: true
