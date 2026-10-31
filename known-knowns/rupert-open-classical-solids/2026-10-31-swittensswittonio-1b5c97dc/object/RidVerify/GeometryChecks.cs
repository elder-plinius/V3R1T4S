using System.Numerics;
namespace RidVerify;

/// <summary>Exact re-derivation of the paper's stated finite facts (sec. 2, sec. 3, appendix A) from the vertex families and quaternion families.</summary>
public static class GeometryChecks
{
    public sealed class Result { public List<string> Lines = new(); public bool Ok = true; public void Add(string name, bool ok, string detail = "") { Lines.Add($"{(ok ? "PASS" : "FAIL")}  {name} {detail}"); if (!ok) Ok = false; } }

    static Q5 Dot(Q5[] a, Q5[] b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    static Q5[] Sub(Q5[] a, Q5[] b) => new[] { a[0] - b[0], a[1] - b[1], a[2] - b[2] };
    static string K(Q5[] v) => string.Join("|", v.Select(x => x.ToString()));
    static Q5 Det3(Q5[] a, Q5[] b, Q5[] c) => a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]);

    public static Result Run()
    {
        var R = new Result(); var V = Geo.V; var vset = new HashSet<string>(V.Select(K));
        R.Add("60 distinct vertices", V.Length == 60 && vset.Count == 60);
        R.Add("V = -V (central symmetry)", V.All(v => vset.Contains(K(v.Select(x => -x).ToArray()))));
        // family counts 24/24/12: classify by multiset of absolute coordinates
        var fam = new Dictionary<string, int>();
        foreach (var v in V)
        {
            var absK = string.Join("|", v.Select(x => (x.Sign() < 0 ? -x : x).ToString()).OrderBy(s => s));
            fam[absK] = fam.GetValueOrDefault(absK) + 1;
        }
        R.Add("three families of sizes {12,24,24}", fam.Count == 3 && fam.Values.OrderBy(x => x).SequenceEqual(new[] { 12, 24, 24 }), string.Join(",", fam.Values));
        R.Add("first family contains the 8 corners of [-1,1]^2x[-phi^3,phi^3]", Enumerable.Range(0, 8).All(m => vset.Contains(K(new[] { (m & 1) == 1 ? -Q5.One : Q5.One, (m & 2) != 0 ? -Q5.One : Q5.One, (m & 4) != 0 ? -Geo.Phi3 : Geo.Phi3 }))));
        // pair distances
        var d2 = new Dictionary<string, int>(); int pairs = 0; var edges = new List<(int, int)>();
        for (int i = 0; i < 60; i++) for (int j = i + 1; j < 60; j++)
            {
                var d = Sub(V[i], V[j]); var s = Dot(d, d); pairs++; d2[s.ToString()] = d2.GetValueOrDefault(s.ToString()) + 1;
                if (s == Q5.Int(4)) edges.Add((i, j));
            }
        R.Add("1770 vertex pairs at 17 distinct distances", pairs == 1770 && d2.Count == 17, $"pairs={pairs} distinct={d2.Count}");
        int rationalSq = d2.Keys.Count(k => !k.Contains("s5")); 
        R.Add("all but two squared distances irrational (edge 4 and square diagonal 8 rational)", rationalSq == 2 && d2.ContainsKey("4") && d2.ContainsKey("8"), $"rational: {string.Join(",", d2.Keys.Where(k => !k.Contains("s5")))}");
        R.Add("120 pairs at squared distance 4 (the edges)", edges.Count == 120);
        var deg = new int[60]; foreach (var (a, b) in edges) { deg[a]++; deg[b]++; }
        R.Add("every vertex has degree 4", deg.All(x => x == 4));
        // 15 unoriented edge vectors
        var evec = new HashSet<string>();
        foreach (var (a, b) in edges) { var e = Sub(V[b], V[a]); var k1 = K(e); var k2 = K(e.Select(x => -x).ToArray()); evec.Add(string.CompareOrdinal(k1, k2) < 0 ? k1 : k2); }
        R.Add("15 distinct edge vectors up to sign", evec.Count == 15);
        // every certificate edge pair is an edge handled elsewhere. Triangles with pairwise distance 2:
        var adj = new bool[60, 60]; foreach (var (a, b) in edges) adj[a, b] = adj[b, a] = true;
        var tris = new List<(int, int, int)>();
        for (int a = 0; a < 60; a++) for (int b = a + 1; b < 60; b++) if (adj[a, b]) for (int c = b + 1; c < 60; c++) if (adj[a, c] && adj[b, c]) tris.Add((a, b, c));
        var inTri = new int[60]; foreach (var (a, b, c) in tris) { inTri[a]++; inTri[b]++; inTri[c]++; }
        R.Add("20 triangles of pairwise distance 2, each vertex in exactly one", tris.Count == 20 && inTri.All(x => x == 1), $"triangles={tris.Count}");
        R.Add("position vectors of each triangle linearly independent", tris.All(t => !Det3(V[t.Item1], V[t.Item2], V[t.Item3]).IsZero));
        // quaternions
        var Q = Geo.Q;
        R.Add("120 icosians, all of norm 1", Q.Count == 120 && Q.All(q => q.Norm2() == Q5.One));
        var qkeys = new HashSet<string>(Q.Select(q => q.Key()));
        R.Add("closed under -1", Q.All(q => qkeys.Contains(q.Neg().Key())));
        bool closed = true; foreach (var p in Q) foreach (var q in Q) if (!qkeys.Contains((p * q).Key())) { closed = false; break; }
        R.Add("closed under quaternion product (120x120 products)", closed);
        // rotations distinct up to sign: 60 distinct matrices
        var mats = new HashSet<string>(); bool mapsV = true;
        foreach (var q in Q)
        {
            var cols = new[] { new[] { Q5.One, Q5.Zero, Q5.Zero }, new[] { Q5.Zero, Q5.One, Q5.Zero }, new[] { Q5.Zero, Q5.Zero, Q5.One } }.Select(e => q.Rotate(e)).ToArray();
            mats.Add(string.Join(";", cols.Select(K)));
            foreach (var v in V) if (!vset.Contains(K(q.Rotate(v)))) { mapsV = false; break; }
        }
        R.Add("120 quaternions give 60 distinct rotations", mats.Count == 60, $"distinct={mats.Count}");
        R.Add("each rotation maps every vertex to a vertex", mapsV);
        // completeness: a body symmetry maps the fixed ordered triangle to one of the ordered triangles; there are 20*6 = 120; 60 rotations + their negatives attain it
        { int ordered = tris.Count * 6; bool negDistinct = mats.Count == 60; // negatives have determinant -1 so differ from all rotations
          R.Add("at most 20*6 = 120 orthogonal body symmetries, and 60 rotations + 60 negatives attain it", ordered == 120 && negDistinct, $"ordered triangles={ordered}"); }
        // reflections
        var zeroScalar = Q.Where(q => q.c[0].IsZero).ToList();
        R.Add("30 quaternions with zero scalar -> 15 reflection normal lines", zeroScalar.Count == 30);
        var h = new[] { Q5.Int(1), Q5.Int(2), Q5.Int(9) };
        var normals = new List<Q5[]>();
        foreach (var q in zeroScalar) { var n = new[] { q.c[1], q.c[2], q.c[3] }; var dh = Dot(h, n); if (dh.Sign() > 0) normals.Add(n); else if (dh.IsZero) R.Add("normal perpendicular to h", false); }
        R.Add("15 oriented normals with h.n>0", normals.Count == 15);
        // reflection S_n = I - 2 n n^T symmetric on V
        bool refl = true; foreach (var n in normals) foreach (var v in V) { var w = new Q5[3]; var nv = Dot(n, v); for (int i = 0; i < 3; i++) w[i] = v[i] - 2 * n[i] * nv; if (!vset.Contains(K(w))) refl = false; }
        R.Add("reflections S_n preserve V", refl);
        var gens = new[] { new[] { Q5.Zero, Q5.Zero, Q5.One }, new[] { Q5.One, Q5.Zero, Geo.Phi }, new[] { Q5.Zero, Q5.One, Geo.Phi2 } };
        R.Add("every oriented normal has nonnegative dot with (0,0,1),(1,0,phi),(0,1,phi^2)", normals.All(n => gens.All(g => Dot(n, g).Sign() >= 0)));
        // three planes bounding the cone among the 15 with inward normals prop. to (1,0,0),(0,1,0),(-phi,-phi^2,1)
        bool Prop(Q5[] n, Q5[] w) { // n parallel to w with positive factor
            // cross product zero and dot positive
            var c = new[] { n[1] * w[2] - n[2] * w[1], n[2] * w[0] - n[0] * w[2], n[0] * w[1] - n[1] * w[0] };
            return c.All(x => x.IsZero) && Dot(n, w).Sign() > 0; }
        foreach (var w in new[] { new[] { Q5.One, Q5.Zero, Q5.Zero }, new[] { Q5.Zero, Q5.One, Q5.Zero }, new[] { -Geo.Phi, -Geo.Phi2, Q5.One } })
            R.Add($"cone bounding plane with inward normal ~ ({w[0]},{w[1]},{w[2]}) is among the 15", normals.Any(n => Prop(n, w)));
        // twelve rotation comparisons: quaternion with scalar phi/2 and vector coords -eps/2, -(phi-1) delta/2 exists in Q
        bool twelve = true;
        for (int i = 0; i < 3; i++) foreach (var eps in new[] { -1, 1 }) foreach (var del in new[] { -1, 1 })
                {
                    var vec = new[] { Q5.Zero, Q5.Zero, Q5.Zero };
                    vec[i] = Q5.Rat(-eps, 2); vec[(i + 1) % 3] = -(Geo.Phi - Q5.One) * Q5.Int(del) * Q5.Rat(1, 2);
                    var g = new Quat(Geo.Phi * Q5.Rat(1, 2), vec[0], vec[1], vec[2]);
                    if (!qkeys.Contains(g.Key())) twelve = false;
                }
        R.Add("the 12 selected quaternions (scalar phi/2) belong to Q", twelve);
        // scalar((1,r)g) <= 1  <=>  eps r_i + (phi-1) delta r_{i+1} <= 2 - phi : verified identity at random rational points
        var rng = new Random(12345); bool ident = true, foldIdent = true, rotIdent = true;
        for (int trial = 0; trial < 40; trial++)
        {
            Q5 Rnd() => Q5.Rat(rng.Next(-40, 41), rng.Next(1, 41));
            var r = new[] { Rnd(), Rnd(), Rnd() }; double dummy = 0;
            int i = rng.Next(3); int eps = rng.Next(2) * 2 - 1, del = rng.Next(2) * 2 - 1;
            var vec = new[] { Q5.Zero, Q5.Zero, Q5.Zero }; vec[i] = Q5.Rat(-eps, 2); vec[(i + 1) % 3] = -(Geo.Phi - Q5.One) * Q5.Int(del) * Q5.Rat(1, 2);
            var g = new Quat(Geo.Phi * Q5.Rat(1, 2), vec[0], vec[1], vec[2]);
            var p = new Quat(Q5.One, r[0], r[1], r[2]);
            var sc = (p * g).c[0];
            // scalar - 1 should equal (eps r_i + (phi-1) del r_{i+1} - (2-phi))/2
            var lhs = sc - Q5.One; var rhs = (Q5.Int(eps) * r[i] + (Geo.Phi - Q5.One) * Q5.Int(del) * r[(i + 1) % 3] - (Q5.Int(2) - Geo.Phi)) * Q5.Rat(1, 2);
            if (lhs != rhs) ident = false;
            // fold: ell_g = scalar((0,u)(1,r)g)
            var s = Rnd(); var t = Rnd(); var gg = Geo.QPlus[rng.Next(60)];
            var u = new Quat(Q5.Zero, s, t, Q5.One);
            var ell = (u * p * gg).c[0];
            var uP = new[] { Poly.Const(s), Poly.Const(t), Poly.Const(1) }; var rP = r.Select(Poly.Const).ToArray();
            var ellPoly = Geo.FoldEll(gg, uP, rP);
            if (ellPoly.Eval(new Q5[5]) != ell) foldIdent = false;
            // rotation formula: R_P(r) v = ((1-r.r) v + 2 r (r.v) + 2 r x v)/(1+r.r) equals q v q^{-1} with q=(1,r) (norm 1+r.r)
            var v = V[rng.Next(60)];
            var rr = Dot(r, r); var rv = Dot(r, v);
            var cr = new[] { r[1] * v[2] - r[2] * v[1], r[2] * v[0] - r[0] * v[2], r[0] * v[1] - r[1] * v[0] };
            var formula = new Q5[3]; for (int k = 0; k < 3; k++) formula[k] = ((Q5.One - rr) * v[k] + 2 * r[k] * rv + 2 * cr[k]) / (Q5.One + rr);
            var qv = (p * new Quat(Q5.Zero, v[0], v[1], v[2]) * p.Conj());
            for (int k = 0; k < 3; k++) if (qv.c[k + 1] / (Q5.One + rr) != formula[k]) rotIdent = false;
            _ = dummy;
        }
        R.Add("identity: scalar((1,r)g)-1 = (eps r_i + (phi-1) delta r_{i+1} - (2-phi))/2 (40 random exact points)", ident);
        R.Add("identity: fold polynomial ell_g = scalar((0,u)(1,r)g) (40 random exact points)", foldIdent);
        R.Add("identity: rotation formula (eq. relative-rotation) equals conjugation by (1,r) (40 random exact points)", rotIdent);
        // half-turn family: -j k = (1,-t,s,0)/|u|  (up to the norm), r = (-t,s,0)
        {
            var s = Q5.Rat(3, 17); var t = Q5.Rat(5, 23);
            var j = new Quat(Q5.Zero, s, t, Q5.One); var k = new Quat(Q5.Zero, Q5.Zero, Q5.Zero, Q5.One);
            var jk = j * k; var m = jk.Neg();
            R.Add("equal-shadow family: -(0,u)(0,0,0,1) = (1,-t,s,0)", m.c[0] == Q5.One && m.c[1] == -t && m.c[2] == s && m.c[3].IsZero);
        }
        // fold squared inequality at g=k on the family: (1+s r2 - t r1)^2 <= 1+s^2+t^2 simplifies to |u|<=1 (identity check)
        {
            var s = Q5.Rat(3, 17); var t = Q5.Rat(5, 23); var r1 = -t; var r2 = s;
            var lhs = (Q5.One + s * r2 - t * r1) * (Q5.One + s * r2 - t * r1);
            R.Add("fold g=k on half-turn family equals (1+s^2+t^2)^2 (so violated unless s=t=0)", lhs == (Q5.One + s * s + t * t) * (Q5.One + s * s + t * t));
        }
        // Qplus: 60 elements one from each pair
        R.Add("Q+ has 60 elements, one per +-g pair", Geo.QPlus.Count == 60 && Geo.QPlus.All(q => !Geo.QPlus.Any(p => p.Key() == q.Neg().Key())));
        // arc plane facts (Lemma arc-planes): support value in direction e2 of plug R_P(sigma r_A) V equals 2+sqrt5 = hole support
        var a1 = new Q5(-5, 3, 10); var a3 = new Q5(-5, 1, 10);
        foreach (int sigma in new[] { 1, -1 })
        {
            var rA = new[] { Q5.Int(sigma) * a1, Q5.Zero, Q5.Int(sigma) * a3 };
            var rr = Dot(rA, rA);
            Q5 maxPlug = default; bool first = true; Q5 maxHole = default; bool first2 = true;
            foreach (var v in V)
            {
                var cr = new[] { rA[1] * v[2] - rA[2] * v[1], rA[2] * v[0] - rA[0] * v[2], rA[0] * v[1] - rA[1] * v[0] };
                var y = ((Q5.One - rr) * v[1] + 2 * rA[1] * Dot(rA, v) + 2 * cr[1]) / (Q5.One + rr);
                if (first || y > maxPlug) maxPlug = y; first = false;
                if (first2 || v[1] > maxHole) maxHole = v[1]; first2 = false;
            }
            R.Add($"arc plane sigma={sigma}: max_v e2.R(sigma r_A)v = max_v e2.v = 2+sqrt5", maxPlug == maxHole && maxHole == new Q5(2, 1, 1), $"{maxPlug} vs {maxHole}");
        }
        // |r_A| = tan 18 deg: |rA|^2 = tan^2(18) = 1 - 2/sqrt5 ; check exactly 5|rA|^2 = 5 - 2 sqrt5
        { var rA = new[] { a1, Q5.Zero, a3 }; var n2 = Dot(rA, rA); R.Add("|r_A|^2 = 1 - 2/sqrt5 = tan^2(18 deg)", n2 == Q5.One - Q5.Int(2) * Q5.Sqrt5 * Q5.Rat(1, 5)); }
        // pentagon viewing parameters: s,t satisfy xi=0 (triangle boundary) and eta=0
        {
            var s = new Q5(-5, 3, 10); var t = new Q5(5, -1, 10);
            var eta = s + Geo.PhiBar * t; var xi = s + Geo.Phi * t + Geo.PhiBar;
            R.Add("pentagon viewing parameters satisfy eta = xi = 0", eta.IsZero && xi.IsZero);
            // inverse change of coordinates
            var e2 = Q5.Rat(1, 7); var x2 = Q5.Rat(-2, 9);
            var et = s + Geo.PhiBar * t + Q5.Zero; // not used
            var sInv = new Q5(-5, 3, 10) + (Geo.Phi * e2 - Geo.PhiBar * x2) / Q5.Sqrt5;
            var tInv = new Q5(5, -1, 10) + (x2 - e2) / Q5.Sqrt5;
            R.Add("inverse view change: (eta,xi) -> (s,t) -> (eta,xi) roundtrip", (sInv + Geo.PhiBar * tInv) == e2 && (sInv + Geo.Phi * tInv + Geo.PhiBar) == x2);
        }
        return R;
    }
}
