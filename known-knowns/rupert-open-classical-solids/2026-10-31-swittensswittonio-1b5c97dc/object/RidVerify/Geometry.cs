using System.Numerics;
namespace RidVerify;

public sealed class Quat
{
    public readonly Q5[] c = new Q5[4]; // (scalar, i, j, k)
    public Quat(Q5 w, Q5 x, Q5 y, Q5 z) { c[0] = w; c[1] = x; c[2] = y; c[3] = z; }
    // paper eq. (quaternion-product): (a,A)(b,B) = (ab - A.B, aB + bA + A x B)
    public static Quat operator *(Quat p, Quat q)
    {
        var a = p.c[0]; var b = q.c[0];
        Q5[] A = { p.c[1], p.c[2], p.c[3] }, B = { q.c[1], q.c[2], q.c[3] };
        var w = a * b - (A[0] * B[0] + A[1] * B[1] + A[2] * B[2]);
        var x = a * B[0] + b * A[0] + (A[1] * B[2] - A[2] * B[1]);
        var y = a * B[1] + b * A[1] + (A[2] * B[0] - A[0] * B[2]);
        var z = a * B[2] + b * A[2] + (A[0] * B[1] - A[1] * B[0]);
        return new Quat(w, x, y, z);
    }
    public Quat Conj() => new Quat(c[0], -c[1], -c[2], -c[3]);
    public Q5 Norm2() => c[0] * c[0] + c[1] * c[1] + c[2] * c[2] + c[3] * c[3];
    public Quat Neg() => new Quat(-c[0], -c[1], -c[2], -c[3]);
    public bool Same(Quat o) { for (int i = 0; i < 4; i++) if (c[i] != o.c[i]) return false; return true; }
    public string Key() => string.Join("|", c.Select(x => x.ToString()));
    /// <summary>Rotation matrix action v -> q v q^{-1} for unit q (columns computed on basis vectors), as Q5 3-vectors.</summary>
    public Q5[] Rotate(Q5[] v)
    {
        var qv = this * new Quat(Q5.Zero, v[0], v[1], v[2]) * Conj();
        return new[] { qv.c[1], qv.c[2], qv.c[3] };
    }
}

public static class Geo
{
    public static readonly Q5 Phi = Q5.Phi;
    public static readonly Q5 Phi2 = Phi * Phi;
    public static readonly Q5 Phi3 = Phi2 * Phi;
    public static readonly Q5 PhiBar = Q5.One - Phi; // 1 - phi = -1/phi

    /// <summary>Total order used to number vertices: lexicographic over coordinates, each coordinate compared as the pair (rational part, sqrt5 part).</summary>
    public static int PairCmp(Q5 x, Q5 y)
    {
        // rational part A/D vs A'/D'
        int c = (x.A * y.D).CompareTo(y.A * x.D);
        if (c != 0) return c;
        return (x.B * y.D).CompareTo(y.B * x.D);
    }
    public static int VecCmp(Q5[] u, Q5[] v) { for (int i = 0; i < 3; i++) { int c = PairCmp(u[i], v[i]); if (c != 0) return c; } return 0; }

    public static Q5[][] BuildVertices(bool ascending = true)
    {
        var fams = new[] { new[] { Q5.One, Q5.One, Phi3 }, new[] { Phi2, Phi, Phi * 2 }, new[] { Q5.Int(2) + Phi, Q5.Zero, Phi2 } };
        var set = new Dictionary<string, Q5[]>();
        foreach (var f in fams)
            for (int cyc = 0; cyc < 3; cyc++)
            {
                var p = new[] { f[cyc % 3], f[(cyc + 1) % 3], f[(cyc + 2) % 3] };
                for (int m = 0; m < 8; m++)
                {
                    var v = new Q5[3];
                    for (int i = 0; i < 3; i++) v[i] = ((m >> i) & 1) == 1 ? -p[i] : p[i];
                    set[string.Join("|", v.Select(x => x.ToString()))] = v;
                }
            }
        var list = set.Values.ToList();
        list.Sort(VecCmp);
        if (!ascending) list.Reverse();
        return list.ToArray();
    }
    public static Q5[][] V = BuildVertices(Environment.GetEnvironmentVariable("RID_VDESC") != "1"); // RID_VDESC=1: label-sensitivity experiment only
    // doubled vertices as integer pairs (a,b): 2*coord = a + b*sqrt5
    public static (BigInteger a, BigInteger b)[][] V2 = V.Select(v => v.Select(x =>
    {
        var y = x * 2;
        if (!y.D.IsOne) throw new Exception("2*coordinate not in Z[sqrt5]");
        return (y.A, y.B);
    }).ToArray()).ToArray();

