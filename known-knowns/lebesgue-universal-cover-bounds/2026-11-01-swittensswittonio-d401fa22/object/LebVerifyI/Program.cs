using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;
using System.Threading;
using System.Diagnostics;

namespace LebVerify
{
    // header + bit blocks of a LEBCERTB certificate
    public sealed class Cert
    {
        public double Target, Thresh, Tmax, Inflate; public int M, K, Depth, NSeed; public ulong NBlk;
        public long[] Off; public int[] Len; public byte[] Data; public bool Truncated; public string Err;
        public static Cert Load(string path)
        {
            var c = new Cert(); c.Data = File.ReadAllBytes(path); var d = c.Data;
            if (d.Length < 64 || Encoding.ASCII.GetString(d, 0, 8) != "LEBCERTB") { c.Err = "bad magic / short file"; return c; }
            int p = 8;
            c.Target = BitConverter.ToDouble(d, p); p += 8; c.Thresh = BitConverter.ToDouble(d, p); p += 8; c.Tmax = BitConverter.ToDouble(d, p); p += 8;
            c.M = BitConverter.ToInt32(d, p); p += 4; c.K = BitConverter.ToInt32(d, p); p += 4; c.Depth = BitConverter.ToInt32(d, p); p += 4; c.NSeed = BitConverter.ToInt32(d, p); p += 4;
            c.Inflate = BitConverter.ToDouble(d, p); p += 8; c.NBlk = BitConverter.ToUInt64(d, p); p += 8;
            if (c.NBlk != (ulong)c.NSeed) { c.Err = "nblk != nseed"; return c; }
            if ((long)p + 4L * c.NSeed > d.Length) { c.Err = "truncated size table"; return c; }
            c.Len = new int[c.NSeed]; c.Off = new long[c.NSeed]; long off = p + 4L * c.NSeed;
            for (int i = 0; i < c.NSeed; i++) { c.Len[i] = (int)BitConverter.ToUInt32(d, p + 4 * i); c.Off[i] = off; off += c.Len[i]; }
            if (off != d.Length) { c.Err = off > d.Length ? "truncated: block sizes exceed file" : "trailing bytes after last block"; c.Truncated = off > d.Length; }
            return c;
        }
    }

    public sealed class ChunkResult
    {
        public int Idx; public long Nodes, Leaves, Ap, Hull, Fail, Desync, Order; public double Worst = double.PositiveInfinity;
        public double[] WorstBox; public double MinHalfT = double.PositiveInfinity, MinHalfR = double.PositiveInfinity; public int MaxDepth;
        public double[] Lo = { 9, 9, 9, 9, 9 }, Hi = { -9, -9, -9, -9, -9 };
        public double MaxD3, MaxD5; public long FallbackDirs; public long Pad; public double WorstFine = double.PositiveInfinity; public double[] WorstFineBox; public long FineRechecked;
        public string FirstFail = ""; public long Cover; public long[] TierAcc = new long[8];
        public long MinBits;  // unused
    }

    public static class Prog
    {
        const double CIRC5 = 0.5257311121191336;   // split-rule selector only (which coordinate to bisect); coverage is verified per split by Iv, so any value is sound
        static double Tau, TauThr, D0, D0sq, FLo0; static double DumpSlack = -1; static long ChunkSize = 1024;
        public static double FineThr = 2e-5; static StreamWriter LeafLog; static int LeafLogMod = 0;   // optional per-leaf lb log (hash-sampled) for cross-checks
        static void InitConsts() { }
        static readonly Iv One = Iv.Pt(1.0);
        static readonly Iv E11 = Iv.Ratio(1, 100000000000L);
        static readonly Iv K2 = Iv.Pt(1.0) + Ctx.E12;                    // 1 + 1e-12 (enclosure)
        static readonly Iv TwoPiOver5 = (IvConsts.Pi.Twice()) / Iv.Pt(5.0);

        // INTERVAL lower bound of f(d) = area conv(disc radius 1/2, point at distance d) = (pi - acos(1/(2d)))/4 + sqrt(d^2 - 1/4)/2,  d > 0.5, d an exact double.
        //  acos(y) = pi/2 - asin(y), asin(y) = sum_k u_k y^(2k+1)/(2k+1) with ALL terms positive (u_k = C(2k,k)/4^k), so any partial sum is a LOWER bound of asin
        //  (the 199 terms are summed with Iv operations; its .lo is a rigorous lower bound of the partial sum, hence of asin), hence an upper bound of acos.
        static double FLower(double d)
        {
            Iv dI = Iv.Pt(d); Iv y = Iv.Pt(0.5) / dI, y2 = Iv.Sqr(y), u = One, pw = y, sum = y;
            for (int k = 1; k < 200; k++) { u = u * (Iv.Pt(2.0 * k - 1.0) / Iv.Pt(2.0 * k)); pw = pw * y2; sum = sum + u * pw / Iv.Pt(2.0 * k + 1.0); }
            Iv acosUb = IvConsts.Pi.Half() - Iv.Pt(sum.lo);               // pi/2 - asin_lower ; use .hi
            Iv sq = Iv.Sqrt(Iv.Sqr(dI) - Iv.Pt(0.25));
            Iv f = (IvConsts.Pi - Iv.Pt(acosUb.hi)) * Iv.Pt(0.25) + sq * Iv.Pt(0.5);
            return f.lo;
        }

        // smallest d0 with FLower(d0) >= thr + 1e-7 (bisection on the interval lower bound), inflated by (1+1e-9)+1e-9 and RE-CERTIFIED at the returned double; f is nondecreasing in d.
        static double ComputeD0(double thr)
        {
            double need = (Iv.Pt(thr) + Iv.Ratio(1, 10000000)).hi;
            double lo = 0.5001, hi = 1.0;
            if (FLower(hi) < need) return double.PositiveInfinity;
            for (int i = 0; i < 100; i++) { double mid = 0.5 * (lo + hi); if (FLower(mid) >= need) hi = mid; else lo = mid; }
            double d0 = hi * (1 + 1e-9) + 1e-9;
            if (!(d0 > 0.5001 && FLower(d0) >= need)) return double.PositiveInfinity;
            FLo0 = FLower(d0);
            return d0;
        }

