# Honesty gate (main session)

Panel: three fresh subagent contexts (reproduce, novelty, criterion). Read all three panel files; live MinT re-fetch at gate time; downgrade only.

- panel/reproduce.md: pass: true — independent C checker (written before reading claim/checkers/) exhaustively PASS on all 67863915 compositions; author checkers B and F2 also PASS; t=10 and mutation controls FAIL; hashes match REPRODUCE.md.
- panel/novelty.md: pass: true — live MinT constructive-digital t=13 (lower bound 8) for (2,24,17); claimed t=11 strictly better; no literature/code/PR/TROPHY_CASE match or trivial edit of a published net. Caveat: releases page timed out once (not retried); not a hedge on the MinT/literature result.
- panel/criterion.md: pass: true — criteria (1)–(3) and two-checker rule met; (4) deferred to novelty (who passed). Caveats (same-day scout snapshot for "live"; same-author checkers) addressed by novelty's live fetch and reproduce's independent checker.

Gate-time MinT re-fetch (2026-10-31 ~16:15 UTC) of http://mint.sbg.ac.at/query.php?b=2&m=24&s=17&p=smt: still Constructive and digital t=13, lower bound t=8. Panel fetches are under 6 hours old.

Downgrade reasons applied: none. Never upgrade.

status: CONFIRMED_SOLUTION
confirmed_scope: The 17 explicit 24x24 F_2 matrices in claim/net_F2_t11_m24_s17.txt (sha256 c3c441c5…) generate a digital (11,24,17)-net over F_2, verified exhaustively over all 67,863,915 compositions by two independently implemented checkers, which is strictly below the MinT "Constructive and digital" value t=13 and at or above the lower bound t=8 as recorded for (b,m,s)=(2,24,17) on 2026-10-31, with literature novelty (criterion 4) not assessed here.
