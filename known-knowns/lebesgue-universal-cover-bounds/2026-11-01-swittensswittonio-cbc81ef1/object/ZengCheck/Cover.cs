using System;
using System.Collections.Generic;
using System.Numerics;

// Exact partition check of a set of boxes (scaled integer endpoints) against a root cell: recursive separating-plane recovery.
// partition(C,S): |S|==1 => box must EQUAL C; else find axis a and value v, lo_a(C) < v < hi_a(C), such that every box of S lies
// entirely in {x_a <= v} or {x_a >= v}; both sides must be non-empty; recurse on (C cut, S side). All comparisons exact (Int128).
public static class Cover {
    public sealed class Res { public bool ok; public string err; public long nodes; public BigInteger volSum, volRoot; }

    public static Res Partition(Int128[][] lo, Int128[][] hi, Int128[] rootLo, Int128[] rootHi) {
        int D = rootLo.Length, n = lo.Length; var R = new Res();
        for (int d = 0; d < D; d++) if (rootHi[d] <= rootLo[d]) { R.err = "degenerate root"; return R; }
        R.volRoot = Vol(rootLo, rootHi);
        for (int i = 0; i < n; i++) {
            BigInteger v = BigInteger.One;
            for (int d = 0; d < D; d++) {
                if (hi[i][d] <= lo[i][d]) { R.err = $"leaf {i} non-positive width axis {d}"; return R; }
                if (lo[i][d] < rootLo[d] || hi[i][d] > rootHi[d]) { R.err = $"leaf {i} outside root axis {d}"; return R; }
            }
            R.volSum += Vol(lo[i], hi[i]);
        }
        if (R.volSum != R.volRoot) { R.err = $"volume mismatch sum!=root"; return R; }
        // presorted index arrays per axis (by lo)
        var perm = new int[D][];
        for (int d = 0; d < D; d++) {
            var p = new int[n]; for (int i = 0; i < n; i++) p[i] = i; int dd = d;
            Array.Sort(p, (a, b) => lo[a][dd].CompareTo(lo[b][dd])); perm[d] = p;
        }
        var stack = new Stack<(int s, int e, Int128[] cl, Int128[] ch)>();
        // we keep every perm[d] segment [s,e) holding the same set of boxes (each sorted by lo_d)
        stack.Push((0, n, (Int128[])rootLo.Clone(), (Int128[])rootHi.Clone()));
        var side = new byte[n]; var tmp = new int[n];
        while (stack.Count > 0) {
            var (s, e, cl, ch) = stack.Pop(); R.nodes++;
            int cnt = e - s;
            if (cnt == 0) { R.err = "empty cell (gap)"; return R; }
            if (cnt == 1) {
                int b = perm[0][s];
                for (int d = 0; d < D; d++) if (lo[b][d] != cl[d] || hi[b][d] != ch[d]) { R.err = $"singleton box != cell (axis {d})"; return R; }
                continue;
            }
            int cutAxis = -1; Int128 cutV = default; int cutPos = -1;
            for (int d = 0; d < D && cutAxis < 0; d++) {
                var p = perm[d]; Int128 maxHi = hi[p[s]][d];
                for (int q = s + 1; q < e; q++) {
                    int b = p[q]; Int128 l = lo[b][d];
                    if (l > lo[p[q - 1]][d]) {          // candidate cut v = l (strictly greater than previous los)
                        if (maxHi <= l && l > cl[d] && l < ch[d]) { cutAxis = d; cutV = l; cutPos = q; break; }
                    }
                    if (hi[b][d] > maxHi) maxHi = hi[b][d];
                }
            }
            if (cutAxis < 0) { R.err = "no separating plane (overlap or irregular cell)"; return R; }
            // mark sides using the cut axis sorted order: positions [s,cutPos) are left, [cutPos,e) right
            var pa = perm[cutAxis];
            for (int q = s; q < e; q++) side[pa[q]] = (byte)(q < cutPos ? 1 : 2);
            for (int d = 0; d < D; d++) {
                if (d == cutAxis) continue;
                var p = perm[d]; int l = s, r = s + (cutPos - s); int k = 0;
                // stable partition into tmp then back
                int li = s, ri = cutPos;
                for (int q = s; q < e; q++) { int b = p[q]; if (side[b] == 1) tmp[li++] = b; else tmp[ri++] = b; }
                Array.Copy(tmp, s, p, s, cnt);
            }
            var cl2 = (Int128[])cl.Clone(); var ch1 = (Int128[])ch.Clone(); ch1[cutAxis] = cutV; cl2[cutAxis] = cutV;
            stack.Push((cutPos, e, cl2, ch)); stack.Push((s, cutPos, cl, ch1));
        }
        R.ok = true; return R;
    }
    static BigInteger Vol(Int128[] lo, Int128[] hi) { BigInteger v = BigInteger.One; for (int d = 0; d < lo.Length; d++) v *= (BigInteger)(hi[d] - lo[d]); return v; }
}
