# NOVELTY review: finite K_10^(2) exclusion

context: fresh subagent, fork_turns=none; publication edition of the original independent review and its dated reassessment.

Review and reassessment date: 2026-11-04 UTC. This publication edition consolidates the existing evidence and verdict; it includes no new source access or computation. The reviewer inspected the frozen claim, public prior work, original source documents, and relevant prior programs independently, without reading the author's attempt notes or the other current panel reports.

**Verdict: pass for the single finite n=10 cell.** The claim is nonexistence of an injective harmonious labeling of two copies of K10 sharing exactly one vertex: 19 vertex labels in Z_90 and 90 distinct unordered edge sums modulo 90. This is the enumerated partial win p1. It makes no claim to a new algorithm, the general windmill conjecture, a performance record, or a universal proof of bibliographic absence.

Package references, relative to the package root: `the-record-we-beat/status.json` records the comparison status; `object/PROOF.md` describes the finite exclusion and its reductions.

## Primary status and original sources

KNOWN, directly inspected: the official [DS6 status page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6) was fetched once with an honest research client. Request started 2026-11-04T18:12:23.972111+00:00 and finished 2026-11-04T18:12:25.116594+00:00; HTTP 200, 18415 bytes, SHA-256 `657dcc530c17b46c5a5fec9bf0a1b4a05c37c20f3158e7e4b56aee065ae28655`.

Its linked [survey PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/) was fetched separately once: request started 2026-11-04T18:12:48.652806+00:00 and finished 2026-11-04T18:12:52.598273+00:00; HTTP 200, 3945134 bytes, SHA-256 `b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e`. The cover identifies the twenty-eighth edition, October 30, 2025. The inspected Table 2 on printed page 50 retains the conjectural two-clique windmill entry, `m = 2, H? iff n = 4`. Pages 25–26 report known restrictions. This source does not give a decision for n=10; its age alone is not the basis for the novelty verdict.

| Directly inspected original source | Relevant scope | Application to n=10 |
|---|---|---|
| Graham and Sloane, *On Additive Bases and Harmonious Graphs* (1980), Theorem 20, printed p.398 | n=4 harmonious; odd n and n=6 nonharmonious | Does not decide n=10 |
| Same paper, note added in proof, printed p.401 | Attributes to E. Levine, in a written communication dated June 24, 1980, the necessary condition that n be a sum of two squares | 10=1²+3² satisfies the condition |
| Liu and Zhang, *On harmonious labelings of graphs*, Ars Combinatoria 36 (1993), 315–326, Theorem 3.5, pp.320–321 | Excludes even n if n/2 has a prime congruent to 3 modulo 4 to an odd exponent | 10/2=5=1²+2²; no exclusion |

