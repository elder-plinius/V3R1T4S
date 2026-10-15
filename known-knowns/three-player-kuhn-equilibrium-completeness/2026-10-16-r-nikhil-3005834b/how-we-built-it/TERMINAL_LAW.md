# From joint terminal laws to reached actions

For an information set I=(player i, card j, Table-1 public prefix h), let R_I be the sum of the joint probabilities of all (deal,terminal action history) cells with deal_i=j and terminal history beginning with h. Let A_I be the analogous sum with the chosen bet/call letter appended to h. Every terminal continuation of h is represented, and the player's action probability sigma_I is constant over I. Consequently A_I=sigma_I R_I. If R_I>0, sigma_I=A_I/R_I.

Equality of two joint terminal laws therefore implies equality of their reach probabilities, and of their action probabilities at every reached information set. Conversely, if a second profile agrees with a first profile at every information set reached by the first, induction down the finite tree shows equality of every prefix mass: a zero prefix remains zero; at a positive prefix both outgoing probabilities agree. Thus all joint terminal cells agree. These facts apply to all behavioral profiles, independently of Nash optimality.

The word joint matters: marginalizing out the private chance deal can discard information about card-dependent action probabilities. The supplied completeness certificate compares every deal/history cell, so it proves the stronger, sufficient equality.

Supplementary exact check: python3 supplementary/terminal_reconstruction.py. It independently constructs the full behavioral tree from Table 1, verifies all prefix and action-cylinder identities with rational symbolic coefficients, and rejects an omitted terminal leaf. Its finite synthetic counterexample concerns public-action marginals alone and is not an equilibrium counterexample.
