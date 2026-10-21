# Independent NOVELTY review

context: fresh subagent, independent NOVELTY skeptic
reviewer: Independent Codex NOVELTY skeptic
scope: the fixed claim A(26,6,9) >= 5997, equivalently A(26,6,17) >= 5997; public-source comparison only
reviewed_utc: 2026-10-17T14:29:50.771752+00:00
claim_object_sha256: 6be5a215f0b662497e21330c98db83b5128095af52e4a45a8484ba60ff524de8

**Verdict: the fixed claimed size strictly exceeds the strongest identified public comparison, 5986, by 11.** This is a novelty pass for this one cell. Code validity belongs to the independent reproduction review. This report does not set a gate status or assert optimality, public priority, or maintainer acceptance.

I began with only `claim/` and the pinned rules, not the research conversation, memory, historical panel reports, or sibling reviewers. I read `target.json` verbatim. Cached inputs and published claims were treated as source data; their verdicts were not adopted. I wrote and ran my own source-screen and coordinate-incidence scripts. No downloaded construction or verification code was executed, and no new code search was conducted. Later additions were raw primary papers and the two missing published word listings, with the original inputs retained.

## Binding rule

> Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.

## Live table and mirror

KNOWN — One honest request to [A. E. Brouwer's primary table](https://aeb.win.tue.nl/codes/Andw.html), using an identified V3R1T4S client, started **2026-10-17T14:23:32.118520+00:00** and completed **2026-10-17T14:23:32.496453+00:00**, returned **HTTP 200**. Body: **127383 bytes**, SHA256 **117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8**. There was no retry, challenge, cookie replay, proxy, or browser impersonation.

The `d6` table has column headings 4 through 14. In row 26, the weight-9 entry is explicitly `5986` with reference `Pl`, followed by upper bound `16122`; its code link is `cwc/d6/a26.6.9.5986H`. Thus **5986 < 5997 <= 16122**. I parsed the row and column, rather than taking the separate historical prose example 5700 as the current bound. There is no separate weight-17 column in this triangular table.

PROVED-HERE — Complementation is a bijection on binary length-26 words, sends weight 9 to weight 17, and leaves every pairwise Hamming distance unchanged. Hence both cells have the same comparison; the mirror is checked through this exact equivalence, not an invented second printed cell. Fresh fetch and parsed row are in `../independent-novelty/live-table-receipt.json`, `live-table.html`, and `live-cell.json`.

## Literature comparison

KNOWN — I independently screened the actual **378** cached metadata records, including **153** updated during the last 24 months beginning 2024-10-17. The exact cached query receipts describe a complete 309-record phrase search and a 70-record recent binary-construction search; the union is not assumed to cover all scholarly literature. I used titles and abstracts to identify construction and propagation leads and inspected the cached primary texts and their actual tables. `../independent-novelty/metadata-screen.json` records the independent screen; `primary-text-inventory.json` records the **33** opened text inputs, hashes, and extracted tables. Supplemental exact-cell/mirror/5997 web searches produced no additional technical competitor; search snippets were not used to establish the current table value.

The binding sources were examined directly:

- [William Echols, arXiv:2608.13906v1](https://arxiv.org/html/2608.13906v1), `primary-texts/mandatory-primary/2608.13906v1.{html,txt}`: I parsed all **124** new Table 1 entries. None is the target or its mirror. The largest reported new code size is **4386**, so neither complementation nor shortening one of those reported codes can yield a competitor of size 5997.
- [Christian Lysenstoen, arXiv:2607.19550v1](https://arxiv.org/html/2607.19550v1), same directory: the four reported new lower bounds are **2979, 4214, 3539, 1855**, for other cells; the text also reports the maintainer's subsequent polishing. All remain below the candidate size. Its local-search and symmetry exclusions do not constitute a larger target code.
- [Christopher D. Rosin, arXiv:2603.00174v1](https://arxiv.org/html/2603.00174v1), same directory: the reported new code table has other parameters and no size approaching this candidate.

Newer construction leads included [Yang et al., arXiv:2609.35051v1](https://arxiv.org/html/2609.35051v1), whose Theorem 5.4 gives weight-8/distance-8 sizes **1803, 1960, 2843, 3077, 3383**, and [Alfonso Gippini Requeijo's Zenodo deposit](https://doi.org/10.5281/zenodo.23075336), whose length-29 distance-6 codes have sizes **14313** and **25896**. The latter require actual shortening comparison, performed below; their larger raw counts are not target-cell records.

I also examined the actual primary texts for `2610.15340v1` (weight-three orbit codes), `2610.10973v1` (asymptotic invariant packings), `2610.08480v1` (graph/ring linear codes), `2609.33753v1` (ranging schedules), `2608.14437v1` (intersection distributions), `2606.03299v1` (signed weight-four configurations), `2604.05607v1` (one forbidden distance), `2512.22754v1` (tilings, conditional general constructions and explicit weight-three cases), `2411.16028v1` and `2401.00733v2` (asymptotic results), `2410.22607v2` (large-block packing results), `2501.11461v2` (symmetric-distance upper bounds), `2501.12379v1` (polarization), and `2502.15019v1` (Johnson-graph clique covers). They supply no established finite binary (26,6,9) or mirror lower bound of 5997 or greater. Asymptotic attainment of a Johnson bound was not treated as a finite construction.

The three additional concrete leads were checked in `primary-texts/page2-addendum/`: [2503.11934v1](https://arxiv.org/html/2503.11934v1) constructs nonbinary weight-four diameter-perfect codes from quadruple systems; [2407.11554v2](https://arxiv.org/html/2407.11554v2) concerns disjoint difference sets for conflict-avoiding codes; [2407.04193v2](https://arxiv.org/html/2407.04193v2) constructs quaternary additive codes. Their definitions and parameter conclusions do not provide a larger binary target-cell code. I did not convert an alphabet or a distance convention silently.

Other binary-family leads were read in `primary-texts/corpus-review/`: `2610.11609v1` reports unrestricted binary code sizes **84,196,65**; `2610.04617v1` gives the book-graph family with parameters `[2c(n-1),2c-1,2n-2]`; `2510.09057v1` studies binary subfield weight distributions; `2609.25086v1` is a lattice/design classification. Older constructions `1707.02315v1`, `1505.06524v4`, and `1004.1503v3` were also inspected for parameter and alphabet applicability. None establishes the competing target lower bound.

PROVED-HERE — A potentially misleading nearby source is [Gerald Höhn, arXiv:2606.24573v1](https://arxiv.org/html/2606.24573v1), the self-dual binary `[26,13,6]` code. Its total size 8192 is not a weight-nine code size. Because the dual has minimum weight six, coordinate pairs are uniform in every coset; for its random coset word weight W, E(W)=13 and Var(W)=26/4. Therefore a weight-9 or weight-17 slice has at most `8192*(26/4)/16 = 3328` words. Any nontrivial coordinate fixing already reduces its coset to at most 4096 words. This source does not subsume the candidate through those operations.

KNOWN / PROVED-HERE — I read [Chee, Xing and Yeo's propagation paper, arXiv:1008.1610v1](https://arxiv.org/html/1008.1610v1), including the coset averaging and shortening examples. The displayed Goethals/Preparata average bounds specialized to the target yield **48** and **1526**, respectively, rather than a bound above 5997. An average lower bound is not an upper bound on every slice; the finite actual-code comparisons below are separate.

## Public repository and finite propagation

KNOWN — The cached public [TROPHY_CASE excerpt](https://github.com/elder-plinius/V3R1T4S/blob/7dd4480512cc47fe0f897164844432a2738fe649/TROPHY_CASE.md), family README, and full `reference-data/upstream-index.csv` at that commit give **5986** for this exact cell. I independently screened all **343** cached open/closed PR metadata records (**111 open, 232 closed**) and all **19** relevant file lists. No metadata or relevant filename identifies a target/mirror contribution of 5997 or greater. The explicit neighboring PR #28 code was separately counted; the other family contributions either concern upper bounds or smaller code sizes. Public filenames mentioning historical panel files were inventoried only; their reviewer contents were not used. `../independent-novelty/pr-screen.json` preserves the independent result. The supplied exact-cell and 5997 GitHub search responses also contain no matches.

PROVED-HERE — My independent coordinate-incidence program exhaustively counts every minimum fixing pattern for each supplied potentially competitive INDEX code and both complementary orientations. To reach weight 9 with at most 17 zeros after optional constant-coordinate extension, a source of oriented weight v requires at least `max(v-9,0)` fixed ones and `max(n-v-17,0)` fixed zeros. Every further fixing only removes words. Where necessary I used the packing upper bound `floor(C(n_remaining,t)/C(w_remaining,t))`, with `t=w_remaining-d/2+1`, to exclude all such subcodes before enumeration.

The nontrivial actual maxima are:

| Published source | Maximum surviving target-compatible words |
|---|---:|
| INDEX A(25,6,11), 8718 words | 1641 |
| INDEX A(26,6,11), 12222 words | 2393 |
| INDEX A(27,6,9), 8325 words | 5555 |
| INDEX A(29,6,10), 25974 words | 4476 |
| INDEX A(29,6,11), 41219 words | 3760 |
| INDEX A(29,6,12), 61823 words | 3756 |
| Gippini A(29,6,9), 14313 words | 4517 |
| Gippini A(29,6,10), 25896 words | 4290 |
| PR #28 A(27,6,10), 13026 words | 4827 |
| Brouwer A(28,6,9), 11388 words | 5162 |

All other supplied INDEX cases are excluded by source size or the independently evaluated packing bounds. I checked binary format, lengths, weights, distinctness and hashes for every code actually counted. Four exact calibration cases passed. For every pattern census, the checksum equals `M*C(w,e)*C(n-w,z)`. I did not rely on the supplied shortening script or its computed verdict.

For the two word listings initially absent from `claim/`, I made one identified, successful request per immutable public object, spaced by more than three seconds: [PR #28's fixed code](https://raw.githubusercontent.com/elder-plinius/V3R1T4S/b139a28ec67c0f0a947bc8e26705dff36bb87cba/known-knowns/bigger-codes/2026-10-14-freelsgood-9e824e9f/object/A27_6_10_13026.txt) at **2026-10-17T14:24:59.948615+00:00**, SHA256 **9e824e9f8a92e74226231152fc8e8a972be5ba79549e2a10e512fe63a3934f49**, and [Brouwer's length-28 code](https://aeb.win.tue.nl/codes/cwc/d6/a28.6.9.11388H) at **2026-10-17T14:25:03.427176+00:00**, SHA256 **fb3b5b58781c44148de6feae646ad74d97ac1f6591058416e12282b4cc1a503a**. Both returned HTTP 200. These source listings are data only. Receipts and the complete census are in `../independent-novelty/`; run `shortening_independent.py` there with Python 3 to reproduce the finite comparison.

## Evidence limits and scope of pass

This is a dated comparison against accessible, identified public evidence, not a theorem excluding all future, private, unindexed, or unposted work. The cached query responses have their stated query scopes; exact phrase absence alone was not taken as proof of novelty. I read concrete construction leads and rederived the relevant finite propagation checks. PR inspection covers all supplied paginated metadata and relevant file lists, not every unrelated comment. The finite shortening exclusion covers the listed published objects, complements, coordinate fixing and constant extension; it does not claim to exclude arbitrary unions, translations of arbitrary nonlinear codes, or new constructions. Such new operations would require their own valid competing result. No identified target-cell competitor remains unresolved in this review.

Historical access failures remain historical data; the current authorization was not treated as evidence of novelty, and no access control was bypassed. I made no repeated arXiv query or download. No publication or contact occurred.

Credit: Jean Francois Gutierrez / DrZuzzjen for the fixed candidate; Jordan Boisclair for the seed; A. E. Brouwer and the cited table and construction authors for the comparison objects and methods. The pass is limited to strict public-source improvement for the fixed claimed value, subject to independent reproduction and the separate gate.

pass: true
