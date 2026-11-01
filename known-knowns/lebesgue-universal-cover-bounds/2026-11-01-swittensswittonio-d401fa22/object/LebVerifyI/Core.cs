// Leaf-bound engine, INTERVAL MODE.  Written from the definitions (paper arXiv:2608.30538 Lemma 4.7, Prop 4.9, Def 5.6).
//
// Rigour model: every quantity that is CERTIFIED is computed with the outward-rounded Iv type (Iv.cs).  Witness points are exact doubles
// (pairs px,py).  Candidate points are produced by ordinary double arithmetic / library trig (heuristic selectors only) and are then
// CERTIFIED to lie in their body: sup over the interval corner enclosures of the squared distance (Iv upper bound) <= lower bound of rUse^2;
// an undecided test is a failure of that point (it is dropped).  The polygon built from the points is certified counter-clockwise about the
// origin by interval cross products (lo > 0), and its area lower bound is the lower end of the interval shoelace sum.  No floating-point error
// theorem is used anywhere.
using System;
using System.Runtime.CompilerServices;

namespace LebVerify
{
    public sealed class Ctx
    {
        public readonly int N;                      // number of base support directions (instance; several tiers with different N are used)
        double[] Ux, Uy;                            // direction table (need only be roughly unit; |u|^2-1 checked at table construction)
        double[] RingX, RingY, RingD;               // cached witness points of D (centre 0, radius 0.5) : constant per Ctx
        public const double RefTol = 1e-9;         // support-excess tolerance for adaptive edge refinement
        public double RefMinLen = 0.01;      // only edges at least this long are refined
        const int MAXP = 1 << 14;

        // final witness polygon (counter-clockwise by construction, verified in Finish)
        public double[] Px = new double[MAXP], Py = new double[MAXP]; public byte[] Pt = new byte[MAXP]; public int Cnt;
        public int FallbackDirs, Refined;

        // registered bodies
        sealed class Body { public double[] Vx = new double[8], Vy = new double[8], Cx = new double[64], Cy = new double[64]; public Iv[] IX = new Iv[8], IY = new Iv[8]; public int N, Nc; public double R2, RArc; public byte Tag; public bool Ring; }
        readonly Body[] bodies = NewBodies(); int nb;
        static Body[] NewBodies() { var b = new Body[4]; for (int i = 0; i < 4; i++) { b[i] = new Body(); } return b; }

        static readonly System.Collections.Generic.Dictionary<int, (double[], double[])> tables = new System.Collections.Generic.Dictionary<int, (double[], double[])>();
        static (double[], double[]) Table(int n)
        {
            lock (tables)
            {
                if (tables.TryGetValue(n, out var t)) return t;
                var ux = new double[n]; var uy = new double[n];
                for (int i = 0; i < n; i++)
                {
                    double a = 2.0 * Math.PI * i / n;
                    ux[i] = Math.Cos(a); uy[i] = Math.Sin(a);
                    // library Math.Cos/Sin: heuristic direction table only; no value from it is trusted (every point built from it is re-certified by Iv tests)
                }
                tables[n] = (ux, uy); return (ux, uy);
            }
        }

        public Ctx(int n)
        {
            N = n; (Ux, Uy) = Table(n);
            double rUseD = (Iv.Pt(0.5) - E12).lo, rr = rUseD - M2;      // ring radius (heuristic construction); certified below with Iv
            double rr2 = Iv.Sqr(Iv.Pt(rUseD)).lo;
            RingX = new double[n]; RingY = new double[n]; RingD = new double[n];
            for (int i = 0; i < n; i++)
            {
                RingX[i] = rr * Ux[i]; RingY[i] = rr * Uy[i]; RingD[i] = RingX[i] * Ux[i] + RingY[i] * Uy[i];
                double s = Iv.Up(Iv.SqrHi(Iv.Pt(RingX[i])) + Iv.SqrHi(Iv.Pt(RingY[i])));     // centre of D is exactly (0,0)
                if (!(s <= rr2)) throw new Exception("ring point not certified inside D");   // fail closed
            }
        }

        // A body is  K(V,r) = intersection_j Disc(V_j, r)  with INTERVAL corners V_j (enclosures) and interval radius r.  Witness points are tested against
        // rUse = lower end of (r - M1) : a point is accepted only if the Iv UPPER bound of |p-V_j|^2 is <= (rUse)^2 rounded down, for every corner j and every
        // position of V_j inside its enclosure.  Candidate points are constructed on radius rArc = rUse - M2 (plain doubles, heuristic).
        public static readonly Iv E12 = Iv.Ratio(1, 1000000000000L);
        public const double M2 = 1e-12;   // heuristic construction margin only (not used for certification)

        public void Reset() { nb = 0; FallbackDirs = 0; Refined = 0; Cnt = 0; }