        // (old double F removed; replaced by FLower above)
        // Child-covers-parent certificate for ONE split in coordinate k: parent (c,h), left child (cL,hL), right child (cR,hR), all exact doubles.
        // Real boxes are [c-h,c+h]; with Iv:  c-h >= cL-hL  <=>  (c-cL) >= (h-hL);   cR+hR >= c+h  <=>  (cR-c)+hR-h >= 0;   no gap  <=>  (cL-cR)+hL+hR >= 0.
        // Each difference is of two nearby doubles so its Iv width is relative to the half-width; undecided => false (certificate failure).
        public static bool Cover(double c, double h, double cL, double hL, double cR, double hR)
        {
            Iv C = Iv.Pt(c), H = Iv.Pt(h), CL = Iv.Pt(cL), HL = Iv.Pt(hL), CR = Iv.Pt(cR), HR = Iv.Pt(hR);
            if (!(hL > 0 && hR > 0 && h > 0)) return false;
            if (!((C - CL).lo >= (H - HL).hi)) return false;
            if (!(((CR - C) + HR - H).lo >= 0)) return false;
            if (!(((CL - CR) + HL + HR).lo >= 0)) return false;
            return true;
        }

        // returns lower bound of the hull area over the leaf box, from interval arithmetic only; mode: 1 = a-priori (f) pass, 2 = hull; NaN = not certified
        public static double LeafBound(double[] b, int o, Worker wk, out int mode, out double d3o, out double d5o, int only = -1)
        {
            double c3x = b[o], h3x = b[o + 1], c3y = b[o + 2], h3y = b[o + 3], cr = b[o + 4], hr = b[o + 5], c5x = b[o + 6], h5x = b[o + 7], c5y = b[o + 8], h5y = b[o + 9];
            d3o = d5o = 0; mode = 0;
            // a-priori (Lemma 4.4): body k contains its centre; centre distance >= box distance; true distance^2 >= lower end of Iv sum
            Iv ax = Iv.Max0(Iv.Abs(Iv.Pt(c3x)) - Iv.Pt(h3x)), ay = Iv.Max0(Iv.Abs(Iv.Pt(c3y)) - Iv.Pt(h3y));
            if ((Iv.Sqr(ax) + Iv.Sqr(ay)).lo >= D0sq) { mode = 1; return FLo0; }
            ax = Iv.Max0(Iv.Abs(Iv.Pt(c5x)) - Iv.Pt(h5x)); ay = Iv.Max0(Iv.Abs(Iv.Pt(c5y)) - Iv.Pt(h5y));
            if ((Iv.Sqr(ax) + Iv.Sqr(ay)).lo >= D0sq) { mode = 1; return FLo0; }
            mode = 2;
            // erosion radii: upper bounds of the corner movement (Lemma 4.7/4.8), all Iv.   delta3 = hypot(h3), delta5 = hypot(h5) + 2 R5 sin(hr/2)
            Iv H3 = Iv.Sqrt(Iv.Sqr(Iv.Pt(h3x)) + Iv.Sqr(Iv.Pt(h3y)));
            Iv d3 = H3 * K2;
            Iv xh = Iv.Pt(hr).Half(); if (!(xh.lo >= 0 && xh.hi <= 0.7)) return double.NaN;   // sin series range guard (fail closed)
            Iv sn = IvTrig.Sin(xh, 7);
            Iv H5 = Iv.Sqrt(Iv.Sqr(Iv.Pt(h5x)) + Iv.Sqr(Iv.Pt(h5y)));
            Iv d5 = (H5 + IvConsts.R5.Twice() * sn) * K2;
            d3o = d3.hi; d5o = d5.hi;
            Iv r3 = One - d3 - E11, r5 = One - d5 - E11;
            // box-centre corners (Iv enclosures)
            for (int k = 0; k < 3; k++) { wk.V3x[k] = IvConsts.V3x0[k] + Iv.Pt(c3x); wk.V3y[k] = IvConsts.V3y0[k] + Iv.Pt(c3y); }
            if (!(cr >= 0.0 && cr <= 1.3)) return double.NaN;
            Iv xr = Iv.Pt(cr); Iv sa = IvTrig.Sin(xr, 10), ca = IvTrig.Cos(xr, 10);
            Iv C5x = Iv.Pt(c5x), C5y = Iv.Pt(c5y);
            for (int k = 0; k < 5; k++)
            {
                wk.V5x[k] = IvConsts.V5x0[k] * ca - IvConsts.V5y0[k] * sa + C5x;
                wk.V5y[k] = IvConsts.V5x0[k] * sa + IvConsts.V5y0[k] * ca + C5y;
            }
            double lb = double.NaN;
            for (int ti = 0; ti < wk.Tiers.Length; ti++)
            {
                if (only >= 0 && ti != only) continue;
                var cx = wk.Tiers[ti];
                wk.Cx = cx;
                long t0 = Stopwatch.GetTimestamp(); cx.Reset();
                cx.AddDiscIntersection(wk.Zx, wk.Zy, 1, Iv.Pt(0.5), 0);
                cx.AddDiscIntersection(wk.V3x, wk.V3y, 3, r3, 1);
                cx.AddDiscIntersection(wk.V5x, wk.V5y, 5, r5, 2);
                long t1 = Stopwatch.GetTimestamp(); lb = cx.Finish(); ProfAdd += t1 - t0; ProfFin += Stopwatch.GetTimestamp() - t1;
                if (lb >= TauThr) break;
            }
            return lb;
        }

        public static string TierSpec = "256:0.01,1024:0.01,4096:0.01";   // N:refine-min-edge-length, tried in order; any tier's bound is sound on its own
        static Ctx[] MakeTiers() { var l = new List<Ctx>(); foreach (var t in TierSpec.Split(',')) { var q = t.Split(':'); var cx = new Ctx(int.Parse(q[0])); cx.RefMinLen = double.Parse(q[1], CultureInfo.InvariantCulture); l.Add(cx); } return l.ToArray(); }
        public sealed class Worker
        {
            public Iv[] V3x = new Iv[3], V3y = new Iv[3], V5x = new Iv[5], V5y = new Iv[5], Zx = { Iv.Pt(0.0) }, Zy = { Iv.Pt(0.0) };
            public double[] St = new double[10 * 512]; public Ctx[] Tiers = MakeTiers(); public Ctx Cx; public int AccTier;
        }

