context: Claude Code subagent, fresh context [Sonnet 5.5]

# Novelty skeptic report: (3, 11, 19)-net in base 3, claim of nonexistence via OOA(M, 19, S_3, 4, 8) LP dual

Scope: I assessed novelty only. I did not re-verify the certificate arithmetic (that is another skeptic's job). Files in this package were read for the claim text and baseline snapshot only.

## 1. Primary page, fetched once, no retries

Fetch log (UTC time, URL, HTTP code, sha256):

| time | URL | code | sha256 |
|---|---|---|---|
| 2026-11-18T01:26:36Z | http://mint.sbg.ac.at/query.php?b=3&s=19&m=11&p=smt | 200 | 9c138a9b22271f54ab1818ba33ecff9ed21603cce456cb91414caa924a1da399 |

The hash is identical to the one in the-record-we-beat/SNAPSHOT.md, so the page was unchanged since the claimant's fetch of 2026-11-17T15:18Z. Page footer: "Last update to the database: 2024-09-05".

Quoted values:
- "Best known t": "(5, 11, 19)-Net over F3 — Constructive and digital. Digital (5, 11, 19)-net over F3, using s-reduction based on digital (5, 11, 25)-net over F3, using linear code embedding found in a computer search".
- "Lower bound on t (digital)": "(4, 11, 19)-Net over F3 — Lower bound on t (digital). There is no digital (3, 11, 19)-net over F3, because s-reduction would yield digital (3, 11, 16)-net over F3, but 2 times m-reduction would yield digital (3, 9, 16)-net over F3, but extracting embedded orthogonal array would yield linear OA(3^9, 16, F3, 6) (dual of [16, 7, 7]-code), but "vE2" bound on codes from Brouwer's database".
- "Lower bound on t": "(3, 11, 19)-Net in Base 3 — Lower bound on t. There is no (2, 11, 19)-net in base 3, because s-reduction would yield (2, 11, 12)-net in base 3, but extracting embedded OOA would yield OOA(3^11, 12, S3, 2, 9), but the linear programming bound for OOAs shows that M >= 11160261/52 > 3^11".

So the open gap (general 3 vs digital 4) is confirmed live.

## 2. Propagation from neighbouring cells (11 further MinT queries, about 4 s apart)

All queries used the same curl user agent and returned HTTP 200. Times and hashes:

| time (2026-11-18) | cell (b=3) | sha256 |
|---|---|---|
| 01:27:17Z | m=11, s=13 | 4e053f233b495bf84a5e96eef4e7bdef06bd580d86bed8c7c7eb1ec927637c55 |
| 01:27:21Z | m=11, s=15 | f86d9e48f5d1a035950d8a165634ed48a7cde9b1f7ddac4ced79dca91568c396 |
| 01:27:26Z | m=11, s=16 | 564716b15ded17d87224a5b85fef9e9b8429ebaf354337636f817e872f69acda |
| 01:27:30Z | m=11, s=18 | c384f3f0ded86d33c41206ce26e870a13731029cd9d35b77e8d628820e25cf5d |
| 01:27:35Z | m=10, s=19 | 043005c2c4a643ae1148721f7e8477f132211b2aa04689c0612297a224d1d88a |
| 01:27:40Z | m=12, s=19 | 3ef65ff8e2fecd372b9afecc17db57d01f1479a3bd3c68609fa0c53664526e5c |
| 01:27:44Z | m=11, s=17 | 9d2f0879beda5e89fc49bd56488c803964c1998684d121c276c650ec47433399 |
| 01:29:04Z | m=11, s=8 | fcc5ef7092b6f7ade0dad83623c8951d80a5d202cbc4de87370a7404233c6b81 |
| 01:29:08Z | m=11, s=12 | 6b9daf1c60b59f443d48568dd80a907c1b416625c4624f92e0001add8ea1d519 |
| 01:29:13Z | m=11, s=14 | 5dd73161c189127fe5e5b00f76c70299a4f9dad9078f1a738119263634c8f239 |
| (earlier mistyped URLs with a space were rejected by curl before any request left the machine; no HTTP exchange occurred) | | |

URLs follow http://mint.sbg.ac.at/query.php?b=3&s=S&m=M&p=smt. The page for (m=11, s=19) was fetched once, and the 10 neighbour queries come to 11 MinT query-page fetches in total. I also fetched http://mint.sbg.ac.at/desc_OBoundLP.html at 2026-11-18T01:27:57Z (200, sha256 a878ed653883ad890fd2648a1a63655b23dbb7e8b48c38efdd2d035ea07b4404). That is 12 MinT fetches, within the 15 bound.

Findings:
- m=11, s=12 to 18: the general lower bound on t is 3 in every cell (no (2,11,s)-net via s-reduction to (2,11,12) and the depth-2 OOA LP). None of them excludes a t=3 net. Best known t is 4 at s=12 to 15. The digital bound is 4 at s=16 to 19.
- m=11, s=8: general bound t >= 2. This is irrelevant to t=3.
- m=10, s=19: general bound t >= 3 (generalized Rao bound on (2,10,15)). It does not exclude t=3.
- m=12, s=19: general bound t >= 4, from "no (3,12,19)-net, because s-reduction yields (3,12,18), whose embedded OOA(3^12,18,S3,2,9) violates the LP bound". This is nonexistence at larger m. The only propagation rules are m-reduction (which maps m down to smaller m, so it goes the wrong way) and t-increase, which maps (t,m,s) to (t+1,m+1,s) or (t+1,m,s). A (3,11,19)-net gives (4,12,19) or (4,11,19), not (3,12,19). Nothing here implies (3,11,19) nonexistence.
- s-reduction goes from s=19 down to s'<=18, and every such cell (3,11,s') is open at t=3 on MinT. So no known nonexistence propagates to (3,11,19).
- The nonexistence of the digital net comes from a linear-OA bound that applies only to linear objects.

