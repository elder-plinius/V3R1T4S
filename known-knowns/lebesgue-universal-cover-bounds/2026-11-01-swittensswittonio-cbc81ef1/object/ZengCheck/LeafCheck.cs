using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

public sealed class LeafResult {
    public int variant; public int[] cand;
    public bool pass; public string kind; public double lower = double.NegativeInfinity; public int cands; public int hull; public int used;
    public string note;
}

public sealed class Checker {
    public static bool Dbg = Environment.GetEnvironmentVariable("ZC_DEBUG") == "1";
    readonly Tables T; readonly double tauHi; public double Tau;  // tauHi >= tau (upward rounded), pass needs lower > tauHi
    public Checker(Tables t, double tau) { T = t; Tau = tau; tauHi = Math.BitIncrement(tau); }

    // exact-decimal text -> enclosure of the real number denoted by the text
    static Iv Enc(string text, bool zeroExact = true) {
        double d = double.Parse(text, CultureInfo.InvariantCulture);
        if (d == 0) return Iv.P(0);
        return new Iv(Math.BitDecrement(d), Math.BitIncrement(d));
    }
    // box coordinate interval; angle coordinates get the pi-bridge on a top endpoint equal to the recorded float(pi/n) text
    Iv Coord(string lo, string hi, double angleTopUp, string angleTopText) {
        var a = Enc(lo); var b = Enc(hi);
        double l = a.lo; if (l < 0 && double.Parse(lo, CultureInfo.InvariantCulture) >= 0) l = Math.Max(l, 0);
        double h = b.hi;
        if (angleTopText != null && hi == angleTopText) h = angleTopUp;   // bridge: float(pi/n) endpoint stands for the true pi/n
        return new Iv(l, h);
    }
    static P2 Pt2(Pt p) => new P2(p.x, p.y);

    // ---------- one-body collar leaf (r, theta) ----------
    public LeafResult OneBody(Leaf L, int n) {
        var res = new LeafResult();
        string topText = n == 3 ? "1.0471975511965976" : "0.6283185307179586"; double topUp = n == 3 ? T.Pi3Up : T.Pi5Up;
        var R = Coord(L.lo[0], L.hi[0], 0, null); var TH = Coord(L.lo[1], L.hi[1], topUp, topText);
        if (!T.sets.TryGetValue(("disk", 0, L.disk), out var disk) || !T.sets.TryGetValue(("reul", n, L.r3), out var reul)) { res.note = "no table for sample config"; return res; }
        // centre c = (r cos th, r sin th) over the box
        Iv cx = R * Iv.Cos(TH), cy = R * Iv.Sin(TH);
        // float centre for hull heuristic
        double rc = 0.5 * (R.lo + R.hi), tc = 0.5 * (TH.lo + TH.hi); double fx = rc * Math.Cos(tc), fy = rc * Math.Sin(tc);
        int N = disk.Length + reul.Length; var xs = new double[N]; var ys = new double[N];
        for (int i = 0; i < disk.Length; i++) { xs[i] = disk[i].mx; ys[i] = disk[i].my; }
        for (int i = 0; i < reul.Length; i++) { xs[disk.Length + i] = fx + reul[i].mx; ys[disk.Length + i] = fy + reul[i].my; }
        var hull = Geo.Hull(xs, ys, N, new int[N], null); res.hull = hull.Length;
        var poly = new P2[hull.Length];
        for (int k = 0; k < hull.Length; k++) { int i = hull[k]; poly[k] = i < disk.Length ? Pt2(disk[i]) : new P2(cx + reul[i - disk.Length].x, cy + reul[i - disk.Length].y); }
        // PASS_ONEBODY_INNER_POLYGON-style: simple (interval-certified) polygon with interval shoelace lower bound > tau
        var S = Geo.SignedArea(poly); res.lower = S.lo; res.cands = 1;
        if (Dbg) Console.WriteLine("hullclass " + string.Concat(hull.Select(i => i < disk.Length ? "D" : "R")) + " idx " + string.Join(",", hull));
        if (Dbg) Console.WriteLine($"onebody hull={hull.Length} nd={disk.Length} nr={reul.Length} S={S} cx={cx} cy={cy} R={R} TH={TH}");
        if (S.lo > tauHi && Geo.SimpleCert(poly)) { res.pass = true; res.kind = "onebody_inner_polygon"; return res; }
        // fallback: greedy vertex removal on the hull polygon (any subsequence of the hull vertices is a legitimate witness polygon; it is
        // re-certified from scratch: interval shoelace + interval simplicity).
        var cur = new List<P2>(poly);
        for (int it = 0; it < 12; it++) {
            double best = double.NegativeInfinity; int bk = -1;
            for (int k = 0; k < cur.Count; k++) {
                var q = new List<P2>(cur); q.RemoveAt(k); if (q.Count < 3) continue;
                double lo = Geo.SignedArea(q.ToArray()).lo; if (lo > best) { best = lo; bk = k; }
            }
            if (bk < 0) break;
            cur.RemoveAt(bk); res.cands++;
            if (best > res.lower) res.lower = best;
            if (best > tauHi && Geo.SimpleCert(cur.ToArray())) { res.pass = true; res.kind = "onebody_inner_polygon_pruned"; res.used = cur.Count; return res; }
        }
        res.note = "area bound too low / simple not certified";
        return res;
    }

