# Honesty gate (kit/RUN.md step 7): run 2026-11-24-0730, primes between consecutive cubes (outside-bank target, like A034793)

gated: Tue Nov 24 08:01:41 UTC 2026 by the run's main session (executor follow-up), after reading all three panel files in full.
panel files read (sha256): reproduce.md 7eb8158a8445e1338fd0b4a918bc64f74ed6ac8dda51f4317a595432e3f68050, novelty.md 9b436704aca14f8ad03e5c6da6ced58db63545ed078a7e7bde6223352f70ac9f, criterion.md f826bd9c4cdf1e53bc18499139812a5c08abd17b672f6e36bfd5d4b1c3b08e46
panel: REPRODUCE pass: true, NOVELTY pass: true, CRITERION pass: true (with confirmed_scope); three fresh subagent contexts, each given only kit/RULES.md, its PANEL_BRIEFS.md section and a copy of claim/; panel files kept exactly as written.
prereg: sha256sum -c PREREG.sha256: PREREG.md OK (unchanged since frozen 07:36:41Z). Frozen bar "beats the record" (Y_cert <= 32.527 at prec 128 and 256 plus the standalone checker) and "meaningful drop" (<= 32.337) both met: 29.735.

## Downgrade checks (kit/RUN.md step 7), each judged literally
- hedging panelist: none; all three pass: true. NOVELTY's pass is conditional on credit fixes 4.1/4.2 before packaging; both are made in claim_v2/ (below).
- reproduction mismatch: none. REPRODUCE's own arb + mpmath.iv: Phi(3e^29.735) = 0.934253344488... < 1, Y = 29.734 fails (Phi = 1.04447); run_all.sh output byte-identical and deterministic. CRITERION's independent check agrees to 13 digits.
- value not strictly better than the record: no. 29.735 < 32.537 (Cully-Hugill thesis Thm 4.3, best rigorous prior), < 32.76 (MTY 2024, the OEIS A060199 status value fetched 07:34:04Z and re-fetched by NOVELTY 07:53:27Z, byte-identical), < 32.892, and below the non-rigorous rStation ~30.07. Status fetch under 6 h old at gating.
- stretched criterion or hidden quantifier: none (CRITERION (a)). Threshold result only; all n >= 1 stays open.
- scope wider than reproduced: no; confirmed_scope below is the CRITERION sentence verbatim and names the thesis (I3) and the unrefereed preprint (I4).
- sample / capped search / probable prime: not applicable (deterministic interval certificate).
- table value by evasion: none. One honest-UA status fetch each by the run and by NOVELTY; arXiv 429s not retried. The run's first PDF fetches used a generic Mozilla UA (re-fetched honestly); the OEIS status fetch did not (data/fetch_log.txt audit).
- several objects bundled: no; one threshold, one certificate (claim/out/main_prec256.txt).
- unresolved benchmark baseline: not applicable.

## Fixes applied after the panel (claim_v2/, see claim_v2/CHANGES.md; claim/ kept exactly as panelled; the main number does not change)
(a) rStation paper 130 (u/span_of_dilates, §2.3, 08 Nov 2026, https://rstation.ai/problems/riemann_hypothesis/papers/130) cited in CLAIM.md and PROOF.md as prior non-rigorous anticipation (~30.07, "model, not a theorem", Bellotti Thm 1.3, not Yang's c = 51.34). RULES 13.
(b) 32.76 credited to Mossinghoff, Trudgian & Yang, Res. Number Theory 10 (2024), doi:10.1007/s40993-023-00498-y; 32.537 kept as the best rigorous prior, with a cautious note that it may use Ford's c = 51.82 outside its stated range (CRITERION concern 2, not established).
(c) Journal-only variant recomputed with c = 54.004 (arXiv:2306.10680v1, the text in data/): Y = 29.907 (arb 128/256 PASS, 29.906 FAIL, standalone PASS); no-preprint/thesis row 32.677.
(d) PREREG.md copied into claim_v2/, byte-identical (sha256 11805ff4...a8bb).
(e) data/fetch_log.txt: User-Agent audit appended, history unchanged.

## Remaining gaps (for the human)
- Unindexed deposits: Google Scholar citation lists, Zenodo, aiXiv and Hexagon were covered only via web search; a deposit those engines do not index cannot be ruled out (NOVELTY §2).
- arXiv rate limits: arXiv search "primes between cubes" and the export API returned 429 to NOVELTY and were not retried.
- Inputs: I3 is a 2025 PhD thesis and I4 an unrefereed 2023 preprint (v1 only, no journal-ref as of 07:55Z); I4's constant is load-bearing (C1 x 1.2 breaks 29.735).
- Possible flaw in the 32.537 record itself (Ford's c range): a matter for the human / the thesis author, never asserted publicly by us.
- Neighbouring inputs not used (Bellotti arXiv:2508.02041, JNT 269 (2025)) may lower the threshold further.
- Outside-bank target: the id primes-between-cubes-explicit-threshold is not in bank/targets.json or charter.md, so check_run FAILs on the target line (as for A034793 before its quarry 6 was added with Matthew's approval). Adding it as a charter quarry needs Matthew's approval.

status: CONFIRMED_SOLUTION
confirmed_scope: Conditional on Yang's 2025 UNSW PhD thesis Theorem 1.3 (zero-free region, c = 51.34) and Bellotti's unrefereed preprint arXiv:2311.05136v1 Theorem 1.1 (zero density near sigma = 1), plus published results, for every integer n >= exp(exp(29.735)) there is a prime in (n^3 + 1/2, n^3 + 3n^2 + 1/2], and so between n^3 and (n+1)^3; this is a threshold result, and the claim for all n >= 1 stays open.
stands_only_if: python3 repo/kit/check_run.py prints CHECK_RUN: PASS for the run and for the package; otherwise the status is PROMISING. As of this gate it FAILs only on the outside-bank target id, so the effective status is PROMISING until Matthew approves adding the charter quarry.