        static bool SeedBox(Cert c, int idx, double[] box)
        {
            bool ok = true; double t = c.Tmax; double[] b = { 0, t, 0, t, Math.PI / 5, Math.PI / 5, 0, t, 0, t };
            double[] n = new double[10];
            for (int l = c.Depth - 1; l >= 0; l--)
            {
                int s = ((idx >> l) & 1) == 0 ? -1 : 1;
                int k = Widest(b, 0);
                double half = b[2 * k + 1] * 0.5;
                Array.Copy(b, n, 10); n[2 * k] = b[2 * k] + s * half; n[2 * k + 1] = half * (1.0 + c.Inflate);
                // coverage of the parent by the two children of this split (both children recomputed from the parent exactly as DoTask/Walk do)
                double cL = b[2 * k] - half, cR = b[2 * k] + half, hh = half * (1.0 + c.Inflate);
                if (!Cover(b[2 * k], b[2 * k + 1], cL, hh, cR, hh)) ok = false;
                Array.Copy(n, b, 10);
            }
            Array.Copy(b, box, 10); return ok;
        }

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        static int Widest(double[] b, int o)
        {
            double w0 = b[o + 1], w1 = b[o + 3], w2 = CIRC5 * b[o + 5], w3 = b[o + 7], w4 = b[o + 9];
            int k = 0; double m = w0;
            if (w1 > m) { m = w1; k = 1; }
            if (w2 > m) { m = w2; k = 2; }
            if (w3 > m) { m = w3; k = 3; }
            if (w4 > m) { m = w4; k = 4; }
            return k;
        }

        // Process one unit: DFS from bit position `start` of block `si` beginning at box `seed`.  If end>=0 the unit is a subtree that must end exactly at `end`;
        // if end<0 the unit is a whole seed (block) and the trailing-bit rules apply.
        static ChunkResult DoTask(Cert c, int si, double[] seed, long start, long end, Worker w, ChunkResult res, StreamWriter dump, double dumpProb, Random rng)
        {
            var st = w.St;
            Array.Copy(seed, 0, st, 0, 10); int sp = 1;
            long pos = start; long nbits = 8L * c.Len[si]; long off = c.Off[si]; var d = c.Data; int maxsp = 0;
            double infl1 = 1.0 + c.Inflate;
            while (sp > 0)
            {
                sp--; int o = sp * 10;
                if (pos >= nbits) { res.Desync++; return res; }
                int bit = (d[off + (pos >> 3)] >> (int)(7 - (pos & 7))) & 1; pos++; res.Nodes++;
                if (bit == 0)
                {
                    res.Leaves++;
                    int mode; double d3, d5;
                    double lb = LeafBound(st, o, w, out mode, out d3, out d5);
                    // extents of the leaf (domain coverage bookkeeping)
                    for (int q = 0; q < 5; q++) { double lo = st[o + 2 * q] - st[o + 2 * q + 1], hi = st[o + 2 * q] + st[o + 2 * q + 1]; if (lo < res.Lo[q]) res.Lo[q] = lo; if (hi > res.Hi[q]) res.Hi[q] = hi; }
                    if (LeafLog != null && mode == 2 && LeafHash(si, pos) % (uint)LeafLogMod == 0) lock (LeafLog) LeafLog.WriteLine(si + " " + pos + " " + BitConverter.DoubleToInt64Bits(lb).ToString("X16") + " " + Hx(lb));
                    if (mode == 2) res.TierAcc[double.IsNaN(lb) || lb < TauThr ? 7 : w.AccTier]++;
                    if (mode == 1) res.Ap++;
                    else
                    {
                        res.Hull++; res.FallbackDirs += w.Cx.Refined;
                        if (d3 > res.MaxD3) res.MaxD3 = d3; if (d5 > res.MaxD5) res.MaxD5 = d5;
                    }
                    if (double.IsNaN(lb)) { res.Order++; res.Fail++; if (res.FirstFail == "") res.FirstFail = "ORDER-FAIL seed " + si + " leafbox " + BoxStr(st, o); }
                    else
                    {
                        double slack = lb - TauThr;   // leaf passes iff interval LB >= TauThr (= upper bound of tau + 1e-12)
                        if (mode == 2 && slack < res.Worst) { res.Worst = slack; res.WorstBox = new double[10]; Array.Copy(st, o, res.WorstBox, 0, 10); }
                        if (mode == 2 && slack < FineThr)
                        {   // near-threshold leaf: also record its slack at the finest witness tier (N=4096), for an honest "true worst slack" figure
                            res.FineRechecked++; int m2; double e3, e5; double lb2 = LeafBound(st, o, w, out m2, out e3, out e5, w.Tiers.Length - 1);
                            double s2 = Math.Max(lb2, lb) - TauThr;
                            if (s2 < res.WorstFine) { res.WorstFine = s2; res.WorstFineBox = new double[10]; Array.Copy(st, o, res.WorstFineBox, 0, 10); }
                        }
                        if (slack < 0) { res.Fail++; if (res.FirstFail == "") res.FirstFail = "LEAF-FAIL lb=" + lb.ToString("R", CultureInfo.InvariantCulture) + " seed " + si + " box " + BoxStr(st, o); }
                    }
                    if (dump != null && mode == 2 && (rng.NextDouble() < dumpProb || (!double.IsNaN(lb) && lb - Tau < DumpSlack))) lock (dump) DumpLeaf(dump, si, st, o, w, lb);
                }
                else
                {
                    int k = Widest(st, o);
                    double half = st[o + 2 * k + 1] * 0.5;
                    if (k == 2) { if (half < res.MinHalfR) res.MinHalfR = half; } else if (half < res.MinHalfT) res.MinHalfT = half;
                    if (sp + 2 >= 510) { res.Desync++; return res; }
                    int o2 = (sp + 1) * 10;
                    for (int q = 0; q < 10; q++) { st[o2 + q] = st[o + q]; }
                    double cc = st[o + 2 * k];
                    // layout: slot sp = c2 (+), slot sp+1 = c1 (-), so c1 pops first (DFS pre-order, c1 before c2)
                    double hOld = st[o + 2 * k + 1];
                    st[o + 2 * k] = cc + half; st[o + 2 * k + 1] = half * infl1;
                    st[o2 + 2 * k] = cc - half; st[o2 + 2 * k + 1] = half * infl1;
                    if (!Cover(cc, hOld, st[o2 + 2 * k], st[o2 + 2 * k + 1], st[o + 2 * k], st[o + 2 * k + 1])) { res.Cover++; res.Fail++; if (res.FirstFail == "") res.FirstFail = "COVER-FAIL seed " + si + " parent c=" + Hx(cc) + " h=" + Hx(hOld) + " coord " + k; }
                    sp += 2; if (sp > maxsp) maxsp = sp;
                }
            }
            if (maxsp > res.MaxDepth) res.MaxDepth = maxsp;
            if (end >= 0) { if (pos != end) res.Desync++; }
            else TrailCheck(c, si, pos, res);
            return res;
        }

        static uint LeafHash(int si, long pos) { ulong x = (ulong)si * 0x9E3779B97F4A7C15UL ^ (ulong)pos * 0xC2B2AE3D27D4EB4FUL; x ^= x >> 29; x *= 0xBF58476D1CE4E5B9UL; x ^= x >> 32; return (uint)x; }

