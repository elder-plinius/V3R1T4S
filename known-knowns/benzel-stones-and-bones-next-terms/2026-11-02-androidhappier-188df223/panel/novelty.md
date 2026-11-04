# Novelty review: A364417(20) = 225354012176304818

context: subagent (novelty)

Claim read from a private copy of claim/ (claim/claim.md, claim/result/A_final/A364417_n20.out). Nothing was written into claim/.

## Live status fetches (one GET each, UA "V3R1T4S-research-agent", no cookies, no retries), 2026-11-02 06:40:30 UTC (01:40 EST)
| URL | HTTP | What it shows |
|---|---|---|
| https://oeis.org/search?q=id:A364417&fmt=text | 200 | `%I A364417 #26 Apr 25 2024`; DATA a(3..19), last term **a(19) = 20915277691567206**; keyword `nonn,more`; `%E a(15)-a(19) from James Propp, Apr 25 2024` |
| https://oeis.org/A364417/b364417.txt | 200 | "b-file synthesized from sequence entry", n = 3..19, last line `19 20915277691567206` (identical to claim/data/b364417.txt) |
| https://oeis.org/draft/A364417 | 200 | "(No pending changes for A364417.)" |
| https://oeis.org/A364416 (status_source) | 200 | A364416 DATA to a(20) = 87817595880192684, "Table of n, a(n) for n=3..20"; cross-refs A364417; page "Last modified November 2 01:10 EST 2026" |

So OEIS has no a(20) for A364417, and no draft adds one. The claimed value 225354012176304818 does not appear in any OEIS page fetched.

## Literature and code search (last 24 months)
- Propp, arXiv:2206.06472 (v4, Jan 2024), Problem 16: asks about T113(n,2n-3) and gives no a(20) (claim/data/propp_2206.06472_text.txt). The Benzel Tilings Site (via search, status June 2025) lists Problem 16 as **Open**.
- arXiv API search for "benzel": the newest hits are Byun-Ciucu-Lee (2406, EJC 2025), DFLPY generalized compression (2403, SIDMA 2025), DLPY abacus (2209), and Propp (2206). None gives new terms of A364417.
- Zenodo 10.5281/zenodo.20367029, "Advances on Propp's benzel problems" (The Clankers, 2026-05-24). The record API returned HTTP 410 (deleted 2026-10-30, "User was blocked"), so it cannot be read, and no Wayback capture was found. Its abstract mentions "valuation tables for Problems 15-18" (v2(T113(n,2n-3)) = 1 "throughout the tabulated ranges"). Its exhaustive computations are stated only for max{a,b} <= 14 or n <= 10, far below the (20,37)-benzel. This is a residual risk that cannot be checked. Nothing indicates it gives a(20).
- GitHub release assets: crabsatellite/peripheral-benzel-tilings v2.0.2 PDF and crabsatellite/benzel-problem4 v1.0.0 PDF were downloaded and searched. Neither contains 225354, 20915277691567206, or 364417.
- GitHub code search: "225354012176304818" returned 0 hits, and "20915277691567206" returned 0. "1944808008842490" (a(18)) returned 0. "A364417" returned only the V3R1T4S known-unknowns page plus unrelated noise. "benzel stones bones" and "T113 benzel" found no table past a(19).
- Web search for "225354012176304818": no relevant hit.

## This repo
- TROPHY_CASE.md: no benzel or A364417 entry.
- known-knowns/: no benzel entry. The only "364417" matches are digit substrings inside unrelated certificate and candidate files.
- bank/targets.json, target `benzel-stones-and-bones-next-terms`: says A364417 is known to n = 19, which matches the live data.
- Open and closed PRs in elder-plinius/V3R1T4S, searched for "benzel", "A364417", "stones bones" and "Propp": 0 relevant (the one "Propp" hit is #764, a Langton's-ant proposal).

## Sanity (not a correctness review)
225354012176304818 ≡ 2 (mod 4), so v2 = 1, which fits the pattern conjectured for this diagonal. The ratio a(20)/a(19) ≈ 10.775 fits the trend of earlier ratios.

## Verdict
OEIS DATA, b-file and draft all end at a(19) = 20915277691567206. No source found in the literature, in code or release assets, or in this repo or its PRs has a(20). The claimed a(20) is a new term beyond everything known: it strictly extends the record and is not a tie. Novelty holds. Correctness is for the other panelists.

pass: true
