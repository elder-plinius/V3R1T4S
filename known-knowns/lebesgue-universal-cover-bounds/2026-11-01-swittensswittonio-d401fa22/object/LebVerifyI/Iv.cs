// Outward-rounded interval arithmetic on IEEE-754 binary64.
// Soundness rests only on: + - * / and Math.Sqrt are CORRECTLY ROUNDED (round-to-nearest-even) in IEEE-754 binary64, hence the exact
// result r of one operation on two doubles satisfies  BitDecrement(fl(r)) <= r <= BitIncrement(fl(r)).  Every operation below returns
// [Dn(fl(min)), Up(fl(max))] over the exact endpoint combinations, so the exact image of the operand intervals is contained.
// NaN endpoints propagate and make every later comparison false (callers phrase tests as "if (!(x.lo > 0)) fail").
using System;
using System.Runtime.CompilerServices;

namespace LebVerify
{
    public readonly struct Iv
    {
        public readonly double lo, hi;
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public Iv(double l, double h) { lo = l; hi = h; }
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv Pt(double x) => new Iv(x, x);        // exact double point
        // Up(x) = next double above x (== Math.BitIncrement for every finite x; +-inf/NaN give NaN or +-max (fail-closed side)); Dn(x) = -Up(-x).  Branch-free bit version, unit-tested against Math.BitIncrement/BitDecrement.
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static double Up(double x) { long b = BitConverter.DoubleToInt64Bits(x + 0.0); return BitConverter.Int64BitsToDouble(b + 1 + ((b >> 63) << 1)); }   // x+0.0 turns -0.0 into +0.0
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static double Dn(double x) => -Up(-x);
        public static double UpRef(double x) => Math.BitIncrement(x);
        public static double DnRef(double x) => Math.BitDecrement(x);

        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv operator +(Iv a, Iv b) => new Iv(Dn(a.lo + b.lo), Up(a.hi + b.hi));
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv operator -(Iv a, Iv b) => new Iv(Dn(a.lo - b.hi), Up(a.hi - b.lo));
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv operator -(Iv a) => new Iv(-a.hi, -a.lo);   // exact
        // min/max by comparisons (Math.Min/Max are slow): NaN is propagated explicitly through the sum test (a NaN or inf-inf operand gives a NaN interval => callers fail closed)
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        static Iv Hull4(double p1, double p2, double p3, double p4)
        {
            double chk = (p1 + p2) + (p3 + p4);
            if (chk != chk) return new Iv(double.NaN, double.NaN);
            double m1 = p1 < p2 ? p1 : p2, m2 = p3 < p4 ? p3 : p4, M1 = p1 > p2 ? p1 : p2, M2 = p3 > p4 ? p3 : p4;
            return new Iv(Dn(m1 < m2 ? m1 : m2), Up(M1 > M2 ? M1 : M2));
        }
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static Iv operator *(Iv a, Iv b) => Hull4(a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi);
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static Iv operator /(Iv a, Iv b)
        {
            if (!(b.lo > 0 || b.hi < 0)) return new Iv(double.NegativeInfinity, double.PositiveInfinity);   // divisor interval contains 0 (or NaN): no information
            return Hull4(a.lo / b.lo, a.lo / b.hi, a.hi / b.lo, a.hi / b.hi);
        }
        // exact point times exact point: the exact product lies in [Dn(fl(ab)), Up(fl(ab))]
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static Iv MulPt(double a, double b) { double p = a * b; return new Iv(Dn(p), Up(p)); }
        // multiplication by an exact power of two / exact doubling: result exactly representable (no overflow/underflow on our ranges) -> no widening needed
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public Iv Half() => new Iv(lo * 0.5, hi * 0.5);
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public Iv Twice() => new Iv(lo * 2.0, hi * 2.0);

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static Iv Sqr(Iv a)
        {
            if (a.lo >= 0) return new Iv(Dn(a.lo * a.lo), Up(a.hi * a.hi));
            if (a.hi <= 0) return new Iv(Dn(a.hi * a.hi), Up(a.lo * a.lo));
            return new Iv(0.0, SqrHi(a));
        }
        // upper endpoint of Sqr(a) only (identical to Sqr(a).hi, cheaper)
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static double SqrHi(Iv a) { double x = a.lo * a.lo, y = a.hi * a.hi; double m = x > y ? x : y; return Up(m + (x + y) * 0.0); }   // NaN-propagating max; (x+y)*0 = 0 for finite x,y
        // a - b where b is an exact point: both endpoints of Pt(b) coincide
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public static Iv Sqrt(Iv a)
        {
            if (!(a.hi >= 0)) return new Iv(double.NaN, double.NaN);
            double l = a.lo <= 0 ? 0.0 : Dn(Math.Sqrt(a.lo));
            return new Iv(l, Up(Math.Sqrt(a.hi)));
        }
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv Abs(Iv a) => a.lo >= 0 ? a : (a.hi <= 0 ? new Iv(-a.hi, -a.lo) : new Iv(0.0, Math.Max(-a.lo, a.hi)));
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv Max0(Iv a) => new Iv(Math.Max(a.lo, 0.0), Math.Max(a.hi, 0.0));
        [MethodImpl(MethodImplOptions.AggressiveInlining)] public static Iv Ratio(long p, long q) => Pt(p) / Pt(q);       // |p|,|q| < 2^53: both exact doubles
        public double Mid => 0.5 * lo + 0.5 * hi;                         // heuristic only (never used for certification)
        public override string ToString() => "[" + lo.ToString("R") + "," + hi.ToString("R") + "]";
    }