        // Register the body intersection_j Disc(V_j, r) (n discs, equal radius).  n=1 is a plain disc.
        public void AddDiscIntersection(Iv[] vx, Iv[] vy, int n, Iv r, byte tag)
        {
            double rUse = (r - E12).lo; if (!(rUse > 0)) return;
            double rArc = rUse - M2;
            if (!(rArc > 1e-9)) return;
            var B = bodies[nb]; B.N = n; B.R2 = Iv.Sqr(Iv.Pt(rUse)).lo; B.RArc = rArc; B.Tag = tag; B.Nc = 0;
            for (int j = 0; j < n; j++) { B.IX[j] = vx[j]; B.IY[j] = vy[j]; B.Vx[j] = vx[j].Mid; B.Vy[j] = vy[j].Mid; }
            var vxm = B.Vx; var vym = B.Vy;
            B.Ring = n == 1 && vx[0].lo == 0.0 && vx[0].hi == 0.0 && vy[0].lo == 0.0 && vy[0].hi == 0.0 && r.lo == 0.5 && r.hi == 0.5;
            double rc2 = rArc * rArc;
            for (int j = 0; j < n; j++)
                for (int k = j + 1; k < n; k++)
                {
                    double dx = vxm[k] - vxm[j], dy = vym[k] - vym[j];
                    double d2 = dx * dx + dy * dy;
                    if (d2 >= 4.0 * rc2 || d2 <= 0) continue;
                    double h = Math.Sqrt(rc2 - 0.25 * d2);
                    double inv = 1.0 / Math.Sqrt(d2);
                    double mx = 0.5 * (vxm[j] + vxm[k]), my = 0.5 * (vym[j] + vym[k]);
                    double qx = -dy * inv * h, qy = dx * inv * h;
                    for (int s = -1; s <= 1; s += 2)
                    {
                        double px = mx + s * qx, py = my + s * qy;
                        if (Inside(px, py, B)) { B.Cx[B.Nc] = px; B.Cy[B.Nc] = py; B.Nc++; }
                    }
                }
            nb++;
        }

        // HEURISTIC candidate support point of body B in direction u: V_jm + RArc u with jm = argmin_j V_j.u (plain doubles; NOT certified here).
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        static void Cand(Body B, double ux, double uy, out double px, out double py, out double dot)
        {
            int n = B.N; var vx = B.Vx; var vy = B.Vy;
            int jm = 0; double best = vx[0] * ux + vy[0] * uy;
            for (int j = 1; j < n; j++) { double t = vx[j] * ux + vy[j] * uy; if (t < best) { best = t; jm = j; } }
            px = vx[jm] + B.RArc * ux; py = vy[jm] + B.RArc * uy; dot = px * ux + py * uy;
        }
        // best of the body's precomputed corner points (circle-circle intersections); each was Iv-certified when registered
        static void Fallback(Body B, double ux, double uy, out double px, out double py, out double dot)
        {
            px = py = 0; dot = double.NegativeInfinity;
            for (int c = 0; c < B.Nc; c++) { double t = B.Cx[c] * ux + B.Cy[c] * uy; if (t > dot) { dot = t; px = B.Cx[c]; py = B.Cy[c]; } }
        }

        readonly double[] cpx = new double[4], cpy = new double[4], cdt = new double[4]; readonly bool[] ccert = new bool[4];
        // Support point of the union of registered bodies in direction u, CERTIFIED: heuristic candidates per body are ranked by dot product; the winner is
        // accepted only after the Iv membership test (or if it is an Iv-certified cached point); a failing winner is replaced by that body's certified corner point and the
        // ranking is repeated.  Ring (disc D) points for base direction i come from the table certified at construction.
        bool SupportAll(double ux, double uy, int dirIdx, out double px, out double py, out byte tag)
        {
            px = py = 0; tag = 255;
            for (int b = 0; b < nb; b++)
            {
                var B = bodies[b];
                if (B.Ring && dirIdx >= 0) { cpx[b] = RingX[dirIdx]; cpy[b] = RingY[dirIdx]; cdt[b] = RingD[dirIdx]; ccert[b] = true; }
                else { Cand(B, ux, uy, out cpx[b], out cpy[b], out cdt[b]); ccert[b] = false; }
            }
            while (true)
            {
                int bb = -1; double best = double.NegativeInfinity;
                for (int b = 0; b < nb; b++) if (cdt[b] > best) { best = cdt[b]; bb = b; }
                if (bb < 0) return false;
                var B = bodies[bb];
                if (ccert[bb] || Inside(cpx[bb], cpy[bb], B)) { px = cpx[bb]; py = cpy[bb]; tag = B.Tag; return true; }
                FallbackDirs++;
                Fallback(B, ux, uy, out cpx[bb], out cpy[bb], out cdt[bb]); ccert[bb] = true;
            }
        }

