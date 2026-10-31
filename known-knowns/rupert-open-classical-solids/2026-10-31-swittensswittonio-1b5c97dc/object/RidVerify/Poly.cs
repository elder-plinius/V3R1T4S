using System.Numerics;
namespace RidVerify;

/// <summary>Sparse polynomial in NV variables with Q(sqrt5) coefficients. Exponent vector packed 5 bits per variable.</summary>
public sealed class Poly
{
    public const int NV = 5;
    public readonly Dictionary<int, Q5> T = new();
    static int Pack(int[] e) { int k = 0; for (int i = 0; i < NV; i++) k |= e[i] << (5 * i); return k; }
    public static int Exp(int key, int i) => (key >> (5 * i)) & 31;
    public static Poly Const(Q5 c) { var p = new Poly(); if (!c.IsZero) p.T[0] = c; return p; }
    public static Poly Const(long c) => Const(Q5.Int(c));
    public static Poly Var(int i) { var p = new Poly(); p.T[1 << (5 * i)] = Q5.One; return p; }
    public static Poly Affine(Q5 c0, params (int var, Q5 coef)[] terms)
    {
        var p = Const(c0);
        foreach (var (v, c) in terms) p.AddTerm(1 << (5 * v), c);
        return p;
    }
    void AddTerm(int key, Q5 c)
    {
        if (c.IsZero) return;
        if (T.TryGetValue(key, out var old)) { var s = old + c; if (s.IsZero) T.Remove(key); else T[key] = s; }
        else T[key] = c;
    }
    public static Poly operator +(Poly a, Poly b) { var r = a.Clone(); foreach (var kv in b.T) r.AddTerm(kv.Key, kv.Value); return r; }
    public static Poly operator -(Poly a, Poly b) { var r = a.Clone(); foreach (var kv in b.T) r.AddTerm(kv.Key, -kv.Value); return r; }
    public static Poly operator -(Poly a) { var r = new Poly(); foreach (var kv in a.T) r.T[kv.Key] = -kv.Value; return r; }
    public static Poly operator *(Poly a, Poly b)
    {
        var r = new Poly();
        foreach (var x in a.T) foreach (var y in b.T)
        {
            int key = x.Key + y.Key; // exponents add; guard overflow of 5-bit fields
            for (int i = 0; i < NV; i++) if (Exp(x.Key, i) + Exp(y.Key, i) > 31) throw new OverflowException("degree");
            r.AddTerm(key, x.Value * y.Value);
        }
        return r;
    }
    public static Poly operator *(Q5 c, Poly a) { var r = new Poly(); if (c.IsZero) return r; foreach (var kv in a.T) r.T[kv.Key] = c * kv.Value; return r; }
    public static Poly operator *(Poly a, Q5 c) => c * a;
    public static Poly operator *(long c, Poly a) => Q5.Int(c) * a;
    public Poly Clone() { var r = new Poly(); foreach (var kv in T) r.T[kv.Key] = kv.Value; return r; }
    public bool IsZero => T.Count == 0;
    public int[] Degrees()
    {
        var d = new int[NV];
        foreach (var k in T.Keys) for (int i = 0; i < NV; i++) d[i] = Math.Max(d[i], Exp(k, i));
        return d;
    }
    /// <summary>Exact division by the monomial y^a; throws if any term is not a multiple.</summary>
    public Poly DivideByMonomial(int[] a)
    {
        var r = new Poly();
        foreach (var kv in T)
        {
            int key = 0;
            for (int i = 0; i < NV; i++)
            {
                int e = Exp(kv.Key, i) - a[i];
                if (e < 0) throw new InvalidOperationException("term not divisible by zoom factor");
                key |= e << (5 * i);
            }
            r.T[key] = kv.Value;
        }
        return r;
    }
    public bool DivisibleBy(int[] a)
    {
        foreach (var k in T.Keys) for (int i = 0; i < NV; i++) if (Exp(k, i) < a[i]) return false;
        return true;
    }
    public Q5 Eval(Q5[] x)
    {
        var s = Q5.Zero;
        foreach (var kv in T)
        {
            var t = kv.Value;
            for (int i = 0; i < NV; i++) { int e = Exp(kv.Key, i); for (int j = 0; j < e; j++) t = t * x[i]; }
            s = s + t;
        }
        return s;
    }
    /// <summary>Substitute variable i by polynomial q.</summary>
    public Poly Subst(int i, Poly q)
    {
        var r = new Poly();
        var powCache = new Dictionary<int, Poly>();
        foreach (var kv in T)
        {
            int e = Exp(kv.Key, i);
            int rest = kv.Key & ~(31 << (5 * i));
            if (!powCache.TryGetValue(e, out var qp)) { qp = Const(1); for (int j = 0; j < e; j++) qp = qp * q; powCache[e] = qp; }
            var mono = new Poly(); mono.T[rest] = kv.Value;
            r = r + mono * qp;
        }
        return r;
    }
    /// <summary>Compose: new polynomial in the y variables, where variable i of this is replaced by images[i] (polys in y).</summary>
    public Poly Compose(Poly[] images)
    {
        var r = new Poly();
        // cache powers
        var pw = new Poly[NV][];
        var deg = Degrees();
        for (int i = 0; i < NV; i++)
        {
            pw[i] = new Poly[deg[i] + 1]; pw[i][0] = Const(1);
            for (int e = 1; e <= deg[i]; e++) pw[i][e] = pw[i][e - 1] * images[i];
        }
        foreach (var kv in T)
        {
            var m = Const(kv.Value);
            for (int i = 0; i < NV; i++) { int e = Exp(kv.Key, i); if (e > 0) m = m * pw[i][e]; }
            r = r + m;
        }
        return r;
    }

