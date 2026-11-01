using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;

public struct Pt { public Iv x, y; public double mx, my; }

public sealed class Tables {
    public Dictionary<(string, int, int), Pt[]> sets = new();           // ("disk",0,s) / ("reul",n,s)
    public Dictionary<(string, int, int), Pt[]> sets1 = null;           // variant 1: same sets minus the near-vertex samples the author's code drops (completeness heuristic only)
    public Dictionary<int, Pt[]> centers = new();                        // n -> centers (enclosures)
    public double Pi5Up, Pi3Up, Pi5Lo, Pi3Lo;
    public int membershipRejectedByCs = 0;
    public void LoadExclusions(string jsonPath) {
        sets1 = new();
        var doc = System.Text.Json.JsonDocument.Parse(File.ReadAllText(jsonPath));
        foreach (var kv in sets) {
            var pts = kv.Value;
            if (kv.Key.Item1 == "reul" && doc.RootElement.TryGetProperty($"{kv.Key.Item2},{kv.Key.Item3}", out var e)) {
                var drop = new HashSet<int>(); foreach (var d in e.GetProperty("drop_indices").EnumerateArray()) drop.Add(d.GetInt32());
                var l = new List<Pt>(); for (int i = 0; i < pts.Length; i++) if (!drop.Contains(i)) l.Add(pts[i]); pts = l.ToArray();
            }
            sets1[kv.Key] = pts;
        }
    }
    public static Tables Load(string path) {
        var T = new Tables();
        using var sr = new StreamReader(path);
        string line;
        while ((line = sr.ReadLine()) != null) {
            var f = line.Split(' ');
            if (f[0] == "const") {
                T.Pi5Up = double.Parse(f[2], CultureInfo.InvariantCulture); T.Pi3Up = double.Parse(f[4], CultureInfo.InvariantCulture);
                T.Pi5Lo = double.Parse(f[6], CultureInfo.InvariantCulture); T.Pi3Lo = double.Parse(f[8], CultureInfo.InvariantCulture); continue;
            }
            if (f[0] == "cent") {
                int n = int.Parse(f[1]); int cnt = int.Parse(f[2]); var arr = new Pt[cnt];
                for (int i = 0; i < cnt; i++) arr[i] = ReadPt(sr.ReadLine());
                T.centers[n] = arr; continue;
            }
            int a = int.Parse(f[1]), s = int.Parse(f[2]), c = int.Parse(f[3]);
            var pts = new Pt[c];
            for (int i = 0; i < c; i++) pts[i] = ReadPt(sr.ReadLine());
            T.sets[(f[0], a, s)] = pts;
        }
        // independent C# membership recheck of every Reuleaux sample: upper bound of |p-c_i|^2 <= 1 for all vertices c_i
        foreach (var kv in T.sets) {
            if (kv.Key.Item1 != "reul") continue;
            var cs = T.centers[kv.Key.Item2];
            foreach (var p in kv.Value)
                foreach (var c in cs) {
                    Iv d2 = Iv.Sqr(p.x - c.x) + Iv.Sqr(p.y - c.y);
                    if (!(d2.hi <= 1.0)) throw new Exception($"membership recheck failed for {kv.Key}");
                }
        }
        return T;
    }
    static Pt ReadPt(string l) {
        var g = l.Split(' ');
        var p = new Pt { x = new Iv(double.Parse(g[0], CultureInfo.InvariantCulture), double.Parse(g[1], CultureInfo.InvariantCulture)),
                         y = new Iv(double.Parse(g[2], CultureInfo.InvariantCulture), double.Parse(g[3], CultureInfo.InvariantCulture)) };
        p.mx = double.Parse(g[4], CultureInfo.InvariantCulture); p.my = double.Parse(g[5], CultureInfo.InvariantCulture); return p;
    }
}

