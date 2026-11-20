// Exhaustive enumeration of all MINIMAL dominating sets of exactly m squares of the n x n queens graph.
// Method (different from EnumDom/EnumDom2/EnumDom3, which pick squares in increasing index order): branch on an
// undominated square u. Some member of the set must lie in N[u]; try each d in N[u] that is not forbidden, and after
// trying d forbid it for the later branches of this node (and everything below them). A set S is then reached
// along exactly one path: at each node the branch taken is the first allowed member of S in N[u]. If everything is
// dominated before m picks, the branch is dropped (a dominating set with fewer than m squares has no minimal
// superset of size m). Leaves are tested for minimality.
// rule 0: u = first undominated square; rule 1: u = undominated square with the fewest allowed dominators.
// Usage: EnumCovK.exe n m outFile rule [tdom]   (tdom: open neighbourhoods, total domination)
using System;
using System.IO;
using System.Collections.Generic;

class EnumCovK
{
    static int n, N, m, maxDeg, rule;
    static ulong[] A, B, C;   // closed neighbourhood masks, 3 words (N <= 192)
    static ulong F0, F1, F2;
    static int[] pick; static long count, nodes; static StreamWriter w;
    static System.Diagnostics.Stopwatch sw; static long nextReport; static int reportEvery;

    static int Pop(ulong x)
    {
        x = x - ((x >> 1) & 0x5555555555555555UL);
        x = (x & 0x3333333333333333UL) + ((x >> 2) & 0x3333333333333333UL);
        x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0FUL;
        return (int)((x * 0x0101010101010101UL) >> 56);
    }
    static int Low(ulong x) { int i = 0; while (((x >> i) & 1) == 0) i++; return i; }

    static void Leaf()
    {
        // minimality: removing any one pick must leave some square undominated
        for (int i = 0; i < m; i++) {
            ulong c0 = 0, c1 = 0, c2 = 0;
            for (int j = 0; j < m; j++) if (j != i) { c0 |= A[pick[j]]; c1 |= B[pick[j]]; c2 |= C[pick[j]]; }
            if (c0 == F0 && c1 == F1 && c2 == F2) return;
        }
        var s = (int[])pick.Clone(); Array.Sort(s);
        var parts = new string[m]; for (int i = 0; i < m; i++) parts[i] = s[i].ToString();
        w.WriteLine(string.Join(" ", parts)); count++;
    }

    static void Rec(int depth, ulong c0, ulong c1, ulong c2, ulong f0, ulong f1, ulong f2)
    {
        nodes++;
        ulong u0 = ~c0 & F0, u1 = ~c1 & F1, u2 = ~c2 & F2;
        if (u0 == 0 && u1 == 0 && u2 == 0) { if (depth == m) Leaf(); return; }
        if (depth == m) return;
        int left = m - depth;
        int unc = Pop(u0) + Pop(u1) + Pop(u2);
        if (unc > left * maxDeg) return;
        if (left == 1) {
            // one square must dominate every undominated square: intersect their neighbourhoods
            ulong k0 = ~f0 & F0, k1 = ~f1 & F1, k2 = ~f2 & F2;
            ulong t = u0; while (t != 0) { int i = Low(t); t &= t - 1; k0 &= A[i]; k1 &= B[i]; k2 &= C[i]; if ((k0 | k1 | k2) == 0) return; }
            t = u1; while (t != 0) { int i = 64 + Low(t); t &= t - 1; k0 &= A[i]; k1 &= B[i]; k2 &= C[i]; if ((k0 | k1 | k2) == 0) return; }
            t = u2; while (t != 0) { int i = 128 + Low(t); t &= t - 1; k0 &= A[i]; k1 &= B[i]; k2 &= C[i]; if ((k0 | k1 | k2) == 0) return; }
            t = k0; while (t != 0) { int i = Low(t); t &= t - 1; pick[depth] = i; Leaf(); }
            t = k1; while (t != 0) { int i = 64 + Low(t); t &= t - 1; pick[depth] = i; Leaf(); }
            t = k2; while (t != 0) { int i = 128 + Low(t); t &= t - 1; pick[depth] = i; Leaf(); }
            return;
        }
        int u = -1;
        if (rule == 0) {
            if (u0 != 0) u = Low(u0); else if (u1 != 0) u = 64 + Low(u1); else u = 128 + Low(u2);
        } else {
            int best = int.MaxValue;
            for (int i = 0; i < N; i++) {
                bool isU = i < 64 ? ((u0 >> i) & 1) != 0 : i < 128 ? ((u1 >> (i - 64)) & 1) != 0 : ((u2 >> (i - 128)) & 1) != 0;
                if (!isU) continue;
                int c = Pop(A[i] & ~f0) + Pop(B[i] & ~f1) + Pop(C[i] & ~f2);
                if (c < best) { best = c; u = i; }
            }
            if (best == 0) return;
        }
        ulong d0 = A[u] & ~f0, d1 = B[u] & ~f1, d2 = C[u] & ~f2;
        for (int word = 0; word < 3; word++) {
            ulong t = word == 0 ? d0 : word == 1 ? d1 : d2;
            while (t != 0) {
                int b = Low(t); t &= t - 1; int d = 64 * word + b;
                pick[depth] = d;
                Rec(depth + 1, c0 | A[d], c1 | B[d], c2 | C[d], f0, f1, f2);
                if (word == 0) f0 |= 1UL << b; else if (word == 1) f1 |= 1UL << b; else f2 |= 1UL << b;
                if (depth == 0) {
                    w.Flush();
                    Console.Error.WriteLine("progress: top-level branch {0} done, count={1} nodes={2} t={3:F0}s", d, count, nodes, sw.Elapsed.TotalSeconds);
                }
            }
        }
    }

    static int Main(string[] args)
    {
        n = int.Parse(args[0]); m = int.Parse(args[1]); rule = int.Parse(args[3]); bool tdom = args.Length > 4 && args[4] == "tdom";
        N = n * n; if (N > 192) { Console.WriteLine("N > 192 not supported"); return 1; }
        A = new ulong[N]; B = new ulong[N]; C = new ulong[N]; maxDeg = 0;
        for (int s = 0; s < N; s++) {
            int deg = 0;
            for (int t = 0; t < N; t++) {
                int r1 = s / n, c1 = s % n, r2 = t / n, c2 = t % n;
                if ((s != t || !tdom) && (r1 == r2 || c1 == c2 || r1 - c1 == r2 - c2 || r1 + c1 == r2 + c2)) {
                    if (t < 64) A[s] |= 1UL << t; else if (t < 128) B[s] |= 1UL << (t - 64); else C[s] |= 1UL << (t - 128);
                    deg++;
                }
            }
            maxDeg = Math.Max(maxDeg, deg);
        }
        F0 = N >= 64 ? ulong.MaxValue : (1UL << N) - 1;
        F1 = N > 64 ? (N >= 128 ? ulong.MaxValue : (1UL << (N - 64)) - 1) : 0;
        F2 = N > 128 ? (N >= 192 ? ulong.MaxValue : (1UL << (N - 128)) - 1) : 0;
        pick = new int[m];
        sw = System.Diagnostics.Stopwatch.StartNew();
        using (w = new StreamWriter(args[2])) Rec(0, 0, 0, 0, 0, 0, 0);
        Console.WriteLine("n={0} m={1} rule={2} minimal dominating sets={3} nodes={4} time={5:F1}s", n, m, rule, count, nodes, sw.Elapsed.TotalSeconds);
        return 0;
    }
}
