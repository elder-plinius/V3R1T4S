# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/2x4x7_m45_cr169_ZT_reduced.json (sha256 ba03797bb02013423a43e98b27ac46c6897018e12f9e90f0761e874c402070d7) is a ternary straight-line program over the inputs that exactly computes the 2x4 times 4x7 product with the 45 products of Perminov's rank-45 scheme (same U, V, W rows as his file), using 169 reduced additions (U 35, V 67, W 67) against his only 2x4x7 rank-45 count of 174, with no lower count on the Lille page or in the COVERAGE.md adds column (naive 308) as fetched 2026-10-15.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 174), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 169, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 174, rank 45 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 247-45       308         181        177          0, 0.26, 0           - / 247-45         308       180       176     132   42.9       0, 0.21, 0.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
