# Exact b=2 equilibrium certificate

The object is `equilibrium.json`. Polynomials are stored in ascending coefficient order, and every interval endpoint is rational. Let B be the unique root of its degree-eight polynomial in the stored B interval, C=(3B²-1)/(2B), and A=2(1-B)/(7C-2). Exact rational polynomial reduction and Sturm counts verify the three defining equations and isolate A, C, and the game value as well. Rational interval arithmetic establishes 0<A<C<B<1.

The three equations are

    3A²=5C²-2;  3B²-2CB-1=0;  7CA=2(A+1-B).

A player contributes one ante. At b=2, a bettor/caller contributes three. If I checks, all hands show and the winner receives net +2. If I bets and nobody calls, I receives +2. With one caller, the winner receives +4 and the loser -3; the folder receives -1. With both callers, the winner receives +6 and each loser -3. These utilities sum to zero.

I's check payoff at hand x is 3x²-1. Against both callers using C, I's bet payoff is 5C²-3 for x<=C and 9x²-4Cx-3 for x>=C. To derive this, partition opponents' hands into folded (<C), called-and-lower (<x), and called-and-higher (>x). Above C the sum is

    2C² + 8C(x-C) + 6(x-C)² - 3(1-x²).

Thus bet-minus-check is

    3(A-x)(A+x)                  for 0<=x<=C;
    2(x-B)(3(x+B)-2C)            for C<=x<=1.

Because the second factor in the second line is positive, these differences have precisely the signs required for betting on [0,A) and (B,1], and checking between A and B. At A and B either action is optimal. Both formulas agree at C.

For the complete caller action payoffs, let H(y) be 0 below A, y-A between A and B, and B-A above B. The fold-policy payoff is -1+3yH(y), including I-check states; the call-policy payoff adds D(y) below. For II, let T=A+1-B be the probability that I bets, and W(y) the measure of I's betting hands below y. On the intervals [0,A], [A,C], [C,B], [B,1], W is respectively y, A, A, A+y-B. The analogous quantities for III are identical. The difference between calling and folding, integrated over I's hand before conditioning on I's bet, is

    D(y) = W(y) [7C+9 max(y-C,0)] - 2T.

Explanation: calling costs two more than folding. If III folds (probability C) and II beats I, the difference from the losing baseline is +7. If III calls with a weaker hand (measure max(y-C,0)) and II beats I, the increment is +9. Those events are independent conditional on II's hand because the continuous hands are independent. When I checks, II has no action and the two counterfactual payoffs agree.

Using 7CA=2T, D(y) becomes

    7C(y-A)                                  on [0,A];
    0                                        on [A,C];
    9A(y-C)                                  on [C,B];
    9A(y-C)+(y-B)(9y-2C)                      on [B,1].

All signs follow directly from 0<A<C<B<1. Folding is optimal below C (with a full indifference plateau [A,C]); calling is optimal above C. T is positive and independent of y, so conditioning on the observed bet divides D by a positive constant without changing signs. Symmetry gives exactly the same argument for III; allowed deviations need not be symmetric.

Each player has only one binary decision. Any measurable randomized unilateral policy assigns an action probability in [0,1] to each available information set. Its conditional utility is the convex combination of the two action utilities above. Pointwise maximality therefore bounds it above by the prescribed policy, and integration preserves the inequality. Utilities are bounded, so every such integral exists. Correlated decisions between deviators are not unilateral deviations. Hands tying an opponent have conditional probability zero even at endpoints. At x=0 and x=1 we use the continuous-extension optimal actions, bet and bet respectively; at caller y=0 fold and y=1 call. Threshold ties may use either action. This also makes the pointwise statement valid on the closed hand domain, rather than only almost everywhere.

Integrating I's optimal payoff gives the algebraic number

    V=-A³+5AC²-2A-2B³+2B²C+2B-2C.

The JSON object gives its exact polynomial, isolating interval, and polynomial expression in B. The other payoffs are -V/2 by caller symmetry and zero sum. The standard-library checker certifies all these algebraic definitions without floating-point root decisions; a separate symbolic rectangle-integration implementation independently checks all action-payoff polynomials from the game tree.

## Printed decimal discrepancy

Endpoint scope: the displayed closed-domain pointwise proof uses the explicitly stated optimal continuous-extension actions at 0 and 1. The source's strict interval wording has different “otherwise” actions at those endpoints if interpreted on [0,1]. On its uniform(0,1) hand space the policies agree; under a closed-space convention they differ only on null sets and have identical ex ante equilibrium comparisons. Literal endpoint pointwise requirements must be judged separately from Nash equilibrium.

The certified value begins 0.1225570747148686867377787982761502092550102815857780623. The paper prints 0.122557074714865. The exact interval is disjoint from the interval that rounds to the printed number at fifteen decimal places. The difference is 3.686737778798276150209255010281585778062318339345021075e-15. Thus this proof does not literally satisfy the bank's printed-digit clause, even though it verifies the equilibrium defined by Eq. A-C. This is not a counterexample to equilibrium and must not be reported as branch B. The bank is not edited here.
