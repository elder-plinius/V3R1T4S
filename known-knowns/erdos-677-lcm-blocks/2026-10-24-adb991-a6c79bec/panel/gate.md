# Honesty gate: erdos-677-lcm-blocks (JSP-000550 = Erdős 677), claim "no counterexample with n ≤ 5871·k" (run 2026-10-15-0724)

round-1 status: PROMISING (superseded below)
round-1 confirmed_scope: Computer-assisted and relying on the cited explicit prime bounds of Rosser–Schoenfeld 1962 (ψ(x) < 1.03883·x for all x > 0) and Schoenfeld 1976 (a prime in (x, x(1 + 1/16597)) for every x > 2010759.9), object/PROOF.md together with the reproduced run of object/range_nCk.py 5871 shows that lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k) for every k ≥ 1, every n with 0 ≤ n ≤ 5871·k and every m ≥ n + k with no cap on m, i.e. every instance of Erdos677.erdos_677 with n ≤ 5871·k holds — an informal, not kernel-checked result that meets the first enumerated partial win and is not a solution of the problem.

Read by the run's main session at 2026-10-15T10:21Z: reproduce.md (pass: true), criterion.md (pass: true) and
novelty.md (pass: false, "novelty: PENDING STATUS CHECK"). Each was written by a fresh subagent context that saw only
claim/, plus what it fetched itself. The scope line above is CRITERION's sentence, copied exactly. The claim is **not
confirmed**: the gate stops at PROMISING because NOVELTY could not read the place where partial results on this
problem are recorded.

## Why PROMISING
NOVELTY read the status source (prize catalog, 2026-10-15T09:45:23Z, HTTP 200, sha256 78ecc0e2…7834; JSP-000550
"Open", "Lean proof: No"). It also read:
- formal-conjectures (no variants or solved sub-cases);
- teorth/erdosproblems data (677 open);
- all 4521 prize-repository PR heads (filler or two-instance checks only);
- plby/lean-proofs;
- a k = 2 slice in jaredwilder/erdos-proved-lemmas;
- TROPHY_CASE.md and all 156 V3R1T4S PR heads;
- eight web searches.

None of these covers n ≤ 5871·k. But erdosproblems.com/677, its forum thread and arXiv listings were blocked by this
container's proxy (one request each, not retried). The method reduces "n ≤ C·k" to a finite computation for every C,
so a recorded result with C ≥ 5871 is plausible, and novelty cannot be confirmed from here. Per kit/RUN.md step 6,
the human checks by hand.

## Downgrade checks (kit/RUN.md step 7)
- **Hedging.**
  - REPRODUCE passed but stated a gap: it could not re-read the two cited papers (proxy 403). It gave their statements
    from its own knowledge, with numerical consistency checks: max ψ(n)/n for n ≤ 10^8 is 1.0388206 at n = 113; the
    Schoenfeld property holds on (2010759.9, 10^9).
  - CRITERION passed with the same gap, and said a forum post that subsumes the claim cannot be ruled out.
  - Both gaps are about cited KNOWN results and novelty, not about the computation. The novelty gap alone decides the
    status.
- **Reproduction.**
  - The author's program was rerun twice, by REPRODUCE (133.8 s) and by CRITERION (134 s). Both outputs are
    byte-identical to object/out/range_nCk_C5871.txt.
  - Two independent checkers were written from the definition:
    - REPRODUCE: exact C, all prime-free blocks with m ≤ 2010759, pinning by every maximal prime power, no size bound.
      19,745,817 pairs; 89,006,987 candidates also compared exactly with the pinning cut back to one prime power;
      0 equalities.
    - CRITERION: Python, m bounded by the exact (E1) bound only for k ≤ 147, so it uses neither cited paper there.
      0 cases with lcm(B) dividing lcm(A).
  - A separate C rewrite by REPRODUCE matches the author's counts exactly (1,449,175 pairs; 7,567,449 candidates;
    7,567,420 comparisons).
- **Literalness.** No stretched criterion and no hidden quantifier, per CRITERION: k ≥ 1, n = 0, m = n + k and every
  m ≥ n + k are covered. The range is a stated cone, uncapped in m.
- **Scope.** It is no wider than what was reproduced, and it names its dependence on the two cited theorems.
- **Completeness.** No sample is presented as complete, no capped search is used as an exclusion, and no probable
  prime is used: the primes come from a deterministic sieve.
- **Evasion.** None: one request per page, and blocks are recorded.
- **Bundling.** One object, one claim. The lens results "n + k ≤ 10^8" and "k ≤ 22, n ≤ 10^494" (signature-search)
  and the k = 3, 4 Thue results (structure-prover) were deliberately not bundled in. They are not panelled.
