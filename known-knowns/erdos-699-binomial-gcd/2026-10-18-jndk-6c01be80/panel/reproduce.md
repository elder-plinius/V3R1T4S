context: fresh REPRODUCE subagent; scientific input restricted to claim/; no parent scientific notes, earlier runs, dossiers, or other panel opinions read
role: mathematical reproduction only
verdict: SURVIVES

Definition quoted from CLAIM.md: "For every integer n>=65536 and every integer j with 4<=j<=floor(n/2) and 2^36*(n-2j)^6<=n^5, there exists an odd prime dividing both C(n,3) and C(n,j)."

PROVED-HERE: The elementary argument in PROOF.md proves exactly this theorem. My pass concerns its mathematical reproduction, not novelty, external refereeing, a bank partial-win qualification, any all-n result, or the full conjecture.

## Independence and execution

I wrote panel-work/reproduce/independent_check.py from the quoted definition before opening author-code/verify_algebraic_core_direct.py. The checker computes exact binomial coefficients and their gcd, independently computes factorial valuations, checks active prime-power localization, and expands independently coded sparse polynomials. It does not load author-code or algebraic-core-direct.json. All mathematical execution used the prescribed existing remote Python environment with nice priority and explicit timeouts; no installation or outward action occurred. The initial negative control (6,3) was incorrectly chosen: its odd gcd is positive. Its assertion failed, and I corrected my control to (4,2), outside the theorem domain; this was a checker-fixture correction, not a theorem repair.

Saved independent output: panel-work/reproduce/independent-output.json. It reports 15625 direct admissible pairs for 8<=n<=256, 14104 active-localization checks, including 1326 active full-3-power checks, and PASS for the exact polynomial identities and constant arithmetic. The positive arithmetic control is (8,4), and the negative arithmetic control is (4,2). These are corroborative tests, not an exhaustive verification of the claimed infinite region.

Independent checker SHA256: aa51761b91a3cc7be06286d92edd31bea6d24a009f1e745912cb1b802ac2945c.
Independent output SHA256: f5cf24460a13f1bc6050caaa037e56a443732016a139a84a751e68a61aa92a0a.
Reviewed PROOF.md SHA256: 6c01be8056dce86ca1cef0df2df38c99b1747e463bc1069c6c4e0a3fcf915837.
Reviewed CLAIM.md SHA256: e71c54b43a6d2b6fa4212a902939cb9c604199e9161e3900c92e96a05b59a0d2.

The following is my independent derivation of all infinite steps.

## Active primes and the full 3-power

Assume there is no common odd prime. For odd p and t in {0,1,2}, at most one of n,n-1,n-2 is divisible by p. If p^e exactly divides n-t, the factorial formula C(n,3)=n(n-1)(n-2)/6 gives valuation e for p>3 and e-1 for p=3. Thus p is active precisely except at p=3,e=1. Every active p must have v_p(C(n,j))=0.

Here full p^e localization is justified even for p=3, where the valuation in C(n,3) is only e-1. In characteristic p, the binomial theorem and divisibility of the intermediate binomial coefficients give (1+X)^p=1+X^p. Iterating and multiplying along the base-p digits n_r gives (1+X)^n=product_r (1+X^(p^r))^(n_r). The exponent choices in each factor are between 0 and p-1, so base-p uniqueness makes the coefficient of X^j equal to product_r C(n_r,j_r) modulo p. Each factor with j_r<=n_r<p is nonzero modulo p. Consequently nondivisibility implies j_r<=n_r for every digit.

Since n mod p^e=t<p, its lowest e digits have only the units digit t. Thus j mod p^e lies in {0,...,t}. This proves the claimed full modulus, including 3^e when e>=2, without incorrectly identifying e with v_3(C(n,3)). Multiplying the t=0 coprime prime powers gives m|j, with m=odd(n)/3^delta, delta=1 exactly when v_3(n)=1. Writing n=mq gives q=2^s*3^delta and j=ma, 1<=a<=q/2.

For a t=1 active prime power, the permitted residues 0,1 imply divisibility of j(j-1); for t=2, the residues 0,1,2 imply divisibility of j(j-1)(j-2). Multiplication of these coprime powers is legitimate. For odd p, the factors in these products have no shared p, so no prime-power exponent is lost. Removing a single factor 3 only when its valuation is exactly one correctly omits precisely the inactive factor.

## Centre and parity

For even n, let A be n-1 with its single factor 3 removed only if v_3(n-1)=1. Then A is odd and A|j(j-1). If 2j=n, multiplying by 4 gives A|n(n-2). Since A|n-1, reduction gives A|-1, hence A=1. This forces n-1 to be 1 or 3, contradicting the domain. Thus the centre is excluded without invoking a prior-work theorem.

For odd n, q is 1 or 3. The q=1 case has no positive a<=q/2. In the q=3 case a=1 and j=n/3. Now n-2 is odd and coprime to 3, so all its prime powers are active and n-2|j(j-1)(j-2). Multiplication by 27 gives divisibility of n(n-3)(n-6). Modulo n-2 this is 2*(-1)*(-4)=8. The resulting n-2|8 contradicts n>=65536.

