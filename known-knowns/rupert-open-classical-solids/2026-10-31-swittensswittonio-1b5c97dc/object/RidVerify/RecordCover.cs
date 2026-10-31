using System.Text.RegularExpressions;
namespace RidVerify;

/// <summary>Covered sets of the 38 covers, taken from the paper's text (tab:local-covers and sections 8-10), and exact box-inclusion tests.</summary>
public static class RecordCover
{
    public sealed class LocalRow { public Q5 S0, S1, T0, T1, Delta; }
    public static LocalRow[] LocalRows;
    static Q5 ParseTexFrac(string s)
    {
        s = s.Trim().Trim('$');
        return Q5.ParseRat(s);
    }
    /// <summary>Read the 30 rows of Table (local covers) from the paper's LaTeX source.</summary>
    public static void LoadLocalTable(string texPath)
    {
        var rows = new List<LocalRow>();
        var rx = new Regex(@"^\s*(\d+)\s*&\s*\$([^$]*)\$\s*&\s*\$([^$]*)\$\s*&\s*\$([^$]*)\$\s*&\s*\$([^$]*)\$\s*&\s*\$([^$]*)\$\s*&\s*(\d+)\s*\\\\");
        foreach (var line in File.ReadAllLines(texPath))
        {
            var m = rx.Match(line); if (!m.Success) continue;
            int idx = int.Parse(m.Groups[1].Value);
            if (idx != rows.Count) throw new Exception("table order");
            rows.Add(new LocalRow { S0 = ParseTexFrac(m.Groups[2].Value), S1 = ParseTexFrac(m.Groups[3].Value), T0 = ParseTexFrac(m.Groups[4].Value), T1 = ParseTexFrac(m.Groups[5].Value), Delta = ParseTexFrac(m.Groups[6].Value) });
        }
        if (rows.Count != 30) throw new Exception($"expected 30 local rows, got {rows.Count}");
        LocalRows = rows.ToArray();
    }
    static readonly Q5 Eps = Q5.Rat(1, 1024);
    static readonly Q5 A1 = new Q5(-5, 3, 10), A3 = new Q5(-5, 1, 10);
    static readonly Q5 EStar = new Q5(-2, 1, 1); // sqrt5 - 2

    // helpers on a box
    static (Q5 lo, Q5 hi) Lin(Q5 c0, (Q5 coef, int var)[] terms, Q5[] lo, Q5[] hi)
    {
        Q5 a = c0, b = c0;
        foreach (var (c, v) in terms) { if (c.Sign() >= 0) { a = a + c * lo[v]; b = b + c * hi[v]; } else { a = a + c * hi[v]; b = b + c * lo[v]; } }
        return (a, b);
    }
    static bool Within((Q5 lo, Q5 hi) r, Q5 a, Q5 b) => r.lo >= a && r.hi <= b;
    static bool RotWithin(Q5[] lo, Q5[] hi, Q5 d) { for (int i = 2; i < 5; i++) if (lo[i] < -d || hi[i] > d) return false; return true; }

