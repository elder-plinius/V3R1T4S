using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;

public static class Program {
    static string ExportPath = Environment.GetEnvironmentVariable("ZC_EXPORT");
    static HashSet<string> ExportSet = ExportPath == null ? null : new HashSet<string>(File.ReadAllLines(Environment.GetEnvironmentVariable("ZC_LEAFLIST")));
    static string Arg(string[] a, string k, string d = null) { for (int i = 0; i < a.Length - 1; i++) if (a[i] == k) return a[i + 1]; return d; }
    static bool Has(string[] a, string k) => a.Contains(k);

    static readonly Dictionary<string, (string[] lo, string[] hi)> Domain = new() {
        ["core5d"] = (new[] { "-0.08", "-0.08", "0.0", "-0.08", "-0.08" }, new[] { "0.08", "0.08", "0.6283185307179586", "0.08", "0.08" }),
        ["r3_collar"] = (new[] { "0.08", "0.0" }, new[] { "0.1907", "1.0471975511965976" }),
        ["r5_collar"] = (new[] { "0.08", "0.0" }, new[] { "0.194601", "0.6283185307179586" }),
    };

    public static int Main(string[] args) {
        if (args.Length > 0 && args[0] == "selftest") return SelfTest.Run(args);
        if (args.Length > 0 && args[0] == "verdict") return Verdict.Run(args);
        string cert = Arg(args, "--cert"), tablesPath = Arg(args, "--tables"), outp = Arg(args, "--out", "out.jsonl");
        string partsA = Arg(args, "--parts", "core5d,r3_collar,r5_collar"); double tau = double.Parse(Arg(args, "--tau", "0.834"), CultureInfo.InvariantCulture);
        int threads = int.Parse(Arg(args, "--threads", "2")); int every = int.Parse(Arg(args, "--every", "1"));
        string fr = Arg(args, "--frontiers", "0-255"); var fp = fr.Split('-'); int f0 = int.Parse(fp[0]), f1 = int.Parse(fp[^1]);
        bool nocover = Has(args, "--nocover"); string tag = Arg(args, "--tag", "run");
        var T = Tables.Load(tablesPath); string excl = Arg(args, "--excl"); if (excl != null) T.LoadExclusions(excl); var chk = new Checker(T, tau);
        var done = new HashSet<string>();
        if (File.Exists(outp)) foreach (var l in File.ReadLines(outp)) { try { var d = JsonDocument.Parse(l); if (d.RootElement.TryGetProperty("shard", out var s)) done.Add(s.GetString()); } catch { } }
        var swAll = Stopwatch.StartNew();
        var outLock = new object();
        var summary = new List<ShardRes>();
        foreach (var part in partsA.Split(',')) {
            var work = new ConcurrentQueue<string>();
            for (int i = f0; i <= f1; i++) { string rel = $"shards/{part}/{i:D8}.jsonl.gz"; if (File.Exists(Path.Combine(cert, rel)) && !done.Contains(rel)) work.Enqueue(rel); }
            var frontierRoots = new ConcurrentDictionary<string, (string[] lo, string[] hi)>();
            var ths = new List<Thread>();
            for (int t = 0; t < threads; t++) {
                var th = new Thread(() => {
                    while (work.TryDequeue(out var rel)) {
                        var r = ProcessShard(cert, rel, part, chk, every, nocover);
                        lock (outLock) { File.AppendAllText(outp, r.ToJson() + "\n"); summary.Add(r); Console.WriteLine($"[{swAll.Elapsed:hh\\:mm\\:ss}] {rel} leaves={r.leaves} checked={r.checked_} fail={r.fails} cover={r.coverOk} minSlack={r.minSlack:E3} {r.secs:F1}s"); }
                    }
                }, 64 * 1024 * 1024);
                th.Priority = ThreadPriority.BelowNormal; th.Start(); ths.Add(th);
            }
            foreach (var th in ths) th.Join();
        }
        Console.WriteLine($"ALL DONE {swAll.Elapsed}");
        return 0;
    }

    public sealed class ShardRes {
        public string part, shard, minLeaf, firstErr, coverErr, summaryRoot, readErr; public double tau; public string version = "zc1";
        public long leaves, checked_, fails, nodes; public bool coverOk; public double minSlack = 9, minVsClaim = 9, secs; public int summaryLeafCount = -1;
        public Dictionary<string, long> kinds = new(); public List<string> failList = new(); public string[] rootLo, rootHi; public long maxCands; public long candsTotal;
        public string ToJson() => JsonSerializer.Serialize(new { tau, version, readErr, part, shard, leaves, checked_, fails, coverOk, coverErr, nodes, minSlack, minLeaf, minVsClaim, secs, summaryLeafCount, kinds, maxCands, candsTotal, rootLo, rootHi, failList = failList.Take(50) });
    }

