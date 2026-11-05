// Exhaustive enumeration of ALL dominating sets of exactly m squares of the n x n queens graph (dom: closed
// neighbourhoods; tdom: open). Squares are chosen in increasing index order; a branch is cut when the first
// undominated square cannot be dominated by any square with a larger index than the last pick, or when the number of
// undominated squares exceeds (picks left) * (max neighbourhood size). Each set is produced exactly once.
// Usage: EnumDom.exe n dom|tdom m outFile [minimalOnly 0|1]
using System;
using System.IO;

class EnumDom
{
    static int n, N, m, maxDeg; static bool minimalOnly;
    static ulong[] A, B;          // 128-bit masks (n <= 11) — this program is for N <= 128
    static int[][] nbr;           // closed/open neighbourhood lists
    static int[] maxIdx;          // largest index in nbr[u]
    static int[] pick; static long count; static StreamWriter w;

    static int Pop(ulong x) { int c = 0; while (x != 0) { x &= x - 1; c++; } return c; }

    static void Rec(int start, int depth, ulong c0, ulong c1)
    {
        ulong F0 = N >= 64 ? ulong.MaxValue : (1UL << N) - 1;
        ulong F1 = N > 64 ? (N >= 128 ? ulong.MaxValue : (1UL << (N - 64)) - 1) : 0;
        ulong u0 = ~c0 & F0, u1 = ~c1 & F1;
        if (depth == m) {
            if (u0 == 0 && u1 == 0) {
                if (minimalOnly && !IsMinimal()) return;
                count++;
                var parts = new string[m];
                for (int i = 0; i < m; i++) parts[i] = pick[i].ToString();
                w.WriteLine(string.Join(" ", parts));
            }
            return;
        }
        int unc = Pop(u0) + Pop(u1);
        if (unc > (m - depth) * maxDeg) return;
        int first = -1;
        if (u0 != 0) { first = 0; while (((u0 >> first) & 1) == 0) first++; }
        else if (u1 != 0) { first = 64; while (((u1 >> (first - 64)) & 1) == 0) first++; }
        if (first >= 0 && maxIdx[first] < start) return;   // nobody left can dominate 'first'
        for (int s = start; s < N; s++) {
            if (first >= 0) {
                // the next picks are all >= s; if s does not dominate 'first' and no later square can, stop
                if (maxIdx[first] < s) return;
            }
            pick[depth] = s;
            Rec(s + 1, depth + 1, c0 | A[s], c1 | B[s]);
        }
    }

    static bool IsMinimal()
    {
        for (int i = 0; i < m; i++) {
            ulong c0 = 0, c1 = 0;
            for (int j = 0; j < m; j++) if (j != i) { c0 |= A[pick[j]]; c1 |= B[pick[j]]; }
            ulong F0 = N >= 64 ? ulong.MaxValue : (1UL << N) - 1;
            ulong F1 = N > 64 ? (N >= 128 ? ulong.MaxValue : (1UL << (N - 64)) - 1) : 0;
            if ((c0 & F0) == F0 && (c1 & F1) == F1) return false;
        }
        return true;
    }

    static int Main(string[] args)
    {
        n = int.Parse(args[0]); string kind = args[1]; m = int.Parse(args[2]);
        minimalOnly = args.Length > 4 && args[4] == "1";
        N = n * n; if (N > 128) { Console.WriteLine("N > 128 not supported"); return 1; }
        A = new ulong[N]; B = new ulong[N]; nbr = new int[N][]; maxIdx = new int[N];
        for (int s = 0; s < N; s++) {
            var l = new System.Collections.Generic.List<int>();
            for (int t = 0; t < N; t++) {
                int r1 = s / n, c1 = s % n, r2 = t / n, c2 = t % n;
                bool a = s != t && (r1 == r2 || c1 == c2 || r1 - c1 == r2 - c2 || r1 + c1 == r2 + c2);
                if (a || (kind == "dom" && s == t)) {
                    if (t < 64) A[s] |= 1UL << t; else B[s] |= 1UL << (t - 64);
                    l.Add(t);
                }
            }
            nbr[s] = l.ToArray();
        }
        maxDeg = 0;
        for (int u = 0; u < N; u++) { maxDeg = Math.Max(maxDeg, nbr[u].Length); int mx = -1; foreach (int s in nbr[u]) mx = Math.Max(mx, s); maxIdx[u] = mx; }
        // note: domination is symmetric (s dominates u iff u dominates s), so nbr[u] = squares dominating u
        pick = new int[m];
        var sw = System.Diagnostics.Stopwatch.StartNew();
        using (w = new StreamWriter(args[3])) Rec(0, 0, 0, 0);
        Console.WriteLine("n={0} kind={1} m={2} minimalOnly={3} count={4} time={5:F1}s", n, kind, m, minimalOnly, count, sw.Elapsed.TotalSeconds);
        return 0;
    }
}
