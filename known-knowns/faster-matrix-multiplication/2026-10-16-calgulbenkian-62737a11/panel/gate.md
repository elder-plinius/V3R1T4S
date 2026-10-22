# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: claim/object/2x5x5_m40_cr147_ZT_reduced.json (sha256 62737a117df29bc9dc6194509ed47f95a6f763ea3ca21fca84f79a78c44e6e1a) is an exact ternary straight-line program for the rank-40 <2,5,5> scheme with Perminov's product set using 147 reduced additions (U 31, V 54, W 62), strictly below the 153 of his only live addition_reduced_ZT file for that format and rank, with Lille's page citing no operation count and COVERAGE.md's adds column being a naive count under another convention.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 153), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 147, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 153, rank 40 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: lowest count listed for 255-40: 154 over Z (Table 3.3); 144 over Z2 (Table 3.6, a scheme with naive count 256, not comparable; below the reference 153 and below our 147, which is over Z); author's reading of a hand-downloaded PDF
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
