# Preregistered Evaluation Bar (`coin-basket-adversarial-games`)

frozen_utc: 2026-10-28T00:34:00Z
target_id: coin-basket-adversarial-games
category: graphs-games-automata
null_test: not needed because deterministic combinatorial game minimax with two-sided strategy certificates and exhaustive game-graph verification against exact OEIS values

## 1. Verbatim Target Bank Criteria
> CONFIRMED: the exact values of A392305(17), A392305(18), A392305(19), A392305(20) (K = 4 new terms; direction: new terms) under the entry's definition (presenter chooses the basket, then the placer chooses the coin, each turn; payoff = largest basket sum minus second-largest; placer maximises, presenter minimises; a(n) is that minimax value), each with a game certificate: a placer strategy table guaranteeing margin >= a(n) against every presenter choice AND a presenter strategy table holding the margin <= a(n) against every placer choice, both checked by an independent program that walks the (memoised) game graph exhaustively; plus exact reproduction of A392305 for n = 1..16. The terms must not already be in the OEIS entry, its b-file or edit history at verification time. Submitting to the OEIS is an action for the human only.
> Partial Win p1: A391538 for every n from 15 through 22 with the same two-sided certificate (opponent strategy capping the player's guaranteed sum at a(n), player strategy achieving it), reproducing n = 1..14; this confirms the conjectured formula floor(n(n-1)/6) + n on that range or refutes it at the first n where it fails (a certified counterexample to the formula as stated in the entry).
> Partial Win p2: A392305(17) and A392305(18) only, with the two-sided certificate and calibration.

## 2. Evaluation Metric & Thresholds
- Target sequences:
  - OEIS A392305: Payoff = $S_{\max} - S_{\text{mid}}$. Turn structure: Presenter chooses basket, Placer chooses remaining coin. Minimax value $a(n) = \min_{\text{basket}} \max_{\text{coin}} \dots$
  - OEIS A391538: Payoff = $S_{\max}$. Same turn structure. Minimax value $a(n) = \min_{\text{basket}} \max_{\text{coin}} \dots$
- Verification Bar:
  - Positive controls: Full exact calibration reproducing A392305 for $n=1..16$ (1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6) and A391538 for $n=1..14$ (1, 2, 3, 5, 8, 11, 14, 17, 21, 25, 29, 34, 39, 44).
  - Two-sided certificate verification:
    - Placer strategy table evaluated against ALL reachable presenter moves -> proves margin $\ge a(n)$ (or sum $\ge a(n)$).
    - Presenter strategy table evaluated against ALL reachable placer moves -> proves margin $\le a(n)$ (or sum $\le a(n)$).
  - Full Win (CONFIRMED_SOLUTION): A392305 for $n \in \{17, 18, 19, 20\}$ with two-sided certificates verified by independent game-graph walker.
  - Partial Win p1: A391538 for $n \in [15..22]$ with two-sided certificates and formula comparison.
  - Partial Win p2: A392305 for $n \in \{17, 18\}$ with two-sided certificates.
