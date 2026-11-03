# Honesty gate (kit/RUN.md step 7)

status: CONFIRMED_PARTIAL
confirmed_scope: The files cert_n18.txt, cert_n19.txt and cert_n20.txt (sha256 in object/certificates.sha256; archive sha256 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b, DOI 10.5281/zenodo.23918679) give, for every one of the 123867, 317955 and 823065 unlabeled trees on 18, 19 and 20 vertices (A000055(n), matched one-to-one by canonical form against an independent regeneration and against nauty gentreeg), a bijection to {1..n} whose n-1 edge sums are consecutive integers, so, with Lee and Shan's verification for at most 17 vertices as cited in DS6 (28th ed., Section 5.2), this is a certificate (as in (a)) that every tree on at most 20 vertices is super edge-magic (partial win p1).

Read by the run's main session from panel/reproduce.md, panel/novelty.md and panel/criterion.md, each written by a
fresh-context subagent that saw the package only, each ending pass: true.
- REPRODUCE: own checker from the definition, every line of cert_n18/19/20 matched, 0 mismatches. SURVIVES.
- NOVELTY: DS6 28th ed. fetched once at 2026-11-03T12:47:14Z (under 6 hours old at this gate, 2026-11-03T13:03Z);
  live value 17, this package 20, strictly above; no prior art at or beyond 18 vertices found. NOVEL.
- CRITERION: meets partial win p1 literally; cross-checked against nauty gentreeg (panel/criterion-work/).
- No downgrade trigger: no hedging on the science, no reproduction mismatch, scope no wider than reproduced, no
  sample presented as complete, no capped search used as exclusion, no evasion, one cell (p1).
- Packaging item G1 closed: archive hosted on Zenodo (DOI 10.5281/zenodo.23918679, https://zenodo.org/records/23918679), SHA256SUMS recomputed. Gate re-read 2026-11-03 against the fresh CRITERION panel file; scope copied verbatim from it.
