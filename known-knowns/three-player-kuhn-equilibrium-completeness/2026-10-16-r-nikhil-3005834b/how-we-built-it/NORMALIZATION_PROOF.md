# Zero-sum normalization lemma

This is the normalization component of the certificate for the game in
Szafron, Gibson and Sturtevant (2013), Section 2. At this stage the separate
no-initial-bet certificate has already proved that P1 never opens in any Nash
equilibrium. The component works in the resulting no-opening game; it does
not assume that arbitrary changes to unreachable actions preserve Nash.

Let F_i be player i's full no-opening realization-strategy domain, and let R_i
be its normalized restriction. There is a feasible embedding e_i:R_i -> F_i
and a projection t_i:F_i -> R_i. Write T_i=e_i t_i and T=(T_1,T_2,T_3).
Each map changes only its own player's coordinates. Utilities are zero-sum.

For an equilibrium x, the precondition certificate proves the opponent
equalities used by the checker. The dominance certificate establishes, for
each player i and every z_i in R_i,

u_i(e_i z_i, x_-i) >= u_i(e_i z_i, T_-i x_-i).

These inequalities use only feasible-domain signs, after substituting
certified equalities of the opponents. No equilibrium condition is imposed
on the deviating strategy z_i.

Choose z_i=t_i x_i. Nash optimality and dominance give

u_i(x) >= u_i(T_i x_i, x_-i) >= u_i(Tx).

Both sums over players are zero, so each of the outer inequalities is an
equality. For an arbitrary z_i in R_i, Nash and dominance then imply

u_i(Tx)=u_i(x) >= u_i(e_i z_i, x_-i)
                    >= u_i(e_i z_i, T_-i x_-i).

Consequently Tx is a Nash equilibrium in the normalized restriction and has
the same payoffs as x. Equality of terminal-history probabilities is a
separate conclusion checked by the terminal-family certificate; this lemma
alone asserts equality of payoffs and restricted optimality.

The maps, exact domain inequalities, the zero-sum identities, all three
dominance polynomials, and the restricted equilibrium certificate are checked
by attempts/certifier/code/verify_normalization.py. The complete entry point
attempts/certifier/code/verify_completeness.py supplies the no-opening result
and the final exhaustive terminal-history comparison.
