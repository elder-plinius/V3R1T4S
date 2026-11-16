context: Claude Code subagent, fresh context [Sonnet 5.5]

NOVELTY SKEPTIC REPORT: 4-to-1 single-qubit QRAC with shared randomness, rigorous optimality p(4) <= 0.741482

Status source (fetched once, no retries)
- 2026-11-16T02:46:40Z, https://arxiv.org/abs/2607.10414, HTTP 200, sha256 d142a0b5...e9756f (identical to the hash in the-record-we-beat/README.md). Tan and Jafar, v3 revised 23 Oct 2026. The abstract proves the conjectured bound only for (n,n-1) and (n,n-2). The HTML intro says the high-rate cases m in {n-1, n-2} are open and lists no (4,1) result. I found nothing in v3 that settles (4,1), and the snapshot in the-record-we-beat/README.md reports (4,1) as open between 0.741481 and 0.75.
- Primary papers fetched the same minute: 0810.2937 (200), 2106.00155 (200). The original ALMO numerical value for n=4 is 0.741481 (Table 2, per the claim text).
- All fetches (UTC time, URL, status, sha256) are in a working copy (not shipped).

Literature search (last 24 months and the key older papers)
Queries: arXiv API (export.arxiv.org, queries listed in a working copy (not shipped)) for all:"random access code" AND (optimal OR optimality), for abs:"random access code" AND abs:"shared randomness", and for "random access codes" AND qubit AND "upper bound", sorted by date. Web search: "optimal 4-to-1 quantum random access code qubit shared randomness 0.7415 optimality proof" and "quantum random access code upper bound SDP NPA hierarchy (4,1) qubit proof optimal". I read the abstract or full text of the following (all 2026-11-16 02:4x UTC, HTTP 200):
- 2604.21274 (Random Access Codes: Explicit Constructions, Optimality, Classical-Quantum Gaps). Its Tables IV and V list (4,1) with 0.74148. The pdftotext table text is not cleanly aligned, so I could not map every row to its column. Table V is headed "Achievable" success probabilities, and the text says it uses numerical experiments for non-infinite-family cases. This is numerical. It gives a closed-form upper bound (Eq. 57) alongside, but nothing I found proves 0.74148 optimal for (4,1). Caveat: I did not read its Section IV in detail.
- 2606.12700 (Measurement geometry for QRACs: beyond Nayak bound): improved Nayak-type bounds and a two-qubit statement. No (4,1) optimum. No 0.7414 string in the text.
- 2607.15617 (classical codes violate the conjectured sqrt bound): about large n. Irrelevant to (4,1).
- 2601.19190 (analytical (n,n-1) construction): (n,n-1) only.
- 2312.14142 (Farkas, Miklin, Tavakoli): general analytic and SDP-style bounds. Abstract says the bound is not tight overall, and the web summary says it is tight only in known special cases. It does not settle (4,1).
- 2606.02416, 2607.10273, 2609.13075: entanglement-assisted or foundations papers. Different setting.
- Tan-Jafar 2607.10414 itself: (n,n-1), (n,n-2) only. It does not prove (4,1).
- ALMO 0810.2937 lists "optimality of numerical codes" as an open problem.
No query returned a paper with a rigorous, computer-assisted or analytic proof that the 4-to-1 SR optimum is 0.741481. The best published result is numerical: ALMO 2009 Table 2 (0.741481) plus the 2604.21274 table. The best proven upper bound is 0.75 (ALMO, Mancinska-Storgaard 2106.00155 for m=1). Limits of my search: I used a web search tool and the arXiv API, not Google Scholar, and I did not check the Ozols thesis or journal versions in detail.

This repo (elder-plinius/V3R1T4S, read-only gh)
- TROPHY_CASE.md: no match for qrac or "random access".
- The repository's known-knowns folder: directory listing (30 entries) has no QRAC entry.
- Pull requests: the 300 most recent (all states) have no title with "qrac" or "random access". GitHub issue search for "qrac" PRs and for "random access" returned 0 hits. Code search finds only the known-unknowns entries (not shipped: and the qutrit one), which describe the target as open.

Comparison with neighbouring cells and trivial edits
The claim is an upper-bound proof, not a new object. Nothing published gives the value 0.741481 as a proven optimum, so it cannot follow by deletion, restriction, relabelling or propagation from a proven result. Proven neighbours are (2,1), (3,1) (orthogonal axes), (n,n-1), (n,n-2); none implies (4,1). The success criterion's wording matches the claim exactly, and at status time the target is open. A tie rule does not apply: the claim improves the proven upper bound from 0.75 to 0.741482.

Not assessed here (other panelists' scope): correctness of the certificate and rigor of the interval arithmetic.

novelty: PASS. No prior rigorous proof found; the best published result for (4,1) is numerical (ALMO 2009 Table 2; 2604.21274 tables).
pass: true
