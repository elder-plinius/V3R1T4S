using System.Diagnostics;
using RidVerify;

static class Program
{
    public const int Threads = 4;
    static int Main(string[] args)
    {
        string cmd = args.Length > 0 ? args[0] : "help";
        string cert = Environment.GetEnvironmentVariable("RID_CERT") ?? "../../../../data/hervay_inputs/certificate/search.cert";
        var sw = Stopwatch.StartNew();
        if (cmd == "probe")
        {
            var P = Cert.Parse(cert);
            Console.WriteLine($"lines={P.Lines} ckok={P.LinesChecksumOk} problems={P.Problems.Count} records={P.Records.Count}");
            foreach (var p in P.Problems.Take(5)) Console.WriteLine(p);
            Console.WriteLine($"geometry: V={Geo.V.Length} Q={Geo.Q.Count} Q+={Geo.QPlus.Count}");
            var dom = P.Records.Where(r => r.Component == "Domain").ToList();
            var gl = P.Records.Where(r => r.Component == "Global").Take(int.Parse(args[1])).ToList();
            int okg = 0, okf = 0;
            foreach (var r in gl)
            {
                bool f = Checks.GlobalFast(r.EdgeA, r.EdgeB, r.Vertex, r.Path);
                bool g = args.Length > 2 && Checks.GlobalGeneric(r.EdgeA, r.EdgeB, r.Vertex, r.Path);
                if (f) okf++; if (g) okg++;
                if (args.Length > 2 && f != g) Console.WriteLine($"MISMATCH line {r.Line}");
            }
            Console.WriteLine($"global fast ok {okf}/{gl.Count} generic ok {okg} time {sw.Elapsed}");
            var doms = dom.Take(200).ToList();
            int okd = 0; var bad = new List<string>();
            foreach (var r in doms) { if (Checks.Domain(r)) okd++; else bad.Add($"{r.Line}:{r.Inequality}"); }
            Console.WriteLine($"domain ok {okd}/{doms.Count} bad(first)={string.Join(",", bad.Take(10))} time {sw.Elapsed}");
            return 0;
        }
        if (cmd == "domain" || cmd == "global")
        {
            var P = Cert.Parse(cert);
            var comp = cmd == "domain" ? "Domain" : "Global";
            var rs = P.Records.Where(r => r.Component == comp).ToList();
            int ok = 0, rej = 0; var bad = new System.Collections.Concurrent.ConcurrentBag<int>();
            Parallel.ForEach(rs, new ParallelOptions { MaxDegreeOfParallelism = Threads }, r =>
            {
                bool a = cmd == "domain" ? Checks.Domain(r) : Checks.GlobalFast(r.EdgeA, r.EdgeB, r.Vertex, r.Path);
                if (a) Interlocked.Increment(ref ok); else { Interlocked.Increment(ref rej); bad.Add(r.Line); }
            });
            Console.WriteLine($"{comp}: accepted {ok} rejected {rej} of {rs.Count}; time {sw.Elapsed}; bad lines {string.Join(",", bad.OrderBy(x=>x).Take(10))}");
            return 0;
        }
        if (cmd == "localexotic")
        {
            RecordCover.LoadLocalTable("../../../../data/hervay_inputs/paper/appendices/b-zoom-covers.tex");
            var P = Cert.Parse(cert);
            foreach (var comp in new[] { "Local", "Exotic" })
            {
                var rs = P.Records.Where(r => r.Component == comp).ToList();
                int ok = 0; var bad = new List<int>();
                Parallel.ForEach(rs, new ParallelOptions { MaxDegreeOfParallelism = Threads }, r => { if (RecordCover.Record(r)) Interlocked.Increment(ref ok); else lock (bad) bad.Add(r.Line); });
                Console.WriteLine($"{comp}: accepted {ok} of {rs.Count}, bad lines {string.Join(",", bad.OrderBy(x => x).Take(10))} time {sw.Elapsed}");
            }
            return 0;
        }
        if (cmd == "all") return RunAll(args, cert);
        if (cmd == "labels")
        {
            // label-sensitivity experiment: how many of the first N Global / Domain records are accepted under the (possibly reversed) numbering
            var P = Cert.Parse(cert); int n = int.Parse(args[1]);
            var g = P.Records.Where(r => r.Component == "Global").Take(n).ToList(); var d = P.Records.Where(r => r.Component == "Domain" && r.Inequality >= 13).Take(n).ToList();
            int og = 0, od = 0; Parallel.ForEach(g, new ParallelOptions { MaxDegreeOfParallelism = Threads }, r => { if (Checks.GlobalFast(r.EdgeA, r.EdgeB, r.Vertex, r.Path)) Interlocked.Increment(ref og); });
            Parallel.ForEach(d, new ParallelOptions { MaxDegreeOfParallelism = Threads }, r => { if (Checks.Domain(r)) Interlocked.Increment(ref od); });
            Console.WriteLine($"labels: VDESC={Environment.GetEnvironmentVariable("RID_VDESC")} QDESC={Environment.GetEnvironmentVariable("RID_QDESC")}: Global accepted {og}/{g.Count}; fold-Domain accepted {od}/{d.Count}");
            var k = Geo.QPlus[16]; Console.WriteLine("QPlus[16] (fold index 29) = " + k.Key());
            return 0;
        }
        if (cmd == "geom")
        {
            var R = GeometryChecks.Run();
            foreach (var l in R.Lines) Console.WriteLine(l);
            Console.WriteLine(R.Ok ? "GEOMETRY OK" : "GEOMETRY FAILED");
            return R.Ok ? 0 : 1;
        }
        if (cmd == "cube")
        {
            var res = FitTest.RunCubeKnownPositive(Console.WriteLine);
            Console.WriteLine("CUBE KNOWN-POSITIVE: " + res);
            return res == "PASS" ? 0 : 1;
        }
        if (cmd == "cover")
        {
            string dir = Environment.GetEnvironmentVariable("RID_COVERS") ?? "../../../../data/hervay_inputs/covers";
            foreach (var name in args.Skip(1))
            {
                var path = System.IO.Path.Combine(dir, name.Contains('/') ? name : (char.IsDigit(name[0]) ? "local/" + name : "exotic/" + name) ) + ".json";
                var c = Cover.Load(path);
                var rep = CoverCheck.Check(c, int.Parse(Environment.GetEnvironmentVariable("RID_THREADS") ?? "1"));
                Console.WriteLine($"cover {c.Name}: zooms {rep.Zooms} cells {rep.Cells} accepted {rep.Accepted} rejected {rep.Rejected} delegated {rep.Delegated}/{rep.DelegatedOk} domain-witness cells {rep.DomainWitnessCells} problems {rep.Problems.Count} time {sw.Elapsed}");
                foreach (var p in rep.Problems.Take(8)) Console.WriteLine("   " + p);
            }
            return 0;
        }
        return 0;
    }

