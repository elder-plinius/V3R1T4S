using System.Numerics;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
namespace RidVerify;

public sealed class Record
{
    public int Line;            // 1-based line number in the file
    public string Path;
    public string Component;    // Domain | Global | Local | Exotic
    public int Inequality = -1; // Domain
    public int EdgeA = -1, EdgeB = -1, Vertex = -1; // Global
    public string Cover;        // Local: "0".."29"; Exotic: name
    public string Canonical()
    {
        var sb = new StringBuilder();
        sb.Append("{\"path\":\"").Append(Path).Append("\",\"component\":\"").Append(Component).Append('"');
        switch (Component)
        {
            case "Domain": sb.Append(",\"inequality\":").Append(Inequality); break;
            case "Global": sb.Append(",\"edge\":[").Append(EdgeA).Append(',').Append(EdgeB).Append("],\"vertex\":").Append(Vertex); break;
            case "Local": sb.Append(",\"cover\":").Append(Cover); break;
            case "Exotic": sb.Append(",\"cover\":\"").Append(Cover).Append('"'); break;
            default: throw new Exception("component");
        }
        sb.Append('}');
        return sb.ToString();
    }
    public Record Clone() => (Record)MemberwiseClone();
}

public static class Cert
{
    public static string Sha8(string s)
    {
        var h = SHA256.HashData(Encoding.UTF8.GetBytes(s));
        return Convert.ToHexString(h).ToLowerInvariant().Substring(0, 8);
    }
    public static string Sha256File(string path)
    {
        using var fs = File.OpenRead(path);
        return Convert.ToHexString(SHA256.HashData(fs)).ToLowerInvariant();
    }
    public const string HeaderCanon = "{\"format\":\"rid-certificate/1\",\"policy\":\"65c13764df7a6acf6563e4026025a7305d157d70cb9f3bb40803aeeca64418a5\",\"root\":\"\",\"max_depth\":4096}";

    public sealed class Parsed
    {
        public string HeaderJson;
        public List<Record> Records = new();
        public List<string> Problems = new();
        public int LinesChecksumOk;
        public int Lines;
    }

