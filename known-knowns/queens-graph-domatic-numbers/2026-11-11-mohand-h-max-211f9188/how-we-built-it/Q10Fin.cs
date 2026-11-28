// tdom(Q_10) = 16 ? Exhaustive two-phase search (see PREREG.md). Total domination number 6, N = 100, K = 16, slack 4.
// After shrinking, a total domatic 16-partition has a >= 12 classes that are total dominating 6-sets; the other
// 16 - a classes live in the F = 100 - 6a free squares. Phase 1 enumerates every family of a pairwise disjoint
// total dominating 6-sets (a = 14, 13, 12; sets taken in increasing index order, so each family once).
// Phase 2, for each family, decides whether F splits into 16 - a total dominating sets:
//   it does iff (i) there are 16 - a pairwise disjoint minimal total dominating 7-sets inside F, or
//   (ii) there are 16 - a - 1 such 7-sets whose complement in F is total dominating (covers every case in which exactly
//   one class has 8 or more squares), or (iii) a = 14 and F splits into two total dominating sets (tested directly on
//   all 2^15 splits, which also covers (i) and (ii) for a = 14).
// Usage: Q10Fin.exe six.txt seven.txt capSeconds out.txt
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

class Q10Fin
{
    const int n = 10, N = 100;
    struct M { public ulong a, b; }
    static M[] nb = new M[N]; static M full;
    static List<int[]> S6 = new List<int[]>(), S7 = new List<int[]>(); static M[] m6, m7;
    static long[] fam = new long[20]; static long phase2; static System.Diagnostics.Stopwatch sw; static double cap; static bool capped, found;
    static int[] pick = new int[16]; static string outPath;

    static M Mask(IEnumerable<int> s) { M m = new M(); foreach (int v in s) { if (v < 64) m.a |= 1UL << v; else m.b |= 1UL << (v - 64); } return m; }
    static bool Disj(M x, M y) { return (x.a & y.a) == 0 && (x.b & y.b) == 0; }
    static bool Sub(M x, M y) { return (x.a & ~y.a) == 0 && (x.b & ~y.b) == 0; }
    static M Or(M x, M y) { M m; m.a = x.a | y.a; m.b = x.b | y.b; return m; }
    static M Minus(M x, M y) { M m; m.a = x.a & ~y.a; m.b = x.b & ~y.b; return m; }
    static List<int> Sq(M m) { var l = new List<int>(); for (int v = 0; v < N; v++) if (v < 64 ? ((m.a >> v) & 1) != 0 : ((m.b >> (v - 64)) & 1) != 0) l.Add(v); return l; }
    static bool TD(M set) { M cov = new M(); foreach (int v in Sq(set)) cov = Or(cov, nb[v]); return cov.a == full.a && cov.b == full.b; }

    static void Write(int a, List<M> classes)
    {
        int[] lab = new int[N]; int k = 0;
        for (int i = 0; i < a; i++) { foreach (int v in S6[pick[i]]) lab[v] = k; k++; }
        M used = new M(); for (int i = 0; i < a; i++) used = Or(used, m6[pick[i]]);
        foreach (var c in classes) { foreach (int v in Sq(c)) lab[v] = k; used = Or(used, c); k++; }
        foreach (int v in Sq(Minus(full, used))) lab[v] = 0;   // loose squares join class 0
        using (var w = new StreamWriter(outPath))
            for (int r = 0; r < n; r++) w.WriteLine(string.Join(" ", Enumerable.Range(0, n).Select(c => lab[r * n + c].ToString())));
        Console.WriteLine("FOUND with a={0}: grid written, {1} classes", a, k);
    }

    // choose 'need' pairwise disjoint 7-sets from cand (indices >= start) inside F; lastIsRemainder: after need sets,
    // the complement in F must be total dominating
    static bool Choose(List<M> cand, int start, int need, M free, bool rem, List<M> acc)
    {
        if (need == 0) { if (!rem) return true; if (TD(free)) { acc.Add(free); return true; } return false; }
        for (int i = start; i < cand.Count; i++) {
            if (!Sub(cand[i], free)) continue;
            acc.Add(cand[i]);
            if (Choose(cand, i + 1, need - 1, Minus(free, cand[i]), rem, acc)) return true;
            acc.RemoveAt(acc.Count - 1);
        }
        return false;
    }

