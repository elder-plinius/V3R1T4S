# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The program claim/object/3x5x5_m58_cr211_ZT_reduced.json (sha256 9407c156647ed8a24fbd9e29d7f644e1fd6281aabc4eaa317bb5cb3a3a9b5b23) is, on my checks, a ternary straight-line program for the rank-58 scheme for <3,5,5> (the same 58 products as Perminov's cr221 file) that exactly computes A*B over Z and uses 211 reduced additions (U 48, V 69, W 94), below 221, the only addition_reduced_ZT count for this format and rank in his live tree on 2026-10-15, and below the +413 naive adds in matmulcatalog COVERAGE.md; the Lille 3x5x5 page cites no operation count.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 221), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 211, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 221, rank 58 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: lowest count listed for 355-58: 222 over Z (Table 3.3); 220 over Z2 (Table 3.6, not comparable; below the reference 221, above our 211); author's reading of a hand-downloaded PDF
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
