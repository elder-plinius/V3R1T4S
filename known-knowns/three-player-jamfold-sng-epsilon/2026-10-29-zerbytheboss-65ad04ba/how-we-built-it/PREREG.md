# PREREG: three-player-jamfold-sng-epsilon

- **Frozen timestamp (UTC)**: 2026-10-29T21:12:00Z
- **Target ID**: three-player-jamfold-sng-epsilon

## Criterion Verbatim
An explicit stationary jam/fold profile for G: for each of the 946 stack vectors, the jam probability of the button, the small blind and the big blind for each of the 169 hand classes in every decision situation. Its ex post epsilon must be at most $0.0010, at least 48 times below the published $0.0488 (direction: lower). Epsilon is the maximum, over all 946 starting states and all three players, of the player's best-response value in the induced undiscounted MDP minus the player's value under the profile, in dollars of the $100 pool, computed as in Ganzfried's thesis section 9.4. All-in outcome probabilities must be exact: full enumeration of boards and of the remaining cards. The sources do not say how two players eliminated in the same hand are ranked, so the bound must hold under both readings: (i) the player who started the hand with more chips takes the higher place, and equal starting stacks split the two prizes; (ii) all players eliminated in the same hand split their prizes equally. Values in unmerged pull requests are not bars.

Partial wins verbatim:
- p1: A profile whose certified ex post epsilon is strictly below $0.0488 (but above $0.0010) under both readings, verified exactly as in the success criterion. This is a new record for the published model, though not the full win.

## Exact Statistic and Checker
1. **Stationary Strategy Profile $\sigma$**:
   For each of the 946 non-terminal stack vectors $v = (s_{\text{BTN}}, s_{\text{SB}}, s_{\text{BB}})$, the profile specifies:
   - $\sigma_{\text{BTN}}(C) \in [0, 1]$ for all 169 hand classes $C$.
   - $\sigma_{\text{SB}}(C \mid \text{BTN Fold}) \in [0, 1]$ for all 169 hand classes.
   - $\sigma_{\text{SB}}(C \mid \text{BTN Jam}) \in [0, 1]$ for all 169 hand classes.
   - $\sigma_{\text{BB}}(C \mid \text{BTN Fold, SB Jam}) \in [0, 1]$ for all 169 hand classes.
   - $\sigma_{\text{BB}}(C \mid \text{BTN Jam, SB Fold}) \in [0, 1]$ for all 169 hand classes.
   - $\sigma_{\text{BB}}(C \mid \text{BTN Jam, SB Call}) \in [0, 1]$ for all 169 hand classes.

2. **Transition Probability Matrix & Terminal Payoff Vectors**:
   For a given elimination convention $c \in \{(i), (ii)\}$:
   - Transition matrix $P_c^\sigma \in \mathbb{R}^{2838 \times 2838}$ and terminal reward vector $b_c^\sigma \in \mathbb{R}^{2838}$.
   - Profile expected value vector $V_c^\sigma$ solved via:
     $$(I - P_c^\sigma) V_c^\sigma = b_c^\sigma$$
     verified to residual $\|(I - P_c^\sigma) V_c^\sigma - b_c^\sigma\|_\infty < 10^{-10}$.

3. **Undiscounted MDP Best Response $V_c^*$**:
   - For each player position $p \in \{\text{BTN}, \text{SB}, \text{BB}\}$, compute the optimal best response $\pi_p^*$ against opponents playing $\sigma$ via undiscounted Policy Iteration (minimal non-negative solution).
   - Compute exploitability:
     $$\epsilon_c = \max_{v \in S_G, p \in \{\text{BTN}, \text{SB}, \text{BB}\}} (V_{c, p}^*(v) - V_{c, p}^\sigma(v))$$

4. **Certified Epsilon**:
   $$\epsilon = \max(\epsilon_{(i)}, \epsilon_{(ii)})$$

## Thresholds
- **Partial Win (p1)**: $\epsilon < \$0.0488$ under both conventions (i) and (ii).
- **Full Win (CONFIRMED_SOLUTION)**: $\epsilon \le \$0.0010$ under both conventions (i) and (ii).

## Null Design
null_test: not needed because preflop hand equities, transition probabilities, linear system solutions, and undiscounted policy iteration best responses are exact mathematical quantities computed deterministically over finite discrete state and action spaces without statistical estimation or sampling.
