using System;
using System.Globalization;
using System.IO;
using System.Text;
// Emits random interval operations with their results; code/iv_selftest.py re-checks containment with exact rationals (Fractions) / mpmath.
public static class SelfTest {
    static string R(double d) => d.ToString("R", CultureInfo.InvariantCulture);
    public static int Run(string[] a) {
        string path = a.Length > 1 ? a[1] : "iv_selftest.txt"; int N = a.Length > 2 ? int.Parse(a[2]) : 20000;
        var rnd = new Random(12345); var sb = new StringBuilder();
        Func<double> rv = () => (rnd.NextDouble() - 0.5) * Math.Pow(10, rnd.Next(-8, 2));
        Func<Iv> riv = () => { double x = rv(), y = rv(); if (rnd.Next(5) == 0) y = x; return new Iv(Math.Min(x, y), Math.Max(x, y)); };
        for (int i = 0; i < N; i++) {
            Iv x = riv(), y = riv();
            Iv s = x + y, d = x - y, m = x * y, q2 = Iv.Sqr(x);
            sb.AppendLine($"add {R(x.lo)} {R(x.hi)} {R(y.lo)} {R(y.hi)} {R(s.lo)} {R(s.hi)}");
            sb.AppendLine($"sub {R(x.lo)} {R(x.hi)} {R(y.lo)} {R(y.hi)} {R(d.lo)} {R(d.hi)}");
            sb.AppendLine($"mul {R(x.lo)} {R(x.hi)} {R(y.lo)} {R(y.hi)} {R(m.lo)} {R(m.hi)}");
            sb.AppendLine($"sqr {R(x.lo)} {R(x.hi)} 0 0 {R(q2.lo)} {R(q2.hi)}");
            var yp = new Iv(Math.Abs(y.lo) + 1e-3, Math.Abs(y.lo) + 1e-3 + Math.Abs(y.hi - y.lo));
            Iv dv = Iv.Div(x, yp);
            sb.AppendLine($"div {R(x.lo)} {R(x.hi)} {R(yp.lo)} {R(yp.hi)} {R(dv.lo)} {R(dv.hi)}");
            var xp = new Iv(Math.Abs(x.lo), Math.Abs(x.lo) + Math.Abs(x.hi - x.lo)); Iv sq = Iv.Sqrt(xp);
            sb.AppendLine($"sqrt {R(xp.lo)} {R(xp.hi)} 0 0 {R(sq.lo)} {R(sq.hi)}");
            double ang = rnd.NextDouble() * 1.5; Iv sn = Iv.SinPt(ang), cs = Iv.CosPt(ang);
            sb.AppendLine($"sin {R(ang)} {R(ang)} 0 0 {R(sn.lo)} {R(sn.hi)}");
            sb.AppendLine($"cos {R(ang)} {R(ang)} 0 0 {R(cs.lo)} {R(cs.hi)}");
            double a0 = rnd.NextDouble() * 1.2, a1 = a0 + rnd.NextDouble() * 0.2; var ai = new Iv(a0, a1);
            Iv sI = Iv.Sin(ai), cI = Iv.Cos(ai);
            sb.AppendLine($"sinI {R(a0)} {R(a1)} 0 0 {R(sI.lo)} {R(sI.hi)}");
            sb.AppendLine($"cosI {R(a0)} {R(a1)} 0 0 {R(cI.lo)} {R(cI.hi)}");
        }
        File.WriteAllText(path, sb.ToString()); Console.WriteLine($"wrote {path}"); return 0;
    }
}
