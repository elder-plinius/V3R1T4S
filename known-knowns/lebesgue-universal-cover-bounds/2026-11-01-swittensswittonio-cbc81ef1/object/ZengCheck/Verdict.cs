using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Text.Json;

// Final aggregation: combines per-shard result lines (leaf proofs + exact leaf partition of each frontier) with
// (a) the exact partition of the part domain by the 256 frontier roots, (b) counts against the shipped part_summary,
// (c) the domain constants against the values stated in the paper, (d) completeness: every one of 256 shards of each part present exactly once.
public static class Verdict {
    static readonly Dictionary<string, (string[] lo, string[] hi, long leaves, long leafCountPaper)> Dom = new() {
        ["core5d"] = (new[] { "-0.08", "-0.08", "0.0", "-0.08", "-0.08" }, new[] { "0.08", "0.08", "0.6283185307179586", "0.08", "0.08" }, 6742989, 6742989),
        ["r3_collar"] = (new[] { "0.08", "0.0" }, new[] { "0.1907", "1.0471975511965976" }, 2374, 2374),
        ["r5_collar"] = (new[] { "0.08", "0.0" }, new[] { "0.194601", "0.6283185307179586" }, 1029, 1029),
    };
    public static int Run(string[] a) {
        string cert = null, outp = null; double tau = 0.834; string vout = null;
        for (int i = 1; i < a.Length - 1; i++) { if (a[i] == "--cert") cert = a[i + 1]; if (a[i] == "--out") outp = a[i + 1]; if (a[i] == "--tau") tau = double.Parse(a[i + 1], System.Globalization.CultureInfo.InvariantCulture); if (a[i] == "--verdict") vout = a[i + 1]; }
        var latest = new Dictionary<string, JsonElement>(); var docs = new List<JsonDocument>();
        foreach (var l in File.ReadLines(outp)) { var d = JsonDocument.Parse(l); docs.Add(d); latest[d.RootElement.GetProperty("shard").GetString()] = d.RootElement; }
        var sb = new StringBuilder(); bool all = true; long totLeaves = 0, totFails = 0; double worst = 9;
        foreach (var part in new[] { "r3_collar", "r5_collar", "core5d" }) {
            var dom = Dom[part]; bool ok = true; var msgs = new List<string>();
            var rows = new List<JsonElement>();
            for (int i = 0; i < 256; i++) { string rel = $"shards/{part}/{i:D8}.jsonl.gz"; if (latest.TryGetValue(rel, out var r)) rows.Add(r); else { ok = false; msgs.Add("missing result " + rel); } }
            long leaves = 0, fails = 0, checked_ = 0; double minSlack = 9; string minLeaf = "";
            var kinds = new Dictionary<string, long>();
            foreach (var r in rows) {
                leaves += r.GetProperty("leaves").GetInt64(); fails += r.GetProperty("fails").GetInt64(); checked_ += r.GetProperty("checked_").GetInt64();
                if (!r.GetProperty("coverOk").GetBoolean()) { ok = false; msgs.Add("cover fail " + r.GetProperty("shard").GetString()); }
                if (Math.Abs(r.GetProperty("tau").GetDouble() - tau) > 0) { ok = false; msgs.Add("tau mismatch in " + r.GetProperty("shard").GetString()); }
                double ms = r.GetProperty("minSlack").GetDouble(); if (ms < minSlack) { minSlack = ms; minLeaf = r.GetProperty("minLeaf").GetString(); }
                foreach (var k in r.GetProperty("kinds").EnumerateObject()) kinds[k.Name] = kinds.GetValueOrDefault(k.Name) + k.Value.GetInt64();
            }
            if (fails != 0) { ok = false; msgs.Add($"{fails} failing leaves"); }
            if (checked_ != leaves) { ok = false; msgs.Add($"checked {checked_} != leaves {leaves}"); }
            // frontier roots partition the part root exactly
            var rl = new List<Int128[]>(); var rh = new List<Int128[]>();
            foreach (var r in rows) { rl.Add(r.GetProperty("rootLo").EnumerateArray().Select(x => Parse.Scaled(x.GetString())).ToArray()); rh.Add(r.GetProperty("rootHi").EnumerateArray().Select(x => Parse.Scaled(x.GetString())).ToArray()); }
            string frontierErr = null; if (rows.Count == 256) { var pr = Cover.Partition(rl.ToArray(), rh.ToArray(), dom.lo.Select(Parse.Scaled).ToArray(), dom.hi.Select(Parse.Scaled).ToArray()); if (!pr.ok) { ok = false; frontierErr = pr.err; msgs.Add("frontier roots do not partition domain: " + pr.err); } }
            // part_summary
            long sumLeaves = -1; string rootTxt = null;
            using (var fs = File.OpenRead(Path.Combine(cert, "shards", part, "metadata.jsonl.gz"))) using (var gz = new GZipStream(fs, CompressionMode.Decompress)) using (var sr = new StreamReader(gz)) {
                var d = JsonDocument.Parse(sr.ReadLine()); var e = d.RootElement; sumLeaves = e.GetProperty("leaf_count").GetInt64();
                rootTxt = e.GetProperty("root_box").ToString();
                var lo = e.GetProperty("root_box").GetProperty("lo").EnumerateArray().Select(x => Parse.Scaled(x.GetRawText())).ToArray(); var hi = e.GetProperty("root_box").GetProperty("hi").EnumerateArray().Select(x => Parse.Scaled(x.GetRawText())).ToArray();
                if (!lo.SequenceEqual(dom.lo.Select(Parse.Scaled)) || !hi.SequenceEqual(dom.hi.Select(Parse.Scaled))) { ok = false; msgs.Add("part_summary root differs from paper domain"); }
                if (e.GetProperty("frontier_count").GetInt64() != 256) { ok = false; msgs.Add("frontier_count != 256"); }
            }
            if (sumLeaves != leaves) { ok = false; msgs.Add($"part_summary leaf_count {sumLeaves} != replayed {leaves}"); }
            if (leaves != dom.leafCountPaper) { ok = false; msgs.Add($"paper leaf count {dom.leafCountPaper} != {leaves}"); }
            sb.AppendLine($"PART {part}: shards={rows.Count}/256 leaves={leaves} checked={checked_} failing={fails} min_slack={minSlack:E6} (leaf {minLeaf}) cover_and_frontier_partition={(ok ? "EXACT" : "FAIL")} kinds={string.Join(",", kinds.Select(k => k.Key + ":" + k.Value))}");
            foreach (var m in msgs.Take(10)) sb.AppendLine("   ! " + m);
            all &= ok; totLeaves += leaves; totFails += fails; worst = Math.Min(worst, minSlack);
        }
        sb.AppendLine($"TOTAL leaves={totLeaves} failing={totFails} worst_slack_over_{tau}={worst:E6}");
        sb.AppendLine(all ? $"VERDICT: ACCEPT (all leaf proofs pass with interval lower bound > {tau}; exact box partitions; counts equal shipped summaries)" : "VERDICT: REJECT");
        Console.Write(sb.ToString()); if (vout != null) File.WriteAllText(vout, sb.ToString());
        return all ? 0 : 2;
    }
}