        static void TrailCheck(Cert c, int si, long pos, ChunkResult res)
        {
            long nbits = 8L * c.Len[si], off = c.Off[si]; var d = c.Data;
            if (pos > nbits || nbits - pos >= 8) res.Desync++;
            else for (long q = pos; q < nbits; q++) if (((d[off + (q >> 3)] >> (int)(7 - (q & 7))) & 1) != 0) { res.Pad++; res.Desync++; break; }
        }

        sealed class Unit { public int Seed; public double[] Box; public long Start, End; public long Size; }
        const long LIMIT = 150000;   // max nodes per unit (heavy seeds are cut into subtrees of at most this many nodes by a bit-only pre-walk)

        // bit-only walk of a heavy seed: returns subtree node count; adds cut units; accumulates prefix (non-cut) node stats
        static long Walk(Cert c, int si, double[][] boxes, int depth, ref long pos, List<Unit> cuts, ChunkResult prefix, double infl1)
        {
            long nbits = 8L * c.Len[si], off = c.Off[si]; var d = c.Data;
            if (pos >= nbits) { prefix.Desync++; return 1; }
            long startPos = pos;
            int bit = (d[off + (pos >> 3)] >> (int)(7 - (pos & 7))) & 1; pos++;
            if (bit == 0) return 1;
            double[] b = boxes[depth];
            int k = Widest(b, 0); double half = b[2 * k + 1] * 0.5; double cc = b[2 * k];
            if (depth + 2 >= boxes.Length) { prefix.Desync++; return 1; }
            var cb = boxes[depth + 1];
            if (!Cover(cc, b[2 * k + 1], cc - half, half * infl1, cc + half, half * infl1)) { prefix.Cover++; prefix.Fail++; if (prefix.FirstFail == "") prefix.FirstFail = "COVER-FAIL(prewalk) seed " + si + " c=" + Hx(cc); }
            Array.Copy(b, cb, 10); cb[2 * k] = cc - half; cb[2 * k + 1] = half * infl1;     // c1 (-)
            long s1pos = pos; long sL = Walk(c, si, boxes, depth + 1, ref pos, cuts, prefix, infl1);
            Unit uL = null; if (sL <= LIMIT) uL = new Unit { Seed = si, Box = (double[])cb.Clone(), Start = s1pos, End = pos, Size = sL };
            cb = boxes[depth + 1]; Array.Copy(b, cb, 10); cb[2 * k] = cc + half; cb[2 * k + 1] = half * infl1;   // c2 (+)
            long s2pos = pos; long sR = Walk(c, si, boxes, depth + 1, ref pos, cuts, prefix, infl1);
            long tot = 1 + sL + sR;
            if (tot > LIMIT)
            {
                prefix.Nodes++;
                if (k == 2) { if (half < prefix.MinHalfR) prefix.MinHalfR = half; } else if (half < prefix.MinHalfT) prefix.MinHalfT = half;
                if (uL != null) cuts.Add(uL);
                if (sR <= LIMIT) cuts.Add(new Unit { Seed = si, Box = (double[])cb.Clone(), Start = s2pos, End = pos, Size = sR });
            }
            return tot;
        }

        static List<Unit> Plan(Cert c, int threads, ChunkResult prefixAll, TextWriter log)
        {
            long badTop = 0, nTop = 0, badBot = 0, badSeedCover = 0; var units = new Unit[c.NSeed][]; var pres = new ChunkResult[c.NSeed]; int next = 0; double infl1 = 1.0 + c.Inflate;
            var ths = new List<Thread>();
            for (int t = 0; t < threads; t++)
            {
                var th = new Thread(() =>
                {
                    var boxes = new double[600][]; for (int i = 0; i < boxes.Length; i++) boxes[i] = new double[10];
                    while (true)
                    {
                        int si = Interlocked.Increment(ref next) - 1; if (si >= c.NSeed) return;
                        long nbits = 8L * c.Len[si];
                        var box = new double[10]; if (!SeedBox(c, si, box)) Interlocked.Increment(ref badSeedCover);
                        {   // top-end seeds (rho upper edge near 2pi/5) must reach TRUE 2pi/5 (interval: lower end of c+h >= upper end of enclosure of 2pi/5); bottom-end seeds must reach 0 (upper end of c-h <= 0)
                            double hiRd = box[4] + box[5], loRd = box[4] - box[5];      // selectors only
                            if (hiRd > 1.2) { Interlocked.Increment(ref nTop); if (!((Iv.Pt(box[4]) + Iv.Pt(box[5])).lo >= TwoPiOver5.hi)) Interlocked.Increment(ref badTop); }
                            if (loRd < 0.05) { if (!((Iv.Pt(box[4]) - Iv.Pt(box[5])).hi <= 0.0)) Interlocked.Increment(ref badBot); } }
                        if (nbits <= LIMIT) { units[si] = new[] { new Unit { Seed = si, Box = box, Start = 0, End = -1, Size = nbits } }; continue; }
                        var cuts = new List<Unit>(); var pre = new ChunkResult(); long pos = 0; Array.Copy(box, boxes[0], 10);
                        long tot = Walk(c, si, boxes, 0, ref pos, cuts, pre, infl1);
                        TrailCheck(c, si, pos, pre);
                        if (tot <= LIMIT) { units[si] = new[] { new Unit { Seed = si, Box = box, Start = 0, End = -1, Size = nbits } }; continue; }
                        units[si] = cuts.ToArray(); pres[si] = pre;
                    }
                });
                th.Start(); ths.Add(th);
            }
            foreach (var th in ths) th.Join();
            var all = new List<Unit>(); long heavy = 0;
            for (int i = 0; i < c.NSeed; i++)
            {
                all.AddRange(units[i]);
                if (pres[i] != null) { heavy++; var r = pres[i]; prefixAll.Nodes += r.Nodes; prefixAll.Desync += r.Desync; prefixAll.Pad += r.Pad; prefixAll.Cover += r.Cover; prefixAll.Fail += r.Fail; if (prefixAll.FirstFail == "") prefixAll.FirstFail = r.FirstFail; prefixAll.MinHalfT = Math.Min(prefixAll.MinHalfT, r.MinHalfT); prefixAll.MinHalfR = Math.Min(prefixAll.MinHalfR, r.MinHalfR); }
            }
            log.WriteLine($"  seed rho-coverage (Iv): seeds at top end {nTop:N0}, of which not certified to reach true 2pi/5: {badTop}; bottom-end seeds not certified to reach 0: {badBot}; seed-split coverage failures: {badSeedCover}");
            prefixAll.Cover += badSeedCover; prefixAll.Fail += badSeedCover; if (badSeedCover != 0 && prefixAll.FirstFail == "") prefixAll.FirstFail = "COVER-FAIL(seed boxes)";
            if (badTop != 0 || badBot != 0) prefixAll.Desync += 1;
            log.WriteLine($"  plan: {all.Count:N0} work units ({heavy:N0} heavy seeds cut into subtrees of <= {LIMIT:N0} nodes), prefix split nodes {prefixAll.Nodes:N0}");
            return all;
        }

