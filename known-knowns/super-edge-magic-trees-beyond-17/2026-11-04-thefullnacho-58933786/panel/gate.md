# Honesty gate (kit/RUN.md step 7)

status: CONFIRMED_PARTIAL
confirmed_scope: For every n in 18..22, the files object/cert_n18.txt .. object/cert_n22.txt.xz (one per order, cert_nN for order N) list exactly A000055(n) pairwise non-isomorphic trees on n vertices (hence every unlabeled tree on n vertices), each with a bijection onto {1..n} whose n-1 edge sums are consecutive integers, so every tree on 18 to 22 vertices is super edge-magic, and together with Lee and Shan's cited verification up to 17 vertices every tree on at most 22 vertices is super edge-magic (partial win p2).

Read in full by the run's main session (live session on the contributor's desktop, 2026-11-04T03:12Z) from panel/reproduce.md, panel/novelty.md and
panel/criterion.md, each written by a fresh-context subagent that saw claim/ only, each ending pass: true.
- REPRODUCE: own checker written before reading the author's code, every line of all five files (no sampling),
  own canonical form and own A000055 (Otter); 0 invalid, 0 isomorphic duplicates, counts equal A000055(n) for n = 18..22;
  4 injected defects rejected; deterministic on rerun; author's commands agree. SURVIVES.
- NOVELTY: DS6 status page fetched once at 2026-11-04T03:02:53Z, HTTP 200 (under 6 hours old at this gate); edition
  Oct 30, 2025, live value 17; the only pending claim on this target is the same contributor's #917 (at most 20);
  no verification above 17 found in Zenodo, arXiv, Crossref, GitHub or the web. 22 strictly beats both. NOVEL.
- CRITERION: meets partial win p2 literally; own checker over every line; WROM regeneration (indep_check.py --regen)
  and networkx regeneration (n = 18..20) match one-to-one; definition is the published super edge-magic one; p2 not
  subsumed. Five non-blocking gaps recorded in criterion.md.
- No downgrade trigger: no hedging on the science, no reproduction mismatch, scope no wider than reproduced (orders up
  to 17 rest on the citation the criterion itself builds in), no sample presented as complete, no capped search used
  as an exclusion, no evasion in any fetch, one cell (p2).
- To fix in the package, not in the claim: criterion gaps 1 (hash command path) and 2 (stale "at most 20" in the
  copied record file); gaps 3 to 5 go under "Not claimed".
- Gate rewritten 2026-11-04T03:22Z after REPRODUCE and CRITERION replaced the n-in-angle-brackets
  file notation in their own files (a template-placeholder clash with kit/check_run.py); their edit lines say no
  finding changed, and the diffs touch only that notation. confirmed_scope copied verbatim from the edited criterion.md.
