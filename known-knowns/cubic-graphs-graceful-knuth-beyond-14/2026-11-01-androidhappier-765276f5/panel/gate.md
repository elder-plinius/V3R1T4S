# Honesty gate — cubic-graphs-graceful-knuth-beyond-14 (run 2026-11-01-1516)

Read: panel/reproduce.md, panel/novelty.md, panel/criterion.md (all last-line pass: true).
Gate time: 2026-11-01T17:20:30Z. Novelty status fetches were 2026-11-01T16:56:19–16:58:40Z (< 6 h old); no re-fetch required.

## Downgrade audit (never upgrade)
- Hedging panelist: none. Each ends pass: true with concrete evidence.
- Reproduction mismatch: none. Independent C checker + fresh nauty 2.8.8 geng/labelg; counts = A002851; graph6 columns byte-identical; canonical sets equal, dup_canon=0 for n=16/18/20/22.
- Value not strictly better than live table: novelty quotes DS6 28th ed. bound 14 and Knuth fasc. 7A / Kennedy bound 16; certificates settle 18, 20 and 22. Strictly beats known verification bound.
- Stretched criterion / hidden quantifier: criterion skeptic walked every clause of (a); "orders already covered do not count" discounts order 16 as new credit but does not void a certificate that also covers uncovered 18/20/22. Full (a) met literally.
- Scope wider than reproduced: no. confirmed_scope matches what reproduce verified.
- Sample as complete / capped search as exclusion: no; exhaustive certificates, fails=0.
- Probable prime as proof / table by evasion / bundled cells / unresolved baseline: none apply.

## Decision
Full success criterion (a) is met. Status is CONFIRMED_SOLUTION (not CONFIRMED_PARTIAL): the top-tier criterion is satisfied, with new substance at 18/20/22.

status: CONFIRMED_SOLUTION
confirmed_scope: Every connected (simple) cubic graph on 16, 18, 20 and 22 vertices is graceful, as certified by result/cert_16.txt, cert_18.txt, cert_20.txt and cert_22.txt (4,060 / 41,301 / 510,489 / 7,319,447 graphs, canonically identical to a fresh nauty 2.8.8 geng -c -d3 -D3 n run with no duplicates, every labeling verified graceful by two checkers), of which orders 18, 20 and 22 are new relative to the sources cited in CLAIM.md.
