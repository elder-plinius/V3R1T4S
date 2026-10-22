# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/2x4x8_m51_cr181_ZT_reduced.json (sha256 e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95) is a ternary straight-line program that exactly computes the full 2x4 times 4x8 product over Z with Perminov's own 51 products, using 181 additions under the reduced convention (U 37, V 67, W 77), against 188 for his only live 2x4x8 file, with no lower addition count on the Lille page, in reduced_known.json, or in COVERAGE.md, as fetched on 2026-10-15.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 188), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 181, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 188, rank 51 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: lowest count listed for 248-51: 190 over Z (Table 3.3); 183 over Z2 (Table 3.6, not comparable; below the reference 188, above our 181); author's reading of a hand-downloaded PDF
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
