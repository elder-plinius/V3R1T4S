using System;
using System.IO;
namespace LebVerify
{
    // Emits random interval operations with their results (raw bit patterns) for exact verification by ivtest_check.py (Fractions / mpmath.iv).
    public static class IvTest
    {
        static string H(double d) => BitConverter.DoubleToInt64Bits(d).ToString("X16");
        static double RndD(Random r, double scale)
        {
            int mode = r.Next(6);
            double m = r.NextDouble() * 2 - 1;
            switch (mode) { case 0: return m * scale; case 1: return m * Math.Pow(10, r.Next(-12, 3)); case 2: return Math.Round(m * 8) / 8.0; case 3: return m * 1e-8; case 4: return (r.NextDouble()) * scale; default: return m * Math.Pow(2, r.Next(-60, 4)); }
        }
        static Iv RndIv(Random r, double scale)
        {
            double a = RndD(r, scale);
            int w = r.Next(5);
            if (w == 0) return Iv.Pt(a);
            double b = w == 1 ? Math.BitIncrement(a) : (w == 2 ? a + Math.Abs(a) * 1e-15 : RndD(r, scale));
            return new Iv(Math.Min(a, b), Math.Max(a, b));
        }
        public static int Run(string[] a)
        {
            int n = int.Parse(a[1]); string path = a[2]; var r = new Random(int.Parse(a.Length > 3 ? a[3] : "7"));
            using var w = new StreamWriter(path);
            for (int i = 0; i < n; i++)
            {
                Iv x = RndIv(r, 3.0), y = RndIv(r, 3.0);
                Iv s = x + y; w.WriteLine($"add {H(x.lo)} {H(x.hi)} {H(y.lo)} {H(y.hi)} {H(s.lo)} {H(s.hi)}");
                s = x - y; w.WriteLine($"sub {H(x.lo)} {H(x.hi)} {H(y.lo)} {H(y.hi)} {H(s.lo)} {H(s.hi)}");
                s = x * y; w.WriteLine($"mul {H(x.lo)} {H(x.hi)} {H(y.lo)} {H(y.hi)} {H(s.lo)} {H(s.hi)}");
                s = x / y; w.WriteLine($"div {H(x.lo)} {H(x.hi)} {H(y.lo)} {H(y.hi)} {H(s.lo)} {H(s.hi)}");
                s = Iv.Sqr(x); w.WriteLine($"sqr {H(x.lo)} {H(x.hi)} 0 0 {H(s.lo)} {H(s.hi)}");
                if (Iv.SqrHi(x) != s.hi) { Console.WriteLine("SqrHi MISMATCH"); return 1; }
                Iv p = Iv.Abs(x) + Iv.Pt(0.0); s = Iv.Sqrt(p); w.WriteLine($"sqrt {H(p.lo)} {H(p.hi)} 0 0 {H(s.lo)} {H(s.hi)}");
                s = Iv.Pt(x.lo) - x; Iv xx = Iv.Pt(x.lo); /* point op: Inside() style SqrHi */
                double t = Iv.Up(Iv.SqrHi(Iv.Pt(y.lo) - x) + Iv.SqrHi(Iv.Pt(y.hi) - y)); Iv e = Iv.Sqr(Iv.Pt(y.lo) - x) + Iv.Sqr(Iv.Pt(y.hi) - y);
                if (t != e.hi) { Console.WriteLine("Inside-style SqrHi sum MISMATCH"); return 1; }
                double c = r.NextDouble() * 1.3; Iv cx = r.Next(3) == 0 ? new Iv(c, Math.BitIncrement(c)) : Iv.Pt(c);
                Iv sn = IvTrig.Sin(cx, 10), cs = IvTrig.Cos(cx, 10);
                w.WriteLine($"sin10 {H(cx.lo)} {H(cx.hi)} 0 0 {H(sn.lo)} {H(sn.hi)}");
                w.WriteLine($"cos10 {H(cx.lo)} {H(cx.hi)} 0 0 {H(cs.lo)} {H(cs.hi)}");
                double c2 = r.NextDouble() * 0.7; Iv cx2 = Iv.Pt(c2); sn = IvTrig.Sin(cx2, 7);
                w.WriteLine($"sin7 {H(cx2.lo)} {H(cx2.hi)} 0 0 {H(sn.lo)} {H(sn.hi)}");
            }
            // Up/Dn vs Math.BitIncrement/BitDecrement on special and random doubles
            var sp = new double[] { 0.0, -0.0, double.Epsilon, -double.Epsilon, 1.0, -1.0, double.MaxValue, -double.MaxValue, 1e-310, -1e-310, 0.5, -0.5, 2.2250738585072014e-308, -2.2250738585072014e-308, Math.BitDecrement(1.0), Math.BitIncrement(-1.0) };
            long bad = 0; for (int i = 0; i < 2000000; i++) { double v = i < sp.Length ? sp[i] : BitConverter.Int64BitsToDouble(((long)r.Next() << 33) ^ ((long)r.Next() << 11) ^ r.Next()); if (double.IsNaN(v) || double.IsInfinity(v)) continue; if (BitConverter.DoubleToInt64Bits(Iv.Up(v)) != BitConverter.DoubleToInt64Bits(Math.BitIncrement(v)) || BitConverter.DoubleToInt64Bits(Iv.Dn(v)) != BitConverter.DoubleToInt64Bits(Math.BitDecrement(v))) { bad++; if (bad < 5) Console.WriteLine("UpDn mismatch " + v.ToString("R")); } }
            Console.WriteLine("Up/Dn vs Math.BitIncrement/BitDecrement mismatches: " + bad); if (bad != 0) return 1;
            // constants
            foreach (var (nm, v) in new (string, Iv)[] { ("pi", IvConsts.Pi), ("R5", IvConsts.R5), ("V3x0_0", IvConsts.V3x0[0]), ("V3x0_1", IvConsts.V3x0[1]), ("V5x0_1", IvConsts.V5x0[1]), ("V5x0_2", IvConsts.V5x0[2]), ("V5x0_3", IvConsts.V5x0[3]), ("V5y0_2", IvConsts.V5y0[2]), ("V5y0_3", IvConsts.V5y0[3]), ("V5x0_4", IvConsts.V5x0[4]), ("twopi5", (IvConsts.Pi.Twice()) / Iv.Pt(5.0)), ("e11", Iv.Ratio(1, 100000000000L)), ("e12", Ctx.E12) })
                w.WriteLine($"const:{nm} {H(v.lo)} {H(v.hi)} 0 0 0 0");
            return 0;
        }
    }
}
