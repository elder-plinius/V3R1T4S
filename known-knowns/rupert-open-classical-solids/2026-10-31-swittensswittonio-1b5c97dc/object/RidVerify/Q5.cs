using System.Numerics;
namespace RidVerify;

/// <summary>Exact element (A + B*sqrt5)/D of Q(sqrt5); D>0, normalised by gcd(A,B,D)=1.</summary>
public readonly struct Q5 : IEquatable<Q5>
{
    public readonly BigInteger A, B, D;
    public Q5(BigInteger a, BigInteger b, BigInteger d)
    {
        if (d.IsZero) throw new DivideByZeroException();
        if (d.Sign < 0) { a = -a; b = -b; d = -d; }
        if (!(d.IsOne))
        {
            var g = BigInteger.GreatestCommonDivisor(BigInteger.GreatestCommonDivisor(a, b), d);
            if (!g.IsOne && !g.IsZero) { a /= g; b /= g; d /= g; }
        }
        A = a; B = b; D = d;
    }
    public static Q5 Zero => new Q5(0, 0, 1);
    public static Q5 One => new Q5(1, 0, 1);
    public static Q5 Sqrt5 => new Q5(0, 1, 1);
    public static Q5 Int(long n) => new Q5(n, 0, 1);
    public static Q5 Rat(BigInteger n, BigInteger d) => new Q5(n, 0, d);
    public static Q5 Of(BigInteger a, BigInteger b) => new Q5(a, b, 1);
    public static readonly Q5 Phi = new Q5(1, 1, 2);          // (1+sqrt5)/2
    public bool IsZero => A.IsZero && B.IsZero;
    public bool IsRational => B.IsZero;
    public static Q5 operator +(Q5 x, Q5 y) => x.D == y.D ? new Q5(x.A + y.A, x.B + y.B, x.D) : new Q5(x.A * y.D + y.A * x.D, x.B * y.D + y.B * x.D, x.D * y.D);
    public static Q5 operator -(Q5 x, Q5 y) => x.D == y.D ? new Q5(x.A - y.A, x.B - y.B, x.D) : new Q5(x.A * y.D - y.A * x.D, x.B * y.D - y.B * x.D, x.D * y.D);
    public static Q5 operator -(Q5 x) => new Q5(-x.A, -x.B, x.D);
    public static Q5 operator *(Q5 x, Q5 y) => new Q5(x.A * y.A + 5 * x.B * y.B, x.A * y.B + x.B * y.A, x.D * y.D);
    public static Q5 operator *(Q5 x, long k) => new Q5(x.A * k, x.B * k, x.D);
    public static Q5 operator *(long k, Q5 x) => x * k;
    public Q5 Inv()
    {
        // 1/((A+B s)/D) = D (A - B s)/(A^2-5B^2)
        var n = A * A - 5 * B * B;
        if (n.IsZero) throw new DivideByZeroException();
        return new Q5(D * A, -D * B, n);
    }
    public static Q5 operator /(Q5 x, Q5 y) => x * y.Inv();
    /// <summary>Exact sign of (A+B sqrt5)/D, by the rule of the paper (sec. 5.1).</summary>
    public int Sign()
    {
        int sa = A.Sign, sb = B.Sign;
        if (sb == 0) return sa;
        if (sa == 0) return sb;
        if (sa == sb) return sa;
        return sa * (A * A - 5 * B * B).Sign;
    }
    public int CompareTo(Q5 o) => (this - o).Sign();
    public bool Equals(Q5 o) => A == o.A && B == o.B && D == o.D;
    public override bool Equals(object o) => o is Q5 q && Equals(q);
    public override int GetHashCode() => HashCode.Combine(A, B, D);
    public static bool operator ==(Q5 x, Q5 y) => x.Equals(y);
    public static bool operator !=(Q5 x, Q5 y) => !x.Equals(y);
    public static bool operator <(Q5 x, Q5 y) => x.CompareTo(y) < 0;
    public static bool operator >(Q5 x, Q5 y) => x.CompareTo(y) > 0;
    public static bool operator <=(Q5 x, Q5 y) => x.CompareTo(y) <= 0;
    public static bool operator >=(Q5 x, Q5 y) => x.CompareTo(y) >= 0;
    public static Q5 Min(Q5 x, Q5 y) => x <= y ? x : y;
    public static Q5 Max(Q5 x, Q5 y) => x >= y ? x : y;
    public override string ToString() => B.IsZero ? (D.IsOne ? A.ToString() : $"{A}/{D}") : $"({A}+{B}*s5)/{D}";
    /// <summary>Parse "a/b" rational text.</summary>
    public static Q5 ParseRat(string s)
    {
        var i = s.IndexOf('/');
        if (i < 0) return new Q5(BigInteger.Parse(s), 0, 1);
        return new Q5(BigInteger.Parse(s.AsSpan(0, i)), 0, BigInteger.Parse(s.AsSpan(i + 1)));
    }
    public double ToDouble() => ((double)A + (double)B * Math.Sqrt(5)) / (double)D;
    public static Q5 Pow(Q5 x, int n) { var r = One; for (int i = 0; i < n; i++) r = r * x; return r; }
}
