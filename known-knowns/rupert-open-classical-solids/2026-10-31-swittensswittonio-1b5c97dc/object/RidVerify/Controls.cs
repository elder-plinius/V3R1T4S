using System.Numerics;
namespace RidVerify;

/// <summary>Negative controls. Each corrupted claim carries an independent falsity certificate: an exact point evaluation (pointwise code, not the Bernstein/interval code)
/// showing that the corrupted claim is mathematically false at some rational point of the box. The verifier must refuse every certified-false mutant.</summary>
public static class Controls
{
    public sealed class Outcome { public string Category; public int Tried, Certified, Refused, Accepted; public List<string> AcceptedExamples = new(); public int UncertifiedAccepted; }
    static Q5 Mid(Q5 a, Q5 b) => (a + b) * Q5.Rat(1, 2);
    static IEnumerable<Q5[]> TestPoints(Q5[] lo, Q5[] hi)
    {
        yield return Enumerable.Range(0, 5).Select(i => Mid(lo[i], hi[i])).ToArray();
        for (int m = 0; m < 32; m++) yield return Enumerable.Range(0, 5).Select(i => ((m >> i) & 1) == 1 ? hi[i] : lo[i]).ToArray();
    }
    // --- pointwise falsity certificates ---
    static bool DomainClaimFalseAt(int idx, Q5[] pt) => Geo.DomainIneq(idx).Eval(pt).Sign() <= 0; // q<=0 at the point: point satisfies the inequality, so "q>0 throughout the box" is false
    static bool GlobalClaimFalseAt(int a, int b, int vp, Q5[] pt)
    {
        var s = pt[0]; var t = pt[1]; var r = new[] { pt[2], pt[3], pt[4] };
        var u = new[] { s, t, Q5.One }; var e = new[] { Geo.V[b][0] - Geo.V[a][0], Geo.V[b][1] - Geo.V[a][1], Geo.V[b][2] - Geo.V[a][2] };
        var n = new[] { u[1] * e[2] - u[2] * e[1], u[2] * e[0] - u[0] * e[2], u[0] * e[1] - u[1] * e[0] };
        var rr = r[0] * r[0] + r[1] * r[1] + r[2] * r[2]; var d = Q5.One + rr;
        var vpv = Geo.V[vp]; var rv = r[0] * vpv[0] + r[1] * vpv[1] + r[2] * vpv[2];
        var cr = new[] { r[1] * vpv[2] - r[2] * vpv[1], r[2] * vpv[0] - r[0] * vpv[2], r[0] * vpv[1] - r[1] * vpv[0] };
        var Rv = new Q5[3]; for (int k = 0; k < 3; k++) Rv[k] = (Q5.One - rr) * vpv[k] + 2 * r[k] * rv + 2 * cr[k];
        Q5 plug = n[0] * Rv[0] + n[1] * Rv[1] + n[2] * Rv[2];
        for (int v = 0; v < 60; v++)
        {
            var hv = Geo.V[v]; var hole = d * (n[0] * hv[0] + n[1] * hv[1] + n[2] * hv[2]);
            if ((plug - hole).Sign() <= 0) return true; // some hole vertex is not strictly below the plug vertex in direction n: claim false at this point
        }
        return false;
    }
    /// <summary>Pointwise membership in the covered set (independent of the interval code in RecordCover).</summary>
    public static bool PointInLocal(int k, Q5[] p)
    {
        var row = RecordCover.LocalRows[k]; var eps = Q5.Rat(1, 1024);
        var s0 = row.S0 - eps; if (s0.Sign() < 0) s0 = Q5.Zero; var s1 = row.S1 + eps; if (s1 > Q5.Rat(2, 3)) s1 = Q5.Rat(2, 3);
        var t0 = row.T0 - eps; if (t0.Sign() < 0) t0 = Q5.Zero; var t1 = row.T1 + eps; if (t1 > Q5.Rat(2, 5)) t1 = Q5.Rat(2, 5);
        if (p[0] < s0 || p[0] > s1 || p[1] < t0 || p[1] > t1) return false;
        for (int i = 2; i < 5; i++) if (p[i].Sign() < 0 ? -p[i] > row.Delta : p[i] > row.Delta) return false;
        return true;
    }
    public static bool PointInExotic(string name, Q5[] p)
    {
        Q5 Abs(Q5 x) => x.Sign() < 0 ? -x : x;
        var s = p[0]; var t = p[1]; var r = new[] { p[2], p[3], p[4] };
        if (name == "square") return s.Sign() >= 0 && s <= Q5.Rat(1, 8) && t.Sign() >= 0 && t <= Q5.Rat(1, 8) && r.All(x => Abs(x) <= Q5.Rat(1, 8));
        if (name == "pentagon") { var eta = s + Geo.PhiBar * t; var xi = s + Geo.Phi * t + Geo.PhiBar; return Abs(eta) <= Q5.Rat(1, 32) && xi >= Q5.Rat(-1, 32) && r.All(x => Abs(x) <= Q5.Rat(1, 16)); }
        int sg = name.EndsWith("+") ? 1 : -1;
        var e = (Q5.One - 2 * s) / (Q5.Int(2) + s); var v = 5 * t / (Q5.Int(2) + s);
        var a1 = new Q5(-5, 3, 10); var a3 = new Q5(-5, 1, 10);
        var th = r[1]; var z1 = r[0] - sg * (a1 + a3 * th); var z3 = r[2] - sg * (a3 - a1 * th);
        Q5 dd = name.StartsWith("crossing") ? Q5.Rat(1, 16) : Q5.Rat(1, 32);
        bool offs = Abs(th) <= dd && Abs(z1) <= dd && Abs(z3) <= dd;
        if (name.StartsWith("arc")) return e >= Q5.Rat(3, 64) && e <= Q5.Rat(3, 16) && v.Sign() >= 0 && v <= Q5.Rat(1, 16) && offs;
        if (name.StartsWith("endpoint")) { var es = new Q5(-2, 1, 1); return e >= es - Q5.Rat(1, 16) && e <= es + Q5.Rat(1, 32) && v.Sign() >= 0 && v <= Q5.Rat(1, 16) && offs; }
        return Abs(e) <= Q5.Rat(1, 16) && v.Sign() >= 0 && v <= Q5.Rat(5, 64) && offs;
    }
    static readonly string[] ExoticNames = { "square", "pentagon", "arc+", "arc-", "endpoint+", "endpoint-", "crossing+", "crossing-" };