    // Interval sin/cos with an explicit Lagrange remainder:  sin x = sum_{k=0}^{n} (-1)^k x^(2k+1)/(2k+1)! + R,  |R| <= |x|^(2n+3)/(2n+3)!   (|f^(m)| <= 1)
    //                                                         cos x = sum_{k=0}^{n} (-1)^k x^(2k)/(2k)!     + R,  |R| <= |x|^(2n+2)/(2n+2)!
    // Interval Horner in y = x^2 encloses the polynomial over the whole operand interval; coefficients are the enclosures IvConsts.InvFact.
    public static class IvTrig
    {
        static Iv PowMag(Iv x, int e) { double m = Math.Max(Math.Abs(x.lo), Math.Abs(x.hi)); Iv mm = Iv.Pt(m), r = Iv.Pt(1.0); for (int i = 0; i < e; i++) r = r * mm; return r; }
        public static Iv Sin(Iv x, int n)
        {
            Iv y = Iv.Sqr(x);
            Iv acc = (n % 2 == 0 ? IvConsts.InvFact[2 * n + 1] : -IvConsts.InvFact[2 * n + 1]);
            for (int k = n - 1; k >= 0; k--) { Iv c = (k % 2 == 0 ? IvConsts.InvFact[2 * k + 1] : -IvConsts.InvFact[2 * k + 1]); acc = acc * y + c; }
            Iv rem = PowMag(x, 2 * n + 3) * IvConsts.InvFact[2 * n + 3];
            return x * acc + new Iv(-rem.hi, rem.hi);
        }
        public static Iv Cos(Iv x, int n)
        {
            Iv y = Iv.Sqr(x);
            Iv acc = (n % 2 == 0 ? IvConsts.InvFact[2 * n] : -IvConsts.InvFact[2 * n]);
            for (int k = n - 1; k >= 0; k--) { Iv c = (k % 2 == 0 ? IvConsts.InvFact[2 * k] : -IvConsts.InvFact[2 * k]); acc = acc * y + c; }
            Iv rem = PowMag(x, 2 * n + 2) * IvConsts.InvFact[2 * n + 2];
            return acc + new Iv(-rem.hi, rem.hi);
        }
    }
}
