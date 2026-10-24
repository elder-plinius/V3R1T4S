# Threshold equilibrium for every positive fixed bet

This is the proposed enumerated p1 theorem. No uniqueness of the game's full equilibrium set is asserted. The original b=2 printed-digit clause is not changed.

For every real b>0 there is exactly one ordered triple 0<A<C<B<1 satisfying the paper's Eq. A-C, and its threshold profile is a Nash equilibrium against every measurable unilateral deviation in the simultaneous-caller game.

## Existence of the ordered triple

Fix b>0 and define

    c0 = sqrt(b/(b+3)),
    B(c) = (c+sqrt(c²+3))/3,
    L(c) = sqrt(((b+3)c²-b)/3),
    R(c) = b(1-B(c))/((2b+3)c-b),       c0 <= c <= 1.

We have 0<c0<1. The denominator D(c)=(2b+3)c-b is positive throughout [c0,1]. To see this at the left endpoint, both (2b+3)c0 and b are positive, and

    ((2b+3)c0)²-b² = 3b(b²+3b+3)/(b+3) > 0.

It follows that (2b+3)c0>b; D is strictly increasing, so no denominator vanishes. The radicand for L is nonnegative on this interval. All four displayed functions are continuous there.

For 0<c<1, B(c)<1: equivalently sqrt(c²+3)<3-c, whose positive sides square to c²+3 < 9-6c+c², or c<1. Also B(c)>c: the positive sides of sqrt(c²+3)>2c square to 3>3c². Finally B(c) is strictly increasing, since its derivative is (1+c/sqrt(c²+3))/3>0, and B(1)=1.

Consequently L is strictly increasing from L(c0)=0 to L(1)=1. R is strictly decreasing from a positive value at c0 to R(1)=0: its numerator is positive and strictly decreasing on [c0,1), while its denominator is positive and strictly increasing. At the right endpoint the numerator is zero. Therefore L-R is continuous and strictly increasing, negative at c0 and positive at 1. The intermediate value theorem gives a unique C in (c0,1) with L(C)=R(C).

Set A=L(C)=R(C) and B=B(C). These definitions give exactly

    3A²=(b+3)C²-b,
    3B²-2CB-1=0,
    (2b+3)CA=b(A+1-B).

A>0. Moreover A²-C²=b(C²-1)/3<0, so A<C. The inequalities C<B<1 were established above. Conversely, any ordered solution of the three equations must have C>c0, B=B(C) (the other quadratic root is negative), and A=L(C)=R(C), so the ordered threshold triple is unique. This is uniqueness only within the specified three-cut parameterization.

## Global best response for Player I

Let I's hand be x. Checking gives 3x²-1. Betting gives (b+3)C²-(b+1) for x<=C. For x>=C it gives

    2C²+2C(x-C)(b+2)+2(b+1)(x-C)²-(b+1)(1-x²)
      =3(b+1)x²-2bCx-(b+1).

The same terminal-pot partition as for b=2 gives these expressions. Subtracting the check payoff and using Eq. A-B factors the action difference as

    3(A-x)(A+x)                       for 0<=x<=C,
    b(x-B)(3(x+B)-2C)                 for C<=x<=1.

On the second interval 3(x+B)-2C >= C+3B>0. Thus I optimally bets for x<A and x>B and checks for A<x<B. At A and B both actions tie.

## Global best response for each caller

For complete action payoffs, define H(y)=0 on [0,A], H(y)=y-A on [A,B], and H(y)=B-A on [B,1]. H(y) is the measure of I's checking hands below y. The caller's fold-policy payoff, including states where I checks and no caller decision occurs, is U_fold(y)=-1+3yH(y): the baseline is -1, and a check-showdown win adds 3. Its call-policy payoff is U_call(y)=U_fold(y)+D(y), where D follows below. These expressions give every player's action payoff as a piecewise polynomial, not just the sign comparison.

Let T=A+1-B>0, and let W(y) measure I's betting hands below y. As before, W(y) is y, A, A, A+y-B on the four intervals [0,A], [A,C], [C,B], [B,1]. The difference between call and fold before normalizing by the probability T of a bet is

    W(y)[(2b+3)C+3(b+1)max(y-C,0)]-bT.

The first term accounts for beating I while the other caller folds or has a lower hand; -bT is the extra called stake lost in the baseline outcome. Eq. C gives the following exact expressions:

    (2b+3)C(y-A)                                   on [0,A],
    0                                             on [A,C],
    3(b+1)A(y-C)                                   on [C,B],
    3(b+1)A(y-C)+(y-B)(3(b+1)y-bC)                  on [B,1].

The signs are nonpositive below C and nonnegative above C. In the last line, y>=B>C gives 3(b+1)y-bC>(2b+3)C>0. Hence the stated call/fold strategy is optimal. Dividing by positive T gives the conditional-on-bet action difference. The other caller has the same best-response calculation, with no restriction that a deviating policy be symmetric.

## Measurable deviations, endpoints and values

Each player has one binary decision based on their hand (callers also observe I's bet). For any measurable randomized unilateral policy the payoff at a hand is a convex combination of the two conditional action payoffs. Their pointwise maximum is achieved by the profile above. Utilities are bounded for each fixed finite b, so integration shows that no such deviation improves ex ante utility. At 0 and 1 use the continuous-extension optimal actions; threshold ties allow either action. Opponent-hand ties have probability zero conditional on every own hand.

The source writes uniform(0,1) hands and strict betting intervals. The closed-endpoint actions just specified are a chosen representative, not a verbatim transcription of its “otherwise” actions at 0 and 1. The equilibrium proof holds on the open hand space and ex ante under either endpoint convention. Pointwise optimality on the closed interval is asserted only for this explicitly extended representative. A criterion that insists on the literal source actions at the closed endpoints must account for this distinction.

I's algebraic payoff when b is algebraic is the integral

    V(b)=-A³+(b+3)AC²-bA-bB³+bB²C+bB-bC
        =2A³+b(B-C)(1-B²).

The latter equality uses Eq. A. For general real b this formula still defines the real payoff. By symmetry and zero sum, each caller receives -V(b)/2. The b=2 specialization, including independent isolating intervals, is in equilibrium.json.

## Scope and checking

`universal_identities.py` verifies every polynomial identity and the squared endpoint margin exactly. The independent standard-library polynomial checker `universal_check.py` verifies explicit ideal-membership multipliers and five existence identities stored in `universal.json`; it needs no computer algebra package. The continuity, monotonicity, positive-square-root implications and integration argument above are the analytical part of the proof; they are explicit and have not been checked by an independent context. `rectangle_check.py` independently rebuilds all action-payoff pieces for symbolic b from terminal pots. Finite numerical samples are diagnostics only.

The exact b=2 value is 0.1225570747148686867377787982761502092550102815857780623, not the printed 0.122557074714865. This proposed p1 theorem must not be used to assert that the original branch-A printed-digit condition passed. That criterion issue and independent panel review remain unresolved.


The additional `ordered_cone_check.py raw_payoffs.txt` check starts from the independent terminal-pot rectangle output. After subtracting the relevant defining equation and orienting toward the prescribed action, it substitutes nonnegative gaps between adjacent ordered cutoffs and the hand. Every resulting coefficient is nonnegative in each of the twelve player/region combinations. It also verifies all complete action payoffs and integrated values. This is an exact polynomial check of the whole conditional sign domain; the analytic existence and measurable-policy arguments above remain separate.
