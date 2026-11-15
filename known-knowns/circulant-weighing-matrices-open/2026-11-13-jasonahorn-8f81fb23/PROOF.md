# Completeness of the CW(208,81) exhaustion

## 1. The forced family and sign normalization

Let A(x) = sum a_i x^i in Z[x]/(x^208-1), with a_i in {-1,0,1}.
A circulant weighing matrix of weight 81 is equivalent to

    A(x) A(x^-1) = 81.

The prime-power multiplier theorem states that if CW(v,p^(2e)) exists and gcd(v,p)=1, some translate is fixed by multiplication by p. Use p=3, e=2, v=208; the hypotheses hold. References: Tan, Result 2.3 at https://arxiv.org/html/2608.18468v2 and Arasu–Gordon–Zhang, Theorem 2.2 at https://arxiv.org/html/1908.08447v3.

Consequently it suffices to enumerate rows constant on multiplication-by-3 orbits modulo 208. Translation preserves correlations and weight. Evaluating the identity at x=1 gives A(1)^2=81. Global negation preserves all conditions, so the C search takes A(1)=9 without loss of generality. Together with weight 81, this implies 45 pluses and 36 minuses. The independent Python search covers both signs instead.

The 35 orbits modulo 208 have sizes: two of size 1, three of size 2, eight of size 3, two of size 4, twelve of size 6 and eight of size 12. Each row constant on these orbits corresponds to one assignment of a value in {-1,0,1} to each orbit.

## 2. Contraction modulo 13

Map the group ring to Z[x]/(x^13-1), writing

    B_j = sum a_i over i congruent to j modulo 13.

This is a ring homomorphism, so B(x)B(x^-1)=81. Each fiber has 16 terms; hence |B_j|<=16. Also sum B_j=9, sum B_j^2=81, and all nonzero cyclic correlations of B vanish. Multiplication-by-3 invariance descends to B.

There are five quotient orbits: {0} and four orbits of size 3. Write the singleton as t and the four other orbit values as u_1,...,u_4. Then

    t + 3 sum u_i = 9
    t^2 + 3 sum u_i^2 = 81.

The first identity forces t=3b. Thus

    -3 <= b <= 3
    sum u_i = 3-b
    sum u_i^2 = 27-3b^2.

These bounds, all integer choices of four values, and exact contraction correlations give exactly 25 positive-sum contractions. Energy further bounds |u_i|<=5. The C enumerator uses the original broader bound 16; the Python enumerator may use the tighter energy bound. Neither can omit a valid contraction. The checker compares actual C rows, Python rows and object/contractions.txt, not merely their counts.

## 3. Lifting the contractions

Each original multiplier orbit projects into exactly one quotient orbit. Group the 35 original orbits accordingly; there are five groups with seven original orbits each. Each group's support is disjoint from the others (at most 48 positions per group).

For each contraction, enumerate all 3^7 assignments to each group and retain those with the required fiber sum on a representative residue. The other residue sums within that quotient orbit are equal by multiplier invariance. Thus no possible lift is discarded. Enumerating one representative of the quotient orbit here is an equality consequence, not an extra symmetry restriction.

## 4. Exact join and final checking

For a shift that is a multiple of 13, positions before and after the shift have the same residue modulo 13 and therefore belong to the same group. Cross-group terms vanish. Consequently each such correlation of a full row is the sum of its per-group correlations.

The C program stores assignments of two groups and streams assignments of the other three. Their correlation vectors must cancel at shifts 13,26,39,52,65,78,91. Hash buckets are only indexes: every candidate key is compared exactly, including collisions. These are necessary filters, not sufficient tests.

Every matching pair is combined and checked for entries in {-1,0,1}, exact weight 81, and zero correlations at all nonzero shifts (including 104). Thus neither the omitted midpoint hash coordinate nor any other unchecked hash coordinate is omitted from the final test. The completed exhaustive search has 43,196,762 streamed assignments and 5,519,232 join matches, with zero accepted rows. The reported node count is streamed half-assignments, not the cardinality of all possible full rows.

C integer correlations have magnitude at most 208. int16 hash coordinates and int arithmetic therefore suffice. Hash arithmetic intentionally uses unsigned integer wraparound.

## 5. Separately implemented confirmation

verify-it-yourself/independent.py was initially written before its author read liftjoin.c. It independently constructs multiplier orbits, enumerates contraction equations without positive-sum normalization (50 contractions), and forms all group assignments. Its join uses exact weight and all shifts that are multiples of 13, including 104. It uses a fixed-seed additive unsigned-64 hash: equality of the full vector implies equality of the hash, so collisions can create extra candidates but cannot lose true matches. Every hash match is rechecked against the full integer vector before all remaining exact integer correlations are tested. There is no floating-point rejection.

The stronger filters leave 1,499,136 matches across both signs and no solution. Half that count, 749,568, agrees with a diagnostic count from the C search restricted to weight 81. Different join counts reflect different necessary filters, not a disagreement.

Positive control: the same independent enumerator finds 48 multiplier-fixed signed solutions for CW(91,81). Negative control: it finds none for CW(104,81), whose nonexistence is known. These controls do not themselves prove completeness, but guard against an implementation that rejects everything.

## 6. Conclusion and limitations

If CW(208,81) existed, the multiplier theorem, sign normalization and contraction would put a translate (possibly negated) in this exact finite enumeration. None survives, so it does not exist. No properness restriction was imposed: improper possibilities are also covered.

This is a computational multiplier argument, not a DRAT/LRAT certificate or a formal proof-assistant development. The named theorem is an external mathematical premise. Reproducibility, coverage and novelty are separate questions; consult README.md for the qualified novelty statement.
