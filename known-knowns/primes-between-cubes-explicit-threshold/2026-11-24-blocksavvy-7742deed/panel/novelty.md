role: novelty
context: fresh subagent (no prior conversation; saw only kit/RULES.md, the NOVELTY section and header of PANEL_BRIEFS.md, and a copy of claim/ in sandbox/panel-0730-novelty/claim; did not open attempts/, notes/, scout.md, BRIEF.md or the other panel files)
claim: For every integer n >= exp(exp(29.735)) there is a prime between n^3 and (n+1)^3, assuming Yang's 2025 UNSW thesis zero-free region (Thm 1.3, c = 51.34) and Bellotti's unrefereed preprint arXiv:2311.05136v1 Thm 1.1, plus published results (CLAIM.md, PROOF.md).
date_utc: Tue Nov 24 07:58:10 UTC 2026

## 1. Status source (one plain fetch, no retry)
- URL: https://oeis.org/search?fmt=json&q=id:A060199
- Client: curl, User-Agent "V3R1T4S-novelty-panel/1.0 (research kit; plain fetch)"; fetched 2026-11-24T07:53:27Z; HTTP 200.
- sha256 d132575bbd4f0fd0d1bf0eb86ef09a0239b5c60ac8817d7becab7dc7fca6cc5e. This is byte-identical to the claim's data/A060199.json. Revision 87, time 2026-05-05T10:45:35-04:00.
- Value (quoted): "Mossinghoff, Trudgian, & Yang improve this to n > exp(exp(32.76)) = 3.62275 * 10^73328286790528. - _Charles R Greathouse IV_, Jul 31 2024". Earlier entries are 33.217 (Dudek) and 32.892 (Cully-Hugill). OEIS has nothing below 32.76. KNOWN
- Record statements in the package, checked against the PDFs (pdftotext):
  - data/ch_thesis.pdf (sha256 0968f349...87f7), Theorem C / Thm 4.3: "There is at least one prime between n3 and (n + 1)3 for all n ≥ exp(exp(32.537))." KNOWN
  - data/arxiv_2601.15564.pdf (v2, 16 Mar 2026; sha256 4098d35f...359b), Johnston-Sorenson-Thomas-Webster: "... exp(exp(33.3)), which has only been improved mildly since to exp(exp(32.537)) by Cully–Hugill in her PhD thesis [7]." KNOWN
  - The best rigorous record is 32.537. The claim's comparison against it is right; 32.76 and 32.892 are weaker.

## 2. Search (2024-11 to 2026-11)
I opened every source below. The time is the fetch time in UTC.
| source | URL | fetched (UTC) | HTTP | cube threshold found |
|---|---|---|---|---|
| Lee, Minimal zero-free regions ... kth powers | https://arxiv.org/abs/2602.14340 (WebFetch) | ~07:54 | 200 (WebFetch) | quotes 32.892 only; k=86 result |
| Cully-Hugill & Johnston, RvM error term II | https://arxiv.org/abs/2402.04272 (WebFetch) | ~07:54 | 200 (WebFetch) | 90th powers only, no cube threshold |
| Chamberland & Straub, Weakening the Legendre Conjecture | https://arxiv.org/pdf/2602.22502 | 07:55:57 | 200 | quotes 32.537 |
| Visser, Effective short intervals (v3, 12 Jul 2026) | https://arxiv.org/pdf/2508.18786 | 07:55:57 | 200 | quotes 32.892, rounds to 33 |
| Fiori & Jaskari, Explicit bounds for the PNT (v2, Oct 2026) | https://arxiv.org/pdf/2609.23222 | 07:57:29 | 200 | no cube result |
| Bellotti, new zero-density near sigma=1 (Aug 2025) | https://arxiv.org/pdf/2508.02041 | 07:57:29 | 200 | no cube result (neighbouring input, unused by the claim) |
| arXiv search "consecutive cubes prime" | https://arxiv.org/search/?query=consecutive+cubes+prime&searchtype=all&order=-announced_date_first | 07:56:14 | 200 | only 2601.15564 is relevant |
| arXiv search "primes between cubes" | same form | 07:56:11 | 429 | not retried; I stopped querying arXiv search |
| arXiv export API (2602.14340, 2402.04272) | https://export.arxiv.org/api/query?id_list=... | 07:54:10 / 07:54:26 | 429 / 429 | none; I fell back to the abs pages |
| rStation paper 130 (u/span_of_dilates, v2, 08 Nov 2026) | https://rstation.ai/problems/riemann_hypothesis/papers/130 | 07:54:59 | 200 | non-rigorous model only (see section 3); sha256 f5ed348e... is identical to data/rstation_130.html, so there is no newer version |
| rStation RH paper list | https://rstation.ai/problems/riemann_hypothesis/papers | 07:54:59 | 200 | no other cube-threshold post; I opened papers 194 and 190 (07:55:15, 200, 200), which are not relevant |
| rStation paper 111 (via search) | https://rstation.ai/problems/riemann_hypothesis/papers/111 (search snippet) | - | - | conditional on a 7/8 half-plane; cites 32.537 as the unconditional record |
| Cairn Commons, Legendre's conjecture | https://cairn-commons.com/problems/legendre-conjecture | 07:54:59 | 200 | lists 32.76 (MTY 2024) as of 2026-10-03 |
| MathOverflow 514949 (search snippet) | https://mathoverflow.net/questions/514949/explicit-number-theory-from-guth-maynard | - | - | Johnston: "the best bound on n is actually n ≥ exp(exp(32.537))" |
| MTY, Res. Number Theory 10 (2024) (search snippet) | https://link.springer.com/article/10.1007/s40993-023-00498-y | - | - | 32.76, from substituting their zero-free region into Cully-Hugill §4 |
| Broucke, Anal. Math. 2026 (search snippet) | https://link.springer.com/article/10.1007/s10476-026-00176-y | - | - | cites 2311.05136 still as an arXiv preprint; no cube result |
| GitHub PR search, elder-plinius/V3R1T4S (open and closed): cubes, A060199, Ingham, between cubes, 32.537, zero-density, Bellotti, Cully-Hugill, primes-between | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+... | 07:55:23 to 07:55:31 | 200 (all) | no PR on this target |
| repo TROPHY_CASE.md, known-knowns/, known-unknowns/, bank/ (local, commit 25c99686) | - | - | - | no entry for primes between cubes |
| Yang thesis and Bellotti JMAA (data/yang_thesis_2025.pdf, data/arxiv_2306.10680.pdf) | - | - | - | neither states a cube threshold (grep "cube" finds nothing) |
Gaps: Google Scholar's citation lists, Zenodo, aiXiv and Hexagon were covered only through web search, which found no relevant hit. I did not query them directly, so a deposit those engines do not index cannot be ruled out. HEURISTIC