For n congruent to 2 modulo 4, q is 2 or 6. The q=2 case is exactly the excluded centre. For q=6, 1<=a<=3, n=6m, and n-1 is odd and not divisible by 3. Hence n-1|j(j-1). Multiplication by 36 and use of 6m=1 modulo n-1 gives n-1|a(a-6). But 0<|a(a-6)|<=9<n-1. Thus 4|n, and d=n-2j is positive and even.

## Integer localization and nonzero quotient

Set a=c1 and b=c2, each equal to 3 only when the relevant n-1 or n-2 has 3-adic valuation exactly one, and equal to 1 otherwise. Both cannot equal 3, since 3 cannot divide consecutive integers. With A=(n-1)/a and B=(n-2)/(2b), both A and B are positive odd integers; v_2(n-2)=1 because 4|n.

The t=1 constraints imply A|j(j-1). Multiply by 4 and reduce n=1 modulo A to get A|d^2-1. The t=2 constraints similarly imply B|j(j-1)(j-2); multiplying by 8 and reducing n=2 modulo B gives B|d(d^2-4). No division by a nonunit is used.

Since d>=2, k=(d^2-1)/A is a positive integer. The equality k(n-1)=a(d^2-1), reduced modulo 4, gives k=a modulo 4. Because a is odd, 3a is not a modulo 4; hence k-3a is nonzero. Reducing the same equality modulo B gives k=a(d^2-1) modulo B, and therefore d(k-3a)=a*d(d^2-4)=0 modulo B. It follows that l=d(k-3a)/B is a nonzero integer. Its sign is not assumed in making this definition.

## Small k and all signs

From 2^36*d^6<=n^5 and n>=2^16>=2^12, we obtain d^6<=n^6/2^48, hence d<=n/256. If k<6a, positivity and integrality of k show |k-3a|<=3a-1<=8. Since the nonzero integer d(k-3a) is divisible by B, B<=8d. Consequently n-2=2bB<=48d<=3n/16. This contradicts n>=65536 (indeed 13n>32). Thus k>=6a, so k-3a>0, k-4a>0, and l>0 thereafter.

## The integer u and v identities

Define integers u=a*d*l-2b*k(k-3a) and v=a*l^2-2b*u*(k-4a). These are integers directly from their definitions; divisibility is not used to assume their integrality. Using Bl=d(k-3a) and 2bB=n-2 gives

B*u=(k-3a)*(a*d^2-k(n-2))=(k-3a)*(k+a),

where a*d^2=k(n-1)+a was substituted in the final equality. Similarly,

B^2*v=(k-3a)*[a*d^2*(k-3a)-(n-2)*(k+a)*(k-4a)].

Substituting a*d^2=k(n-1)+a and expanding the bracket gives (k-a)^2+4a^2(n-3). My independent polynomial checker verifies this bracket expansion and both denominator-cleared identities. Therefore

B^2*v=(k-3a)*[(k-a)^2+4a^2(n-3)].

Both right-hand sides are strictly positive because k>=6a, a>=1, n>=65536, and B>0. In particular v is a positive integer, so v>=1.

## Upper bound and contradiction

Using a,b<=3 and the now established positive factors,

v<=36*k*(k^2+36n)/(n-2)^2.

Also k=a(d^2-1)/(n-1)<=3d^2/(n-1). Substitution into the cubic and linear terms, respectively, gives the coefficients 972 and 3888:

v<=972*d^6/((n-1)^3*(n-2)^2)+3888*n*d^2/((n-1)*(n-2)^2).

For n>=4, each of n-1,n-2 is at least n/2. Thus the denominators are at least n^5/32 and n^3/8. Since 972*32=3888*8=31104,

v<=31104*(d^6/n^5+d^2/n^2).

The first term inside parentheses is at most 2^-36, strictly smaller than 2^-16. The second is at most 2^-16 by d<=n/256. Hence v<62208/65536<1, contradicting the integer lower bound. This closes the complete stated infinite region with no omitted finite residue.

## Optional certificate and limits

Only after writing and running my own checker did I inspect and execute author-code/verify_algebraic_core_direct.py against algebraic-core-direct.json. The captured panel-work/reproduce/author-output.json reports PASS for three identities and fifteen positivity certificates, rejecting both deliberate mutants. This supports only the stated algebraic scope; it is not a proof-assistant formalization of the theorem.

The two supplied AB-relaxation fixtures independently give (k,l,u,v)=(6973,4204,1268,232) and (2737797,480036,14028,72). Both lie outside the claimed band, and neither is treated as a genuine counterexample or as a proof of any universal statement.

The supplied manuscripts are prior-work data. The reproduced theorem does not depend on their global conclusions, external estimates, prime-gap tables, finite computations, or correctness. No manuscript result was imported to fill a gap. No literature, table, novelty, external-refereeing, or criterion clearance is implied by this mathematical verdict. The main run's honesty and mechanical gates remain separate responsibilities.

pass: true