    static string Esc(string x) => System.Text.Json.JsonSerializer.Serialize(x);
    static int RunAll(string[] args, string cert)
    {
        var total = Stopwatch.StartNew();
        string root = Environment.GetEnvironmentVariable("RID_INPUTS") ?? "../../../../data/hervay_inputs";
        string coversDir = System.IO.Path.Combine(root, "covers");
        string tex = System.IO.Path.Combine(root, "paper/appendices/b-zoom-covers.tex");
        string outDir = Environment.GetEnvironmentVariable("RID_RESULT") ?? "../../result";
        System.IO.Directory.CreateDirectory(outDir);
        bool runControls = !args.Contains("--no-controls");
        var res = new SortedDictionary<string, object>();
        bool allOk = true;
        void Say(string m) { Console.WriteLine($"[{total.Elapsed:hh\\:mm\\:ss}] {m}"); }
        void Fail(string m) { allOk = false; Say("FAIL: " + m); }
        Say("RID certificate verifier (C#, .NET " + Environment.Version + "), threads=" + Threads);
        // 1. provenance + framing
        var sha = Cert.Sha256File(cert);
        const string pinned = "df1f8dbab68b561f22fa9daeca48153d71bde7b6fba3345d9f6b7b8077df4b5f";
        Say($"sha256(search.cert) = {sha} (pinned {pinned}) -> {(sha == pinned ? "MATCH" : "MISMATCH")}");
        if (sha != pinned) Fail("sha256 mismatch");
        res["sha256"] = sha; res["sha256_matches_pinned"] = sha == pinned;
        var P = Cert.Parse(cert);
        Say($"framing: {P.Lines} lines, {P.LinesChecksumOk} checksums ok (8 hex = start of SHA-256 of the JSON text after the space), {P.Records.Count} records (header excluded), {P.Problems.Count} framing/canonical-JSON problems");
        if (P.Problems.Count > 0 || P.Records.Count != 192696 || P.LinesChecksumOk != P.Lines) Fail("framing");
        res["lines"] = P.Lines; res["checksums_ok"] = P.LinesChecksumOk; res["records"] = P.Records.Count; res["framing_problems"] = P.Problems.Count;
        // 2. coverage
        var cov = Cert.CheckCoverage(P.Records);
        Say($"coverage: {(cov.ok ? "PASS" : "FAIL")} ({cov.msg}); prefix-free, Kraft sum exactly 1, paper's frontier algorithm leaves no unaccounted box; max depth {cov.maxDepth}, mean depth {cov.meanDepth:F2}");
        if (!cov.ok) Fail("coverage");
        res["coverage_ok"] = cov.ok; res["max_depth"] = cov.maxDepth; res["mean_depth"] = Math.Round(cov.meanDepth, 3);
        // 3. geometry
        var G = GeometryChecks.Run();
        foreach (var l in G.Lines) Say("geometry: " + l);
        if (!G.Ok) Fail("geometry"); res["geometry_ok"] = G.Ok; res["geometry_checks"] = G.Lines.Count;
        // 4. parameter audit + covers
        var bad = ParamAudit.Run(coversDir, tex, out int pchecks);
        Say($"cover parameters vs paper text: {pchecks} checks, {bad.Count} mismatches"); foreach (var b in bad) Say("   MISMATCH " + b);
        if (bad.Count > 0) Fail("parameter audit"); res["param_audit_checks"] = pchecks; res["param_audit_mismatches"] = bad.Count;
        var coverNames = Enumerable.Range(0, 30).Select(i => i.ToString()).Concat(new[] { "square", "pentagon", "arc+", "arc-", "endpoint+", "endpoint-", "crossing+", "crossing-" }).ToList();
        var coverReports = new Dictionary<string, CoverReport>();
        int totCells = 0, totAcc = 0, totRej = 0, totDeleg = 0;
        foreach (var name in coverNames)
        {
            var c = Cover.Load(System.IO.Path.Combine(coversDir, char.IsDigit(name[0]) ? "local" : "exotic", name + ".json"));
            var rep = CoverCheck.Check(c, Threads); coverReports[name] = rep;
            totCells += rep.Cells; totAcc += rep.Accepted; totRej += rep.Rejected; totDeleg += rep.Delegated;
            Say($"cover {name,-9}: zooms {rep.Zooms,2}, terminal cells {rep.Cells,5} (witness {rep.Cells - rep.Delegated}, handed over {rep.Delegated}), accepted {rep.Accepted}, rejected {rep.Rejected}, domain-witness cells {rep.DomainWitnessCells}, problems {rep.Problems.Count}");
            foreach (var p in rep.Problems.Take(3)) Say("     " + p);
        }
        var paperCells = new Dictionary<string, int> { ["square"] = 877, ["pentagon"] = 6173, ["arc+"] = 343, ["arc-"] = 288, ["endpoint+"] = 305, ["endpoint-"] = 246, ["crossing+"] = 1431, ["crossing-"] = 687 };
        int localWit = coverNames.Take(30).Sum(n => coverReports[n].Cells - coverReports[n].Delegated);
        bool cellCountsOk = localWit == 833 && paperCells.All(kv => coverReports[kv.Key].Cells - coverReports[kv.Key].Delegated == kv.Value) && coverReports["crossing+"].Delegated == 34 && coverReports["crossing-"].Delegated == 14;
        Say($"zoom cells: total {totCells} (witness cells {totCells - totDeleg} + handed over {totDeleg}); accepted {totAcc}, rejected {totRej}; counts match paper table (Local 833, square 877, pentagon 6173, arc 343/288, endpoint 305/246, crossing 1431/687, handed 34/14): {cellCountsOk}");
        bool coversOk = coverReports.Values.All(r => r.Ok) && cellCountsOk;
        if (!coversOk) Fail("covers"); res["zoom_cells_total"] = totCells; res["zoom_cells_accepted"] = totAcc; res["zoom_cells_rejected"] = totRej; res["zoom_cells_handed_over"] = totDeleg; res["covers_ok"] = coversOk;
        // 5. records
        var counts = new SortedDictionary<string, object>();
        var expected = new Dictionary<string, int> { ["Global"] = 157458, ["Local"] = 21792, ["Domain"] = 12650, ["Exotic"] = 796 };
        foreach (var comp in new[] { "Domain", "Global", "Local", "Exotic" })
        {
            var sw2 = Stopwatch.StartNew(); var rs = P.Records.Where(r => r.Component == comp).ToList(); int ok = 0, rej = 0; var badl = new System.Collections.Concurrent.ConcurrentBag<int>();
            Parallel.ForEach(rs, new ParallelOptions { MaxDegreeOfParallelism = Threads }, r =>
            {
                bool a;
                switch (comp)
                {
                    case "Domain": a = Checks.Domain(r); break;
                    case "Global": a = Checks.GlobalFast(r.EdgeA, r.EdgeB, r.Vertex, r.Path) && IsEdge(r.EdgeA, r.EdgeB); break;
                    default: a = RecordCover.Record(r) && coverReports[r.Cover].Ok; break;
                }
                if (a) Interlocked.Increment(ref ok); else { Interlocked.Increment(ref rej); badl.Add(r.Line); }
            });
            Say($"records {comp,-6}: {rs.Count} (expected {expected[comp]}), accepted {ok}, rejected {rej}, {sw2.Elapsed.TotalSeconds:F1}s {(rej > 0 ? "bad lines " + string.Join(",", badl.OrderBy(x => x).Take(10)) : "")}");
            if (rs.Count != expected[comp] || rej > 0) Fail("records " + comp);
            counts[comp] = new { total = rs.Count, accepted = ok, rejected = rej };
        }
        res["records_by_component"] = counts;
        // per-cover record counts vs paper
        var perCover = P.Records.Where(r => r.Component != "Domain" && r.Component != "Global").GroupBy(r => r.Component == "Local" ? "Local" : r.Cover).ToDictionary(g => g.Key, g => g.Count());
        var paperRec = new Dictionary<string, int> { ["Local"] = 21792, ["square"] = 56, ["pentagon"] = 315, ["arc+"] = 135, ["arc-"] = 68, ["endpoint+"] = 55, ["endpoint-"] = 23, ["crossing+"] = 86, ["crossing-"] = 58 };
        bool prOk = paperRec.All(kv => perCover.GetValueOrDefault(kv.Key) == kv.Value);
        Say($"records per cover match paper table (Local 21792, square 56, pentagon 315, arc 135/68, endpoint 55/23, crossing 86/58): {prOk}"); if (!prOk) Fail("per-cover record counts");
        // generic cross-check of the fast Global path
        {
            var rng = new Random(99); var gl = P.Records.Where(r => r.Component == "Global").OrderBy(_ => rng.Next()).Take(int.Parse(Environment.GetEnvironmentVariable("RID_XCHECK") ?? "1200")).ToList();
            int agree = 0; var sw3 = Stopwatch.StartNew();
            Parallel.ForEach(gl, new ParallelOptions { MaxDegreeOfParallelism = Threads }, r => { if (Checks.GlobalGeneric(r.EdgeA, r.EdgeB, r.Vertex, r.Path) == Checks.GlobalFast(r.EdgeA, r.EdgeB, r.Vertex, r.Path)) Interlocked.Increment(ref agree); });
            Say($"cross-check fast integer Global test vs generic polynomial/Bernstein implementation on {gl.Count} random Global records: agree {agree}/{gl.Count} ({sw3.Elapsed.TotalSeconds:F1}s)");
            if (agree != gl.Count) Fail("global cross-check"); res["global_crosscheck_sample"] = gl.Count; res["global_crosscheck_agree"] = agree;
        }
        // 5b. independent floating-point geometric sanity sampling
        { var mcr = MonteCarlo.Run(P, int.Parse(Environment.GetEnvironmentVariable("RID_MC") ?? "4000"), 6, Threads, Say); Say("Monte-Carlo geometric sanity (not part of the proof): " + mcr.msg); res["monte_carlo"] = mcr.msg; if (!mcr.ok) Fail("monte carlo"); }
        // 6. cube known positive
        var cubeRes = FitTest.RunCubeKnownPositive(m => Say("cube: " + m)); Say("cube known-positive (fit machinery recognises a genuine Rupert passage): " + cubeRes);
        if (cubeRes != "PASS") Fail("cube"); res["cube_known_positive"] = cubeRes;
        // 7. controls
        if (runControls)
        {
            var outs = Controls.Run(P, coversDir, m => Say(m));
            int ncert = outs.Sum(o => o.Certified), acc = outs.Sum(o => o.Accepted), refd = outs.Sum(o => o.Refused);
            Say($"CONTROLS total: {ncert} certified-false corrupted claims, {refd} refused, {acc} accepted (must be 0; need >=400 certified)");
            if (acc != 0 || ncert < 400) Fail("controls"); res["controls_certified_false"] = ncert; res["controls_refused"] = refd; res["controls_accepted"] = acc;
            res["controls"] = outs.Select(o => new { o.Category, o.Tried, o.Certified, o.Refused, o.Accepted, uncertified_accepted = o.UncertifiedAccepted }).ToList();
        }
        res["all_ok"] = allOk; res["wall_seconds"] = Math.Round(total.Elapsed.TotalSeconds, 1);
        Say(allOk ? "OVERALL: ALL CHECKS PASSED" : "OVERALL: FAILURES PRESENT");
        System.IO.File.WriteAllText(System.IO.Path.Combine(outDir, "summary.json"), System.Text.Json.JsonSerializer.Serialize(res, new System.Text.Json.JsonSerializerOptions { WriteIndented = true }));
        return allOk ? 0 : 1;
    }
    static bool IsEdge(int a, int b)
    {
        if (a < 0 || b < 0 || a >= 60 || b >= 60 || a == b) return false;
        Q5 s = Q5.Zero; for (int k = 0; k < 3; k++) { var x = Geo.V[a][k] - Geo.V[b][k]; s = s + x * x; }
        return s == Q5.Int(4);
    }
}