    // ---------- core5d leaf ----------
    sealed class Ctx {
        public Pt[] disk, r3, r5; public int nd, n3, n5, N;
        public double[] xs, ys;                 // float centre points
        public Iv cx3, cy3, cpsiC, cpsiS;       // centre (point) translations as Iv points, cos/sin of centre psi
        public Iv X3, Y3, PSI, X5, Y5, CB, SB;  // box intervals, cos/sin of psi box
        public double[] rad = new double[5];    // half-widths (upper bounds)
        public double c3x, c3y, cps, c5x, c5y;  // centre doubles
        public Iv wTrans3, wTrans5, wPsi;
    }
    P2 BoxPt(Ctx c, int i) {
        if (i < c.nd) return Pt2(c.disk[i]);
        i -= c.nd;
        if (i < c.n3) return new P2(c.X3 + c.r3[i].x, c.Y3 + c.r3[i].y);
        i -= c.n3; var q = c.r5[i];
        return new P2(c.X5 + (q.x * c.CB - q.y * c.SB), c.Y5 + (q.x * c.SB + q.y * c.CB));
    }
    P2 CenPt(Ctx c, int i) {
        if (i < c.nd) return Pt2(c.disk[i]);
        i -= c.nd;
        if (i < c.n3) return new P2(c.cx3 + c.r3[i].x, c.cy3 + c.r3[i].y);
        i -= c.n3; var q = c.r5[i];
        return new P2(Iv.P(c.c5x) + (q.x * c.cpsiC - q.y * c.cpsiS), Iv.P(c.c5y) + (q.x * c.cpsiS + q.y * c.cpsiC));
    }
    Iv Eps(Ctx c, int i) {
        if (i < c.nd) return Iv.P(0);
        i -= c.nd; if (i < c.n3) return c.wTrans3;
        i -= c.n3; var q = c.r5[i]; Iv nq = Iv.Sqrt(Iv.Sqr(q.x) + Iv.Sqr(q.y));
        return c.wTrans5 + nq * c.wPsi;
    }

