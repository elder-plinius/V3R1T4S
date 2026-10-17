# Honesty gate (fmm-additive-complexity-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/object/5x5x5_m93_cr332_ZT_reduced.json (sha256 9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2) is a ternary straight-line program that exactly computes the 5x5 by 5x5 product with Perminov's 93 products using 332 reduced additions (U 87, V 88, W 157), against 383 for the only 5x5x5 file in his live addition_reduced_ZT directory (recounted by me), with no count for this rank on the Lille 5x5x5 page and a naive +846 in COVERAGE.md.

## Gate notes
- Panel, each in a fresh context: reproduce (codex exec, gpt-6.1-sol, no network), novelty (Claude Code subagent, Opus 5.5), criterion (Claude Code subagent, Fable 5.1). All three end `pass: true`. The reproduce skeptic is a different model family from the program's builder (a Claude Opus agent).
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The criterion skeptic wrote its own checker, calibrated it on Perminov's reference file (it returns 383), and rejected every corrupted variant it tried.
- The reproduce skeptic wrote its own checker without network access; the reference file is third-party data and is not shipped, so it judged the saved object only (exactness over Z, ternary intermediates, straight-line order, count 332, hashes, determinism).
- The novelty skeptic fetched every primary page once (all HTTP 200, hashes equal to the author's record), found the live minimum 383, rank 93 equal to the best known rank, no count on the Lille page or a comparable one in COVERAGE.md, and listed IACR ePrint 2026/849 as unread; the author then read it from a hand-downloaded copy: rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 555-93       846         401        387       0.01, 0.2, 0.08         - / 555-93      1,031     450            427      604    58.6      0.15, 0.15, 0.01 / 555-93      1,013     442            425      588    58.0       0.18, 0.14, 0.08 / 555-93      1,013         438       417       596    58.5      0.16, 0.16, 0.02.
- An open pull request on this repository claims 358 for the same cell; 332 is strictly below it, and the table value compared against is Perminov's 383.
- Full success criterion met, not a partial win. The bank's enumerated partial win p1 concerns 3x3x3 and is not claimed.
- One cell per claim. Other formats from the same sweep are separate packages.
- No downgrade triggers found (no hedging panelist, no mismatch, value strictly better than every comparable count, scope no wider than reproduced).