    static ShardRes ProcessShard(string cert, string rel, string part, Checker chk, int every, bool nocover) {
        var sw = Stopwatch.StartNew(); var R = new ShardRes { part = part, shard = rel, tau = chk.Tau };
        try { return ProcessShardInner(cert, rel, part, chk, every, nocover, R, sw); } catch (Exception ex) { R.readErr = ex.GetType().Name + ": " + ex.Message; R.coverOk = false; R.fails++; R.secs = sw.Elapsed.TotalSeconds; return R; }
    }
    static ShardRes ProcessShardInner(string cert, string rel, string part, Checker chk, int every, bool nocover, ShardRes R, Stopwatch sw) {
        var los = new List<Int128[]>(); var his = new List<Int128[]>();
        using var fs = File.OpenRead(Path.Combine(cert, rel)); using var gz = new GZipStream(fs, CompressionMode.Decompress); using var sr = new StreamReader(gz, Encoding.UTF8, false, 1 << 20);
        string line; long idx = 0; string frontierId = null; Leaf summ = null;
        while ((line = sr.ReadLine()) != null) {
            if (line.Length == 0) continue;
            var L = Parse.Line(Encoding.UTF8.GetBytes(line));
            if (L.type == "frontier_summary") { summ = L; continue; }
            if (L.type != "leaf") { continue; }
            R.leaves++; frontierId ??= L.frontierId;
            string only = Environment.GetEnvironmentVariable("ZC_LEAF"); if (only != null && !L.leafId.EndsWith(only)) { los.Add(L.lo.Select(Parse.Scaled).ToArray()); his.Add(L.hi.Select(Parse.Scaled).ToArray()); continue; }
            if (L.frontierId != frontierId) { R.fails++; R.failList.Add($"{L.leafId}: mixed frontier ids"); }
            try {
                var lo = new Int128[L.lo.Length]; var hi = new Int128[L.hi.Length];
                for (int d = 0; d < lo.Length; d++) { lo[d] = Parse.Scaled(L.lo[d]); hi[d] = Parse.Scaled(L.hi[d]); }
                los.Add(lo); his.Add(hi);
            } catch (Exception ex) { R.fails++; R.failList.Add($"{L.leafId}: box parse {ex.Message}"); continue; }
            if ((idx++ % every) != 0) continue;
            R.checked_++;
            LeafResult res;
            try {
                if (part == "core5d") res = chk.Core(L); else res = chk.OneBody(L, part == "r3_collar" ? 3 : 5);
            } catch (Exception ex) { res = new LeafResult { note = "exception " + ex.Message }; }
            if (ExportPath != null && ExportSet.Contains(L.leafId) && res.pass) lock (ExportPath) File.AppendAllText(ExportPath, JsonSerializer.Serialize(new { leaf = L.leafId, shard = rel, variant = res.variant, kind = res.kind, lower = res.lower, cand = res.cand, lo = L.lo, hi = L.hi, ds = L.disk, r3 = L.r3, r5 = L.r5 }) + "\n");
            R.candsTotal += res.cands; if (res.cands > R.maxCands) R.maxCands = res.cands;
            if (!res.pass) { R.fails++; if (R.failList.Count < 200) R.failList.Add($"{L.leafId}: {res.note} lower={res.lower:R} cands={res.cands}"); continue; }
            R.kinds[res.kind] = R.kinds.GetValueOrDefault(res.kind) + 1;
            double slack = res.lower - 0.834; if (slack < R.minSlack) { R.minSlack = slack; R.minLeaf = L.leafId; }
            if (L.claimedLower != null) {
                var m = L.claimedLower.TrimStart('[').Split(' ')[0]; if (double.TryParse(m, NumberStyles.Float, CultureInfo.InvariantCulture, out var cl)) { double dlt = res.lower - cl; if (dlt < R.minVsClaim) R.minVsClaim = dlt; }
            }
        }
        // exact partition check against the frontier summary root
        if (summ == null) { R.coverOk = false; R.coverErr = "no frontier_summary"; }
        else {
            R.rootLo = summ.lo; R.rootHi = summ.hi; R.summaryLeafCount = summ.leafCount;
            if (summ.leafCount != R.leaves) { R.coverOk = false; R.coverErr = $"summary leaf_count {summ.leafCount} != {R.leaves}"; }
            else if (nocover) { R.coverOk = false; R.coverErr = "skipped"; }
            else {
                var rl = summ.lo.Select(Parse.Scaled).ToArray(); var rh = summ.hi.Select(Parse.Scaled).ToArray();
                var pr = Cover.Partition(los.ToArray(), his.ToArray(), rl, rh); R.coverOk = pr.ok; R.coverErr = pr.err; R.nodes = pr.nodes;
            }
        }
        R.secs = sw.Elapsed.TotalSeconds; return R;
    }
}