- **Freshness.** NOVELTY's catalog fetch is less than 6 hours old.

## Main-session notes (context, not part of the verdict)
- For k ≥ 148 the claim is purely analytic (S1 plus Schoenfeld 1976). For k ≤ 147 its range n ≤ 863,037 lies inside
  the signature-search lens's unpanelled verification n + k ≤ 10^8, so the computation adds nothing beyond that lens.
- CRITERION's comparison: explicit Bertrand-type bounds alone reach n/k of about 45 (Dusart 1998). Schoenfeld's 16597
  caps this method at 5871, so the constant is the natural endpoint of a classical method, not a new idea.
- This is a workspace partial win only. It is not prize-eligible: the Justin Sun Prize accepts only complete
  solutions.

## What would change the status
1. The owner reads https://www.erdosproblems.com/677 and https://www.erdosproblems.com/forum/thread/677, and scans
   arXiv.
2. If nothing recorded there already covers n ≤ 5871·k, a wider range, or a solution, a fresh NOVELTY skeptic given
   that evidence can lift the claim to a confirmed partial win.
3. Then gate again, run check_run, and package it.

## Round 2 (2026-10-24, during run 2026-10-24-0818)

status: CONFIRMED_PARTIAL
confirmed_scope: Computer-assisted and relying on the cited explicit prime bounds of Rosser–Schoenfeld 1962 (ψ(x) < 1.03883·x for all x > 0) and Schoenfeld 1976 (a prime in (x, x(1 + 1/16597)) for every x > 2010759.9), object/PROOF.md together with the reproduced run of object/range_nCk.py 5871 shows that lcm(m+1, …, m+k) ≠ lcm(n+1, …, n+k) for every k ≥ 1, every n with 0 ≤ n ≤ 5871·k and every m ≥ n + k with no cap on m, i.e. every instance of Erdos677.erdos_677 with n ≤ 5871·k holds — an informal, not kernel-checked result that meets the first enumerated partial win and is not a solution of the problem.

Read by the run's main session at 2026-10-24T08:47:19Z:
- reproduce.md (pass: true, 2026-10-15) and criterion.md (pass: true, 2026-10-15), unchanged;
- a new novelty.md (pass: true), written on 2026-10-24 by a fresh subagent that saw only claim/. The round-1 novelty
  file (pass: false, "novelty: PENDING STATUS CHECK") is kept as novelty_round1_pending.md.

The scope line above is CRITERION's sentence, copied exactly.

### Why the status changes

Round 1 stopped at PROMISING for one reason: erdosproblems.com/677 and its forum could not be read. The owner widened
the environment's network access on 2026-10-23.

The round-2 NOVELTY skeptic then read:
- the status source, at 2026-10-24T08:26:00Z (HTTP 200, the same sha256 78ecc0e2…7834 as on 2026-10-15; "Open",
  "Lean proof: No");
- the problem page, its history, the proof-claims page and the forum (all HTTP 200);
- the site's external database;
- the forum-linked Lean repository;
- the AI-contributions wiki (through its git repository);
- the TROPHY_CASE and all 615 V3R1T4S PR heads;
- all 4580 prize-repository PR heads;
- ten arXiv API queries for 2024-10 to 2026-10.

None records a range verification of the form n ≤ C·k, any explicit range with uncapped m, or a solution. The only
recorded results are k = 1, Thue–Siegel finiteness for each fixed k, and fixed-gap finiteness in Lean.

### Downgrade checks for round 2

- **Hedging.** NOVELTY lists its limits:
  - Guy's B35 was not read.
  - The forum-linked Farhi–Kane PDF and the GitHub web PR listings were blocked by this environment's proxy (403,
    not retried). They were reached by other channels: the paper's arXiv abstract (it concerns the period of
    n…(n+k)/lcm, not equal lcms), and git refs of every PR head, a superset of the open PRs.
  - These are not the primary status source, which was read with HTTP 200.
  - The different channels are ordinary public endpoints, not a bypass of a site's access control. The 403s came from
    this container's proxy, not from the sites.
  - I accept the call.
- **Freshness.** NOVELTY's catalog fetch (08:26:00Z) is less than 6 hours old at this gate. This run's own scout
  fetched the same catalog at 08:21:40Z (same sha256) and the problem page at 08:21:38Z.
- **Unchanged from round 1.** Reproduction, literalness, scope, completeness, evasion and bundling, all recorded above.
  The cited prime bounds (Rosser–Schoenfeld 1962, Schoenfeld 1976) stay named in the scope sentence. Neither
  REPRODUCE nor CRITERION could re-read those papers. Both checked them numerically within their ranges.
- **Bundling.** This remains one claim. Tonight's run 2026-10-24-0818 works on separate ranges (R2, R1), which are not
  merged into it.