## 3. Pre-emption check: rStation paper 130, §2.3
Quoted: "Remark (model, not a theorem). The same model with [3, Thm 1.3] in place of the Kadiri–Lumley–Ng bound used in [5] gives log log n_0 ≈ 30.07, against the record 32.537 quoted in [7]. We have not checked whether a rigorous version of (17)–(21) keeps this, and we have not read the thesis in which the record is proved."
- This remark does not pre-empt the claim. It is labelled a non-rigorous model and is not a threshold. It uses Bellotti's Thm 1.3 (T ≥ exp(6.7e12), proof only sketched), not Thm 1.1, and it does not use Yang's c = 51.34. KNOWN (from the text)
- It does anticipate the idea: put Bellotti's near-unity density into Cully-Hugill's argument. The claim goes further in three ways. It gives a rigorous chain: Lemma 4(c) is a new integral bound for the T^{B(1-sigma)^{3/2}} shape, and Lemma 6 proves monotonicity for all larger n. Its certificate uses outward-rounded intervals. Its value of 29.735 is below the model's ~30.07. The claim's own journal-only-ZFR variant (Bellotti JMAA c = 53.989, 29.906) is also below 30.07. The Ford variant (30.123) sits close to the model, which fits the model being roughly right. HEURISTIC
- Trivial-edit test: the gain comes from substituting two newer inputs into a published argument. In this field that is how records move: MTY 2024 got 32.76 by plain substitution. Here the density shape changes, which forces new lemmas, so the substitution is not mechanical. The claim beats every published or posted object, including the non-rigorous 30.07, and is not a tie.
- Substituting only Yang's zero-free region gives 32.505 (PROOF.md §5). That is a near-trivial update, 0.032 below 32.537. Novelty must rest on the I4 step, which no source I found has carried out rigorously.

## 4. Defects the gate must have fixed (credit, RULES.md 13)
1. CLAIM.md and PROOF.md never cite rStation paper 130 (u/span_of_dilates, 08 Nov 2026), although it is in data/ and anticipates the idea. It must be named with its URL as prior non-rigorous anticipation, and the scope sentence must not suggest the idea is new.
2. The 32.76 record is credited to "OEIS A060199". It should be credited to Mossinghoff, Trudgian & Yang, Res. Number Theory 10 (2024), with a link. Cully-Hugill (JNT 2023 and thesis), Yang, Bellotti, Kadiri-Lumley-Ng, Hasanalizade-Shen-Wong, Dudek and Johnston-Sorenson-Thomas-Webster are credited.
3. Process flag: data/fetch_log.txt says the first fetches used "a generic curl 'Mozilla/5.0' UA". If that covers the OEIS status fetch at 07:34:04Z, it breaks the honest-UA part of RULES.md 5. My own honest fetch (section 1) returned byte-identical content, so the status value stands regardless.
4. Neighbouring inputs the claim does not use: Bellotti arXiv:2508.02041 (2025, density near sigma=1) and Bellotti JNT 269 (2025, log-free density). These could move the threshold further. They are not a published threshold and do not affect this verdict.

## 5. Verdict
No published or posted rigorous threshold <= 29.735 was found. The best rigorous record is 32.537 (Cully-Hugill thesis Thm 4.3). The OEIS status is 32.76, fetched 2026-11-24T07:53:27Z with HTTP 200. The only lower posted figure is rStation's ~30.07, which its own text calls a non-rigorous model. 29.735 strictly beats everything known, so novelty passes. This holds only within the claim's stated dependence on Yang's thesis (I3) and Bellotti's unrefereed preprint (I4). Passing is conditional on fixes 4.1 and 4.2 being made before anything is packaged; they change credit, not the result.
pass: true
