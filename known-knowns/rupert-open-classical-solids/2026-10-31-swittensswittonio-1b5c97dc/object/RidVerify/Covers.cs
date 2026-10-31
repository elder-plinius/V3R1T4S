using System.Numerics;
using System.Text.Json;
namespace RidVerify;

/// <summary>Zoom covers (appendix B + sections 7-10): rebuild each zoom from its parameters, tile its domain by the stored bisection tree,
/// and re-check every terminal cell by the zoom lemma (exact division by the zoom factor, validity conditions at corners, Bernstein sign test).</summary>
public sealed class Witness
{
    public string Kind;       // dir | edge | ineq
    public Q5 N1, N2;         // direction (screen) for dir
    public int Contact = -1, Vertex = -1; // dir: 'vertex' = plug vertex, 'contact' = hole vertex (the one on the supporting line); edge: both = 'vertex'
    public int EdgeA = -1, EdgeB = -1;     // edge
    public int Ineq = -1;
}
public sealed class Leaf { public int Witness = -1; public int[] Factor; public bool Delegated; }
public sealed class Zoom
{
    public string Name, Kind; // Kind: T A B A'
    public int BaseAxis = -1, BaseSide = 0; public int OffAxis = -1, OffSide = 0;
    public string TreeStr; public List<Leaf> Leaves = new();
}
public sealed class Cover
{
    public string Name, Scope;
    public bool Arc; public int Sigma;
    public Q5[] Centre = new Q5[5]; public Q5[,] Map = new Q5[5, 5];
    public bool IsTube; public int NB, NF;
    public Q5[][] TubeBase; public Q5[][] SigmaBox; public Q5[][] PhiBox;
    public Q5 TubeRadius; public Q5[] Radii; public Q5 Radius, Ratio;
    public bool HasWindow; public int WinAxis, WinSide; public Q5[,] Shear; public Q5 WinRadius;
    public bool HasBeyond; public int BeyondAxis, BeyondIneq;
    public List<Witness> Witnesses = new(); public List<Zoom> Zooms = new();

    static Q5 P(JsonElement e) => Q5.ParseRat(e.ValueKind == JsonValueKind.String ? e.GetString() : e.GetRawText());
    static Q5 Pair(JsonElement e) { var a = Q5.ParseRat(e[0].GetString()); var b = Q5.ParseRat(e[1].GetString()); return a + b * Q5.Sqrt5; }
    static Q5[][] Intervals(JsonElement e) { var l = new List<Q5[]>(); foreach (var x in e.EnumerateArray()) l.Add(new[] { P(x[0]), P(x[1]) }); return l.ToArray(); }