        static string BoxStr(double[] b, int o) { var sb = new StringBuilder("["); for (int i = 0; i < 10; i++) { if (i > 0) sb.Append(','); sb.Append(b[o + i].ToString("R", CultureInfo.InvariantCulture)); } return sb.Append(']').ToString(); }

        static void DumpLeaf(StreamWriter dump, int si, double[] st, int o, Worker w, double lb)
        {
            // re-run to get the witness polygon (Ctx still holds it from LeafBound; Finish() compacted it)
            var cx = w.Cx;
            // after Finish the compacted arrays are in Bx/By/Tag; count = number of valid points: recompute by re-running with no compaction side effects
            var sb = new StringBuilder();
            sb.Append("LEAF ").Append(si).Append(' ').Append(BoxStr(st, o)).Append(' ').Append(lb.ToString("R", CultureInfo.InvariantCulture)).Append('\n');
            // Finish() compacts to the front; points are 0..n'-1 where n' = count of valid points; tags beyond are stale -> use Bd to know validity count
            int cnt = cx.Cnt;
            sb.Append("PTS ").Append(cnt).Append('\n');
            for (int i = 0; i < cnt; i++) sb.Append(cx.Px[i].ToString("R", CultureInfo.InvariantCulture)).Append(' ').Append(cx.Py[i].ToString("R", CultureInfo.InvariantCulture)).Append(' ').Append(cx.Pt[i]).Append('\n');
            dump.Write(sb.ToString());
        }

        static string Hx(double x) => x.ToString("R", CultureInfo.InvariantCulture);

        static string Serialize(ChunkResult r)
        {
            var sb = new StringBuilder();
            sb.Append("C\t").Append(r.Idx).Append('\t').Append(r.Nodes).Append('\t').Append(r.Leaves).Append('\t').Append(r.Ap).Append('\t').Append(r.Hull).Append('\t').Append(r.Fail).Append('\t').Append(r.Desync).Append('\t').Append(r.Order).Append('\t').Append(r.Pad)
              .Append('\t').Append(Hx(r.Worst)).Append('\t').Append(Hx(r.MinHalfT)).Append('\t').Append(Hx(r.MinHalfR)).Append('\t').Append(r.MaxDepth).Append('\t').Append(Hx(r.MaxD3)).Append('\t').Append(Hx(r.MaxD5)).Append('\t').Append(r.FallbackDirs);
            for (int q = 0; q < 5; q++) sb.Append('\t').Append(Hx(r.Lo[q])).Append('\t').Append(Hx(r.Hi[q]));
            sb.Append('\t').Append(r.WorstBox == null ? "-" : BoxStr(r.WorstBox, 0)).Append('\t').Append(r.FirstFail == "" ? "-" : r.FirstFail.Replace('\t', ' '));
            sb.Append('\t').Append(Hx(r.WorstFine)).Append('\t').Append(r.WorstFineBox == null ? "-" : BoxStr(r.WorstFineBox, 0)).Append('\t').Append(r.FineRechecked).Append('\t').Append(r.Cover); for (int q = 0; q < 8; q++) sb.Append('\t').Append(r.TierAcc[q]);
            return sb.ToString();
        }

        static ChunkResult Parse(string line)
        {
            var f = line.Split('\t'); var r = new ChunkResult(); var ic = CultureInfo.InvariantCulture; int p = 1;
            r.Idx = int.Parse(f[p++]); r.Nodes = long.Parse(f[p++]); r.Leaves = long.Parse(f[p++]); r.Ap = long.Parse(f[p++]); r.Hull = long.Parse(f[p++]); r.Fail = long.Parse(f[p++]); r.Desync = long.Parse(f[p++]); r.Order = long.Parse(f[p++]); r.Pad = long.Parse(f[p++]);
            r.Worst = double.Parse(f[p++], ic); r.MinHalfT = double.Parse(f[p++], ic); r.MinHalfR = double.Parse(f[p++], ic); r.MaxDepth = int.Parse(f[p++]); r.MaxD3 = double.Parse(f[p++], ic); r.MaxD5 = double.Parse(f[p++], ic); r.FallbackDirs = long.Parse(f[p++]);
            for (int q = 0; q < 5; q++) { r.Lo[q] = double.Parse(f[p++], ic); r.Hi[q] = double.Parse(f[p++], ic); }
            string wb = f[p++]; if (wb != "-") { var s = wb.Trim('[', ']').Split(','); r.WorstBox = new double[10]; for (int i = 0; i < 10; i++) r.WorstBox[i] = double.Parse(s[i], ic); }
            r.FirstFail = f[p] == "-" ? "" : f[p]; p++;
            r.WorstFine = double.Parse(f[p++], ic); string fb = f[p++]; if (fb != "-") { var s = fb.Trim('[', ']').Split(','); r.WorstFineBox = new double[10]; for (int i = 0; i < 10; i++) r.WorstFineBox[i] = double.Parse(s[i], ic); }
            r.FineRechecked = long.Parse(f[p++]); r.Cover = long.Parse(f[p++]); for (int q = 0; q < 8; q++) r.TierAcc[q] = long.Parse(f[p++]);
            return r;
        }

