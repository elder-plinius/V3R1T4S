# REPRODUCE skeptic verdict: three-player von Neumann poker, partial win p1 (all real b>0)

context: Claude Code Agent subagent (Opus), fresh context, saw only claim/

Scope assessed: the single claim in claim/CLAIM.md. For every real b>0 the ordered solution 0<A<C<B<1 of the paper's Eq. A-C exists and is unique. Its threshold profile (I bets iff x<A or x>B; II and III each call iff own hand >C, each without seeing the other's action) is a Nash equilibrium against every measurable unilateral deviation. The b=2 specialization is in claim/equilibrium.json.

## 1. Definition used (quoted from claim/data/paper.txt, Section 4)

> "The three players each put 1 dollar into the pot. Player I acts first, choosing either to check or to bet a fixed integer amount b>0. If Player I checks, the three hands are immediately compared, and the player with the highest hand wins the pot. However, if Player I bets, Players II and III have two choices: call or fold."

> "each of the three players contributes 1 dollar to the pot and receives independent uniform(0,1) hands. [...] Player I: If 0<x<A or B<x<1 he should bet, otherwise check. Players II and III: If 0<y<C they should fold, otherwise call."

The paper's Eq. A, Eq. B and Eq. C were used verbatim. Their integrands fix the terminal net payoffs I used:
- I checks: three-way showdown; the winner nets +2 and the others -1.
- I bets and both callers fold: I nets +2 and each caller -1.
- I bets and exactly one player calls: heads-up showdown, winner +(b+2), loser -(b+1), the folder -1.
- I bets and both call: three-way showdown, winner +2(b+1), losers -(b+1).

The callers see only their own hand and I's action.

## 2. Independent checker (written before reading any of the author's .py files)

My code lives outside claim/, in my own scratch folder.
- payoffs.py encodes the terminal rules above. For each player and each own-hand region it integrates exactly over the opponents' hands, cell by cell, with symbolic b, A, B, C. The regions are [0,A], [A,C], [C,B] and [B,1]. Each cell value depends only on order relations, so the result holds on the whole ordered cone.
- numcross.py cross-checks these formulas against brute-force numpy quadrature of the raw rules at three (b,A,B,C) points:

```
b=0.7 max |symbolic - grid quadrature| = 2.04e-14
b=2 max |symbolic - grid quadrature| = 8.88e-16
b=9 max |symbolic - grid quadrature| = 4.88e-15
```

The derived action differences and the claimed factorizations agree up to an exact multiple of one paper equation (residual_identities.py):

```
I [0,A] diff == claimed + (-Eq): True     (factor 3(A-x)(A+x), minus Eq.A)
I [A,C] diff == claimed + (-Eq): True
I [C,B] diff == claimed + (-Eq): True     (factor b(x-B)(3(x+B)-2C), minus b*Eq.B')
I [B,1] diff == claimed + (-Eq): True
II/III [0,A]: True  ((2b+3)C(y-A))      II/III [A,C]: True  (0)
II/III [C,B]: True  (3(b+1)A(y-C))      II/III [B,1]: True  (3(b+1)A(y-C)+(y-B)(3(b+1)y-bC))
V - claimed raw formula = 0
Vclaim1 - Vclaim2 - (A * EqA) = 0
V + 2*VII (zero-sum check) = 0
```

Sign analysis, which I re-derived by hand from these forms with b>0 and 0<A<C<B<1:
- **Player I.** On [0,C] the difference is 3(A-x)(A+x), so I bets below A and checks on (A,C). On [C,1] it is b(x-B)(3(x+B)-2C), with 3(x+B)-2C >= C+3B > 0, so I checks on (C,B) and bets above B.
- **Callers.**
  - On [0,A] the difference is (2b+3)C(y-A) <= 0.
  - On [A,C] it is identically 0. This is a positive-measure indifference interval: folding there is a best response, but only weakly.
  - On [C,B] it is 3(b+1)A(y-C) >= 0.
  - On [B,1] it is 3(b+1)A(y-C)+(y-B)(3(b+1)y-bC) > 0, because 3(b+1)y-bC > (2b+3)C > 0.
- **Measurable deviations.** Each player has one binary decision per information set: own hand, plus I's bet for callers. Payoffs are bounded. A randomized measurable policy's payoff at each hand is a convex combination of the two action payoffs, so it is at most their pointwise maximum, and the profile attains that maximum at every hand. Integrating gives no ex ante gain. III's calculation was done separately and is identical to II's. The deviating caller's opponent caller stays at threshold C.

## 3. b=2 exact algebraic check (b2_exact.py; mine)

A lex Groebner basis of {Eq.A, Eq.B, Eq.C, V - value} has shape form: A, B and V are each linear in their own variable over a degree-8 polynomial in C. I isolated the roots of C's polynomial, confirmed the sign change and squarefreeness, and evaluated the shape polynomials with exact Fraction interval Horner arithmetic:

```
C poly sign change on interval: True ; squarefree: True
A enclosure [...] width 2.7e-39 hits 1 root(s): [0.13705819432836894]
B enclosure [...] width 2.6e-40 hits 1 root(s): [0.8294222497953907]
V enclosure [...] width 2.5e-39 hits 1 root(s): [0.12255707471486868]
ordered 0<A<C<B<1 rigorous: True
V in [ 0.12255707471486868673777879827615020925365... , 0.12255707471486868673777879827615020925616... ]
A_interval json interval contains my enclosure-overlap: True  json width 1.0e-65
C_interval ... True ; B_interval ... True ; value_interval ... True
A/B/C/value_polynomial_ascending matches mine: True (all four)
<each json interval> roots of json poly in json interval (sympy count_roots): 1   (all four)
```