    /// <summary>The 120 unit icosians (appendix A), in a canonical generated order.</summary>
    public static List<Quat> BuildQ()
    {
        var res = new List<Quat>(); var seen = new HashSet<string>();
        void Add(Quat q) { if (seen.Add(q.Key())) res.Add(q); }
        var half = Q5.Rat(1, 2);
        for (int i = 0; i < 4; i++) foreach (var sg in new[] { 1, -1 })
            { var c = new Q5[] { Q5.Zero, Q5.Zero, Q5.Zero, Q5.Zero }; c[i] = Q5.Int(sg); Add(new Quat(c[0], c[1], c[2], c[3])); }
        for (int m = 0; m < 16; m++)
        {
            var c = new Q5[4]; for (int i = 0; i < 4; i++) c[i] = ((m >> i) & 1) == 1 ? -half : half;
            Add(new Quat(c[0], c[1], c[2], c[3]));
        }
        // even permutations of 1/2 (0, +-1, +-phi, +-(phi-1))
        var baseV = new[] { Q5.Zero, half, half * Phi, half * (Phi - Q5.One) };
        foreach (var perm in Permutations(4))
        {
            int inv = 0; for (int i = 0; i < 4; i++) for (int j = i + 1; j < 4; j++) if (perm[i] > perm[j]) inv++;
            if (inv % 2 != 0) continue;
            for (int m = 0; m < 16; m++)
            {
                var c = new Q5[4];
                for (int i = 0; i < 4; i++) { var b = baseV[perm[i]]; c[i] = ((m >> i) & 1) == 1 ? -b : b; }
                Add(new Quat(c[0], c[1], c[2], c[3]));
            }
        }
        return res;
    }
    static IEnumerable<int[]> Permutations(int n)
    {
        var a = Enumerable.Range(0, n).ToArray();
        IEnumerable<int[]> Rec(int k)
        {
            if (k == n) { yield return (int[])a.Clone(); yield break; }
            for (int i = k; i < n; i++) { (a[k], a[i]) = (a[i], a[k]); foreach (var r in Rec(k + 1)) yield return r; (a[k], a[i]) = (a[i], a[k]); }
        }
        return Rec(0);
    }
    public static int QuatCmp(Quat x, Quat y) { for (int i = 0; i < 4; i++) { int c = PairCmp(x.c[i], y.c[i]); if (c != 0) return c; } return 0; }
    /// <summary>One quaternion of each +-g pair: the one whose first nonzero coordinate is positive (paper). Ordered ascending by (pair-lexicographic) key.</summary>
    public static List<Quat> BuildQPlus(List<Quat> Q)
    {
        var res = new List<Quat>();
        foreach (var q in Q)
        {
            foreach (var x in q.c) { if (x.IsZero) continue; if (x.Sign() > 0) res.Add(q); break; }
        }
        res.Sort(QuatCmp);
        if (Environment.GetEnvironmentVariable("RID_QDESC") == "1") res.Reverse(); // label-sensitivity experiment only
        return res;
    }
    public static readonly List<Quat> Q = BuildQ();
    public static List<Quat> QPlus = BuildQPlus(Q);

    // ---- polynomial coordinates: 0:s 1:t 2:r1 3:r2 4:r3
    static Poly[] CrossP(Poly[] a, Poly[] b) => new[] { a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] };
    static Poly DotP(Poly[] a, Poly[] b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

    /// <summary>Fold linear form ell_g = -beta u.r - b.(u + u x r) written for a general (homogeneous) viewing vector u and rotation vector r (polys).</summary>
    public static Poly FoldEll(Quat g, Poly[] u, Poly[] r)
    {
        var uxr = CrossP(u, r);
        var beta = g.c[0];
        var res = (-beta) * DotP(u, r);
        for (int i = 0; i < 3; i++) res = res - g.c[i + 1] * (u[i] + uxr[i]);
        return res;
    }
    /// <summary>Number of inequalities of D: 0 viewing triangle; 1..12 rotation; 13..72 fold.</summary>
    public const int NumIneq = 73;
    public static Poly DomainIneqHomogeneous(int idx, Poly[] u, Poly[] r)
    {
        // returns q with q<=0 defining D, written homogeneously in u (triangle: degree 1; fold: degree 2; rotation: degree 0)
        if (idx == 0) return Phi * u[0] + Phi2 * u[1] - u[2];
        if (idx <= 12)
        {
            int k = idx - 1; int i = k / 4; int eps = ((k / 2) % 2 == 0) ? -1 : 1; int del = (k % 2 == 0) ? -1 : 1;
            var ri = r[i]; var rj = r[(i + 1) % 3];
            return Q5.Int(eps) * ri + ((Phi - Q5.One) * Q5.Int(del)) * rj - Poly.Const(Q5.Int(2) - Phi);
        }
        if (idx < NumIneq)
        {
            var g = QPlus[idx - 13];
            var ell = FoldEll(g, u, r);
            return ell * ell - DotP(u, u);
        }
        throw new ArgumentOutOfRangeException(nameof(idx));
    }
    public static Poly[] StdU() => new[] { Poly.Var(0), Poly.Var(1), Poly.Const(1) };
    public static Poly[] StdR() => new[] { Poly.Var(2), Poly.Var(3), Poly.Var(4) };
    public static Poly DomainIneq(int idx) => DomainIneqHomogeneous(idx, StdU(), StdR());

    /// <summary>Gap polynomial p_v = n . (Rhat(r) vp - d v), n given as polynomial 3-vector; Rhat(r) v = (1-r.r) v + 2 r (r.v) + 2 r x v ; d=1+r.r.</summary>
    public static Poly GapPoly(Poly[] n, Poly[] r, Q5[] vp, Q5[] v)
    {
        var rr = DotP(r, r);
        var vpP = vp.Select(Poly.Const).ToArray();
        var rv = DotP(r, vpP);
        var rxv = CrossP(r, vpP);
        var d = Poly.Const(1) + rr;
        Poly total = Poly.Const(0);
        for (int k = 0; k < 3; k++)
        {
            var rhat = (Poly.Const(1) - rr) * Poly.Const(vp[k]) + 2 * r[k] * rv + 2 * rxv[k];
            total = total + n[k] * (rhat - d * Poly.Const(v[k]));
        }
        return total;
    }
    /// <summary>Moving support direction n = sigma u x (vb - va) for u polys.</summary>
    public static Poly[] MovingN(Poly[] u, int a, int b, int sigma = 1)
    {
        var e = new Poly[3]; for (int i = 0; i < 3; i++) e[i] = Poly.Const(V[b][i] - V[a][i]);
        var n = CrossP(u, e);
        if (sigma < 0) n = n.Select(x => -x).ToArray();
        return n;
    }
}