Conclusion: nothing MinT lists, nor any rule applied to a MinT-listed nonexistence, implies that no (3,11,19)-net exists.

## 3. What MinT computes for the OOA LP, and the literature

desc_OBoundLP.html (quoted): "For depth T = 2 we have calculated all LP bounds for s <= 25 ... For depth T = 3 we have calculated all LP bounds for s <= 11 as well as all bounds for k <= 20 and s <= 15. For depth T = 4 we have calculated all LP bounds for s <= 8 and k <= 19." The page cites Martin-Stinson 1999 (base 3, depth 4 appears in one solved LP in that paper), Martin 2000 (s <= 15 at T = 3, base 2) and Bierbrauer 2007. Version 2024-09-05. So the depth-4, s=19, k=8 LP for base 3 is not in MinT. The claimant's HOW_WE_FOUND_IT.md says the same.

Literature search (web search, several queries, mostly foundational hits): Martin-Stinson 1999, Martin-Visentin dual Plotkin, Bierbrauer 2007 (arXiv cs/0702033), Schmidt-Weiss 2021 (arXiv 2109.01586), Schuerer-Schmid MinT. I found no paper, preprint or table from the last 24 months giving a depth-4 base-3 LP result, or any bound on (3,11,19)-nets or OOA(3^11,19,S_3,4,8). I did not run a GitHub code search beyond this repository and a general web search; my search tool is a general web search with limited depth, so this absence is evidence, not proof. The depth-4 LP step is also an obvious one (depth T=4 for t=3 is the natural extension of what MinT does at T=2 and T=3); but it is new as far as I can find, not published.

## 4. This repository (elder-plinius/V3R1T4S, read-only gh)

- the repository's known-knowns folder on main (listing read): no mint-net-below-digital-bound folder exists. No MinT-related known-knowns entry at all.
- TROPHY_CASE.md on main: no MinT, OOA or net row (grepped "mint", "ooa", "(t,m,s)").
- The target file the target's own page in the repository's known-unknowns folder is still open and lists p1 as an unclaimed partial win; the claim's wording matches it.
- Pull requests (all states, search by title, branch, "mint", "net-below-digital", "OOA 19", "(3, 11, 19)", "LP dual certificate OOA"): no PR for mint-net-below-digital-bound. MinT-related PRs are #1050 (open, linear OOA(3^8,8,F_3,2,7) at a different cell, depth 2), #1006 (open) and #875 (closed) (binary digital net (11,24,17), a different cell and a digital construction). None claims (3,11,19) or an LP certificate for it. Nothing merged is a parent that this result follows from by restriction.

## Verdict on novelty

Not implied by MinT or its propagation rules, not in recent literature that I could find, and not claimed in this repository. The claimant names MinT, Martin-Stinson and Bierbrauer as the method source and does not seed from a published object (it is a bound, not a net). Caveats: (a) the novelty of "bound beats everything known" rests on MinT's last database update being 2024-09-05 and my web search being shallow on 2025-2026 preprints; (b) correctness of the certificate was not checked here. A tie is not at issue: the claim raises the general bound from 3 to 4, strictly above MinT's 3 and equal to the digital bound 4, and no stronger published statement exists. It does not beat the digital bound of 4, but the p1 criterion asks only to close the cell at the general lower bound, which is what it claims.

pass: true
