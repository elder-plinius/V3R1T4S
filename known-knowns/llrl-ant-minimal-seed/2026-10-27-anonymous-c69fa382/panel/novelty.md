# NOVELTY skeptic verdict: LLRL ant g(6)=139 unique, target llrl-ant-minimal-seed (partial win p2)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## What I read (claim/ only)

- `claim/CLAIM.md`: LLRL (turns L on colours 0,1,3 and R on 2; write c+1 mod 4). g(k) = least H384 onset over starts with at most k non-zero cells. Table g(0..6) = 256241, 555, 318, 245, 195, 174, **139**. Unique k=6 minimiser `(0,1,3)(0,2,2)(1,2,3)(1,4,3)(2,1,3)(3,0,1)` (k=5 minimiser plus cell `(1,4,3)`). Partial win p2 only; g(0..5) and K0=12 are prior p1.
- `claim/NOVELTY_RECORD.md`, `claim/TARGET_CRITERION.md`, `claim/METHOD.md`.
- `claim/data/scout.md`, `claim/data/minimiser_k6.txt`, `claim/data/prior-p1/NOTE.txt`, stored `claim/data/arxiv_2409.10124_abs.html`.

Did not trust the novelty record; searched independently.

## What I ran (public web, read-only)

OEIS sequence lookups (exact `seq:` searches):

- https://oeis.org/search?q=256241,555,318,245,195,174,139 — “Sorry, but the terms do not match anything in the table.”
- https://oeis.org/search?q=195,174,139 — no match.
- https://oeis.org/search?q=555,318,245,195,174 — no match.
- https://oeis.org/search?q=256241,555,318,245,195,174 — no match.
- https://oeis.org/search?q=554,317,244,194,173,138 — no match (onset−1 convention).
- https://oeis.org/search?q=556,319,246,196,175,140 — no match (onset+1 convention).
- https://oeis.org/search?q=194,173,138 — no match.
- https://oeis.org/search?q=196,175,140 — no match.
- https://oeis.org/search?q=174,139 — two hits, both unrelated: A265367 (integer permutation containing adjacent terms 174,139) and A383641 (even/odd composite sums). Neither is an ant/highway/g(k) sequence.
- https://oeis.org/search?q=256241 — only A256241 (Euler totient property); not the integer 256241 as a term of an ant sequence. OEIS A126978 is classic Langton blank onset 9977, not LLRL.

arXiv / journal:

- https://arxiv.org/abs/2409.10124 and https://arxiv.org/html/2409.10124v1 and https://arxiv.org/pdf/2409.10124 — Gajardo–Lutfalla–Rao. LLRL blank grid: “reaches the dominant 384 period highway after 256100 steps” (rounded g(0)). Table 1: highway *periods* and frequencies from random configs; no g(k) table, no k=6 onset, no 6-cell seed.
- https://doi.org/10.1007/s11047-025-10018-9 — journal version; same content; Springer reports 1 citation.
- Semantic Scholar (CorpusID:272689359): 3 citing papers — Lutfalla arXiv:2505.05426 (LLRRRL / LLRLRLL), Lutfalla arXiv:2506.10482 (LLLR), and “How Long Can the Escaping Ant Be Confined?” (classic LR escaping time). None publish LLRL g(6).
- https://arxiv.org/abs/2506.10482 and HTML — LLLR (different turn word). “Minimal seed pattern that starts the highway” means the highway’s own finite support (P52 / P156), not sparse-start onset g(k) for LLRL. Mentions LLRL only to contrast period-384 dominance.
- https://arxiv.org/abs/2505.05426 — LLRRRL and LLRLRLL, different rules.

Lutfalla simulator / code:

- https://lutfalla.fr/ant/highway.html?antword=LLRL — interactive simulator (play/reset/random/preset highway). No g(k) table, no 139, no listed 6-cell seed.
- Lutfalla GitLab JS simulator commits: widgets for other rules, not LLRL g(6).

GitHub:

- `elder-plinius/V3R1T4S` PR #641: *classic* Langton (RL) g(k) with g(6)=49. Different rule.
- Search for `llrl-ant-minimal-seed`, `g(6)=139` LLRL, `256241` with LLRL on GitHub: no public LLRL g(6)=139 table. Unrelated `g(6)=17` is Erdős–Lovász cover number (Osman209/g6-equals-17).
- Draft PR #709 is this project’s p1 (g(0..5)); instruction treats it as in-project, not a novelty fail.

Forums / wiki / video / social:

- LifeWiki https://conwaylife.com/wiki/OCA:Langton%27s_ant — classic RL highway ~10k / period 104.
- MathOverflow 277040 / 199543 — classic highway conjecture / torus cover times.
- MSE torus-period, Turing-completeness, turmite-duration questions — classic or other rules.
- Reddit r/cellular_automata — highway *periods* of long rule-strings; no LLRL sparse-onset table.
- YouTube https://www.youtube.com/watch?v=22dfYC_q_ho (2026-10-15): “256,241 steps of chaos. Then: a road.” This is blank-grid g(0) for a 4-colour rule (LLRL), already allowed as prior / not the k=6 claim.
- X keyword search `LLRL (139 OR 256241 OR "g(6)") (ant OR highway OR Langton)`: no posts.
- Wikipedia / MathWorld / Grokipedia Langton pages: multi-colour examples; no LLRL g(k).
- timclicks.github.io/turmite-autoresearch (2026-10-23): highway-seed *anatomy* across many rules (classic seed 12 cells); no LLRL g(6)=139.

## Findings

The new content of this claim is **g(6)=139** with unique minimiser `(0,1,3)(0,2,2)(1,2,3)(1,4,3)(2,1,3)(3,0,1)`.

Public literature already has:

- GLR arXiv:2409.10124 / Nat. Comput. 2025: LLRL H384 dominance and **blank** onset ~256100 (exact 256241 is a rounding of that known g(0)).
- YouTube 2026-10-15: exact blank onset 256,241 (g(0)).
- Lutfalla 2506.10482: LLLR highway seeds (different rule).
- This project’s p1 (draft PR #709): g(0..5) and K0=12, which the fail rule says not to treat as a novelty fail.

I found **no** public table, sequence, seed list, or paper giving:

- LLRL g(6)=139, or any smaller k=6 onset, or
- this 6-cell minimiser (or an equivalent published k=6 table).

Near-misses that do **not** anticipate the claim: classic-Langton g(6)=49 (PR #641); LLLR “minimal seed” highway patterns; OEIS 174,139 coincidences; Erdős–Lovász g(6)=17.

## Caveats

- Novelty only: I did not re-simulate onset 139 or re-run the exhaustive checkers.
- Coverage is public web as of 2026-10-27 (OEIS, arXiv, Springer, Semantic Scholar citing set of 2409.10124, Lutfalla pages, GitHub, LifeWiki, MO/MSE, Reddit, YouTube, X). Closed mailing lists, unindexed PDFs, and private gists could exist; none surfaced.
- Draft V3R1T4S PR #709 is in-project p1. If that draft already stated g(6)=139 I did not see it on the public PR search; the claim text presents g(6) as new relative to p1.

scope: Verified that g(6)=139 and the listed unique 6-cell LLRL minimiser are absent from OEIS (including ±1 onset conventions), GLR 2409.10124 and its three Semantic Scholar citations, Lutfalla 2506.10482/2505.05426 and lutfalla.fr/ant, GitHub, LifeWiki, MO/MSE, Reddit, YouTube, and X; did not verify computational correctness or exhaust unpublished private copies.
pass: true
