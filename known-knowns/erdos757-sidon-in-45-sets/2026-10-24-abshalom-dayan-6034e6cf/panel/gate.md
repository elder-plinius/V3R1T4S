# Honesty gate (main session): erdos757-sidon-in-45-sets, partial win p2

gate run at: 2026-10-24T13:20:20Z by the run's main session (second pass, see the last note), after reading panel/reproduce.md, panel/novelty.md and
panel/criterion.md in full.

status: CONFIRMED_PARTIAL
confirmed_scope: The explicit 101-vertex, 99-edge 3-uniform hypergraph in H.json is linear, F7-free, has pairwise distinct label-order middles with none at vertex 0 or 100 (so m = n - 2), and has exact independence number 56, so alpha/n = 56/101 < 5/9 < 4/7, meeting partial win p2 as an abstract hypergraph that satisfies the properties arXiv:2602.23282 proves (Lemmas 2.4, 2.5, 5.2) while being provably not the A.P.-hypergraph of any weak Sidon or (4,5)-set and giving no bound on c*.

## Panel
- REPRODUCE (subagent, fresh context, given only claim/): pass: true. Own checker written from the definitions; every
  property and alpha = 56 reproduced; no mismatch, no missing object, no non-determinism.
- NOVELTY (subagent, fresh context, given claim/, the web and TROPHY_CASE.md): pass: true. Status source
  https://arxiv.org/html/2602.23282 fetched once at 2026-10-24T12:31:38Z, HTTP 200, sha256 6b668ce6...4608 (unchanged
  since the scout's 10:12:22Z copy), value 9/17 <= c* <= 4/7; nothing exhibits, ties or beats 56/101.
- CRITERION (subagent, fresh context, given only claim/): pass: true, confirmed_scope as above.

## Downgrade checks
- Hedging panelist: none. NOVELTY lists residual risks (Henning-Yeo 2021 full text not readable, closed access;
  hturcotte1 raw experiment files not read; search-engine coverage). These are disclosed limits of a search that
  found nothing, not a hedged verdict, and the p2 wording's own novelty test (the paper neither exhibits nor excludes
  such an H) was confirmed by all three skeptics.
- Reproduction mismatch: none (three skeptics and the run's own checkers agree on alpha = 56 by CP-SAT, SAT, MaxSAT,
  SCIP and exact dynamic programs).
- Value strictly better than the live table: 56/101 < 4/7 (392 < 404) on the named sources and 56/101 < 5/9
  (504 < 505) against the community record; strict, exact fractions. Margin under 5/9 is 1/909.
- Stretched criterion or hidden quantifier: p2 asks for an abstract hypergraph with the paper's proven properties;
  realizability is not part of the wording, and the scope sentence says H is not realizable and gives no bound on c*.
- Scope wider than reproduced: the positive part (properties, alpha) was reproduced by REPRODUCE and CRITERION; the
  clause "provably not the A.P.-hypergraph of any weak Sidon or (4,5)-set" narrows the claim and was derived
  independently twice (the run's fresh-context self-break check and CRITERION's exact rational linear algebra).
- Sample presented as complete, capped search as exclusion, probable prime as proof: none in the claim.
- Table value obtained by evasion: none (fetch logs show one GET per URL, no browser user agent, no retries on blocks).
- Several objects bundled: no, one object (claim/H.json, sha256 6034e6cf...9b46).
- Table fetch age at the gate: under 1 hour (12:31:38Z), so no re-fetch.

## Disclosed process note
- After REPRODUCE and NOVELTY had finished and before CRITERION started, the main session appended a "Not claimed"
  section to claim/CLAIM.md (timestamped 2026-10-24T12:42:24Z) stating that H is not realizable, with the 8-vertex
  piece. It narrows the claim (it can only push a skeptic toward fail) and CRITERION re-derived it itself; the claim
  sentence, object files and criterion text were not changed.
- Second gate pass: the package check flagged the token block_edges in angle brackets in panel/reproduce.md line 133 (a quoted
  command, matched by check_run's template-placeholder rule). At the main session's request the REPRODUCE skeptic
  itself replaced it with '[block_edges as JSON]'; the diff is that one token, verdict and pass line unchanged. The
  main session re-read the file and re-ran this gate with the same result.
