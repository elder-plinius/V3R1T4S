using System.Numerics;
namespace RidVerify;

/// <summary>Exact strict-fit test of paper eq. (exact-point-fit-condition) for an arbitrary centrally symmetric polytope given by vertices (Q5) and edges.
/// Hole = P, plug = R_P(r) P (centred); viewing vector u=(s,t,1). Fit iff for every candidate n=+-u x (v_b - v_a) with n != 0:
///   max_v n . Rhat(r) v  <  d * max_v n . v ,   d = 1 + r.r  (strict).</summary>
public static class FitTest
{
    public static List<(int, int)> EdgesAtSquaredDistance(Q5[][] V, Q5 d2)
    {
        var l = new List<(int, int)>();
        for (int i = 0; i < V.Length; i++) for (int j = i + 1; j < V.Length; j++)
            {
                Q5 s = Q5.Zero; for (int k = 0; k < 3; k++) { var x = V[i][k] - V[j][k]; s = s + x * x; }
                if (s == d2) l.Add((i, j));
            }
        return l;
    }
    static Q5[] Cross(Q5[] a, Q5[] b) => new[] { a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] };
    static Q5 Dot(Q5[] a, Q5[] b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    public static Q5[] RhatV(Q5[] r, Q5[] v)
    {
        var rr = Dot(r, r); var rv = Dot(r, v); var cr = Cross(r, v);
        var res = new Q5[3]; for (int k = 0; k < 3; k++) res[k] = (Q5.One - rr) * v[k] + 2 * r[k] * rv + 2 * cr[k];
        return res;
    }
    /// <summary>Returns (isFit, worst score). score = maxPlug - d*maxHole per candidate; fit requires all scores strictly negative.</summary>
    public static (bool fit, Q5 worst, int candidates) Exact(Q5[][] V, List<(int, int)> edges, Q5 s, Q5 t, Q5[] r)
    {
        var u = new[] { s, t, Q5.One };
        var d = Q5.One + Dot(r, r);
        var RV = V.Select(v => RhatV(r, v)).ToArray();
        bool fit = true; Q5 worst = default; bool any = false; int cands = 0;
        foreach (var (a, b) in edges)
        {
            var e = new[] { V[b][0] - V[a][0], V[b][1] - V[a][1], V[b][2] - V[a][2] };
            var n0 = Cross(u, e);
            if (n0.All(x => x.IsZero)) continue;
            foreach (int sg in new[] { 1, -1 })
            {
                var n = n0.Select(x => x * sg).ToArray(); cands++;
                Q5 mp = Dot(n, RV[0]), mh = Dot(n, V[0]);
                for (int i = 1; i < V.Length; i++) { var x = Dot(n, RV[i]); if (x > mp) mp = x; var y = Dot(n, V[i]); if (y > mh) mh = y; }
                var score = mp - d * mh;
                if (!any || score > worst) { worst = score; any = true; }
                if (score.Sign() >= 0) fit = false;
            }
        }
        return (fit, worst, cands);
    }
    // floating-point version used only to LOCATE a candidate passage (never for certification)
    public static double ScoreD(double[][] V, List<(int, int)> edges, double s, double t, double[] r)
    {
        double rr = r[0] * r[0] + r[1] * r[1] + r[2] * r[2]; double d = 1 + rr;
        var RV = V.Select(v =>
        {
            double rv = r[0] * v[0] + r[1] * v[1] + r[2] * v[2];
            return new[] { ((1 - rr) * v[0] + 2 * r[0] * rv + 2 * (r[1] * v[2] - r[2] * v[1])) / d, ((1 - rr) * v[1] + 2 * r[1] * rv + 2 * (r[2] * v[0] - r[0] * v[2])) / d, ((1 - rr) * v[2] + 2 * r[2] * rv + 2 * (r[0] * v[1] - r[1] * v[0])) / d };
        }).ToArray();
        double worst = double.NegativeInfinity;
        foreach (var (a, b) in edges)
        {
            double[] e = { V[b][0] - V[a][0], V[b][1] - V[a][1], V[b][2] - V[a][2] };
            double[] n = { t * e[2] - e[1], e[0] - s * e[2], s * e[1] - t * e[0] };
            double nn = Math.Sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]); if (nn < 1e-12) continue;
            for (int sg = -1; sg <= 1; sg += 2)
            {
                double mp = double.NegativeInfinity, mh = double.NegativeInfinity;
                for (int i = 0; i < V.Length; i++)
                {
                    mp = Math.Max(mp, sg * (n[0] * RV[i][0] + n[1] * RV[i][1] + n[2] * RV[i][2]));
                    mh = Math.Max(mh, sg * (n[0] * V[i][0] + n[1] * V[i][1] + n[2] * V[i][2]));
                }
                worst = Math.Max(worst, (mp - mh) / nn);
            }
        }
        return worst;
    }
    public static string RunCubeKnownPositive(Action<string> log)
    {
        // cube [-1,1]^3
        var V = new List<Q5[]>(); for (int m = 0; m < 8; m++) V.Add(new[] { (m & 1) == 1 ? Q5.Int(-1) : Q5.One, (m & 2) != 0 ? Q5.Int(-1) : Q5.One, (m & 4) != 0 ? Q5.Int(-1) : Q5.One });
        var Va = V.ToArray(); var edges = EdgesAtSquaredDistance(Va, Q5.Int(4));
        log($"cube: {Va.Length} vertices, {edges.Count} edges (expected 8, 12)");
        var Vd = Va.Select(v => v.Select(x => x.ToDouble()).ToArray()).ToArray();
        var rng = new Random(2025);
        double best = double.PositiveInfinity; double bs = 0, bt = 0; double[] br = null;
        for (int it = 0; it < 400000; it++)
        {
            double s = rng.NextDouble() * 1.5, t = rng.NextDouble() * 1.5; var r = new[] { rng.NextDouble() * 2 - 1, rng.NextDouble() * 2 - 1, rng.NextDouble() * 2 - 1 };
            double sc = ScoreD(Vd, edges, s, t, r);
            if (sc < best) { best = sc; bs = s; bt = t; br = r; }
        }
        // local refinement (hill climb in floats)
        double step = 0.05;
        for (int it = 0; it < 20000 && step > 1e-9; it++)
        {
            double s = bs + (rng.NextDouble() - .5) * step, t = bt + (rng.NextDouble() - .5) * step; var r = br.Select(x => x + (rng.NextDouble() - .5) * step).ToArray();
            double sc = ScoreD(Vd, edges, s, t, r);
            if (sc < best) { best = sc; bs = s; bt = t; br = r; } else if (it % 200 == 199) step *= 0.7;
        }
        log($"float search: best normalised worst score {best:G6} at s={bs:G6} t={bt:G6} r=({br[0]:G6},{br[1]:G6},{br[2]:G6})");
        // rationalise to denominator 4096 and certify exactly
        Q5 Rt(double x) => Q5.Rat((long)Math.Round(x * 4096), 4096);
        var s0 = Rt(bs); var t0 = Rt(bt); var r0 = br.Select(Rt).ToArray();
        var (fit, worst, c) = Exact(Va, edges, s0, t0, r0);
        { // margin (ratio) over candidate directions: max_n maxPlug/(d maxHole) must lie in [2*sqrt2/3, 1) for a genuine cube passage (Nieuwland bound 3*sqrt2/4)
          var u = new[] { s0, t0, Q5.One }; var dd = Q5.One + Dot(r0, r0); var RV = Va.Select(v => RhatV(r0, v)).ToArray(); double mr = 0;
          foreach (var (a, b) in edges) { var e = new[] { Va[b][0] - Va[a][0], Va[b][1] - Va[a][1], Va[b][2] - Va[a][2] }; var n0 = Cross(u, e); if (n0.All(x => x.IsZero)) continue;
            foreach (int sg in new[] { 1, -1 }) { var n = n0.Select(x => x * sg).ToArray(); Q5 mp = Dot(n, RV[0]), mh = Dot(n, Va[0]); for (int i = 1; i < Va.Length; i++) { var x = Dot(n, RV[i]); if (x > mp) mp = x; var y = Dot(n, Va[i]); if (y > mh) mh = y; } mr = Math.Max(mr, (mp / (dd * mh)).ToDouble()); } }
          log($"margin over the candidate directions (max ratio plug/hole support) = {mr:G6}; Nieuwland optimum for the cube is 2*sqrt2/3 = {2 * Math.Sqrt(2) / 3:G6}, so a genuine passage has margin in [0.9428, 1)"); }
        log($"EXACT test at s={s0} t={t0} r=({r0[0]},{r0[1]},{r0[2]}): candidates={c}, worst score (maxPlug - d*maxHole) = {worst} (~{worst.ToDouble():G6}); strict fit = {fit}");
        // negative controls with the same machinery
        var (fit2, w2, _) = Exact(Va, edges, s0, t0, new[] { Q5.Zero, Q5.Zero, Q5.Zero });
        log($"control aligned (r=0) at same view: strict fit = {fit2} (worst score {w2}) [expected false: scores are all 0]");
        var (fit3, w3, _) = Exact(Va, edges, Q5.Zero, Q5.Zero, new[] { Q5.Zero, Q5.Zero, Q5.Zero });
        log($"control aligned cube viewed along an axis: strict fit = {fit3} (worst {w3}) [expected false]");
        var (fit4, w4, _) = Exact(Va, edges, s0, t0, new[] { r0[0] + Q5.Rat(1, 2), r0[1], r0[2] });
        log($"control perturbed rotation r1+1/2: strict fit = {fit4} (worst {w4})");
        return fit && !fit2 && !fit3 ? "PASS" : "FAIL";
    }
}
