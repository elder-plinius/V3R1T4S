// Exhaustive search of the skeletons of a domatic 21-partition of Q_12 (see PREREG.md, counting lemma).
// A skeleton: a pairwise disjoint dominating 6-sets and b pairwise disjoint minimal dominating 7-sets, all disjoint,
// leaving L = 144 - 6a - 7b squares. mode "any": any leftover is accepted (L = 0 or 1). mode "dom": the leftover squares
// must themselves form a dominating set (case a = 4, b = 16, L = 8).
// Search: for each family of a disjoint 6-sets (one representative per orbit of the 8 board symmetries), depth-first
// exact-cover style: take the free square with the fewest options, an option being an available 7-set containing it or
// (while the leftover budget lasts) "this square stays in the leftover". Every skeleton is reached, so if the program
// ends with EXHAUSTED the skeleton type does not exist (given complete input lists).
// Usage: Skel.exe sets6.txt sets7.txt a b any|dom capSeconds out.txt
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

class Skel
{
    const int n = 12, N = 144;
    struct M { public ulong a, b, c; }
    static M[] nb = new M[N];
    static List<int[]> S6 = new List<int[]>(), S7 = new List<int[]>();
    static M[] m7; static int[][] bySq;      // 7-sets containing each square (indices into the filtered list)
    static int[][] cand; static long nodes; static System.Diagnostics.Stopwatch sw; static double cap; static bool capped;
    static bool domMode; static List<int> chosen = new List<int>(); static string outPath; static List<int[]> fam;

    static M Mask(IEnumerable<int> s) { M m = new M(); foreach (int v in s) { if (v < 64) m.a |= 1UL << v; else if (v < 128) m.b |= 1UL << (v - 64); else m.c |= 1UL << (v - 128); } return m; }
    static bool Has(M m, int v) { return v < 64 ? ((m.a >> v) & 1) != 0 : v < 128 ? ((m.b >> (v - 64)) & 1) != 0 : ((m.c >> (v - 128)) & 1) != 0; }
    static bool Disj(M x, M y) { return (x.a & y.a) == 0 && (x.b & y.b) == 0 && (x.c & y.c) == 0; }
    static M Or(M x, M y) { M m; m.a = x.a | y.a; m.b = x.b | y.b; m.c = x.c | y.c; return m; }

    static bool Dominating(List<int> sq)
    {
        M cov = new M(); foreach (int v in sq) cov = Or(cov, nb[v]);
        return cov.a == ulong.MaxValue && cov.b == ulong.MaxValue && cov.c == 0xFFFFUL;
    }

    // used = squares in chosen sets; left = squares decided as leftover
    static bool Dfs(M used, M left, int need, int budget)
    {
        nodes++;
        if ((nodes & 0xFFFFF) == 0 && sw.Elapsed.TotalSeconds > cap) capped = true;
        if (capped) return false;
        M occ = Or(used, left);
        if (need == 0) {
            var rest = new List<int>(); for (int v = 0; v < N; v++) if (!Has(used, v)) rest.Add(v);
            if (domMode && !Dominating(rest)) return false;
            Write(rest); return true;
        }
        int best = int.MaxValue, bs = -1;
        for (int v = 0; v < N; v++) {
            if (Has(occ, v)) continue;
            int c = budget > 0 ? 1 : 0;
            foreach (int j in bySq[v]) { if (Disj(m7[j], occ)) { c++; if (c >= best) break; } }
            if (c < best) { best = c; bs = v; if (c == 0) return false; }
        }
        if (bs < 0) return false;
        foreach (int j in bySq[bs]) {
            if (!Disj(m7[j], occ)) continue;
            chosen.Add(j);
            if (Dfs(Or(used, m7[j]), left, need - 1, budget)) return true;
            chosen.RemoveAt(chosen.Count - 1);
        }
        if (budget > 0) {
            M l2 = left; if (bs < 64) l2.a |= 1UL << bs; else if (bs < 128) l2.b |= 1UL << (bs - 64); else l2.c |= 1UL << (bs - 128);
            if (Dfs(used, l2, need, budget - 1)) return true;
        }
        return false;
    }

    static List<int[]> curSets;
    static void Write(List<int> rest)
    {
        int[] lab = new int[N]; for (int i = 0; i < N; i++) lab[i] = -1;
        int k = 0;
        foreach (var s in fam) { foreach (int v in s) lab[v] = k; k++; }
        foreach (int j in chosen) { foreach (int v in curSets[j]) lab[v] = k; k++; }
        int restLabel = domMode ? k : 0;   // dom: leftover squares form their own class; any: they join class 0
        foreach (int v in rest) lab[v] = restLabel;
        using (var w = new StreamWriter(outPath))
            for (int r = 0; r < n; r++) w.WriteLine(string.Join(" ", Enumerable.Range(0, n).Select(c => lab[r * n + c].ToString())));
        Console.WriteLine("FOUND: grid written with {0} classes ({1} leftover squares)", domMode ? k + 1 : k, rest.Count);
    }