        // header-level checks (all rigorous modulo the stated margins); returns false and prints reason on rejection
        static string ClaimArg = "8344/10000";   // exact decimal claim (default 0.8344); "none" = use the header double only
        static bool HeaderChecks(Cert c, TextWriter log)
        {
            if (c.Err != null) { log.WriteLine("  REJECTED: " + c.Err); return false; }
            if (!(c.Inflate > 0 && c.Inflate < 1e-3)) { log.WriteLine("  REJECTED: inflate = " + Hx(c.Inflate) + " not in (0,1e-3); (coverage itself is certified per split by Iv)"); return false; }
            if (!(c.Target > 0.5 && c.Target < 0.9)) { log.WriteLine("  REJECTED: target out of range"); return false; }
            Tau = c.Target; Iv tauI = Iv.Pt(Tau);
            if (ClaimArg != "none") { var q = ClaimArg.Split('/'); Iv dec = Iv.Ratio(long.Parse(q[0]), long.Parse(q[1])); log.WriteLine($"  claim decimal {ClaimArg} = enclosure [{Hx(dec.lo)},{Hx(dec.hi)}]; header tau double {Hx(Tau)} {(Tau >= dec.lo && Tau <= dec.hi ? "is inside it" : "is OUTSIDE it (REJECT)")}"); if (!(Tau <= dec.hi && Tau >= dec.lo)) return false; tauI = new Iv(tauI.lo, Math.Max(tauI.hi, dec.hi)); }
            TauThr = (Iv.Pt(tauI.hi) + Iv.Ratio(1, 1000000000000L)).hi;   // accept iff leaf lower bound >= this (upper bound of max(tau_header, tau_decimal) + 1e-12)
            D0 = ComputeD0(TauThr); D0sq = Iv.Sqr(Iv.Pt(D0)).hi;
            log.WriteLine($"  header: tau={Hx(c.Target)} thresh={Hx(c.Thresh)} tmax={Hx(c.Tmax)} m={c.M} K={c.K} depth={c.Depth} nseed={c.NSeed} inflate={Hx(c.Inflate)} nblk={c.NBlk}");
            log.WriteLine($"  acceptance threshold TauThr = {Hx(TauThr)} (>= tau + 1e-12, interval upper bound)");
            log.WriteLine($"  a-priori threshold d0 = {Hx(D0)}  (interval-certified f(d0) >= {Hx(FLo0)} >= TauThr + 1e-7)  tmax={Hx(c.Tmax)}");
            if (!(D0 <= c.Tmax)) { log.WriteLine($"  REJECTED: domain |t|<={c.Tmax} is smaller than d0={D0}: placements with d0<=|t|<=tmax would be uncovered/unchecked (f(tmax) < tau+1e-7 => outside placements not excluded)"); return false; }
            if (c.NSeed != (1 << c.Depth)) { log.WriteLine("  REJECTED: nseed != 2^depth"); return false; }
            return true;
        }

        public static int Main(string[] args)
        {
            InitConsts();
            try
            {
                string cmd = args.Length > 0 ? args[0] : "help";
                                if (cmd == "verify") return Verify(args);
                if (cmd == "summarize") return Summarize(args);
                if (cmd == "leaf") return LeafCmd(args);
                if (cmd == "bench") return Bench(args);
                if (cmd == "ivtest") return IvTest.Run(args);
                Console.WriteLine("usage: LebVerify selftest | verify <cert> [--threads n] [--ckpt file] [--frac f | --chunks a-b] [--dump file --dumpn k] [--N dirs] | summarize <cert> <ckpt>");
                return 2;
            }
            catch (Exception e) { Console.WriteLine("EXCEPTION " + e); return 3; }
        }

        static string Arg(string[] a, string key, string def) { for (int i = 0; i < a.Length - 1; i++) if (a[i] == key) return a[i + 1]; return def; }

        sealed class Plan2 { public List<Unit> Units; public List<(int a, int b)> Jobs; public ChunkResult Prefix = new ChunkResult(); }

        static Plan2 MakePlan(Cert cert, int threads, TextWriter log)
        {
            var pl = new Plan2(); pl.Units = Plan(cert, threads, pl.Prefix, log); pl.Jobs = new List<(int, int)>();
            int s = 0; long acc = 0;
            for (int i = 0; i < pl.Units.Count; i++)
            {
                acc += pl.Units[i].Size;
                if (acc >= 100000 || i == pl.Units.Count - 1) { pl.Jobs.Add((s, i + 1)); s = i + 1; acc = 0; }
            }
            log.WriteLine($"  plan: {pl.Jobs.Count:N0} jobs");
            return pl;
        }

        static int Verify(string[] a)
        {
            string path = a[1]; int threads = int.Parse(Arg(a, "--threads", "6")); string ckpt = Arg(a, "--ckpt", null);
            int N = 0; ClaimArg = Arg(a, "--claim", "8344/10000"); TierSpec = Arg(a, "--tiers", TierSpec); FineThr = double.Parse(Arg(a, "--finethr", "2e-5"), CultureInfo.InvariantCulture);
            string llp = Arg(a, "--leaflog", null); if (llp != null) { LeafLog = new StreamWriter(llp, false); LeafLogMod = int.Parse(Arg(a, "--leafmod", "200")); }
            DumpSlack = double.Parse(Arg(a, "--dumpslack", "-1"), CultureInfo.InvariantCulture); string dumpPath = Arg(a, "--dump", null); double dumpProb = double.Parse(Arg(a, "--dumpprob", "0"), CultureInfo.InvariantCulture);
            var log = Console.Out;
            try { Process.GetCurrentProcess().PriorityClass = ProcessPriorityClass.BelowNormal; } catch { }
            var cert = Cert.Load(path);
            log.WriteLine("VERIFY " + path + "  tiers N=256/1024/4096  threads=" + threads + "  " + DateTime.UtcNow.ToString("o") + "  pid=" + Process.GetCurrentProcess().Id);
            if (cert.Err != null) { log.WriteLine("  REJECTED: " + cert.Err); log.WriteLine("RESULT: REJECTED"); return 1; }
            if (!HeaderChecks(cert, log)) { log.WriteLine("RESULT: REJECTED"); return 1; }
            var plan = MakePlan(cert, threads, log);
            if (plan.Prefix.Desync != 0) { log.WriteLine("  REJECTED: bit-stream inconsistency in pre-walk (desync " + plan.Prefix.Desync + ")"); log.WriteLine("RESULT: REJECTED"); return 1; }
            int totalJobs = plan.Jobs.Count;
            string cr = Arg(a, "--jobs", null); int cLo = 0, cHi = totalJobs;
            if (cr != null) { var s = cr.Split('-'); cLo = int.Parse(s[0]); cHi = Math.Min(totalJobs, int.Parse(s[1])); }
            var done = new Dictionary<int, ChunkResult>();
            if (ckpt != null && File.Exists(ckpt)) foreach (var l in File.ReadLines(ckpt)) if (l.StartsWith("C\t")) { var r = Parse(l); done[r.Idx] = r; }
            string smp = Arg(a, "--sample", null); double sfrac = 1; var srng = new Random(int.Parse(Arg(a, "--sseed", "1"))); if (smp != null) sfrac = double.Parse(smp, CultureInfo.InvariantCulture);
            var todo = new List<int>();
            for (int k = cLo; k < cHi; k++) { bool pick = sfrac >= 1 || srng.NextDouble() < sfrac; if (pick && !done.ContainsKey(k)) todo.Add(k); }
            // heaviest jobs first is irrelevant for correctness; run in index order (deterministic)
            log.WriteLine($"  jobs {cLo}..{cHi} of {totalJobs}; already done (checkpoint): {done.Count}; to run: {todo.Count}");
            StreamWriter ck = ckpt != null ? new StreamWriter(new FileStream(ckpt, FileMode.Append, FileAccess.Write, FileShare.Read)) { AutoFlush = true } : null;
            StreamWriter dump = dumpPath != null ? new StreamWriter(dumpPath, false) : null;
            int next = 0; object lk = new object(); var sw = Stopwatch.StartNew(); long doneLeaves = 0; int doneChunks = 0; long lastPrint = 0;
            var ths = new List<Thread>();
            for (int t = 0; t < threads; t++)
            {
                int tid = t;
                var th = new Thread(() =>
                {
                    var w = new Worker(); var rng = new Random(12345 + tid);
                    while (true)
                    {
                        int my; lock (lk) { if (next >= todo.Count) return; my = todo[next++]; }
                        var r = new ChunkResult(); r.Idx = my;
                        var (ja, jb) = plan.Jobs[my];
                        for (int u = ja; u < jb; u++) { var un = plan.Units[u]; DoTask(cert, un.Seed, un.Box, un.Start, un.End, w, r, dump, dumpProb, rng); }
                        lock (lk)
                        {
                            done[my] = r; if (ck != null) ck.WriteLine(Serialize(r));
                            doneLeaves += r.Leaves; doneChunks++;
                            long nowS = (long)sw.Elapsed.TotalSeconds;
                            if (nowS - lastPrint >= 30 || doneChunks == todo.Count)
                            {
                                lastPrint = nowS;
                                log.WriteLine($"  [{sw.Elapsed.TotalMinutes:F1} min] jobs {doneChunks}/{todo.Count}  leaves {doneLeaves:N0}  {doneLeaves / Math.Max(sw.Elapsed.TotalSeconds, 1e-9):N0} leaves/s  working set {Process.GetCurrentProcess().WorkingSet64 / 1048576} MB");
                            }
                        }
                    }
                });
                th.Priority = ThreadPriority.BelowNormal; th.Start(); ths.Add(th);
            }
            foreach (var th in ths) th.Join();
            if (ck != null) ck.Dispose(); if (dump != null) dump.Dispose(); if (LeafLog != null) LeafLog.Dispose();
            log.WriteLine($"  wall time this run: {sw.Elapsed.TotalMinutes:F2} min");
            return Report(cert, done, plan, cLo, cHi, smp != null || cr != null, log);
        }

