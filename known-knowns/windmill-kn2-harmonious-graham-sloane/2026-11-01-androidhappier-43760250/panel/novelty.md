# Novelty skeptic: windmill-kn2-harmonious-graham-sloane, cell n = 8

context: subagent (novelty)

Fresh context. I read the claim only from a private copy ($TMPDIR/claim-novelty-2341, a `cp -a` of claim/). Nothing was written into claim/. `sha256sum -c SHA256SUMS.txt` on the copy: all OK.
Claim under review (CLAIM.md, result/DECISION.txt): K_8^(2) (two K_8 sharing one vertex, 15 vertices, q = 56) is NOT harmonious, by branch (b): two independent exhaustive programs, checkers/wsearch.c (P1) and checkers/mitm.py (P2), each report 449,472 sum-distinct 8-subsets of Z_56 containing 0 and 0 labelings.
Here novelty means only this: DS6 and the literature do not already decide K_8^(2). Whether the search is correct is a question for the other panel members.

## Status fetch (one honest GET per page, UA "V3R1T4S-research-agent", no cookies, no retries)

| URL | fetch time (UTC) | HTTP | bytes | sha256 |
|---|---|---|---|---|
| https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 | 2026-11-02T00:22:54Z | 200 | 18415 | 68a1f0a879c8b46b7ac04137674be7a412cd6dc441a83a280a00037ec84c8703 |
| https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/ | 2026-11-02T00:22:55Z | 200 | 3945134 (application/pdf) | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| https://fanchung.ucsd.edu/ron/papers/80_07_harmonious.pdf | 2026-11-02T00:22:59Z | 200 | 1155753 | 109e4ea21bb10a1a1b89c12e8b0df46ac2c496846c3ed0ae64edb3385263afe6 |

(These are 2026-11-01, about 7:23 PM EST, America/New_York.) The PDF and the Graham-Sloane hashes are byte-identical to the scout's hashes in CLAIM.md, so the survey has not changed since scout time. The HTML landing page hash is different, which is expected because OJS pages are dynamic. Its content still reads "DS6: Oct 30, 2025", so no newer edition is listed.

### Value read from DS6 (28th ed., "Twenty-eighth edition, October 30, 2025")
- Table 2 (harmonious), row "windmills K_n^(m) (n > 3) (see §2.4)":
  "H if n = 4 [1376]" / "m = 2, H? iff n = 4 [1249]" / "not H if m = 2, n odd or 6 [1249]" / "not H for some cases m = 3 [2153]".
- §2.4 text (p. 25): "Graham and Sloane [1249] conjectured that K_n^(2) is harmonious if and only if n = 4. They verified this conjecture for the cases that n is odd or n = 6. Liu [2153] has shown that K_n^(2) is not harmonious if n = 2^a p_1^a_1 ... p_s^a_s where a, a_1, ..., a_s are positive integers and p_1, ..., p_s are distinct odd primes and there is a j for which p_j ≡ 3 (mod 4) and a_j is odd."
- So DS6's current value for m = 2 is: the conjecture is open ("H?"). It is settled only for n odd, n = 4 (harmonious) and n = 6 (computer). Liu's condition cannot apply to n = 8 = 2^3, which has no odd prime factor at all. n = 8 is therefore undecided in DS6.
- Graham-Sloane 1980, Theorem 20 (p. 398): "K_n^(2) is harmonious if n = 4 but is not harmonious if n is odd or n = 6. Proof. ... The computer eliminated n = 6." Followed by: "We conjecture that K_n^(2) is harmonious only when n is 4." This does not cover n = 8.

## Literature (last 24 months and older, decisive results)
- E. Levine, On a harmonious graph conjecture, Discrete Math. 46 (1983) 99-101, abstract: "if K_n^(2) is harmonious, then n must be a sum of two squares." 8 = 2^2 + 2^2 is a sum of two squares, so n = 8 is NOT excluded. Caution: one web-search AI synthesis said "8 is not a sum of two squares, so K_8^(2) cannot be harmonious". That arithmetic is false and I rejected it. A second synthesis confused gracefulness (Bermond-Kotzig-Turgeon: K_n^(m) ungraceful for n ≥ 6) with harmoniousness. I rejected that as well.
- B. Liu 1994 (DS6 ref [2153]): the hypothesis requires an odd prime ≡ 3 mod 4 with odd exponent. For even n this is the same as Levine's condition, and n = 8 is outside it. Liu's other result concerns K_n^(3), a neighbouring cell and not this one.
- D. F. Hsu 1982 (JGT, ref [1376]): K_4^(m) is harmonious for all m. Q. T. Yan 2004 ([3944]): strongly harmonious windmills. Neither touches n = 8, m = 2.
- 2024-2026 searches (web: "windmill K_8^(2) harmonious", "harmonious one-point union two complete graphs 2025/2026", "harmonious windmill computer search arXiv 2025", "Liu sums of squares labels of graphs") turned up nothing newer that decides K_n^(2) for any even n ≠ 4, 6. Nearest hit: arXiv 2403.14098 (Γ-harmonious Dutch windmills, i.e. cycles), a different family. The DS6 2024 (27th ed.) text matches the 28th ed.
- GitHub code search "harmonious windmill K_n^(2)": the only hit is this repo's bank file (known-unknowns/graphs-games-automata/windmill-kn2-harmonious-graham-sloane.md, which says "open as of 2026-10-30").

## This repo
- TROPHY_CASE.md: 0 lines match "harmon" or "windmill".
- known-knowns/: no folder for this target. Grep hits for "harmon" were unrelated binary data, a "harmonic" mention in a criterion file, and an unrelated known-unknowns harmonic-energy entry.
- Pull requests (open and closed, via GitHub search `repo:elder-plinius/V3R1T4S` for "windmill", "harmonious", "graham-sloane"): 0 results each. Issues search for "windmill": 0. The full PR list (newest 100, through #887 on 2026-11-02) has no windmill or harmonious PR. The one "harmonic" hit is #881 (LJ cluster ZPE), which is unrelated.
- Releases: list_releases returns [] (no release assets to lag the tree).

## Comparison against published objects for the cell and its neighbours
- Cell n = 8, m = 2: there is no published decision, and no published labeling to edit. A non-existence result cannot come from trivial edits of a published object (deletion, restriction, relabelling, symmetry, propagation) because none exists for this cell.
- Neighbours: n = 6 non-existence (Graham-Sloane, computer) does not imply n = 8, since K_8^(2) does not reduce to K_6^(2) under any of those edits. n = 4 harmonious (labeling exists) says nothing about n = 8. Odd n (parity theorem) and the Levine/Liu sum-of-two-squares conditions do not apply to n = 8. Hsu's K_4^(m) is a different n.
- The claim is not seeded from any published object. It is a from-scratch exhaustive search. The only symmetry used is translation (f -> f - f(c)), as documented in REPRODUCE.md and validated at n = 4 in result/brute_n4.txt (48 ordered pairs, which match result/n4_solutions_P1.txt and result/n4_solutions_P2.txt).
- Strictly beats what is known: the known state is "open (H?)", and a correct decision either way is strictly new. It is not a tie.

## Verdict
On the status read this turn (DS6 28th ed., Oct 30, 2025, unchanged since scout) and the literature and repo search, the harmoniousness of K_8^(2) is NOT already decided. If the decision is correct (for the other skeptics to judge), it is novel. Caveat: I read Levine 1983 and Liu 1994 only through abstracts and DS6's quotation, not the full texts. Both stated conditions leave n = 8 open.

pass: true