    public LeafResult Core(Leaf L) {
        var r0 = CoreV(L, 0);
        if (r0.pass || T.sets1 == null) return r0;
        var r1 = CoreV(L, 1);
        if (r1.pass) { r1.kind += "+altset"; r1.cands += r0.cands; return r1; }
        r0.cands += r1.cands; return r0;
    }
    LeafResult CoreV(Leaf L, int variant) {
        var res = new LeafResult();
        var S = variant == 0 ? T.sets : T.sets1;
        if (!S.TryGetValue(("disk", 0, L.disk), out var disk) || !S.TryGetValue(("reul", 3, L.r3), out var r3) || !S.TryGetValue(("reul", 5, L.r5), out var r5)) { res.note = "no table for sample config"; return res; }
        var c = new Ctx { disk = disk, r3 = r3, r5 = r5, nd = disk.Length, n3 = r3.Length, n5 = r5.Length };
        c.N = c.nd + c.n3 + c.n5;
        c.X3 = Coord(L.lo[0], L.hi[0], 0, null); c.Y3 = Coord(L.lo[1], L.hi[1], 0, null);
        c.PSI = Coord(L.lo[2], L.hi[2], T.Pi5Up, "0.6283185307179586");
        c.X5 = Coord(L.lo[3], L.hi[3], 0, null); c.Y5 = Coord(L.lo[4], L.hi[4], 0, null);
        double Raw(string t) => double.Parse(t, CultureInfo.InvariantCulture);
        c.c3x = (Raw(L.lo[0]) + Raw(L.hi[0])) / 2.0; c.c3y = (Raw(L.lo[1]) + Raw(L.hi[1])) / 2.0; c.cps = (Raw(L.lo[2]) + Raw(L.hi[2])) / 2.0;
        c.c5x = (Raw(L.lo[3]) + Raw(L.hi[3])) / 2.0; c.c5y = (Raw(L.lo[4]) + Raw(L.hi[4])) / 2.0;
        c.cx3 = Iv.P(c.c3x); c.cy3 = Iv.P(c.c3y); c.cpsiC = Iv.CosPt(c.cps); c.cpsiS = Iv.SinPt(c.cps);
        c.CB = Iv.Cos(c.PSI); c.SB = Iv.Sin(c.PSI);
        Iv[] bx = { c.X3, c.Y3, c.PSI, c.X5, c.Y5 }; double[] cen = { c.c3x, c.c3y, c.cps, c.c5x, c.c5y };
        for (int k = 0; k < 5; k++) {
            Iv a1 = new Iv(bx[k].hi, bx[k].hi) - Iv.P(cen[k]); Iv b1 = Iv.P(cen[k]) - new Iv(bx[k].lo, bx[k].lo);
            c.rad[k] = Math.Max(0.0, Math.Max(a1.hi, b1.hi));   // rigorous upper bound of max |z_k - c_k| over the box
        }
        Iv[] rI = new Iv[5]; for (int k = 0; k < 5; k++) rI[k] = Iv.P(c.rad[k]);
        c.wTrans3 = Iv.P(Iv.Sqrt(Iv.Sqr(rI[0]) + Iv.Sqr(rI[1])).hi); c.wTrans5 = Iv.P(Iv.Sqrt(Iv.Sqr(rI[3]) + Iv.Sqr(rI[4])).hi); c.wPsi = rI[2];
        // float centre cloud and hull
        c.xs = new double[c.N]; c.ys = new double[c.N];
        double cf = Math.Cos(c.cps), sf = Math.Sin(c.cps);
        for (int i = 0; i < c.nd; i++) { c.xs[i] = disk[i].mx; c.ys[i] = disk[i].my; }
        for (int i = 0; i < c.n3; i++) { c.xs[c.nd + i] = c.c3x + r3[i].mx; c.ys[c.nd + i] = c.c3y + r3[i].my; }
        for (int i = 0; i < c.n5; i++) { double qx = r5[i].mx, qy = r5[i].my; c.xs[c.nd + c.n3 + i] = c.c5x + (qx * cf - qy * sf); c.ys[c.nd + c.n3 + i] = c.c5y + (qx * sf + qy * cf); }
        var hull = Geo.Hull(c.xs, c.ys, c.N, new int[c.N], null); res.hull = hull.Length;
        if (hull.Length < 3) { res.note = "hull too small"; return res; }
        var seen = new HashSet<string>();
        // 1) direct inner polygon on the full hull
        var polyB = new P2[hull.Length]; for (int k = 0; k < hull.Length; k++) polyB[k] = BoxPt(c, hull[k]);
        var S0 = Geo.SignedArea(polyB); res.lower = S0.lo; res.cands = 1;
        if (S0.lo > tauHi && Geo.SimpleCert(polyB)) { res.pass = true; res.kind = "inner_polygon"; res.used = hull.Length; res.cand = hull; res.variant = variant; return res; }
        // 2) templates: candidate vertex subsets of the centre hull, each certified by perturbation / mean-value bound + (convex | simple)
        int hint = L.hullHint;
        int npass = hint > 0 ? 3 : 1;
        for (int pass = 0; pass < npass && !res.pass; pass++) {
            int szLo = 0, szHi = int.MaxValue, extraOff = 0;
            if (hint > 0) { if (pass == 0) { szLo = szHi = hint; } else if (pass == 1) { szLo = hint - 6; szHi = hint + 6; extraOff = 8; } else extraOff = 8; }
            else extraOff = 0;
            foreach (var cand in Candidates(c, hull, szLo, szHi, extraOff)) {
                string key = string.Join(",", cand);
                if (!seen.Add(key)) continue;
                res.cands++;
                var r = EvalTemplate(c, cand);
                if (r.lower > res.lower) res.lower = r.lower;
                if (r.pass) { res.pass = true; res.kind = r.kind; res.used = cand.Length; res.lower = r.lower; res.cand = cand; res.variant = variant; return res; }
            }
        }
        if (Dbg) Console.WriteLine($"  hull={hull.Length}");
        res.note = "no certified template"; return res;
    }