    /// <summary>Sound enclosure of the range over a box by term-wise interval arithmetic.</summary>
    public (Q5 lo, Q5 hi) IntervalRange(Q5[] lo, Q5[] hi)
    {
        Q5 slo = Q5.Zero, shi = Q5.Zero;
        foreach (var kv in T)
        {
            Q5 mlo = kv.Value, mhi = kv.Value;
            for (int i = 0; i < NV; i++)
            {
                int e = Exp(kv.Key, i);
                for (int j = 0; j < e; j++)
                {
                    var a = mlo * lo[i]; var b = mlo * hi[i]; var c = mhi * lo[i]; var d = mhi * hi[i];
                    var nl = Q5.Min(Q5.Min(a, b), Q5.Min(c, d)); var nh = Q5.Max(Q5.Max(a, b), Q5.Max(c, d));
                    mlo = nl; mhi = nh;
                }
            }
            slo = slo + mlo; shi = shi + mhi;
        }
        return (slo, shi);
    }
    // ---------- Bernstein ----------
    static BigInteger Binom(int n, int k)
    {
        BigInteger r = 1;
        for (int i = 1; i <= k; i++) r = r * (n - k + i) / i;
        return r;
    }
    /// <summary>1-D matrix M[r,m]: Bernstein coefficient b_r = sum_m M[r,m] a_m for p(x)=sum a_m x^m on [l,h], degree n.</summary>
    public static Q5[,] BernsteinMatrix(int n, Q5 l, Q5 h)
    {
        var w = h - l;
        var M = new Q5[n + 1, n + 1];
        // powers of l and w
        var lp = new Q5[n + 1]; var wp = new Q5[n + 1];
        lp[0] = Q5.One; wp[0] = Q5.One;
        for (int i = 1; i <= n; i++) { lp[i] = lp[i - 1] * l; wp[i] = wp[i - 1] * w; }
        for (int r = 0; r <= n; r++)
            for (int m = 0; m <= n; m++)
            {
                var s = Q5.Zero;
                for (int k = 0; k <= Math.Min(r, m); k++)
                {
                    // C(r,k)/C(n,k) * C(m,k) * l^(m-k) * w^k
                    var coef = new Q5(Binom(r, k) * Binom(m, k), 0, Binom(n, k));
                    s = s + coef * lp[m - k] * wp[k];
                }
                M[r, m] = s;
            }
        return M;
    }
    /// <summary>Dense tensor Bernstein coefficients on the box [lo,hi] using the true per-variable degree (or given degrees).</summary>
    public (int[] dims, Q5[] coefs) Bernstein(Q5[] lo, Q5[] hi, int[] deg = null)
    {
        deg ??= Degrees();
        var dims = new int[NV]; int total = 1;
        for (int i = 0; i < NV; i++) { dims[i] = deg[i] + 1; total *= dims[i]; }
        var a = new Q5[total];
        for (int i = 0; i < total; i++) a[i] = Q5.Zero;
        foreach (var kv in T)
        {
            int idx = 0, stride = 1;
            for (int i = 0; i < NV; i++) { int e = Exp(kv.Key, i); if (e > deg[i]) throw new InvalidOperationException("deg"); idx += e * stride; stride *= dims[i]; }
            a[idx] = kv.Value;
        }
        int strideJ = 1;
        for (int j = 0; j < NV; j++)
        {
            int n = deg[j];
            if (n > 0)
            {
                var M = BernsteinMatrix(n, lo[j], hi[j]);
                var tmp = new Q5[n + 1];
                int outer = total / (strideJ * dims[j]);
                for (int o = 0; o < outer; o++)
                    for (int inner = 0; inner < strideJ; inner++)
                    {
                        int baseIdx = o * strideJ * dims[j] + inner;
                        for (int r = 0; r <= n; r++)
                        {
                            var s = Q5.Zero;
                            for (int m = 0; m <= n; m++)
                            {
                                var am = a[baseIdx + m * strideJ];
                                if (!am.IsZero) s = s + M[r, m] * am;
                            }
                            tmp[r] = s;
                        }
                        for (int r = 0; r <= n; r++) a[baseIdx + r * strideJ] = tmp[r];
                    }
            }
            strideJ *= dims[j];
        }
        return (dims, a);
    }
    /// <summary>Bernstein sign test: true iff every tensor coefficient has the required strict sign (+1 positive, -1 negative).</summary>
    public bool BernsteinAllStrict(Q5[] lo, Q5[] hi, int sign, int[] deg = null)
    {
        var (_, c) = Bernstein(lo, hi, deg);
        foreach (var x in c) if (x.Sign() != sign) return false;
        return true;
    }
}