    static bool Phase2(int a, M used)
    {
        phase2++;
        M F = Minus(full, used); int c = 16 - a;
        var acc = new List<M>();
        if (a == 14) {
            var f = Sq(F); int L = f.Count;
            for (int mask = 0; mask < (1 << (L - 1)); mask++) {
                M x = Mask(new[] { f[0] });
                for (int i = 1; i < L; i++) if (((mask >> (i - 1)) & 1) != 0) x = Or(x, Mask(new[] { f[i] }));
                M y = Minus(F, x);
                if (TD(x) && TD(y)) { Write(a, new List<M> { x, y }); return true; }
            }
            return false;
        }
        var cand = new List<M>(); foreach (var m in m7) if (Sub(m, F)) cand.Add(m);
        if (cand.Count < c - 1) return false;
        if (Choose(cand, 0, c, F, false, acc)) { Write(a, acc); return true; }
        acc.Clear();
        if (Choose(cand, 0, c - 1, F, true, acc)) { Write(a, acc); return true; }
        return false;
    }

    static void Rec(int start, int depth, int a, M used)
    {
        if (found || capped) return;
        if (depth == a) { fam[a]++; if (Phase2(a, used)) found = true; if ((fam[a] & 0x3FF) == 0 && sw.Elapsed.TotalSeconds > cap) capped = true; return; }
        for (int i = start; i <= S6.Count - (a - depth); i++) {
            if (!Disj(m6[i], used)) continue;
            pick[depth] = i; Rec(i + 1, depth + 1, a, Or(used, m6[i]));
            if (found || capped) return;
        }
    }

    static int Main(string[] args)
    {
        foreach (var l in File.ReadAllLines(args[0])) if (l.Trim() != "") S6.Add(l.Split(' ').Select(int.Parse).ToArray());
        foreach (var l in File.ReadAllLines(args[1])) if (l.Trim() != "") S7.Add(l.Split(' ').Select(int.Parse).ToArray());
        cap = double.Parse(args[2], System.Globalization.CultureInfo.InvariantCulture); outPath = args[3];
        for (int s = 0; s < N; s++) { var l = new List<int>(); for (int t = 0; t < N; t++) { int r1 = s / n, c1 = s % n, r2 = t / n, c2 = t % n; if (s != t && (r1 == r2 || c1 == c2 || r1 - c1 == r2 - c2 || r1 + c1 == r2 + c2)) l.Add(t); } nb[s] = Mask(l); }
        full = Mask(Enumerable.Range(0, N)); m6 = S6.Select(s => Mask(s)).ToArray(); m7 = S7.Select(s => Mask(s)).ToArray();
        Console.WriteLine("{0} six-sets, {1} minimal seven-sets", S6.Count, S7.Count);
        sw = System.Diagnostics.Stopwatch.StartNew();
        foreach (int a in new[] { 15, 14, 13, 12 }) {
            if (a == 15) { long before = fam[15]; RecCount(0, 0, 15, new M()); Console.WriteLine("a=15: families {0}", fam[15] - before); continue; }
            Rec(0, 0, a, new M());
            Console.WriteLine("a={0}: families {1}, phase-2 calls so far {2}, t={3:F0}s, {4}", a, fam[a], phase2, sw.Elapsed.TotalSeconds, found ? "FOUND" : capped ? "CAPPED (inconclusive)" : "exhausted, none");
            if (found || capped) break;
        }
        Console.WriteLine(found ? "RESULT: FOUND" : capped ? "RESULT: CAPPED, inconclusive" : "RESULT: EXHAUSTED, no total domatic 16-partition skeleton");
        return 0;
    }
    static void RecCount(int start, int depth, int a, M used)
    {
        if (depth == a) { fam[a]++; return; }
        for (int i = start; i <= S6.Count - (a - depth); i++) { if (!Disj(m6[i], used)) continue; RecCount(i + 1, depth + 1, a, Or(used, m6[i])); }
    }
}
