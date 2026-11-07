# Honesty gate (main session), Tue Oct 20 02:27:32 UTC 2026

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true); all three
written by fresh subagents given only a copy of claim/. Self-break: selfbreak/verdict.md (FLAWED minor, JSON sibling;
repaired in round 1, recheck SURVIVES).
Downgrade checks:
- hedging panelist: none; NOVELTY's judgement that the layout is derived from participant 12's basin is a disclosure
  already in the claim sentence, and it still passes; CRITERION checked trivial repairs of par12 (best 421451.07) and
  found them below the threshold.
- reproduction mismatch: none (424131.9503 official; independent re-implementations 424131.950298).
- strictly better than the live table: yes, NOVELTY fetched the table at 02:24:14 UTC (< 6 h old), unchanged tree
  267f6e5d; 424131.9503 > 421561.89715 by 2570.05 MWh. Not a tie.
- stretched criterion / hidden quantifier: none found; no optimality claimed; local scoring is the benchmark's rule.
- scope wider than reproduced: no; confirmed_scope names only the sources actually checked.
- sample presented as complete / capped search as exclusion / probable prime: not applicable (explicit object).
- table value by evasion: none (plain curl, honest User-Agent, all HTTP 200, no retries).
- bundling: one object, one scenario cell.
status: CONFIRMED_SOLUTION
confirmed_scope: The 16-turbine layout in object/iea37-v3r1t4s-opt16.yaml satisfies the IEA37 case study 1 constraints with no tolerance (all hubs within 1300 m of (0,0), all pairs at least 260 m apart). The unmodified official iea37-aepcalc.py scores it at 424131.9503 MWh, strictly above every 16-turbine value in table/iea37-cs1-results (maximum 421561.89715, par12, infeasible), arXiv 2212.00742 Table 4 (maximum 419935.7905), Baker et al. 2019 Table 2 (maximum 418924.4064), and Pérez-Rúa et al. 2023 Case I (about 418 GW h).