My independent value is V(2) = 0.12255707471486868673777879827615020925..., which is consistent with claim/equilibrium.json.

**Printed-digit mismatch with the source.** The paper prints 0.122557074714865. The exact value minus the printed value is +3.69e-15, so the exact value rounds to 0.122557074714869 at 15 decimals. The paper's printed thresholds are also off: plugging A=0.137058194328370, B=0.829422249795391, C=0.641304115985175 into the equations leaves residuals of about 2.6e-14, 7.5e-15 and 4.6e-16. That is consistent with floating-point error in the paper rather than a different object.

The literal "matching 0.122557074714865 to the digits given" clause of the primary criterion is therefore not met. The claim says so explicitly, and the author's checker reports `printed_15_decimal_match: false`. The claim asserts only p1, which needs no value digits. I flag this for adjudication; it does not obstruct p1.

## 4. All b>0: existence, uniqueness and sign conditions (allb.py plus re-derivation by hand)

```
paper Eq A == EqA: True ; paper Eq B == -b*EqB: True ; paper Eq C == -EqC: True
B(c) solves EqB: True ; root product = -1/3: -1/3
denominator margin ((2b+3)c0)^2-b^2 = 3*b*(b**2 + 3*b + 3)/(b + 3)
A^2-C^2 under EqA = b*(C - 1)*(C + 1)/3
B<1 <=> (3-c)^2-(c^2+3) = 6 - 6*c  ; B>c <=> (c^2+3)-(2c)^2 = 3 - 3*c**2
dB/dc = c/(3*sqrt(c**2 + 3)) + 1/3
L(c0) = 0  L(1) = 1  B(1) = 1
numeric diagnostic: ordered for all 121 sampled b in [1e-6,1e6]: True   (diagnostic only)
```

I re-derived each step of claim/all_b_proof.md:
1. Eq.B divided by b gives 3B^2-2CB-1=0. Its roots have product -1/3, so exactly one root is positive: B(C)=(C+sqrt(C^2+3))/3.
2. Eq.A gives A^2=((b+3)C^2-b)/3, so A>0 forces C>c0=sqrt(b/(b+3)), and c0 lies in (0,1).
3. Eq.C gives A((2b+3)C-b)=b(1-B). The factor (2b+3)C-b is positive and increasing on [c0,1], by the displayed margin.
4. For 0<c<1, c<B(c)<1, and B is strictly increasing.
5. L(c) is strictly increasing from 0 to 1. R(c)=b(1-B(c))/((2b+3)c-b) is positive, strictly decreasing, and reaches 0 at c=1.
6. L-R therefore has exactly one zero C in (c0,1), by the intermediate value theorem plus strict monotonicity. Conversely, any ordered solution must be that zero, which gives uniqueness within the three-cut family.
7. A<C because A^2-C^2=b(C^2-1)/3<0, and C<B<1 by step 4.

Together with section 2, every sign condition holds for every b>0. Every step re-derived without discrepancy.

## 5. Author's checks and package integrity

- MANIFEST.json: all 52 listed SHA-256 hashes match, and no listed file is missing. Four files are present but unlisted, which is a minor packaging note: PRIOR_ART_SOURCES.md, STATUS_RECORD.md, data/simelis-1977-page-one-preview.pdf and data/simelis-1977-page-one-preview.txt. None is a check input.
- `sh run_checks.sh` exits 0, in about 3 s:

```
PASS: exact b=2 equilibrium certificate; printed decimal criterion is FALSE
PASS: universal exact polynomial certificate          (8 action/value identities, 5 existence identities)
PASS: exact nonnegative-gap polynomial certificates for all 12 raw payoff regions   (24 action payoffs, 3 values matched)
PASS: exact finite calibrations and deliberately exploitable profile
PASS: mathematical certificates only; bank criterion and panel review remain separate
```

  Its b=2 value line reads `0.1225570747148686867377787982761502092550102815857780623`, which agrees with my enclosure.
- Optional checks with the SymPy virtual environment:
  - rectangle_check.py: `PASS: all 12 action-difference polynomials match, value sum is zero`. Its stdout's SHA-256 is ac0e2aca...e69a, identical to claim/raw_payoffs.txt.
  - universal_identities.py: `PASS: exact symbolic identities for all b; ...`.
- My comparison of claim/raw_payoffs.txt against my own payoffs: `author raw action payoffs compared with mine: 24 mismatches: 0`.
- Determinism: two runs of run_checks.sh gave byte-identical output (sha256 0a845725...3e71), and my scripts are also repeatable.

## Mismatches and notes

- No mathematical mismatch between my independent derivation and the claim, for b=2 or for all b>0.
- The source's printed b=2 value (and its printed C, A digits) is wrong by a few units in the 15th decimal place. The literal printed-digit clause of the primary criterion fails. This is acknowledged in the claim and does not bear on p1.
- The endpoint convention (bet at x=0 and x=1, fold at y=0, call at y=1) differs from the paper's literal "otherwise" actions only on a null set. The equilibrium is weak: callers are exactly indifferent on all of [A,C]. Neither point affects Nash equilibrium over measurable deviations.
- Four unlisted non-mathematical files in MANIFEST (see section 5).

pass: true
