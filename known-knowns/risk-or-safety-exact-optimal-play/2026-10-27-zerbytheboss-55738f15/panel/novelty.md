# NOVELTY Skeptic Report — `risk-or-safety-exact-optimal-play`

context: subagent (fresh verification context)
target_id: risk-or-safety-exact-optimal-play
review_utc: 2026-10-28T00:45:00Z

## 1. Status Source Check
- Primary status source: `https://oeis.org/A387261`
- Fetched on: 2026-10-28T00:36:28Z (HTTP 200, SHA-256 `125834621bd2a3df06eb2406f93ade8ce74bde69569e8daf05501607d445c852`)
- The published sequence A387261 (numerators) and A387262 (denominators) contains terms for $n = 1..15$ only.
- The repository's `known-knowns/risk-or-safety-exact-optimal-play/2026-10-15-r-nikhil-8e69676d/` previously established terms for $n = 16..30$ (PR #169).
- Literature check (arXiv:2603.01002, OEIS A394776, Neller & Presser Piglet): No prior exact win probabilities or certificates exist for $n \ge 31$.

## 2. Novelty Assessment
- This work claims exact reduced rational values $A387261(n)/A387262(n)$ and complete $n^2(n+1)/2$-position Bellman certificates for $n = 31..45$.
- None of these 15 values were previously published, submitted, or known.
- All 15 values strictly extend the mathematical frontier from $n = 30$ to $n = 45$.
- The claim satisfies the full novelty criteria without overlap with existing records.

pass: true