        // CERTIFIED membership: for every corner m, the Iv upper bound of (px-Vx_m)^2 + (py-Vy_m)^2 must be <= R2 (= lower bound of rUse^2).
        // px,py are exact doubles; V_m are interval enclosures.  Undecided (NaN or bound exceeds R2) => false.
        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        static bool Inside(double px, double py, Body B)
        {
            int n = B.N; double r2 = B.R2; var X = B.IX; var Y = B.IY; Iv P = Iv.Pt(px), Q = Iv.Pt(py);
            for (int m = 0; m < n; m++)
            {
                double s = Iv.Up(Iv.SqrHi(P - X[m]) + Iv.SqrHi(Q - Y[m]));
                if (!(s <= r2)) return false;
            }
            return true;
        }

        void Push(double x, double y, byte t) { if (Cnt >= MAXP) throw new Exception("witness overflow"); Px[Cnt] = x; Py[Cnt] = y; Pt[Cnt] = t; Cnt++; }

        // adaptive refinement of a long edge p->q (exclusive of both): insert the support point in the edge's outward normal if it sticks out
        void Refine(double ax, double ay, double bx, double by, int depth)
        {
            double ex = bx - ax, ey = by - ay; double len = Math.Sqrt(ex * ex + ey * ey);
            if (len < RefMinLen || depth > 30) return;
            double nx = ey / len, ny = -ex / len;
            if (!SupportAll(nx, ny, -1, out double sx, out double sy, out byte st)) return;
            if (sx * nx + sy * ny - (ax * nx + ay * ny) <= RefTol) return;
            if ((sx == ax && sy == ay) || (sx == bx && sy == by)) return;
            Refine(ax, ay, sx, sy, depth + 1);
            Push(sx, sy, st); Refined++;
            Refine(sx, sy, bx, by, depth + 1);
        }

        // Build the witness polygon: N base directions (+ adaptive refinement of long edges)
        public void Build()
        {
            Cnt = 0; int nbase = 0;
            double[] bx = baseX, by = baseY; byte[] bt = baseT;
            for (int i = 0; i < N; i++)
            {
                if (SupportAll(Ux[i], Uy[i], i, out double px, out double py, out byte tg)) { bx[nbase] = px; by[nbase] = py; bt[nbase] = tg; nbase++; }
            }
            for (int i = 0; i < nbase; i++)
            {
                int k = (i + 1) % nbase;
                Push(bx[i], by[i], bt[i]);
                if (bx[i] != bx[k] || by[i] != by[k]) Refine(bx[i], by[i], bx[k], by[k], 0);
            }
        }
        readonly double[] baseX = new double[1 << 13], baseY = new double[1 << 13]; readonly byte[] baseT = new byte[1 << 13];

        // Shoelace lower bound.  The origin must lie in a body that was added (it is the centre of disc D).
        // Returns NaN if the angular-order certificate fails (caller must treat as "not certified").
        public double Finish()
        {
            Build();
            int n = Cnt;
            if (n < 3) return double.NaN;
            Iv S = Iv.Pt(0.0); int wind = 0;
            double x1 = Px[n - 1], y1 = Py[n - 1];
            for (int i = 0; i < n; i++)
            {
                double x2 = Px[i], y2 = Py[i];
                if (x1 != x2 || y1 != y2)
                {
                    // exact points -> interval cross product; strictly positive lower end certifies a strictly counter-clockwise step about O
                    Iv cr = Iv.MulPt(x1, y2) - Iv.MulPt(x2, y1);
                    if (!(cr.lo > 0)) return double.NaN;
                    S = S + cr;
                    if (y1 < 0 && y2 >= 0) wind++;       // exact comparisons of doubles: upward crossing of the positive x-axis by a ccw step of angle < pi
                }
                x1 = x2; y1 = y2;
            }
            if (wind != 1) return double.NaN;
            return 0.5 * S.lo;        // area of the star-shaped polygon = S/2 >= S.lo/2 ; halving is exact
        }
    }

    // Own sin/cos by Taylor on [0, 1.3]; used to cross-check Math.Sin/Cos in selftest (decimal-precision reference).
    public static class RefTrig
    {
        public static void SinCosDecimal(decimal x, out decimal s, out decimal c)
        {
            decimal term = 1m; c = 0; s = 0; decimal t = 1m; // cos
            c = 0; term = 1m;
            for (int k = 0; k < 30; k++) { c += term; term = -term * x * x / ((2 * k + 1) * (2 * k + 2)); }
            term = x; s = 0;
            for (int k = 0; k < 30; k++) { s += term; term = -term * x * x / ((2 * k + 2) * (2 * k + 3)); }
        }
    }
}
