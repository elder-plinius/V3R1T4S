# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/4x5x6_m90_cr348_ZT_reduced.json (sha256 aee2afd0dd35ce54d64786b5439fc37101e55a8a758cfd2a8e572e4431396c8c) is a ternary straight-line program that I verified exactly over Z to compute the 4x5 by 5x6 product with 90 products and 348 reduced additions (U 81, V 104, W 163), below the 380 of the only 4x5x6 file in Perminov's live addition_reduced_ZT directory, with the same 90 products as that file, as of my fetches on 2026-10-15.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 380), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 348, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 380, rank 90 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: lowest count listed for 456-90 over Z: 366 (Table 3.3, ternary coefficients; the row is marked * because the scheme is ternary by Kemper's modification, naive 771, a different and sparser rank-90 scheme than Perminov's), below the reference 380; 348 is below it. Over Z2 the lowest is 358 (Table 3.6, not comparable); author's reading of a hand-downloaded PDF
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
