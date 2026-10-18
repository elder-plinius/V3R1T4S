# Exact n^(5/6) central-band theorem

For n>=65536, 4<=j<=floor(n/2), and 2^36*(n-2j)^6<=n^5, an odd prime divides both C(n,3) and C(n,j).

Assume to the contrary that no odd prime divides both binomial coefficients.

1. Low prime powers. If p is odd, t in {0,1,2}, and p^e exactly divides n-t, then v_p(C(n,3))=e except that it equals e-1 for p=3. Distinct members of n,n-1,n-2 have coprime odd parts. Consequently every such prime power is active except p=3,e=1. For an active prime, p does not divide C(n,j).

In F_p[X], (1+X)^p=1+X^p; expand n in base p to obtain the product of digit binomial coefficients for C(n,j) modulo p. Nondivisibility means every digit of j is no larger than the corresponding digit of n. Since n mod p^e=t, necessarily j mod p^e is in {0,...,t}. This argument is also valid at p=3 for active e>=2.

Let s=v2(n), delta=1 when v3(n)=1 and zero otherwise, m=odd(n)/3^delta, q=2^s*3^delta. The t=0 constraints imply m|j, so j=ma with 0<a<=q/2.

2. Parity and the centre. For even n, put A=strip3(n-1), where strip3(x) removes the single factor 3 exactly when v3(x)=1. Then A is odd and A|j(j-1). If j=n/2, multiplication by 4 gives A|n(n-2), hence A|1. Thus n-1 is 1 or 3, impossible for n>=4096. So j<n/2.

If n is odd, q is 1 or 3. q=1 is impossible since n|j. For q=3, j=n/3 and n-2 is odd and not divisible by 3. The t=2 constraints imply n-2|j(j-1)(j-2). Multiply by 27 and use 3j=n: n-2 divides 8, impossible.

If n=2 mod 4, q is 2 or 6. q=2 permits only the excluded central j. For q=6, m is odd and not divisible by 3; m=1 gives n=6, so m>=5 and n>=30. Here n-1 is odd and not divisible by 3. Multiplication of (n-1)|j(j-1) by q^2 gives (n-1)|a(a-6), while 1<=a<=3 implies 0<|a(a-6)|<=9<n-1. Impossible.

Thus 4|n and 0<d:=n-2j is even.

3. Integer localization and a nonzero quotient. Put c1=3 exactly when v3(n-1)=1, and c1=1 otherwise; c2=3 exactly when v3(n-2)=1, and c2=1 otherwise. Let A=(n-1)/c1, B=(n-2)/(2c2). These are odd, c1*c2<=3, and the local constraints imply

    A | d^2-1,       B | d(d^2-4),    d=n-2j>0 even.

Set k=(d^2-1)/A, a positive integer. Reducing c1(d^2-1)=k(n-1) modulo 4 shows k=c1 mod4, hence k!=3c1. Reducing the identity modulo B and combining with the cubic constraint gives B|d(k-3c1). Therefore

    l=d(k-3c1)/B=2c2*d*(k-3c1)/(n-2)

is a nonzero integer.

4. Split the k ranges. Write a=c1, b=c2. The band implies d<=n/256: d^6<=n^5/2^36<=n^6/2^48 because n>=2^16>=2^12, and sixth roots preserve order.

If k<6a, then |k-3a|<=3a-1<=8. Since B divides the nonzero integer d(k-3a),

    n-2=2bB<=48d<=3n/16,

impossible for n>=65536. Hence k>=6a.

5. Positive integer quotients. Define the integers

    u=a*d*l-2b*k*(k-3a),
    v=a*l^2-2b*u*(k-4a).

The two exact relations already proved are

    k(n-1)=a(d^2-1),      B*l=d(k-3a),      2bB=n-2.

They imply

    B*u=(k+a)(k-3a),                               (I)
    B^2*v=(k-3a)*((k-a)^2+4a^2(n-3)).             (II)

For completeness, multiply (I) by 2b and substitute the definition of u. Its difference from the desired equality is

    a*d*((n-2)l-2bd(k-3a))
      -2b(k-3a)*(k(n-1)-a(d^2-1))=0.

For (II), use B*l=d(k-3a), (I), and the definition of v:

    B^2*v = a*d^2*(k-3a)^2
             -(n-2)*(k+a)*(k-3a)*(k-4a)
          = (k-3a)*[a*d^2*(k-3a)-(n-2)(k+a)(k-4a)].

Replacing a*d^2 by k(n-1)+a expands the bracket to (k-a)^2+4a^2(n-3). Thus both identities are exact, with no division by an unknown sign or zero.

Since k>=6a and n>=65536, B>0 and both right sides are strictly positive. Therefore u and v are positive integers; in particular v>=1.

6. The band forces v<1. From (II), a,b<=3, k-3a<k, (k-a)^2<k^2 and n-3<n give

    v <=36*k*(k^2+36n)/(n-2)^2.

The known k formula also gives k<=3d^2/(n-1). Substitute this into both positive terms of the preceding bound:

    v <=972*d^6/((n-1)^3(n-2)^2)
          +3888*n*d^2/((n-1)(n-2)^2)
      <=31104*(d^6/n^5+d^2/n^2).

Here n>=4 gives (n-1)^3(n-2)^2>=n^5/32 and (n-1)(n-2)^2>=n^3/8. The band implies d^6/n^5<=2^-36<2^-16, while d<=n/256 implies d^2/n^2<=2^-16. Therefore

    v <62208/65536<1,

contradicting v>=1. This proves the stated theorem. No bounded computation or unproved external theorem is an input.

## Optional algebraic certificate and limits

algebraic-core-direct.json and author-code/verify_algebraic_core_direct.py verify exact polynomial identities and positivity certificates, and reject deliberately corrupted data. These are independently checkable algebraic artifacts, not a full formal proof-assistant encoding of prime localization, integer divisibility, all domain implications, or the theorem. The written argument above supplies those explicit steps. A finite spot check never replaces its universal proof.