    IEnumerable<int[]> Candidates(Ctx c, int[] hull, int szLo, int szHi, int extraOff) {
        int h = hull.Length;
        // (a) even cyclic subsamples
        var counts = new SortedSet<int>(); foreach (int b in new[] { 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 48, 56, 64, h }) if (b >= 3 && b <= h) counts.Add(b);
        if (extraOff > 0 && szHi != int.MaxValue) for (int cnt = Math.Max(3, szLo); cnt <= Math.Min(h, szHi); cnt++) counts.Add(cnt);
        foreach (int count in counts) {
            if (count < szLo || count > szHi) continue;
            int noff = count >= h ? 1 : Math.Max(1, h / count) + extraOff;
            for (int off = 0; off < noff; off++) yield return Even(hull, count, off);
        }
        // (b) remove the vertices with smallest centre triangle loss
        var cp = new double[h][]; for (int i = 0; i < h; i++) cp[i] = new[] { c.xs[hull[i]], c.ys[hull[i]] };
        var loss = new List<(double, int)>();
        for (int i = 0; i < h; i++) {
            var p = cp[(i + h - 1) % h]; var q = cp[i]; var n = cp[(i + 1) % h];
            loss.Add((Math.Abs((q[0] - p[0]) * (n[1] - q[1]) - (q[1] - p[1]) * (n[0] - q[0])) / 2, i));
        }
        loss.Sort();
        var sc = new SortedSet<int>(Comparer<int>.Create((a, b) => b.CompareTo(a)));
        foreach (int b in new[] { 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160, 192, 256, h / 3, h / 2, 2 * h / 3, 3 * h / 4, 7 * h / 8 }) if (b >= 3 && b < h) sc.Add(b);
        foreach (int count in sc) {
            if (count < szLo || count > szHi) continue;
            var rem = new HashSet<int>(); for (int i = 0; i < h - count; i++) rem.Add(loss[i].Item2);
            var cand = new List<int>(); for (int i = 0; i < h; i++) if (!rem.Contains(i)) cand.Add(hull[i]);
            if (cand.Count >= 3) yield return cand.ToArray();
        }
        // (c) near-full templates: remove the vertices with the worst centre turn margin
        var eps = new double[h]; for (int i = 0; i < h; i++) eps[i] = Eps(c, hull[i]).hi;
        var marg = new List<(double, int)>();
        for (int i = 0; i < h; i++) {
            var p = cp[(i + h - 1) % h]; var q = cp[i]; var n = cp[(i + 1) % h];
            double ax = q[0] - p[0], ay = q[1] - p[1], bx = n[0] - q[0], by = n[1] - q[1];
            double ea = eps[i] + eps[(i + h - 1) % h], eb = eps[(i + 1) % h] + eps[i];
            marg.Add((ax * by - ay * bx - (ea * Math.Sqrt(bx * bx + by * by) + eb * Math.Sqrt(ax * ax + ay * ay) + ea * eb), i));
        }
        marg.Sort();
        foreach (int rm in new[] { 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256 }) {
            int count = h - rm; if (count < 3 || count >= h) continue;
            if (count < szLo || count > szHi) continue;
            var rem = new HashSet<int>(); for (int i = 0; i < rm; i++) rem.Add(marg[i].Item2);
            var cand = new List<int>(); for (int i = 0; i < h; i++) if (!rem.Contains(i)) cand.Add(hull[i]);
            if (cand.Count >= 3) yield return cand.ToArray();
        }
    }
    // Rotation index of the edge-direction map of the centre polygon equals 1: with all turns strictly positive (certified above) each step rotates
    // the direction counter-clockwise by an angle in (0,pi); the total turning is 2*pi*(number of crossings of the positive x-axis ray), i.e. the number of
    // steps from an edge with y<0 to an edge with y>0. Signs of edge y-components must be strictly certified by the interval enclosure.
    static bool RotIndexOne(P2[] v) {
        int m = v.Length; var sg = new int[m];
        for (int i = 0; i < m; i++) { var a = v[i]; var b = v[(i + 1) % m]; Iv ey = b.y - a.y; sg[i] = ey.lo > 0 ? 1 : ey.hi < 0 ? -1 : 0; if (sg[i] == 0) return false; }
        int cross = 0; for (int i = 0; i < m; i++) if (sg[i] < 0 && sg[(i + 1) % m] > 0) cross++;
        return cross == 1;
    }
    static int[] Even(int[] hull, int count, int offset) {
        int n = hull.Length; if (count >= n) return hull;
        var chosen = new List<int>(); var used = new HashSet<int>();
        for (int k = 0; k < count; k++) { int pos = (int)((offset + (long)k * n / count) % n); if (used.Add(pos)) chosen.Add(hull[pos]); }
        return chosen.Count >= 3 ? chosen.ToArray() : hull;
    }

