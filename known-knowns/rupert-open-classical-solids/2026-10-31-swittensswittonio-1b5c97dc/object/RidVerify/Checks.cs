using System.Numerics;
namespace RidVerify;

public static class Checks
{
    // ======== Domain ========
    static readonly Dictionary<int, Poly> domCache = new();
    static readonly object domLock = new();
    static Poly DomPoly(int idx)
    {
        lock (domLock) { if (domCache.TryGetValue(idx, out var p)) return p; }
        var q = Geo.DomainIneq(idx);
        lock (domLock) { domCache[idx] = q; }
        return q;
    }
    /// <summary>Domain record: certify q>0 on the box by the Bernstein test applied to -q (all coefficients of -q strictly negative).</summary>
    public static bool Domain(Record r)
    {
        if (r.Inequality < 0 || r.Inequality >= Geo.NumIneq) return false;
        var (lo, hi) = Cert.BoxOfPath(r.Path);
        var q = DomPoly(r.Inequality);
        return (-q).BernsteinAllStrict(lo, hi, -1);
    }

    // ======== Global: generic reference implementation (slow) ========
    public static bool GlobalGeneric(int a, int b, int vp, string path)
    {
        if (a < 0 || b < 0 || vp < 0 || a >= 60 || b >= 60 || vp >= 60 || a == b) return false;
        var (lo, hi) = Cert.BoxOfPath(path);
        var u = Geo.StdU(); var rr = Geo.StdR();
        var n = Geo.MovingN(u, a, b, 1);
        for (int v = 0; v < 60; v++)
        {
            var p = Geo.GapPoly(n, rr, Geo.V[vp], Geo.V[v]);
            if (!(-p).BernsteinAllStrict(lo, hi, -1)) return false;
        }
        return true;
    }

    // ======== Global: fast exact integer implementation ========
    // Precomputed per plug vertex: coefficients (a,b in Z[sqrt5]) of the monomials of 2*(Rhat(r) vp) components.
    // monomial order: 0:1, 1:r1, 2:r2, 3:r3, 4:r1^2, 5:r2^2, 6:r3^2, 7:r1r2, 8:r1r3, 9:r2r3
    static readonly int[][] monoExp = {
        new[]{0,0,0}, new[]{1,0,0}, new[]{0,1,0}, new[]{0,0,1}, new[]{2,0,0}, new[]{0,2,0}, new[]{0,0,2}, new[]{1,1,0}, new[]{1,0,1}, new[]{0,1,1} };
    static (BigInteger a, BigInteger b)[][][] rhatCoef; // [vp][k][mono]
    static void InitRhat()
    {
        if (rhatCoef != null) return;
        var res = new (BigInteger, BigInteger)[60][][];
        var rr = Geo.StdR();
        for (int vp = 0; vp < 60; vp++)
        {
            res[vp] = new (BigInteger, BigInteger)[3][];
            // Rhat * (2 vp) via Poly arithmetic (generic), then extract monomials
            var vpP = Geo.V[vp].Select(x => Poly.Const(x * 2)).ToArray();
            var rsq = rr[0] * rr[0] + rr[1] * rr[1] + rr[2] * rr[2];
            var rv = rr[0] * vpP[0] + rr[1] * vpP[1] + rr[2] * vpP[2];
            var cx = new[] { rr[1] * vpP[2] - rr[2] * vpP[1], rr[2] * vpP[0] - rr[0] * vpP[2], rr[0] * vpP[1] - rr[1] * vpP[0] };
            for (int k = 0; k < 3; k++)
            {
                var poly = (Poly.Const(1) - rsq) * vpP[k] + 2 * rr[k] * rv + 2 * cx[k];
                var arr = new (BigInteger, BigInteger)[10];
                int found = 0;
                foreach (var kv in poly.T)
                {
                    int m = -1;
                    for (int q = 0; q < 10; q++)
                        if (Poly.Exp(kv.Key, 2) == monoExp[q][0] && Poly.Exp(kv.Key, 3) == monoExp[q][1] && Poly.Exp(kv.Key, 4) == monoExp[q][2] && Poly.Exp(kv.Key, 0) == 0 && Poly.Exp(kv.Key, 1) == 0) m = q;
                    if (m < 0) throw new Exception("unexpected monomial in Rhat");
                    if (!kv.Value.D.IsOne) throw new Exception("non-integral");
                    arr[m] = (kv.Value.A, kv.Value.B); found++;
                }
                res[vp][k] = arr;
            }
        }
        rhatCoef = res;
    }
    static BigInteger Lcm(BigInteger a, BigInteger b) => a / BigInteger.GreatestCommonDivisor(a, b) * b;