    static int Sym(int v, int f)
    {
        int r = v / n, c = v % n, R, C;
        switch (f) { case 0: R = r; C = c; break; case 1: R = c; C = n - 1 - r; break; case 2: R = n - 1 - r; C = n - 1 - c; break;
            case 3: R = n - 1 - c; C = r; break; case 4: R = r; C = n - 1 - c; break; case 5: R = n - 1 - r; C = c; break;
            case 6: R = c; C = r; break; default: R = n - 1 - c; C = n - 1 - r; break; }
        return R * n + C;
    }
    static string Key(List<int[]> f, int s)
    {
        var parts = f.Select(x => string.Join(",", x.Select(v => Sym(v, s)).OrderBy(v => v).Select(v => v.ToString("D3")))).OrderBy(x => x, StringComparer.Ordinal);
        return string.Join("|", parts);
    }

    static void Families(int start, int a, M used, List<int[]> cur, List<List<int[]>> res)
    {
        if (cur.Count == a) { res.Add(new List<int[]>(cur)); return; }
        for (int i = start; i < S6.Count; i++) { M mi = Mask(S6[i]); if (!Disj(mi, used)) continue; cur.Add(S6[i]); Families(i + 1, a, Or(used, mi), cur, res); cur.RemoveAt(cur.Count - 1); }
    }

    static int Main(string[] args)
    {
        foreach (var l in File.ReadAllLines(args[0])) if (l.Trim() != "") S6.Add(l.Split(' ').Select(int.Parse).ToArray());
        foreach (var l in File.ReadAllLines(args[1])) if (l.Trim() != "") S7.Add(l.Split(' ').Select(int.Parse).ToArray());
        int a = int.Parse(args[2]), b = int.Parse(args[3]); domMode = args[4] == "dom"; cap = double.Parse(args[5], System.Globalization.CultureInfo.InvariantCulture); outPath = args[6];
        int L = N - 6 * a - 7 * b;
        for (int s = 0; s < N; s++) { var l = new List<int>(); for (int t = 0; t < N; t++) { int r1 = s / n, c1 = s % n, r2 = t / n, c2 = t % n; if (r1 == r2 || c1 == c2 || r1 - c1 == r2 - c2 || r1 + c1 == r2 + c2) l.Add(t); } nb[s] = Mask(l); }
        for (int k = 3; k <= 6; k++) { var all = new List<List<int[]>>(); Families(0, k, new M(), new List<int[]>(), all); Console.WriteLine("families of {0} pairwise disjoint 6-sets: {1}", k, all.Count); }
        var fams = new List<List<int[]>>(); Families(0, a, new M(), new List<int[]>(), fams);
        var reps = fams.Where(f => { string k0 = Key(f, 0); for (int s = 1; s < 8; s++) if (string.CompareOrdinal(Key(f, s), k0) < 0) return false; return true; }).ToList();
        Console.WriteLine("a={0} b={1} leftover={2} mode={3}: {4} families, {5} up to symmetry", a, b, L, args[4], fams.Count, reps.Count);
        sw = System.Diagnostics.Stopwatch.StartNew(); bool found = false; int idx = 0;
        foreach (var f in reps) {
            fam = f; M used = new M(); foreach (var s in f) used = Or(used, Mask(s));
            curSets = S7.Where(s => Disj(Mask(s), used)).ToList();
            m7 = curSets.Select(s => Mask(s)).ToArray();
            var lists = new List<int>[N]; for (int v = 0; v < N; v++) lists[v] = new List<int>();
            for (int j = 0; j < curSets.Count; j++) foreach (int v in curSets[j]) lists[v].Add(j);
            bySq = lists.Select(x => x.ToArray()).ToArray();
            chosen.Clear(); long before = nodes;
            found = Dfs(used, new M(), b, L);
            Console.WriteLine("family {0}: {1} available 7-sets, nodes {2}, t={3:F0}s, {4}", idx++, curSets.Count, nodes - before, sw.Elapsed.TotalSeconds, found ? "FOUND" : capped ? "CAPPED (inconclusive)" : "exhausted, none");
            if (found || capped) break;
        }
        Console.WriteLine(found ? "RESULT: FOUND" : capped ? "RESULT: CAPPED, inconclusive" : "RESULT: EXHAUSTED, no skeleton of this type");
        return 0;
    }
}