The [Graham–Sloane author-hosted PDF](https://neilsloane.com/doc/RLG/073.pdf) was fetched with HTTP 200, requested 2026-11-04T18:15:00.764321+00:00 and completed 2026-11-04T18:15:01.857029+00:00, SHA-256 `109e4ea21bb10a1a1b89c12e8b0df46ac2c496846c3ed0ae64edb3385263afe6`. The cited pages and definition were read, including visual inspection of the relevant page renders.

The [Liu–Zhang publisher PDF](https://combinatorialpress.com/article/ars/Volume%20036/volume-36-paper-34.pdf) was obtained on 2026-11-04 at 18:19:15 UTC with HTTP 200; 439456 bytes, SHA-256 `8df6a07604aea628bf1ef5ad6b53adccc207d7d6fa99c13bfb40cf0c8062bcf1`. The reviewer independently checked the preserved document's hash and read the original page images, rather than relying on another reader's interpretation. Theorem 3.5's explicit list of excluded n<=100 omits 10; that list concerns this theorem, not every possible known result. Theorem 3.7 concerns three cliques and cannot be used as a decision for two cliques.

INFERENCE: the inspected obstructions do not subsume n=10. Neighboring n=9 and n=11 are covered by the odd-n result, and n=12 and n=14 satisfy the arithmetic obstruction. Satisfying a necessary arithmetic condition does not establish existence of a labeling.

## Prior computation and search scope

KNOWN, directly inspected: [PR 894](https://github.com/elder-plinius/V3R1T4S/pull/894), created 2026-11-02T03:13:27Z, was an open, unmerged draft at review. Its inspected head was `ed0b44979755ef0bcf2d65bd6dce62183c65a535`. It claims n=8, expressly leaves p1 untouched, and its decision object and verification script cover n=3..8.

Its `wsearch.c` accepts n as an argument and supports q<=128; its `mitm.py` also accepts n and uses arbitrary-width integers. Both therefore accept n=10 without source changes. Nested clique backtracking and complementary edge-sum-mask joining are prior methods, and receive no algorithm-novelty credit here. Those generic programs are not themselves previously completed certificates for every input. The inspected n=8 decision does not provide an n=10 decision through parameter editing, relabeling, or restriction. In particular, restriction would not preserve the required bijection when the modulus changes from 56 to 90. No valid propagation rule deciding n=10 was identified. The additional complete finite domain is the claimed advance.

HEURISTIC, bounded search: the review searched literature and code for 2024-11-04 through 2026-11-04, exact and neighboring cells, original cited obstructions, arXiv, Zenodo, GitHub, relevant mathematical forums, and non-English terms. It also inspected the project's TROPHY_CASE, merged known-knowns, open and closed PRs, releases and assets, the adjacent contributor's fork releases, and relevant generic labeling repositories.

Raw GitHub issue-search results were inspected. The project harmonious-PR query returned one item, PR 894, with `incomplete_results:false`; corresponding windmill and exact-target queries also returned that prior claim. The closed harmonious-PR query returned no items. The fetched default-branch records and project release collection contained no n=10 windmill result; the inspected fork assets concerned other graph-labeling problems. No earlier n=10 certificate or published decision was identified. The [Müyesser–Pokrovskiy 2025 paper](https://arxiv.org/abs/2509.05280) concerns bounded-degree trees, rather than this two-clique graph. These checks extend beyond the survey, but do not constitute an exhaustive negative bibliography.

## Initial assessment, revision, and remaining limits

The initial assessment on 2026-11-04 withheld a positive novelty verdict because the full Levine 1983 and Liu 1994 papers had not been read. This was not a finding of prior n=10 coverage or a refutation of the computation. The same-day reassessment incorporated the directly inspected primary corroboration and corrected the earlier treatment of the remaining uncertainty.

The two unread originals remain explicit limitations:

- Eugene Levine, *On a harmonious graph conjecture*, Discrete Mathematics 46(1) (1983), 99–101, DOI `10.1016/0012-365X(83)90277-7`. The [publisher page](https://www.sciencedirect.com/science/article/pii/0012365X83902777) returned 403. It was not retried or bypassed. The 1980 note confirms the announced necessary condition, but does not exhaust the later paper's contents.
- B. Liu, *Sums of squares and labels of graphs*, Math. Practice Theory (1994), 25–29, cited in DS6. Its full text was not obtained or read. Its complete contents are not represented as independently verified.

The missing readings are observed documentary gaps. The further proposition that they contain an additional n=10 decision omitted by the inspected sources has no concrete supporting evidence. That is a THEORETICAL residual, with no defensible numerical probability, to accept and document. Treating it as an autonomous veto had overstated what the evidence showed. A previously unindexed result remains possible, and any later contrary evidence should correct the novelty attribution. Reading the short originals remains useful; access time is unknown. None of these statements asserts that the missing texts contain no further results.

The REALISTIC, observed methodological overlap with PR 894 is certain and explicitly credited. It does not erase the additional finite cell. After the correction, the combined status, original-source, neighboring-cell, public-artifact, and recent-search comparison supports a positive novelty assessment for n=10. No specific contrary result or trivial derivation from an earlier completed object was found. The dated reassessment therefore changed the reviewer's verdict to pass while retaining these limitations and the initial assessment in the audit history.

pass: true
