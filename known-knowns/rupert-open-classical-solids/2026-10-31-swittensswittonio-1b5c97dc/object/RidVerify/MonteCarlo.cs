namespace RidVerify;

/// <summary>Independent floating-point geometric sanity check (NOT part of the proof): sample random points of the boxes of eliminated records and confirm,
/// directly from the definition (convex hulls of the projected vertices, no polynomials, no Bernstein), that none is a strict fit lying in D.</summary>
public static class MonteCarlo
{
    static readonly double[][] Vd = Geo.V.Select(v => v.Select(x => x.ToDouble()).ToArray()).ToArray();
    static readonly double[][] Qd = Geo.QPlus.Select(q => q.c.Select(x => x.ToDouble()).ToArray()).ToArray();
    static readonly double PhiD = (1 + Math.Sqrt(5)) / 2;
    public static double IneqD(int idx, double s, double t, double[] r)
    {
        if (idx == 0) return PhiD * s + PhiD * PhiD * t - 1;
        if (idx <= 12) { int k = idx - 1; int i = k / 4; int eps = ((k / 2) % 2 == 0) ? -1 : 1; int del = (k % 2 == 0) ? -1 : 1; return eps * r[i] + (PhiD - 1) * del * r[(i + 1) % 3] - (2 - PhiD); }
        var g = Qd[idx - 13]; double[] u = { s, t, 1 };
        double ur = u[0] * r[0] + u[1] * r[1] + u[2] * r[2];
        double[] uxr = { u[1] * r[2] - u[2] * r[1], u[2] * r[0] - u[0] * r[2], u[0] * r[1] - u[1] * r[0] };
        double ell = -g[0] * ur; for (int i = 0; i < 3; i++) ell -= g[i + 1] * (u[i] + uxr[i]);
        return ell * ell - (u[0] * u[0] + u[1] * u[1] + u[2] * u[2]);
    }
    public static bool InD(double s, double t, double[] r)
    {
        for (int i = 0; i < Geo.NumIneq; i++) if (IneqD(i, s, t, r) > 1e-12) return false;
        return true;
    }
    static double Cross(double[] o, double[] a, double[] b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    static List<double[]> Hull(List<double[]> P)
    {
        var p = P.OrderBy(x => x[0]).ThenBy(x => x[1]).ToList(); var h = new List<double[]>();
        foreach (var q in p) { while (h.Count >= 2 && Cross(h[^2], h[^1], q) <= 0) h.RemoveAt(h.Count - 1); h.Add(q); }
        int lower = h.Count + 1;
        for (int i = p.Count - 2; i >= 0; i--) { var q = p[i]; while (h.Count >= lower && Cross(h[^2], h[^1], q) <= 0) h.RemoveAt(h.Count - 1); h.Add(q); }
        h.RemoveAt(h.Count - 1); return h;
    }
    /// <summary>Strict fit (plug shadow in the interior of the hole shadow) by float geometry; returns the margin-like quantity (min over hull edges and plug vertices of signed distance); fit iff > 1e-12.</summary>
    public static double FitSlack(double s, double t, double[] r)
    {
        var H = Hull(Vd.Select(v => new[] { v[0] - s * v[2], v[1] - t * v[2] }).ToList());
        double rr = r[0] * r[0] + r[1] * r[1] + r[2] * r[2], d = 1 + rr, slack = double.PositiveInfinity;
        foreach (var v in Vd)
        {
            double rv = r[0] * v[0] + r[1] * v[1] + r[2] * v[2];
            double[] w = new double[3];
            w[0] = ((1 - rr) * v[0] + 2 * r[0] * rv + 2 * (r[1] * v[2] - r[2] * v[1])) / d;
            w[1] = ((1 - rr) * v[1] + 2 * r[1] * rv + 2 * (r[2] * v[0] - r[0] * v[2])) / d;
            w[2] = ((1 - rr) * v[2] + 2 * r[2] * rv + 2 * (r[0] * v[1] - r[1] * v[0])) / d;
            var p = new[] { w[0] - s * w[2], w[1] - t * w[2] };
            for (int i = 0; i < H.Count; i++)
            {
                var a = H[i]; var b = H[(i + 1) % H.Count]; double len = Math.Sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]));
                slack = Math.Min(slack, Cross(a, b, p) / len);
            }
        }
        return slack;
    }
    public static (string msg, bool ok) Run(Cert.Parsed P, int perComponent, int pointsPerBox, int threads, Action<string> log)
    {
        var rng0 = new Random(4242); int fits = 0, tested = 0, domOk = 0, domTested = 0, domBad = 0; double minAbsSlack = double.PositiveInfinity;
        object lk = new();
        foreach (var comp in new[] { "Domain", "Global", "Local", "Exotic" })
        {
            var rs = P.Records.Where(r => r.Component == comp).OrderBy(_ => rng0.Next()).Take(perComponent).ToList();
            var seeds = rs.Select(_ => rng0.Next()).ToList();
            int cFits = 0, cTested = 0, cDomViol = 0, cDomTested = 0; double cMin = double.PositiveInfinity;
            Parallel.For(0, rs.Count, new ParallelOptions { MaxDegreeOfParallelism = threads }, i =>
            {
                var r = rs[i]; var rng = new Random(seeds[i]); var (lo, hi) = Cert.BoxOfPath(r.Path);
                double[] l = lo.Select(x => x.ToDouble()).ToArray(), h = hi.Select(x => x.ToDouble()).ToArray();
                for (int k = 0; k < pointsPerBox; k++)
                {
                    var x = new double[5]; for (int j = 0; j < 5; j++) x[j] = k == 0 ? (l[j] + h[j]) / 2 : l[j] + rng.NextDouble() * (h[j] - l[j]);
                    var rv = new[] { x[2], x[3], x[4] };
                    if (comp == "Domain")
                    {
                        double q = IneqD(r.Inequality, x[0], x[1], rv); lock (lk) { cDomTested++; if (q > -1e-9) cDomViol++; }
                        continue;
                    }
                    bool inD = InD(x[0], x[1], rv);
                    if (comp == "Exotic" && !inD) continue; // Exotic claims are scoped to D
                    double sl = FitSlack(x[0], x[1], rv);
                    lock (lk) { cTested++; if (sl > 1e-12) cFits++; cMin = Math.Min(cMin, Math.Abs(sl)); }
                }
            });
            if (comp == "Domain") { log($"MC {comp}: {cDomTested} sample points, {cDomViol} violate the named inequality as claimed ({(cDomViol == cDomTested ? "all" : "NOT all")})"); domTested = cDomTested; domOk = cDomViol; }
            else { log($"MC {comp}: {cTested} sample points (r != 0 almost surely), strict fits found: {cFits}, smallest |slack| {cMin:E3}"); tested += cTested; fits += cFits; minAbsSlack = Math.Min(minAbsSlack, cMin); }
        }
        return ($"{tested} geometric samples, {fits} strict fits; Domain samples violating the named inequality {domOk}/{domTested}", fits == 0 && domOk == domTested);
    }
}