    public static List<Outcome> Run(Cert.Parsed P, string coversDir, Action<string> log, int seed = 7)
    {
        var rng = new Random(seed); var outs = new List<Outcome>();
        Outcome New(string c) { var o = new Outcome { Category = c }; outs.Add(o); return o; }
        void Finish(Outcome o, Record mut, bool certified, Func<Record, bool> verify)
        {
            o.Tried++;
            bool acc = false; try { acc = verify(mut); } catch { acc = false; }
            if (certified) { o.Certified++; if (acc) { o.Accepted++; o.AcceptedExamples.Add(mut.Canonical()); } else o.Refused++; }
            else if (acc) o.UncertifiedAccepted++;
        }
        bool VerifyAny(Record r) => r.Component switch
        {
            "Domain" => Checks.Domain(r),
            "Global" => Checks.GlobalFast(r.EdgeA, r.EdgeB, r.Vertex, r.Path),
            "Local" or "Exotic" => RecordCover.Record(r),
            _ => false
        };
        var dom = P.Records.Where(r => r.Component == "Domain").ToList(); var glo = P.Records.Where(r => r.Component == "Global").ToList();
        var loc = P.Records.Where(r => r.Component == "Local").ToList(); var exo = P.Records.Where(r => r.Component == "Exotic").ToList();
        var edgeReps = glo.Select(r => (r.EdgeA, r.EdgeB)).Distinct().ToList();
        T Pick<T>(List<T> l) => l[rng.Next(l.Count)];
        string FlipBit(string path) { int i = rng.Next(path.Length); var c = path.ToCharArray(); c[i] = c[i] == '0' ? '1' : '0'; return new string(c); }

        // A. wrong inequality index (Domain)
        { var o = New("wrong inequality index (Domain)"); int guard = 0;
          while (o.Certified < 100 && guard++ < 4000)
          {
              var r = Pick(dom).Clone(); int old = r.Inequality; int ni; do ni = rng.Next(Geo.NumIneq); while (ni == old); r.Inequality = ni;
              var (lo, hi) = Cert.BoxOfPath(r.Path); bool cert = TestPoints(lo, hi).Any(pt => DomainClaimFalseAt(ni, pt));
              if (!cert && rng.Next(8) != 0) continue; Finish(o, r, cert, VerifyAny); } }
        // B. wrong edge / vertex (Global)
        { var o = New("wrong edge or plug vertex (Global)"); int guard = 0;
          while (o.Certified < 120 && guard++ < 4000)
          {
              var r = Pick(glo).Clone();
              switch (rng.Next(4))
              {
                  case 0: r.Vertex = rng.Next(60); break;
                  case 1: { var e = Pick(edgeReps); r.EdgeA = e.Item1; r.EdgeB = e.Item2; } break;
                  case 2: (r.EdgeA, r.EdgeB) = (r.EdgeB, r.EdgeA); break; // reversed orientation
                  default: r.EdgeA = rng.Next(60); r.EdgeB = rng.Next(60); if (r.EdgeA == r.EdgeB) continue; break;
              }
              var (lo, hi) = Cert.BoxOfPath(r.Path); bool cert = TestPoints(lo, hi).Any(pt => GlobalClaimFalseAt(r.EdgeA, r.EdgeB, r.Vertex, pt));
              if (!cert && rng.Next(8) != 0) continue; Finish(o, r, cert, VerifyAny); } }
        // C. perturbed path
        { var o = New("perturbed path (bit flip, Domain/Global)"); int guard = 0;
          while (o.Certified < 100 && guard++ < 4000)
          {
              bool g = rng.Next(2) == 0; var r = (g ? Pick(glo) : Pick(dom)).Clone(); r.Path = FlipBit(r.Path);
              var (lo, hi) = Cert.BoxOfPath(r.Path);
              bool cert = g ? TestPoints(lo, hi).Any(pt => GlobalClaimFalseAt(r.EdgeA, r.EdgeB, r.Vertex, pt)) : TestPoints(lo, hi).Any(pt => DomainClaimFalseAt(r.Inequality, pt));
              if (!cert && rng.Next(8) != 0) continue; Finish(o, r, cert, VerifyAny); } }
        // D. box moved outside the cover (Local / Exotic)
        { var o = New("box outside named cover (Local/Exotic, other cover or shifted box)"); int guard = 0;
          while (o.Certified < 120 && guard++ < 6000)
          {
              bool l = rng.Next(2) == 0; var r = (l ? Pick(loc) : Pick(exo)).Clone();
              int mode = rng.Next(3);
              if (mode == 0) { if (l) r.Cover = rng.Next(30).ToString(); else r.Cover = Pick(ExoticNames.ToList()); }
              else if (mode == 1) r.Path = FlipBit(r.Path.Substring(0, Math.Min(r.Path.Length, 8))) + r.Path.Substring(Math.Min(r.Path.Length, 8)); // move the box at coarse level
              else { r.Path = FlipBit(r.Path); if (l) r.Cover = rng.Next(30).ToString(); }
              var (lo, hi) = Cert.BoxOfPath(r.Path);
              bool inAll = TestPoints(lo, hi).Skip(1).All(pt => l ? PointInLocal(int.Parse(r.Cover), pt) : PointInExotic(r.Cover, pt));
              bool cert = !inAll; // some corner lies outside the covered set
              if (!cert && rng.Next(8) != 0) continue; Finish(o, r, cert, VerifyAny); } }
        // E. wrong component
        { var o = New("wrong component label"); int guard = 0;
          while (o.Certified < 100 && guard++ < 6000)
          {
              var src = new[] { dom, glo, loc, exo }[rng.Next(4)]; var r = Pick(src).Clone(); var (lo, hi) = Cert.BoxOfPath(r.Path);
              string[] comps = { "Domain", "Global", "Local", "Exotic" }; string to; do to = comps[rng.Next(4)]; while (to == r.Component); r.Component = to;
              bool cert = false;
              switch (to)
              {
                  case "Domain": r.Inequality = rng.Next(Geo.NumIneq); cert = TestPoints(lo, hi).Any(pt => DomainClaimFalseAt(r.Inequality, pt)); break;
                  case "Global": { var e = Pick(edgeReps); r.EdgeA = e.Item1; r.EdgeB = e.Item2; r.Vertex = rng.Next(60); cert = TestPoints(lo, hi).Any(pt => GlobalClaimFalseAt(r.EdgeA, r.EdgeB, r.Vertex, pt)); break; }
                  case "Local": r.Cover = rng.Next(30).ToString(); cert = TestPoints(lo, hi).Skip(1).Any(pt => !PointInLocal(int.Parse(r.Cover), pt)); break;
                  default: r.Cover = Pick(ExoticNames.ToList()); cert = TestPoints(lo, hi).Skip(1).Any(pt => !PointInExotic(r.Cover, pt)); break;
              }
              if (!cert && rng.Next(8) != 0) continue; Finish(o, r, cert, VerifyAny); } }
        // F. structural corruption of the certificate framing and coverage (built on a small synthetic file plus the real record list)
        { var o = New("certificate framing/coverage corruption"); string tmp = Path.Combine(Path.GetTempPath(), "rid_ctl_" + Environment.ProcessId + ".cert");
          var lines = new List<string>(); using (var rd = new StreamReader(File.OpenRead(Environment.GetEnvironmentVariable("RID_CERT") ?? "../../../../data/hervay_inputs/certificate/search.cert"))) { for (int i = 0; i < 6; i++) lines.Add(rd.ReadLine()); }
          Func<string[], Cert.Parsed> parse = ls => { File.WriteAllText(tmp, string.Join("\n", ls) + "\n"); return Cert.Parse(tmp); };
          var baseOk = parse(lines.ToArray()); if (baseOk.Problems.Count != 0) throw new Exception("control base not clean: " + string.Join(";", baseOk.Problems));
          var muts = new List<string[]>();
          for (int k = 0; k < lines.Count; k++) for (int j = 0; j < 8; j++)
              {
                  var ls = lines.ToArray(); var line = ls[k]; var chars = line.ToCharArray(); int pos;
                  switch (j)
                  {
                      case 0: pos = rng.Next(8); chars[pos] = chars[pos] == '0' ? '1' : '0'; break;           // checksum digit flip
                      case 1: pos = 9 + rng.Next(line.Length - 9); chars[pos] = (char)(chars[pos] ^ 1); break; // payload byte flip (checksum stale)
                      case 2: ls[k] = line.Replace("\"component\"", "\"component\" "); chars = ls[k].ToCharArray(); break; // non-canonical whitespace (checksum stale)
                      case 3: { var js = line.Substring(9).Replace("Domain", "Global"); ls[k] = Cert.Sha8(js) + " " + js; chars = ls[k].ToCharArray(); } break; // relabel with fresh checksum -> fails parse/canonical
                      case 4: { var js = line.Substring(9).Replace(":\"", ": \""); ls[k] = Cert.Sha8(js) + " " + js; chars = ls[k].ToCharArray(); } break; // fresh checksum but non-canonical spacing
                      case 5: ls[k] = line.Substring(0, 8) + line.Substring(9); chars = ls[k].ToCharArray(); break; // missing space
                      case 6: ls[k] = line.ToUpperInvariant(); chars = ls[k].ToCharArray(); break;               // uppercase hex checksum
                      default: ls[k] = line + "\r"; chars = ls[k].ToCharArray(); break;                          // CR
                  }
                  ls[k] = new string(chars); if (ls[k] == lines[k]) continue; muts.Add(ls);
              }
          foreach (var ls in muts) { o.Tried++; o.Certified++; var pr = parse(ls); if (pr.Problems.Count > 0) o.Refused++; else { o.Accepted++; o.AcceptedExamples.Add(string.Join("\\n", ls)); } }
          // coverage corruption on the real record list
          var recs = P.Records;
          for (int k = 0; k < 25; k++)
          {
              var copy = recs.Select(x => x).ToList(); int i = rng.Next(copy.Count); string what;
              switch (k % 5)
              {
                  case 0: copy.RemoveAt(i); what = "delete record"; break;
                  case 1: copy.Add(copy[i]); what = "duplicate record"; break;
                  case 2: { var c = copy[i].Clone(); c.Path = FlipBit(c.Path); copy[i] = c; what = "flip path bit"; } break;
                  case 3: { var c = copy[i].Clone(); c.Path = c.Path.Substring(0, c.Path.Length - 1); copy[i] = c; what = "truncate path (prefix)"; } break;
                  default: { var c = copy[i].Clone(); c.Path += "0"; copy[i] = c; what = "extend path"; } break;
              }
              o.Tried++; o.Certified++; var res = Cert.CheckCoverage(copy);
              if (!res.ok) o.Refused++; else { o.Accepted++; o.AcceptedExamples.Add($"coverage accepted after: {what} at record {i}"); }
          }
          try { File.Delete(tmp); } catch { } }
        // G. zoom-cover cell corruption
        { var o = New("zoom-cover cell corruption (witness / factor / validity)"); int guard = 0; var covs = new List<Cover>();
          foreach (var f in Directory.GetFiles(Path.Combine(coversDir, "local"), "*.json").Concat(Directory.GetFiles(Path.Combine(coversDir, "exotic"), "*.json"))) covs.Add(Cover.Load(f));
          while (o.Certified < 100 && guard++ < 3000)
          {
              var c = Pick(covs); int zi = rng.Next(c.Zooms.Count); var z = c.Zooms[zi]; if (z.Leaves.Count == 0) continue; int li = rng.Next(z.Leaves.Count); var leaf = z.Leaves[li];
              if (leaf.Delegated) continue;
              var cells = CoverCheck.CellsOfZoom(c, zi); var (lo, hi) = cells[li];
              var m = new Leaf { Witness = leaf.Witness, Factor = (int[])leaf.Factor.Clone() };
              int kind = rng.Next(3); if (kind == 0) m.Witness = rng.Next(c.Witnesses.Count); else if (kind == 1) { var d = c.Build(z).Dist; m.Factor[d[rng.Next(d.Length)]] += 1; } else { var d = c.Build(z).Dist; int di = d[rng.Next(d.Length)]; if (m.Factor[di] > 0) m.Factor[di] -= 1; else m.Factor[di] += 2; }
              if (m.Witness == leaf.Witness && m.Factor.SequenceEqual(leaf.Factor)) continue;
              // falsity certificate: exact evaluation at points: (i) p does not vanish where the zoom-factor coordinate vanishes, or (ii) quotient N <= 0 at a cell corner/centre
              bool cert = false;
              try
              {
                  var (p, N, bz) = CoverCheck.WitnessPolys(c, zi, m);
                  var pts = new List<Q5[]>(); pts.Add(Enumerable.Range(0, 5).Select(i => Mid(lo[i], hi[i])).ToArray());
                  for (int mm = 0; mm < 32; mm++) pts.Add(Enumerable.Range(0, 5).Select(i => ((mm >> i) & 1) == 1 ? hi[i] : lo[i]).ToArray());
                  if (N != null) cert = pts.Any(pt => N.Eval(pt).Sign() <= 0);
                  else
                  {
                      for (int i = 0; i < 5 && !cert; i++) if (m.Factor[i] > 0 && c.Build(z).Dist.Contains(i))
                          { var pt = Enumerable.Range(0, 5).Select(j => Mid(lo[j], hi[j])).ToArray(); pt[i] = Q5.Zero; cert = !p.Eval(pt).IsZero; }
                  }
              }
              catch { cert = false; }
              if (!cert && rng.Next(6) != 0) continue;
              o.Tried++;
              bool acc; try { acc = CoverCheck.CheckOneCell(c, zi, m, lo, hi, out _); } catch { acc = false; }
              if (cert) { o.Certified++; if (acc) { o.Accepted++; o.AcceptedExamples.Add($"{c.Name}/{z.Name} cell {li}"); } else o.Refused++; } else if (acc) o.UncertifiedAccepted++;
          } }
        foreach (var o in outs) log($"control [{o.Category}]: tried {o.Tried}, certified-false {o.Certified}, refused {o.Refused}, ACCEPTED {o.Accepted}, (uncertified mutants accepted: {o.UncertifiedAccepted})");
        return outs;
    }
}