    /// <summary>Exact test of the 60 gap polynomials (all Bernstein coefficients of p_v strictly positive) using integer Z[sqrt5] arithmetic.
    /// Everything is scaled by a common positive factor (documented in the code).</summary>
    public static bool GlobalFast(int a, int b, int vp, string path)
    {
        if (a < 0 || b < 0 || vp < 0 || a >= 60 || b >= 60 || vp >= 60 || a == b) return false;
        InitRhat();
        var (lo, hi) = Cert.BoxOfPath(path);
        // common denominators
        BigInteger Ds = 1, Dr = 1;
        for (int i = 0; i < 2; i++) { Ds = Lcm(Ds, lo[i].D); Ds = Lcm(Ds, hi[i].D); }
        for (int i = 2; i < 5; i++) { Dr = Lcm(Dr, lo[i].D); Dr = Lcm(Dr, hi[i].D); }
        // endpoints are rational (B=0)
        BigInteger Sl(int i) => lo[i].A * (Ds / lo[i].D);
        BigInteger Sh(int i) => hi[i].A * (Ds / hi[i].D);
        var sv = new[] { Sl(0), Sh(0) }; var tv = new[] { Sl(1), Sh(1) };   // s*Ds, t*Ds
        // n' = 2*Ds*n,  n = u x (vb-va), u=(s,t,1);  e2 = 2*(vb-va) in Z[sqrt5]
        var e = new (BigInteger a, BigInteger b)[3];
        for (int i = 0; i < 3; i++) e[i] = (Geo.V2[b][i].a - Geo.V2[a][i].a, Geo.V2[b][i].b - Geo.V2[a][i].b);
        // n'[k][i,j] as (a,b)
        var n = new (BigInteger a, BigInteger b)[3][,];
        for (int k = 0; k < 3; k++) n[k] = new (BigInteger, BigInteger)[2, 2];
        for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++)
            {
                BigInteger S = sv[i], T = tv[j];
                // n = (t e3 - 1*e2, 1*e1 - s e3, s e2 - t e1)   [u=(s,t,1)]
                n[0][i, j] = (T * e[2].a - Ds * e[1].a, T * e[2].b - Ds * e[1].b);
                n[1][i, j] = (Ds * e[0].a - S * e[2].a, Ds * e[0].b - S * e[2].b);
                n[2][i, j] = (S * e[1].a - T * e[0].a, S * e[1].b - T * e[0].b);
            }
        // r Bernstein 1-D coefficient arrays, degree 2, scaled by Lam = 2*Dr^2: monomial exponent 0,1,2 -> 3 coefs
        var Lr = new BigInteger[3]; var Hr = new BigInteger[3];
        for (int i = 0; i < 3; i++) { Lr[i] = lo[2 + i].A * (Dr / lo[2 + i].D); Hr[i] = hi[2 + i].A * (Dr / hi[2 + i].D); }
        var c1 = new BigInteger[3][][]; // [var][exp][idx]
        for (int i = 0; i < 3; i++)
        {
            c1[i] = new BigInteger[3][];
            c1[i][0] = new[] { 2 * Dr * Dr, 2 * Dr * Dr, 2 * Dr * Dr };
            c1[i][1] = new[] { 2 * Dr * Lr[i], Dr * (Lr[i] + Hr[i]), 2 * Dr * Hr[i] };
            c1[i][2] = new[] { 2 * Lr[i] * Lr[i], 2 * Lr[i] * Hr[i], 2 * Hr[i] * Hr[i] };
        }
        // M[mono][abc] with abc = a + 3b + 9c  (a<->r1, b<->r2, c<->r3)
        var M = new BigInteger[10][];
        for (int m = 0; m < 10; m++)
        {
            M[m] = new BigInteger[27];
            for (int ia = 0; ia < 3; ia++) for (int ib = 0; ib < 3; ib++) for (int ic = 0; ic < 3; ic++)
                        M[m][ia + 3 * ib + 9 * ic] = c1[0][monoExp[m][0]][ia] * c1[1][monoExp[m][1]][ib] * c1[2][monoExp[m][2]][ic];
        }
        // D'[abc] = M[1] + M[r1^2]+M[r2^2]+M[r3^2]  (monos 0,4,5,6)
        var Dp = new BigInteger[27];
        for (int q = 0; q < 27; q++) Dp[q] = M[0][q] + M[4][q] + M[5][q] + M[6][q];
        // W'_k[abc] = sum_mono coef(vp,k,mono) * M[mono][abc]   (Z[sqrt5] pairs)
        var W = new (BigInteger a, BigInteger b)[3][];
        for (int k = 0; k < 3; k++)
        {
            W[k] = new (BigInteger, BigInteger)[27];
            for (int q = 0; q < 27; q++)
            {
                BigInteger xa = 0, xb = 0;
                for (int m = 0; m < 10; m++)
                {
                    var cf = rhatCoef[vp][k][m];
                    if (cf.a.IsZero && cf.b.IsZero) continue;
                    xa += cf.a * M[m][q]; xb += cf.b * M[m][q];
                }
                W[k][q] = (xa, xb);
            }
        }
        // A'[ij][q] = sum_k n'_k[ij] * W'_k[q]   ((a+b s)(c+d s) = (ac+5bd) + (ad+bc) s)
        var A = new (BigInteger a, BigInteger b)[4][];
        for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++)
            {
                var arr = new (BigInteger, BigInteger)[27];
                for (int q = 0; q < 27; q++)
                {
                    BigInteger xa = 0, xb = 0;
                    for (int k = 0; k < 3; k++)
                    {
                        var nn = n[k][i, j]; var ww = W[k][q];
                        xa += nn.a * ww.a + 5 * nn.b * ww.b;
                        xb += nn.a * ww.b + nn.b * ww.a;
                    }
                    arr[q] = (xa, xb);
                }
                A[i * 2 + j] = arr;
            }
        // for each hole vertex v:  N'_v[ij] = sum_k n'_k[ij] * V2[v][k];  coefficient = A[ij][q] - N'_v[ij]*D'[q] must be >0
        for (int v = 0; v < 60; v++)
        {
            for (int ij = 0; ij < 4; ij++)
            {
                int i = ij / 2, j = ij % 2;
                BigInteger na = 0, nb = 0;
                for (int k = 0; k < 3; k++)
                {
                    var nn = n[k][i, j]; var vv = Geo.V2[v][k];
                    na += nn.a * vv.a + 5 * nn.b * vv.b;
                    nb += nn.a * vv.b + nn.b * vv.a;
                }
                for (int q = 0; q < 27; q++)
                {
                    var x = A[ij][q].a - na * Dp[q];
                    var y = A[ij][q].b - nb * Dp[q];
                    if (SignZ5(x, y) <= 0) return false;
                }
            }
        }
        return true;
    }
    /// <summary>Sign of x + y*sqrt5 for integers (paper sec. 5.1).</summary>
    public static int SignZ5(BigInteger x, BigInteger y)
    {
        int sx = x.Sign, sy = y.Sign;
        if (sy == 0) return sx;
        if (sx == 0) return sy;
        if (sx == sy) return sx;
        return sx * (x * x - 5 * y * y).Sign;
    }
}