        static int Report(Cert cert, Dictionary<int, ChunkResult> done, Plan2 plan, int cLo, int cHi, bool sampled, TextWriter log)
        {
            long coverF = 0; long nodes = 0, leaves = 0, ap = 0, hull = 0, fail = 0, desync = 0, order = 0, pad = 0, fb = 0; double worst = double.PositiveInfinity; double[] wbox = null; double worstFine = double.PositiveInfinity; double[] wfbox = null; long fineN = 0; double mhT = double.PositiveInfinity, mhR = double.PositiveInfinity, md3 = 0, md5 = 0; int maxdepth = 0;
            double[] lo = { 9, 9, 9, 9, 9 }, hi = { -9, -9, -9, -9, -9 }; string firstFail = ""; int njobs = 0;
            for (int k = cLo; k < cHi; k++)
            {
                if (!done.TryGetValue(k, out var r)) { if (sampled) continue; log.WriteLine("  MISSING job " + k); return 1; }
                njobs++; coverF += r.Cover; nodes += r.Nodes; leaves += r.Leaves; ap += r.Ap; hull += r.Hull; fail += r.Fail; desync += r.Desync; order += r.Order; pad += r.Pad; fb += r.FallbackDirs;
                if (r.Worst < worst) { worst = r.Worst; wbox = r.WorstBox; }
                if (r.WorstFine < worstFine) { worstFine = r.WorstFine; wfbox = r.WorstFineBox; } fineN += r.FineRechecked;
                mhT = Math.Min(mhT, r.MinHalfT); mhR = Math.Min(mhR, r.MinHalfR); md3 = Math.Max(md3, r.MaxD3); md5 = Math.Max(md5, r.MaxD5); maxdepth = Math.Max(maxdepth, r.MaxDepth);
                for (int q = 0; q < 5; q++) { lo[q] = Math.Min(lo[q], r.Lo[q]); hi[q] = Math.Max(hi[q], r.Hi[q]); }
                if (firstFail == "" && r.FirstFail != "") firstFail = r.FirstFail;
            }
            bool full = !sampled && njobs == plan.Jobs.Count;
            long prefixNodes = 0;
            if (full) { prefixNodes = plan.Prefix.Nodes; nodes += prefixNodes; desync += plan.Prefix.Desync; coverF += plan.Prefix.Cover; fail += plan.Prefix.Fail; if (firstFail == "") firstFail = plan.Prefix.FirstFail; mhT = Math.Min(mhT, plan.Prefix.MinHalfT); mhR = Math.Min(mhR, plan.Prefix.MinHalfR); }
            log.WriteLine("=".PadRight(100, '='));
            log.WriteLine($"  jobs covered {njobs:N0} of {plan.Jobs.Count:N0}  ({(full ? "FULL" : "PARTIAL SLICE")})");
            log.WriteLine($"  nodes {nodes:N0} (incl. {prefixNodes:N0} pre-walk prefix split nodes)  leaves {leaves:N0}   (a-priori leaves {ap:N0}, hull leaves {hull:N0})");
            bool forest = true;
            if (full) { forest = 2 * leaves - cert.NSeed == nodes; log.WriteLine($"  forest identity 2L - nseed = {2 * leaves - cert.NSeed:N0} vs nodes {nodes:N0}: {(forest ? "OK" : "*** MISMATCH")}"); }
            else log.WriteLine("  forest identity: only checked on the full run (each processed subtree already ended exactly at its pre-walk bit position)");
            log.WriteLine($"  bit-stream desync/trailing-bit units {desync}  (nonzero padding {pad})");
            { var ta = new long[8]; for (int k = cLo; k < cHi; k++) if (done.TryGetValue(k, out var rr)) for (int q = 0; q < 8; q++) ta[q] += rr.TierAcc[q]; log.WriteLine($"  hull leaves accepted at tier 0/1/2: {ta[0]:N0} / {ta[1]:N0} / {ta[2]:N0}; failed after last tier: {ta[7]:N0}"); }
            log.WriteLine($"  failing leaves {fail:N0}  (angular-order-certificate failures {order:N0})");
            log.WriteLine($"  worst HULL-leaf INTERVAL slack above TauThr (lb.lo - TauThr): {worst:E6}");
            if (wbox != null) log.WriteLine("  worst leaf box (at the tier where it was accepted): " + BoxStr(wbox, 0));
            log.WriteLine($"  worst slack after re-evaluating the {fineN:N0} leaves with accepted slack < {FineThr:E0} at the finest tier N=4096 (max of accepted and fine LB): {worstFine:E6}");
            if (wfbox != null) log.WriteLine("  worst-fine leaf box: " + BoxStr(wfbox, 0));
            log.WriteLine($"  max erosion delta3 {md3:E6} delta5 {md5:E6};  min half-width over splits: translation {mhT:E6} rho {mhR:E6};  max stack depth {maxdepth}");
            log.WriteLine($"  leaf extents  t3x[{lo[0]:F12},{hi[0]:F12}] t3y[{lo[1]:F12},{hi[1]:F12}] rho[{lo[2]:F15},{hi[2]:F15}] t5x[{lo[3]:F12},{hi[3]:F12}] t5y[{lo[4]:F12},{hi[4]:F12}]");
            log.WriteLine($"  edge-refinement insertions {fb:N0} ({(double)fb / Math.Max(1, hull):F2} per hull leaf)");
            bool covOk = coverF == 0;
            log.WriteLine($"  interval child-covers-parent checks at every split (incl. seed splits and pre-walk): failures {coverF}  => {(covOk ? "OK" : "*** FAIL")}");
            if (firstFail != "") log.WriteLine("  first failure: " + firstFail);
            bool ok = fail == 0 && desync == 0 && forest && covOk;
            if (full) log.WriteLine("  (leaf extents above are informational bookkeeping in plain doubles; domain coverage is certified by the Iv split checks + Iv seed rho checks, not by them)");
            log.WriteLine("=".PadRight(100, '='));
            log.WriteLine(ok ? (full ? "RESULT VERIFIED  (interval mode)  a >= " + Hx(cert.Target) + " nodes " + nodes.ToString("N0") + " leaves " + leaves.ToString("N0") + " failing 0" : "RESULT: SLICE OK (not a full verification)") : "RESULT: VERIFICATION FAILED");
            return ok ? 0 : 1;
        }

