using System;
// Outward-rounded interval arithmetic on IEEE-754 binary64. Every arithmetic result (+ - * / sqrt) is computed in
// round-to-nearest and then widened by one ulp in each direction (Math.BitDecrement / BitIncrement). Since the nearest-rounded
// result differs from the exact real result by at most half an ulp, [BitDecrement(r), BitIncrement(r)] contains the exact result.
// Endpoints are never silently trusted: sin/cos are Taylor sums evaluated in this same arithmetic with an explicit remainder.
public struct Iv {
    public double lo, hi;
    public Iv(double l, double h) { lo = l; hi = h; }
    public static Iv P(double x) => new Iv(x, x);
    static double Dn(double x) => Math.BitDecrement(x);
    static double Up(double x) => Math.BitIncrement(x);
    public static Iv operator +(Iv a, Iv b) => new Iv(Dn(a.lo + b.lo), Up(a.hi + b.hi));
    public static Iv operator -(Iv a, Iv b) => new Iv(Dn(a.lo - b.hi), Up(a.hi - b.lo));
    public static Iv operator -(Iv a) => new Iv(-a.hi, -a.lo);
    public static Iv operator *(Iv a, Iv b) {
        double p1 = a.lo * b.lo, p2 = a.lo * b.hi, p3 = a.hi * b.lo, p4 = a.hi * b.hi;
        double l = Math.Min(Math.Min(p1, p2), Math.Min(p3, p4)), h = Math.Max(Math.Max(p1, p2), Math.Max(p3, p4));
        return new Iv(Dn(l), Up(h));
    }
    public static Iv Sqr(Iv a) {
        if (a.lo >= 0) return new Iv(Dn(a.lo * a.lo), Up(a.hi * a.hi));
        if (a.hi <= 0) return new Iv(Dn(a.hi * a.hi), Up(a.lo * a.lo));
        double m = Math.Max(-a.lo, a.hi); return new Iv(0, Up(m * m));
    }
    public static Iv Div(Iv a, Iv b) { // b strictly positive
        if (!(b.lo > 0)) throw new Exception("div by nonpositive");
        double q1 = a.lo / b.lo, q2 = a.lo / b.hi, q3 = a.hi / b.lo, q4 = a.hi / b.hi;
        double l = Math.Min(Math.Min(q1, q2), Math.Min(q3, q4)), h = Math.Max(Math.Max(q1, q2), Math.Max(q3, q4));
        return new Iv(Dn(l), Up(h));
    }
    public static Iv Sqrt(Iv a) {
        if (a.hi < 0) throw new Exception("sqrt of negative");
        double l = a.lo <= 0 ? 0 : Dn(Math.Sqrt(a.lo)); if (l < 0) l = 0;
        return new Iv(l, Up(Math.Sqrt(a.hi)));
    }
    public static Iv Half(Iv a) => new Iv(a.lo * 0.5, a.hi * 0.5); // exact (no underflow in our ranges; endpoints are >= 1e-300 or 0)
    public double MaxAbs => Math.Max(Math.Abs(lo), Math.Abs(hi));
    public double Mid => 0.5 * lo + 0.5 * hi;
    public static Iv Hull(Iv a, Iv b) => new Iv(Math.Min(a.lo, b.lo), Math.Max(a.hi, b.hi));
    public override string ToString() => $"[{lo:R},{hi:R}]";

    // Taylor enclosures of sin/cos at a POINT x (|x| <= 1.6), degree 2*N+1 / 2*N, remainder bounded by the next term (alternating, decreasing).
    const int NT = 24;
    public static Iv SinPt(double x) {
        Iv X = P(x), X2 = Sqr(X), term = X, sum = X;
        for (int k = 1; k <= NT; k++) {
            term = Div(term * X2, P((2.0 * k) * (2.0 * k + 1)));
            term = -term; sum = sum + term;
        }
        Iv next = Div(term * X2, P((2.0 * (NT + 1)) * (2.0 * (NT + 1) + 1)));
        double r = next.MaxAbs; return new Iv(Dn(sum.lo - r), Up(sum.hi + r));
    }
    public static Iv CosPt(double x) {
        Iv X = P(x), X2 = Sqr(X), term = P(1), sum = P(1);
        for (int k = 1; k <= NT; k++) {
            term = Div(term * X2, P((2.0 * k - 1) * (2.0 * k)));
            term = -term; sum = sum + term;
        }
        Iv next = Div(term * X2, P((2.0 * (NT + 1) - 1) * (2.0 * (NT + 1))));
        double r = next.MaxAbs; return new Iv(Dn(sum.lo - r), Up(sum.hi + r));
    }
    // monotone ranges: a subset of [0, 1.5]: sin increasing, cos decreasing
    public static Iv Sin(Iv a) { if (a.lo < 0 || a.hi > 1.5) throw new Exception("sin range"); return new Iv(SinPt(a.lo).lo, SinPt(a.hi).hi); }
    public static Iv Cos(Iv a) { if (a.lo < 0 || a.hi > 1.5) throw new Exception("cos range"); return new Iv(CosPt(a.hi).lo, CosPt(a.lo).hi); }
}