    (bool pass, double lower, string kind) EvalTemplate(Ctx c, int[] cand) {
        int m = cand.Length;
        var vb = new P2[m]; var vc = new P2[m]; var eps = new Iv[m];
        for (int i = 0; i < m; i++) { vb[i] = BoxPt(c, cand[i]); vc[i] = CenPt(c, cand[i]); eps[i] = Eps(c, cand[i]); }
        Iv Sc = Geo.SignedArea(vc);
        // perturbation bound: S(z) >= S(c) - E,  E = sum eps_i |v_{i+1}-v_{i-1}|/2 + sum eps_i eps_{i+1}/2
        Iv E = Iv.P(0);
        for (int i = 0; i < m; i++) {
            var a = vc[(i + 1) % m]; var b = vc[(i + m - 1) % m];
            Iv chord = Iv.Sqrt(Iv.Sqr(a.x - b.x) + Iv.Sqr(a.y - b.y));
            E = E + Iv.Half(eps[i] * chord) + Iv.Half(eps[i] * eps[(i + 1) % m]);
        }
        double lowPert = (Sc - E).lo;
        // mean-value bound: S(z) >= S(c) - sum_k G_k r_k ; G_k >= sup |dS/dz_k| over the box
        Iv[] D = new Iv[5]; for (int k = 0; k < 5; k++) D[k] = Iv.P(0);
        for (int i = 0; i < m; i++) {
            int idx = cand[i]; if (idx < c.nd) continue;
            var nx = vb[(i + 1) % m]; var pv = vb[(i + m - 1) % m];
            Iv dx = nx.x - pv.x, dy = nx.y - pv.y;
            if (idx < c.nd + c.n3) { D[0] = D[0] + Iv.Half(dy); D[1] = D[1] - Iv.Half(dx); }
            else {
                D[3] = D[3] + Iv.Half(dy); D[4] = D[4] - Iv.Half(dx);
                var q = c.r5[idx - c.nd - c.n3];
                Iv ddx = -(c.SB * q.x) - c.CB * q.y, ddy = c.CB * q.x - c.SB * q.y;   // d/dpsi of rotated local point
                D[2] = D[2] + Iv.Half(ddx * dy - ddy * dx);
            }
        }
        Iv var_ = Iv.P(0);
        for (int k = 0; k < 5; k++) var_ = var_ + Iv.P(Math.BitIncrement(D[k].MaxAbs)) * Iv.P(c.rad[k]);
        double lowMV = (Sc - var_).lo;
        var Sb = Geo.SignedArea(vb); double lowDirect = Sb.lo;
        double lower = Math.Max(lowDirect, Math.Max(lowPert, lowMV));
        if (Dbg) Console.WriteLine($"  cand m={m} lower={lower:R} pert={lowPert:R} mv={lowMV:R} direct={lowDirect:R}");
        if (!(lower > tauHi)) return (false, lower, null);
        // convexity certificate from turn margins over displacement balls (centre polygon strictly convex, index 1 by construction of the hull)
        bool convex = true;
        for (int i = 0; i < m && convex; i++) {
            var p = vc[(i + m - 1) % m]; var q = vc[i]; var n = vc[(i + 1) % m];
            Iv ax = q.x - p.x, ay = q.y - p.y, bx2 = n.x - q.x, by2 = n.y - q.y;
            Iv ea = eps[i] + eps[(i + m - 1) % m], eb = eps[(i + 1) % m] + eps[i];
            Iv turn = ax * by2 - ay * bx2;
            Iv err = ea * Iv.Sqrt(Iv.Sqr(bx2) + Iv.Sqr(by2)) + eb * Iv.Sqrt(Iv.Sqr(ax) + Iv.Sqr(ay)) + ea * eb;
            if (!((turn - err).lo > 0)) convex = false;
        }
        if (convex && !RotIndexOne(vc)) convex = false;
        if (Dbg) Console.WriteLine($"    convex={convex}");
        if (convex) return (true, lower, lower == lowPert ? "template_convex_perturbation" : lower == lowMV ? "template_convex_meanvalue" : "template_convex_direct");
        if (Geo.SimpleCert(vb)) return (true, lower, lower == lowMV ? "template_simple_meanvalue" : lower == lowPert ? "template_simple_perturbation" : "template_simple_direct");
        return (false, lower, null);
    }
}