        public static long ProfAdd, ProfFin;
        static int Bench(string[] a)
        {
            // bench <tau> <dumpfile> : loads LEAF boxes from a --dump file, times tier-0 evaluation with and without edge refinement
            Tau = double.Parse(a[1], CultureInfo.InvariantCulture); ClaimArg = "none"; TauThr = (Iv.Pt(Tau) + Iv.Ratio(1, 1000000000000L)).hi; D0 = ComputeD0(TauThr); D0sq = Iv.Sqr(Iv.Pt(D0)).hi;
            var boxes = new List<double[]>();
            foreach (var l in File.ReadLines(a[2])) if (l.StartsWith("LEAF ")) { var p = l.Split(' '); var s = p[2].Trim('[', ']').Split(','); var b = new double[10]; for (int i = 0; i < 10; i++) b[i] = double.Parse(s[i], CultureInfo.InvariantCulture); boxes.Add(b); }
            Console.WriteLine("boxes " + boxes.Count);
            var w = new Worker(); int mode; double d3, d5;
            foreach (double rml in new[] { 0.01, 1e9, 0.01, 1e9 })
            {
                w.Tiers[0].RefMinLen = rml; var sw = Stopwatch.StartNew(); int pass = 0; long npts = 0;
                for (int rep = 0; rep < 5; rep++) foreach (var b in boxes) { double lb = LeafBound(b, 0, w, out mode, out d3, out d5, 0); if (lb >= TauThr) pass++; npts += w.Cx.Cnt; }
                Console.WriteLine($"   [add {ProfAdd * 1e6 / Stopwatch.Frequency / (5.0 * boxes.Count):F1} us, finish {ProfFin * 1e6 / Stopwatch.Frequency / (5.0 * boxes.Count):F1} us]"); ProfAdd = ProfFin = 0;
                Console.WriteLine($"tier0 RefMinLen={rml}: {sw.Elapsed.TotalMilliseconds * 1000 / (5.0 * boxes.Count):F1} us/leaf  pass {pass}/{5 * boxes.Count}  avg pts {npts / (5.0 * boxes.Count):F0}");
            }
            // phases
            { var sw = Stopwatch.StartNew(); foreach (var b in boxes) for (int r = 0; r < 5; r++) { /* corners only: call with tier index out of range */ LeafBound(b, 0, w, out mode, out d3, out d5, 99); } Console.WriteLine($"setup only (radii, trig, corners): {sw.Elapsed.TotalMilliseconds * 1000 / (5.0 * boxes.Count):F2} us/leaf"); }
            return 0;
        }

        static int LeafCmd(string[] a)
        {
            // leaf <tau> <tier -1|0|1|2> <outfile> <10 box doubles>: evaluates one box (optionally only at one tier) and APPENDS the witness polygon in dump format
            Tau = double.Parse(a[1], CultureInfo.InvariantCulture); ClaimArg = "none"; TauThr = (Iv.Pt(Tau) + Iv.Ratio(1, 1000000000000L)).hi; D0 = ComputeD0(TauThr); D0sq = Iv.Sqr(Iv.Pt(D0)).hi; int only = int.Parse(a[2]);
            var b = new double[10]; for (int i = 0; i < 10; i++) b[i] = double.Parse(a[4 + i], CultureInfo.InvariantCulture);
            var w = new Worker(); int mode; double d3, d5;
            double lb = LeafBound(b, 0, w, out mode, out d3, out d5, only);
            Console.WriteLine($"mode={mode} LB={lb:R} slack={lb - TauThr:E6} d3={d3:R} d5={d5:R} npts={w.Cx?.Cnt}");
            if (mode == 2) { using var f = new StreamWriter(a[3], true); DumpLeaf(f, 0, b, 0, w, lb); }
            return 0;
        }

        static int Summarize(string[] a)
        {
            var cert = Cert.Load(a[1]);  HeaderChecks(cert, Console.Out);
            var plan = MakePlan(cert, int.Parse(Arg(a, "--threads", "6")), Console.Out);
            var done = new Dictionary<int, ChunkResult>(); foreach (var l in File.ReadLines(a[2])) if (l.StartsWith("C\t")) { var r = Parse(l); done[r.Idx] = r; }
            return Report(cert, done, plan, 0, plan.Jobs.Count, false, Console.Out);
        }
    }
}