    /// <summary>Framing: every line "XXXXXXXX json\n"; XXXXXXXX = first 8 lowercase hex of SHA-256 of json (bytes between the space and the newline).
    /// Canonical JSON: re-serialising the parsed record reproduces the text byte for byte.</summary>
    public static Parsed Parse(string file)
    {
        var bytes = File.ReadAllBytes(file);
        var P = new Parsed();
        int pos = 0, ln = 0;
        while (pos < bytes.Length)
        {
            int nl = Array.IndexOf(bytes, (byte)'\n', pos);
            if (nl < 0) { P.Problems.Add($"line {ln + 1}: no terminating newline"); break; }
            var span = new ReadOnlySpan<byte>(bytes, pos, nl - pos);
            ln++;
            pos = nl + 1;
            string line = Encoding.UTF8.GetString(span);
            if (line.Length < 10 || line[8] != ' ') { P.Problems.Add($"line {ln}: framing"); continue; }
            string ck = line.Substring(0, 8), js = line.Substring(9);
            if (js.Contains('\r')) P.Problems.Add($"line {ln}: CR");
            bool ckok = ck == Sha8(js) && ck.All(ch => (ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f'));
            if (ckok) P.LinesChecksumOk++; else P.Problems.Add($"line {ln}: checksum mismatch");
            if (ln == 1)
            {
                P.HeaderJson = js;
                if (js != HeaderCanon) P.Problems.Add("header differs from expected canonical header");
                continue;
            }
            try
            {
                using var doc = JsonDocument.Parse(js);
                var root = doc.RootElement;
                var r = new Record { Line = ln, Path = root.GetProperty("path").GetString(), Component = root.GetProperty("component").GetString() };
                switch (r.Component)
                {
                    case "Domain": r.Inequality = root.GetProperty("inequality").GetInt32(); break;
                    case "Global":
                        var e = root.GetProperty("edge"); r.EdgeA = e[0].GetInt32(); r.EdgeB = e[1].GetInt32(); r.Vertex = root.GetProperty("vertex").GetInt32(); break;
                    case "Local": r.Cover = root.GetProperty("cover").GetInt32().ToString(); break;
                    case "Exotic": r.Cover = root.GetProperty("cover").GetString(); break;
                    default: P.Problems.Add($"line {ln}: unknown component {r.Component}"); continue;
                }
                if (r.Canonical() != js) P.Problems.Add($"line {ln}: non-canonical JSON");
                if (r.Path.Any(ch => ch != '0' && ch != '1')) P.Problems.Add($"line {ln}: path alphabet");
                P.Records.Add(r);
            }
            catch (Exception ex) { P.Problems.Add($"line {ln}: parse error {ex.Message}"); }
        }
        P.Lines = ln;
        return P;
    }

    // ---------- boxes ----------
    public static readonly Q5[] RootLo = { Q5.Zero, Q5.Zero, Q5.Rat(-2, 5), Q5.Rat(-2, 5), Q5.Rat(-2, 5) };
    public static readonly Q5[] RootHi = { Q5.Rat(2, 3), Q5.Rat(2, 5), Q5.Rat(2, 5), Q5.Rat(2, 5), Q5.Rat(2, 5) };
    public static (Q5[] lo, Q5[] hi) BoxOfPath(string path)
    {
        var lo = (Q5[])RootLo.Clone(); var hi = (Q5[])RootHi.Clone();
        for (int k = 0; k < path.Length; k++)
        {
            int a = k % 5;
            var m = (lo[a] + hi[a]) * Q5.Rat(1, 2);
            if (path[k] == '0') hi[a] = m; else if (path[k] == '1') lo[a] = m; else throw new Exception("bad path char");
        }
        return (lo, hi);
    }

    /// <summary>Coverage per paper 11.1: paths are leaves of a finite binary tree rooted at B0.
    /// (a) paper algorithm: read paths by increasing depth, lexicographic within depth, keep list of unaccounted boxes (as paths); must end empty;
    /// (b) independent exact criterion: no duplicates, prefix-free, Kraft sum exactly 1.</summary>
    public static (bool ok, string msg, int maxDepth, double meanDepth) CheckCoverage(List<Record> recs)
    {
        var paths = recs.Select(r => r.Path).ToList();
        int maxD = paths.Max(p => p.Length);
        double meanD = paths.Average(p => (double)p.Length);
        // (b) sorted adjacent prefix test + duplicates
        var sorted = paths.OrderBy(p => p, StringComparer.Ordinal).ToList();
        for (int i = 0; i + 1 < sorted.Count; i++)
        {
            if (sorted[i] == sorted[i + 1]) return (false, $"duplicate path {sorted[i]}", maxD, meanD);
            if (sorted[i + 1].StartsWith(sorted[i], StringComparison.Ordinal)) return (false, $"path {sorted[i]} is a prefix of {sorted[i + 1]}", maxD, meanD);
        }
        BigInteger kraft = 0; var one = BigInteger.One << maxD;
        foreach (var p in paths) kraft += BigInteger.One << (maxD - p.Length);
        if (kraft != one) return (false, $"Kraft sum {kraft}/{one} != 1", maxD, meanD);
        // (a) paper's algorithm: process in depth-then-lexicographic order, maintain unaccounted (frontier) set
        var byOrder = paths.OrderBy(p => p.Length).ThenBy(p => p, StringComparer.Ordinal).ToList();
        var pending = new SortedSet<string>(StringComparer.Ordinal) { "" }; // unaccounted boxes, as paths
        // frontier boxes are refined down to the next record's depth: a pending box that is a proper prefix of the record is split.
        var pend = new HashSet<string> { "" };
        foreach (var p in byOrder)
        {
            // find the pending ancestor (prefix of p); split it down until it equals p
            string anc = null;
            for (int L = 0; L <= p.Length; L++) { var q = p.Substring(0, L); if (pend.Contains(q)) { anc = q; break; } }
            if (anc == null) return (false, $"path {p} not inside an unaccounted box", maxD, meanD);
            pend.Remove(anc);
            for (int L = anc.Length; L < p.Length; L++) { pend.Add(p.Substring(0, L) + (p[L] == '0' ? '1' : '0')); }
        }
        if (pend.Count != 0) return (false, $"{pend.Count} boxes unaccounted at the end", maxD, meanD);
        return (true, "ok", maxD, meanD);
    }
}
