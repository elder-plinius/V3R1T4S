# Honesty gate (kit/RUN.md step 7), written by the run's main session
status: CONFIRMED_PARTIAL
confirmed_scope: Only partial win p1 is confirmed: the reduced fractions P+_{2,11} = 137912544707079557/45735706696680000, P+_{2,12} = 228254911260131056513/75738330289702080000 and P+_{2,13} = 3901622163101296907981/1295524070744904000000 are certified by cert/n11.txt.gz, cert/n12.txt.gz and cert/n13.txt.gz, each verified by my independently written checker state by state over all reachable canonical states (C recomputed from (A.1), max over every label including exhausted ones, closure from the initial state) against Luo's Appendix A recursion (cert/n2.txt.gz to cert/n10.txt.gz and cert/n14.txt.gz also pass that check, which does not complete the full criterion); the full criterion is not met literally, because the code's n = 7 value 206528731/68108040 = 3.0323693... rounds to 3.0324 whereas DGS Table 3 prints 3.0323 under its stated rounding (and truncation would instead fail n = 10, 3.0185 against 3.0186), and because cert/n15.txt.gz and cert/n16.txt.gz were not verified state by state by me.

## Panel files read
- panel/novelty.md: context subagent; one honest status-source GET (2026-10-15 13:52:33 UTC, HTTP 200, byte-identical
  to the scout's page, sha256 b457009a...80ed6fd); no published exact or numerical value of P+_{2,n} for n >= 11
  found (arXiv listings and TeX sources, OEIS, zbMATH, citation graphs, TROPHY_CASE.md, open and recent closed PRs);
  pass: true. Deviation recorded by the skeptic: after an HTTP 429 from the OpenAlex API its loop sent three more
  queries (all 429) before stopping; Semantic Scholar 429 not retried. These were literature-search APIs, not the
  status source or a record table; the status-source comparison itself was one clean GET. Noted, not disqualifying.
- panel/criterion.md: context subagent; own checker on every state for n = 2..14 (structural only for n = 15, 16);
  re-derived the canonical-state quotient and the integer form; reachability set equality for n = 2..11; rebuilt
  n = 2..12 byte-identically; judged the FULL criterion NOT met literally (calibration clause: n = 7 rounds to 3.0324
  vs printed 3.0323; no single convention fits all nine entries) and partial win p1 (n = 11, 12, 13) met; pass: true
  with the scope above. It also found a false sentence in the claim README ("every other entry agrees under rounding
  and truncation alike": n = 10 does not truncate to the printed value); corrected in the package README.
- panel/reproduce.md: context subagent; own checker written before reading the author's code; every state of every
  certificate n = 2..16 verified (37,295,049 states, 174,529,297 actions; 11,110 absent successors all with C = 0;
  count split at all 153,161,345 active-label actions; reachability of every listed state; initial W/C equals
  values.json); 17 mutated copies rejected; determinism of digests across runs; own solvers (full-vector recursion
  n = 2..5, raw game (2,2), (3,2), (3,3)) agree; author's solver rebuilt byte-identically for n = 2..11; pass: true.
  Deviation recorded by the skeptic: a wait trigger fired early and a third process of its own ran for about 25 min
  beside its n = 15 and n = 16 runs (above the 2-thread guidance; memory briefly near 2 GB). Results unaffected.

## Gate decisions (downgrade only)
- Scope: exactly the CRITERION panelist's sentence (p1: n = 11, 12, 13). The full criterion is not confirmed; the
  n = 14..16 values are shipped as data, outside the confirmed scope.
- Table access audit: data/ and panel fetches were single honest GETs (HTTP 200); no browser user agents, cookies or
  retries after blocks in code/ or data/. The NOVELTY skeptic's 429 episode concerned a citation API; recorded above.
- Panel fetch age: NOVELTY fetched the status source at 13:52 UTC; gate written 2026-10-15 20:20:27 UTC, more than 6 h later, so the status source was fetched once more at 2026-10-15 20:19:56 UTC (HTTP 200, sha256 b457009a53b9c7f9ccf724ce8f7c247446977de8a5eb819340e5d339e80ed6fd, byte-identical to the scout's and the panel's page; data/status_source_arxiv_search_gate_refetch.html): still no published value for n >= 11.
- Null test: not required (deterministic certificate check, PREREG.md).
- One object per claim: p1 is one enumerated partial win (three values as a unit).
- Hedging check: the CRITERION panelist's caveat ("if the panel rules that p1 inherits the calibration sentence, the
  outcome becomes neither") was decided here: the bank's p1 text ("Certified exact P+_{2,n} for n = 11, 12 and 13
  (the first values beyond the published table)") carries no calibration clause; the certificates themselves were
  verified independently by two skeptics, which is a stronger validation of the code than the four-decimal table;
  the full criterion stays unconfirmed because its own wording was not met literally at n = 7. No upgrade.
- Final: CONFIRMED_PARTIAL (p1), scope sentence above. Package: outbox/ (kit/SUBMIT.md), built after this gate.