    public static bool LocalContains(int k, Q5[] lo, Q5[] hi)
    {
        var row = LocalRows[k];
        var s0 = Q5.Max(Q5.Zero, row.S0 - Eps); var s1 = Q5.Min(Q5.Rat(2, 3), row.S1 + Eps);
        var t0 = Q5.Max(Q5.Zero, row.T0 - Eps); var t1 = Q5.Min(Q5.Rat(2, 5), row.T1 + Eps);
        return lo[0] >= s0 && hi[0] <= s1 && lo[1] >= t0 && hi[1] <= t1 && RotWithin(lo, hi, row.Delta);
    }
    /// <summary>Arc coordinates ranges over a box: e, v, theta, zeta1, zeta3 for plane sigma.</summary>
    static (Q5, Q5)[] ArcRanges(Q5[] lo, Q5[] hi, int sigma)
    {
        var two = Q5.Int(2);
        // e = (1-2s)/(2+s), decreasing in s
        Q5 E(Q5 s) => (Q5.One - two * s) / (two + s);
        var e = (E(hi[0]), E(lo[0]));
        // v = 5t/(2+s) with t>=0: min at (t lo, s hi), max at (t hi, s lo)  (t>=0 holds for all boxes in B0)
        if (lo[1].Sign() < 0) throw new Exception("t<0");
        var v = (Q5.Int(5) * lo[1] / (two + hi[0]), Q5.Int(5) * hi[1] / (two + lo[0]));
        var th = (lo[3], hi[3]);
        var sg = Q5.Int(sigma);
        // zeta1 = r1 - sigma*(a1 + a3*theta);  zeta3 = r3 - sigma*(a3 - a1*theta)
        var z1 = Lin(-(sg * A1), new[] { (Q5.One, 2), (-(sg * A3), 3) }, lo, hi);
        var z3 = Lin(-(sg * A3), new[] { (Q5.One, 4), (sg * A1, 3) }, lo, hi);
        return new[] { e, v, th, z1, z3 };
    }
    public static bool ExoticContains(string name, Q5[] lo, Q5[] hi)
    {
        switch (name)
        {
            case "square":
                return lo[0] >= Q5.Zero && hi[0] <= Q5.Rat(1, 8) && lo[1] >= Q5.Zero && hi[1] <= Q5.Rat(1, 8) && RotWithin(lo, hi, Q5.Rat(1, 8));
            case "pentagon":
                {
                    // eta = s + phibar t ; xi = s + phi t + phibar ; need |eta|<=1/32, xi>=-1/32, |r|<=1/16
                    var eta = Lin(Q5.Zero, new[] { (Q5.One, 0), (Geo.PhiBar, 1) }, lo, hi);
                    var xi = Lin(Geo.PhiBar, new[] { (Q5.One, 0), (Geo.Phi, 1) }, lo, hi);
                    return Within(eta, Q5.Rat(-1, 32), Q5.Rat(1, 32)) && xi.lo >= Q5.Rat(-1, 32) && RotWithin(lo, hi, Q5.Rat(1, 16));
                }
        }
        int sigma = name.EndsWith("+") ? 1 : name.EndsWith("-") ? -1 : throw new Exception("cover name " + name);
        var R = ArcRanges(lo, hi, sigma);
        var (e, v, th, z1, z3) = (R[0], R[1], R[2], R[3], R[4]);
        bool Offs(Q5 d) => Within(th, -d, d) && Within(z1, -d, d) && Within(z3, -d, d);
        if (name.StartsWith("arc"))
            return Within(e, Q5.Rat(3, 64), Q5.Rat(3, 16)) && v.Item1 >= Q5.Zero && v.Item2 <= Q5.Rat(1, 16) && Offs(Q5.Rat(1, 32));
        if (name.StartsWith("endpoint"))
            return Within(e, EStar - Q5.Rat(1, 16), EStar + Q5.Rat(1, 32)) && v.Item1 >= Q5.Zero && v.Item2 <= Q5.Rat(1, 16) && Offs(Q5.Rat(1, 32));
        if (name.StartsWith("crossing"))
            return Within(e, Q5.Rat(-1, 16), Q5.Rat(1, 16)) && v.Item1 >= Q5.Zero && v.Item2 <= Q5.Rat(5, 64) && Offs(Q5.Rat(1, 16));
        throw new Exception("cover name " + name);
    }

    public static bool Record(Record r)
    {
        var (lo, hi) = Cert.BoxOfPath(r.Path);
        if (r.Component == "Local")
        {
            if (!int.TryParse(r.Cover, out int k) || k < 0 || k > 29) return false;
            return LocalContains(k, lo, hi);
        }
        if (r.Component == "Exotic")
        {
            var names = new HashSet<string> { "square", "pentagon", "arc+", "arc-", "endpoint+", "endpoint-", "crossing+", "crossing-" };
            if (!names.Contains(r.Cover)) return false;
            return ExoticContains(r.Cover, lo, hi);
        }
        return false;
    }
}