    public static Cover Load(string file)
    {
        using var doc = JsonDocument.Parse(File.ReadAllText(file));
        var R = doc.RootElement;
        if (R.GetProperty("format").GetString() != "rid-cover/1") throw new Exception("cover format");
        var c = new Cover { Name = R.GetProperty("name").GetString(), Scope = R.GetProperty("scope").GetString() };
        var pr = R.GetProperty("parameters");
        var co = pr.GetProperty("coordinates");
        if (co.ValueKind == JsonValueKind.String) { if (co.GetString() != "configuration") throw new Exception("coords"); }
        else { c.Arc = true; var pl = co.GetProperty("arc-plane").GetString(); c.Sigma = pl == "plus" ? 1 : pl == "minus" ? -1 : throw new Exception("plane"); }
        for (int i = 0; i < 5; i++) c.Centre[i] = Pair(pr.GetProperty("centre")[i]);
        for (int i = 0; i < 5; i++) for (int j = 0; j < 5; j++) c.Map[i, j] = Pair(pr.GetProperty("map")[i][j]);
        var sh = pr.GetProperty("shape");
        if (sh.TryGetProperty("tube", out var tb))
        {
            c.IsTube = true; c.TubeBase = Intervals(tb.GetProperty("base")); c.PhiBox = Intervals(tb.GetProperty("offset")); c.TubeRadius = P(tb.GetProperty("radius"));
            c.NB = c.TubeBase.Length; c.NF = c.PhiBox.Length;
        }
        else
        {
            var pt = sh.GetProperty("point");
            c.SigmaBox = Intervals(pt.GetProperty("base")); c.PhiBox = Intervals(pt.GetProperty("offset"));
            c.NB = c.SigmaBox.Length; c.NF = c.PhiBox.Length;
            c.Radii = pt.GetProperty("radii").EnumerateArray().Select(P).ToArray(); c.Radius = P(pt.GetProperty("radius")); c.Ratio = P(pt.GetProperty("ratio"));
            var w = pt.GetProperty("window");
            if (w.ValueKind == JsonValueKind.Object)
            {
                c.HasWindow = true; var f = w.GetProperty("faces"); if (f.GetArrayLength() != 1) throw new Exception("window faces");
                c.WinAxis = f[0].GetProperty("axis").GetInt32(); c.WinSide = f[0].GetProperty("side").GetInt32();
                c.WinRadius = P(w.GetProperty("radius"));
                c.Shear = new Q5[c.NF, c.NB];
                var sj = w.GetProperty("shear");
                for (int i = 0; i < c.NF; i++) for (int j = 0; j < c.NB; j++) c.Shear[i, j] = Q5.ParseRat(sj[i][j].GetString());
            }
        }
        if (c.NB + c.NF != 5) throw new Exception("dims");
        var by = pr.GetProperty("beyond");
        if (by.ValueKind == JsonValueKind.Object) { c.HasBeyond = true; c.BeyondAxis = by.GetProperty("axis").GetInt32(); c.BeyondIneq = by.GetProperty("inequality").GetInt32(); }
        foreach (var w in R.GetProperty("witnesses").EnumerateArray())
        {
            var wi = new Witness();
            if (w.TryGetProperty("direction", out var d)) { wi.Kind = "dir"; wi.N1 = Pair(d[0]); wi.N2 = Pair(d[1]); wi.Contact = w.GetProperty("contact").GetInt32(); wi.Vertex = w.GetProperty("vertex").GetInt32(); }
            else if (w.TryGetProperty("edge", out var ed)) { wi.Kind = "edge"; wi.EdgeA = ed[0].GetInt32(); wi.EdgeB = ed[1].GetInt32(); wi.Vertex = w.GetProperty("vertex").GetInt32(); wi.Contact = wi.EdgeA; }
            else { wi.Kind = "ineq"; wi.Ineq = w.GetProperty("inequality").GetInt32(); }
            c.Witnesses.Add(wi);
        }
        foreach (var z in R.GetProperty("zooms").EnumerateArray())
        {
            var zo = new Zoom { Name = z.GetProperty("name").GetString(), TreeStr = z.GetProperty("tree").GetString() };
            ParseName(zo);
            foreach (var l in z.GetProperty("leaves").EnumerateArray())
            {
                var lf = new Leaf();
                if (l.ValueKind == JsonValueKind.String) { if (l.GetString() != "delegated") throw new Exception("leaf"); lf.Delegated = true; }
                else
                {
                    var w = l.GetProperty("witness"); lf.Witness = w.GetProperty("index").GetInt32();
                    lf.Factor = w.GetProperty("factor").EnumerateArray().Select(x => x.GetInt32()).ToArray();
                }
                zo.Leaves.Add(lf);
            }
            c.Zooms.Add(zo);
        }
        return c;
    }
    static void ParseName(Zoom z)
    {
        var parts = z.Name.Split(' ');
        z.Kind = parts[0];
        foreach (var p in parts.Skip(1))
        {
            int axis = p[1] - '0'; int side = p[2] == '+' ? 1 : p[2] == '-' ? -1 : throw new Exception("name");
            if (p[0] == 'b') { z.BaseAxis = axis; z.BaseSide = side; } else if (p[0] == 'o') { z.OffAxis = axis; z.OffSide = side; } else throw new Exception("name");
        }
    }

    // ---------- zoom construction ----------
    public sealed class BuiltZoom
    {
        public Q5[] Lo = new Q5[5], Hi = new Q5[5];
        public Poly[] U = new Poly[3], R = new Poly[3];
        public int[] Dist; // indices of distance coordinates
        public Poly[] OShear; // for delegation: o(y) polynomials (offset in units of mu) - only for A zooms of windowed covers
    }

    List<int> FaceAxes(Q5[][] box, int axisFixed) { var l = new List<int>(); for (int j = 0; j < box.Length; j++) if (j != axisFixed) l.Add(j); return l; }
    static bool HasFace(Q5[][] box, int axis, int side) => side > 0 ? box[axis][1] == Q5.One : box[axis][0] == -Q5.One;
    int FaceIndex(int axis, int side)
    {
        int idx = 0;
        for (int j = 0; j < SigmaBox.Length; j++)
        {
            if (HasFace(SigmaBox, j, -1)) { if (j == axis && side < 0) return idx; idx++; }
            if (HasFace(SigmaBox, j, +1)) { if (j == axis && side > 0) return idx; idx++; }
        }
        throw new Exception("no such base face");
    }