public static class Geo {
    // Andrew monotone chain on double midpoints; returns indices of a counter-clockwise polygon (strict turns). Heuristic only: the
    // output polygon is certified afterwards by interval predicates, so hull errors can only cost completeness, never soundness.
    public static int[] Hull(double[] xs, double[] ys, int n, int[] order, double[] tmp) {
        for (int i = 0; i < n; i++) order[i] = i;
        Array.Sort(order, 0, n, new XYCmp(xs, ys));
        var h = new int[2 * n + 2]; int k = 0;
        for (int ii = 0; ii < n; ii++) {
            int i = order[ii];
            while (k >= 2 && Cross(xs, ys, h[k - 2], h[k - 1], i) <= 0) k--;
            h[k++] = i;
        }
        int lower = k + 1;
        for (int ii = n - 2; ii >= 0; ii--) {
            int i = order[ii];
            while (k >= lower && Cross(xs, ys, h[k - 2], h[k - 1], i) <= 0) k--;
            h[k++] = i;
        }
        var res = new int[k - 1]; Array.Copy(h, res, k - 1); return res;
    }
    static double Cross(double[] xs, double[] ys, int o, int a, int b) => (xs[a] - xs[o]) * (ys[b] - ys[o]) - (ys[a] - ys[o]) * (xs[b] - xs[o]);
    sealed class XYCmp : IComparer<int> {
        double[] x, y; public XYCmp(double[] x, double[] y) { this.x = x; this.y = y; }
        public int Compare(int a, int b) { int c = x[a].CompareTo(x[b]); if (c != 0) return c; c = y[a].CompareTo(y[b]); return c != 0 ? c : a.CompareTo(b); }
    }

    public static Iv Cross(Iv ax, Iv ay, Iv bx, Iv by) => ax * by - ay * bx;
    public static Iv Det(in P2 a, in P2 b, in P2 c) => (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    static bool SameStrictSign(Iv a, Iv b) => (a.lo > 0 && b.lo > 0) || (a.hi < 0 && b.hi < 0);

    public static Iv SignedArea(P2[] v) {
        Iv s = Iv.P(0); int n = v.Length;
        for (int i = 0; i < n; i++) { var p = v[i]; var q = v[(i + 1) % n]; s = s + (p.x * q.y - q.x * p.y); }
        return Iv.Half(s);
    }

    // Interval certificate that the closed polygon with vertices ranging over the boxes v[i] has pairwise disjoint non-adjacent edges for
    // EVERY choice of vertices (disjointness: bbox separation, or both endpoints of one edge strictly on one side of the line of the other).
    public static bool SimpleCert(P2[] v) {
        int n = v.Length; if (n < 3) return false;
        var xl = new double[n]; var xh = new double[n]; var yl = new double[n]; var yh = new double[n];
        for (int i = 0; i < n; i++) {
            var a = v[i]; var b = v[(i + 1) % n];
            xl[i] = Math.Min(a.x.lo, b.x.lo); xh[i] = Math.Max(a.x.hi, b.x.hi);
            yl[i] = Math.Min(a.y.lo, b.y.lo); yh[i] = Math.Max(a.y.hi, b.y.hi);
        }
        var ord = new int[n]; for (int i = 0; i < n; i++) ord[i] = i;
        Array.Sort(ord, (p, q) => xl[p].CompareTo(xl[q]));
        for (int u = 0; u < n; u++) {
            int i = ord[u];
            for (int w = u + 1; w < n; w++) {
                int j = ord[w];
                if (xl[j] > xh[i]) break;                       // bbox x-disjoint (strict) for all later edges too (sorted by xl)
                if (yl[j] > yh[i] || yl[i] > yh[j]) continue;   // bbox y-disjoint
                if (j == (i + 1) % n || i == (j + 1) % n) continue; // adjacent edges share a vertex
                var a = v[i]; var b = v[(i + 1) % n]; var c = v[j]; var d = v[(j + 1) % n];
                if (SameStrictSign(Det(a, b, c), Det(a, b, d))) continue;
                if (SameStrictSign(Det(c, d, a), Det(c, d, b))) continue;
                return false;
            }
        }
        return true;
    }
}
public struct P2 { public Iv x, y; public P2(Iv x, Iv y) { this.x = x; this.y = y; } }
