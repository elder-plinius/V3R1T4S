context: Claude Code subagent, fresh context [Sonnet 5.5]

Novelty skeptic report. Claim: GF(2^7) mod x^7+x^4+1 (0x91) multiplier, 82 gates (object/gf128_0x91_82gates.slp.txt); bar: NIST/CMT 84, partial-win threshold 83.

Status source (fetched once each, no retries; full log in a working copy (not shipped))
- 2026-11-16T02:46:43Z https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits, HTTP 200. Row "GF(2^7) mod x^7+x^4+1": 40 AND, 44 XOR, 84 gates, depth 5. Row for x^7+x^3+1: 85. GF(2^6): 57. GF(2^8): 117. (The page's sha256 differs from the one in the-record-we-beat/README.md, so the page changed since the claimant's fetch, but the 84 value is unchanged.)
- 2026-11-16T02:46:43Z https://www.cs.yale.edu/homes/peralta/CircuitStuff/CMT.html, HTTP 200, byte-identical to the claimant's snapshot (same sha256). Says "a circuit with 84 gates" for x^7+x^4+1.
- 2026-11-16T02:46:45Z https://csrc.nist.gov/projects/circuit-complexity, HTTP 200 (project page, no new GF(2^7) figure found).
- 2026-11-16T02:46:44Z https://github.com/Swapnil-jain/gf2m-circuits, HTTP 200. Via gh api: main head 9daf883e (2026-10-11), no releases, no tags, one branch, 2 PRs (#1 merged contrib for GF(2^9-11) and GHASH; #2 open, GF(2^14-16) and standard fields). No GF(2^7) change. In multipliers/circuits, final_f7.slp (the 0x91 circuit, checked with --field 0x91 in its README) has 87 gate lines (T1..T87). final_f73.slp and final_f73_d6.slp have 83 gates each; they are the other trinomial field (x^7+x^3+1), not 0x91. Gf7_f74.lean also exists (the 0x91 Lean proof). So nothing at 82 or fewer for 0x91 there.
- usnistgov/Circuits data/slp/gf (gh api, latest commits 2026-11-14): gf128-730, gf128-740, gf256-84310, gf64-630 only; no new GF(2^7) file; recent commits are S-box work.

Repository search (elder-plinius/V3R1T4S, read-only)
- gh pr search for "GF(2^7)", "0x91", "gf128", "x^7 + x^4 + 1": no hits. No open or closed PR covers this cell or target gf2-polymult-8term-25-products. TROPHY_CASE.md has no GF(2^7), 0x91 or gf2-polymult mention. Code search finds the target only in a working folder (not shipped) pages.

Literature (web search, queries: "GF(2^7) multiplier circuit gate count x^7+x^4+1 fewer than 84 gates"; "low gate count binary field multiplier small fields SLP SAT heuristic 2025 2026 arXiv ePrint GF(2^7)"): nothing found that gives a classical AND/XOR count for this field below 84. Results were quantum Toffoli/T-count papers (arXiv 2501.16136, 2511.20618, 2407.08695), generic bit-parallel formulas, and patents; none apply. The search tool is shallow, so this is absence of evidence from a limited search, not proof.

Trivial-edit check: the only published circuits for 0x91 are 84 (NIST/CMT) and 87 (Jain). The claim is 2 below the best, with different shape (34 AND, 48 XOR, depth 6 vs 40/44, depth 5), so it is not a deletion, relabelling or small polish of the 84 circuit by gate count; I did not run a structural diff against gf128-740. I did not re-run the claim's verifier (that is the other skeptics' job). The claim does not say it was seeded from a published circuit.

Verdict: nothing published at 82 or fewer found for this exact field and modulus; the claim strictly beats the 84 bar and the 83 threshold on all sources checked. Residual risk: limited literature search depth; Jain's 83-gate circuit for the other trinomial suggests this region is actively worked, so a later upstream value could appear.

novelty: PASS (no published circuit at <=82 found)
pass: true