    public BuiltZoom Build(Zoom z)
    {
        var B = new BuiltZoom();
        var y = Enumerable.Range(0, 5).Select(Poly.Var).ToArray();
        var zb = new Poly[NB]; var zo = new Poly[NF];
        int pos = 0;
        var half = Q5.Zero;
        void SetIv(int i, Q5 lo, Q5 hi) { B.Lo[i] = lo; B.Hi[i] = hi; }
        Poly[] FhatFace(int axisFixed, int side, Q5[][] box, ref int p) // returns unit-cube-face vector with free coords as variables y[p..]
        {
            int n = box.Length; var f = new Poly[n];
            for (int j = 0; j < n; j++)
            {
                if (j == axisFixed) f[j] = Poly.Const(side);
                else { f[j] = y[p]; SetIv(p, box[j][0], box[j][1]); p++; }
            }
            return f;
        }
        if (z.Kind == "T")
        {
            if (!IsTube) throw new Exception("T zoom in a point cover");
            for (int j = 0; j < NB; j++) { zb[j] = y[j]; SetIv(j, TubeBase[j][0], TubeBase[j][1]); }
            var delta = y[NB]; SetIv(NB, Q5.Zero, TubeRadius); pos = NB + 1;
            var f = FhatFace(z.OffAxis, z.OffSide, PhiBox, ref pos);
            for (int k = 0; k < NF; k++) zo[k] = delta * f[k];
            B.Dist = new[] { NB };
        }
        else
        {
            if (IsTube) throw new Exception("point zoom in tube cover");
            if (z.Kind == "A" || z.Kind == "A'")
            {
                if (!HasFace(SigmaBox, z.BaseAxis, z.BaseSide)) throw new Exception("base face not on box");
                var mu = y[0]; var rho = y[1];
                SetIv(0, Q5.Zero, Radii[FaceIndex(z.BaseAxis, z.BaseSide)]);
                SetIv(1, Q5.Zero, z.Kind == "A" ? Ratio : WinRadius);
                pos = 2;
                var bh = FhatFace(z.BaseAxis, z.BaseSide, SigmaBox, ref pos);
                var fh = FhatFace(z.OffAxis, z.OffSide, PhiBox, ref pos);
                for (int j = 0; j < NB; j++) zb[j] = mu * bh[j];
                for (int k = 0; k < NF; k++) zo[k] = rho * mu * fh[k];
                if (z.Kind == "A'")
                {
                    if (!HasWindow || WinAxis != z.BaseAxis || WinSide != z.BaseSide) throw new Exception("sheared zoom on non-window face");
                    for (int k = 0; k < NF; k++) for (int j = 0; j < NB; j++) zo[k] = zo[k] - Shear[k, j] * zb[j];
                }
                B.Dist = new[] { 0, 1 };
            }
            else if (z.Kind == "B")
            {
                var delta = y[0]; SetIv(0, Q5.Zero, Radius);
                var inv = Ratio.Inv();
                pos = 1;
                var b = new Poly[NB];
                for (int j = 0; j < NB; j++) { b[j] = y[pos]; SetIv(pos, Q5.Max(SigmaBox[j][0], -inv), Q5.Min(SigmaBox[j][1], inv)); pos++; }
                var fh = FhatFace(z.OffAxis, z.OffSide, PhiBox, ref pos);
                for (int j = 0; j < NB; j++) zb[j] = delta * b[j];
                for (int k = 0; k < NF; k++) zo[k] = delta * fh[k];
                B.Dist = new[] { 0 };
            }
            else throw new Exception("zoom kind");
        }
        if (pos != 5) throw new Exception($"zoom {z.Name}: coordinate count {pos}");
        // x = centre + map * z
        var zz = zb.Concat(zo).ToArray();
        var x = new Poly[5];
        for (int i = 0; i < 5; i++)
        {
            var s = Poly.Const(Centre[i]);
            for (int j = 0; j < 5; j++) if (!Map[i, j].IsZero) s = s + Map[i, j] * zz[j];
            x[i] = s;
        }
        if (!Arc) { B.U = new[] { x[0], x[1], Poly.Const(1) }; B.R = new[] { x[2], x[3], x[4] }; }
        else
        {
            // arc coordinates x=(e,v,theta,zeta1,zeta3): u=(1-2e, v, 2+e);  r = sigma*rA + theta*w_sigma + (zeta1,0,zeta3)
            var a1 = new Q5(-5, 3, 10); var a3 = new Q5(-5, 1, 10);
            B.U = new[] { Poly.Const(1) - 2 * x[0], x[1], Poly.Const(2) + x[0] };
            var sg = Q5.Int(Sigma);
            B.R = new[] {
                Poly.Const(sg * a1) + (sg * a3) * x[2] + x[3],
                x[2],
                Poly.Const(sg * a3) + (-(sg * a1)) * x[2] + x[4] };
        }
        return B;
    }
}
