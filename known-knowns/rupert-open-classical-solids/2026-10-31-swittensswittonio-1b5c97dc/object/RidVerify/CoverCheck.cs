using System.Collections.Concurrent;
using System.Numerics;
namespace RidVerify;

public sealed class CoverReport
{
    public string Name; public int Zooms, Cells, Accepted, Rejected, Delegated, DelegatedOk, DomainWitnessCells;
    public List<string> Problems = new();
    public bool Ok => Rejected == 0 && Problems.Count == 0;
}

public static class CoverCheck
{
    sealed class Node { public int Axis = -1; public Node Lo, Hi; }
    static Node ParseTree(string s, ref int pos)
    {
        char c = s[pos++];
        if (c == '.') return new Node();
        int ax = c - '0'; if (ax < 0 || ax > 4) throw new Exception("tree axis");
        var n = new Node { Axis = ax }; n.Lo = ParseTree(s, ref pos); n.Hi = ParseTree(s, ref pos); return n;
    }
    static void Cells(Node n, Q5[] lo, Q5[] hi, List<(Q5[] lo, Q5[] hi)> outl)
    {
        if (n.Axis < 0) { outl.Add(((Q5[])lo.Clone(), (Q5[])hi.Clone())); return; }
        var m = (lo[n.Axis] + hi[n.Axis]) * Q5.Rat(1, 2);
        var h1 = (Q5[])hi.Clone(); h1[n.Axis] = m; Cells(n.Lo, lo, h1, outl);
        var l2 = (Q5[])lo.Clone(); l2[n.Axis] = m; Cells(n.Hi, l2, hi, outl);
    }

    static Poly[] NOfWitness(Witness w, Poly[] u)
    {
        if (w.Kind == "dir")
            return new[] { u[2] * w.N1, u[2] * w.N2, -(u[0] * w.N1 + u[1] * w.N2) };
        var e = new Poly[3]; for (int i = 0; i < 3; i++) e[i] = Poly.Const(Geo.V[w.EdgeB][i] - Geo.V[w.EdgeA][i]);
        return new[] { u[1] * e[2] - u[2] * e[1], u[2] * e[0] - u[0] * e[2], u[0] * e[1] - u[1] * e[0] };
    }

    /// <summary>Expected zoom family names for a cover (tube coverage / point coverage lemmas).</summary>
    static HashSet<string> ExpectedZooms(Cover c)
    {
        var set = new HashSet<string>();
        var offFaces = new List<string>();
        for (int k = 0; k < c.NF; k++) { if (c.PhiBox[k][0] == -Q5.One) offFaces.Add($"o{k}-"); if (c.PhiBox[k][1] == Q5.One) offFaces.Add($"o{k}+"); }
        if (c.IsTube) { foreach (var f in offFaces) set.Add("T " + f); return set; }
        var baseFaces = new List<string>();
        for (int j = 0; j < c.NB; j++) { if (c.SigmaBox[j][0] == -Q5.One) baseFaces.Add($"b{j}-"); if (c.SigmaBox[j][1] == Q5.One) baseFaces.Add($"b{j}+"); }
        foreach (var g in baseFaces) foreach (var f in offFaces) set.Add($"A {g} {f}");
        foreach (var f in offFaces) set.Add($"B {f}");
        if (c.HasWindow) { var g = $"b{c.WinAxis}{(c.WinSide > 0 ? '+' : '-')}"; foreach (var f in offFaces) set.Add($"A' {g} {f}"); }
        return set;
    }

    public static CoverReport Check(Cover c, int threads, bool verbose = false)
    {
        var rep = new CoverReport { Name = c.Name };
        // zoom family completeness
        var exp = ExpectedZooms(c); var have = c.Zooms.Select(z => z.Name).ToList();
        if (have.Count != have.Distinct().Count()) rep.Problems.Add("duplicate zoom names");
        if (!exp.SetEquals(have)) rep.Problems.Add($"zoom family mismatch: missing [{string.Join(",", exp.Except(have))}] extra [{string.Join(",", have.Except(exp))}]");
        rep.Zooms = c.Zooms.Count;
        var polyCache = new ConcurrentDictionary<(int, int), Poly>();
        var work = new List<(int zi, Cover.BuiltZoom bz, Node tree, List<(Q5[] lo, Q5[] hi)> cells)>();
        for (int zi = 0; zi < c.Zooms.Count; zi++)
        {
            var z = c.Zooms[zi];
            Cover.BuiltZoom bz;
            try { bz = c.Build(z); } catch (Exception ex) { rep.Problems.Add($"zoom {z.Name}: build failed: {ex.Message}"); continue; }
            // Definition (zoom): u3>0 on Y; u components of degree <=1 in each coordinate; distance coords >=0 and no-fit set when they vanish
            if (!bz.U[2].BernsteinAllStrict(bz.Lo, bz.Hi, +1)) rep.Problems.Add($"zoom {z.Name}: u3 not >0 on domain");
            foreach (var up in bz.U) if (up.Degrees().Any(d => d > 1)) rep.Problems.Add($"zoom {z.Name}: u has degree >1 in a coordinate");
            foreach (var d in bz.Dist)
            {
                if (bz.Lo[d].Sign() < 0) rep.Problems.Add($"zoom {z.Name}: distance coordinate negative");
                // no-fit set at y_d = 0
                var zero = Poly.Const(0);
                if (!c.Arc) { foreach (var rp in bz.R) if (!rp.Subst(d, zero).IsZero) rep.Problems.Add($"zoom {z.Name}: r not zero where distance coordinate {d} vanishes"); }
                else
                {
                    var a1 = new Q5(-5, 3, 10); var a3 = new Q5(-5, 1, 10); var sg = Q5.Int(c.Sigma);
                    var t0 = bz.U[1].Subst(d, zero);
                    var c1 = (bz.R[0] - sg * (Poly.Const(a1) + a3 * bz.R[1])).Subst(d, zero);
                    var c3 = (bz.R[2] - sg * (Poly.Const(a3) - a1 * bz.R[1])).Subst(d, zero);
                    if (!t0.IsZero || !c1.IsZero || !c3.IsZero) rep.Problems.Add($"zoom {z.Name}: not on arc plane where distance coordinate {d} vanishes");
                }
            }
            int p = 0; Node tree;
            try { tree = ParseTree(z.TreeStr, ref p); if (p != z.TreeStr.Length) throw new Exception("trailing tree text"); }
            catch (Exception ex) { rep.Problems.Add($"zoom {z.Name}: tree: {ex.Message}"); continue; }
            var cells = new List<(Q5[], Q5[])>(); Cells(tree, bz.Lo, bz.Hi, cells);
            if (cells.Count != z.Leaves.Count) { rep.Problems.Add($"zoom {z.Name}: {cells.Count} cells but {z.Leaves.Count} leaves"); continue; }
            work.Add((zi, bz, tree, cells));
        }
        var flat = new List<(int zi, int li, Cover.BuiltZoom bz, Q5[] lo, Q5[] hi)>();
        foreach (var w in work) for (int li = 0; li < w.cells.Count; li++) flat.Add((w.zi, li, w.bz, w.cells[li].lo, w.cells[li].hi));
        int acc = 0, rej = 0, del = 0, delOk = 0, domCells = 0;
        var msgs = new ConcurrentBag<string>();
        // window check helper: offset-in-units-of-mu polynomials
        Parallel.ForEach(flat, new ParallelOptions { MaxDegreeOfParallelism = threads }, f =>
        {
            var z = c.Zooms[f.zi]; var leaf = z.Leaves[f.li];
            bool ok;
            string why = "";
            try { ok = CheckLeaf(c, z, f.zi, leaf, f.bz, f.lo, f.hi, polyCache, out why, out bool isDel); if (isDel) { Interlocked.Increment(ref del); if (ok) Interlocked.Increment(ref delOk); } else if (leaf.Witness >= 0 && c.Witnesses[leaf.Witness].Kind == "ineq") Interlocked.Increment(ref domCells); }
            catch (Exception ex) { ok = false; why = "exception " + ex.Message; }
            if (ok) Interlocked.Increment(ref acc); else { Interlocked.Increment(ref rej); if (msgs.Count < 20) msgs.Add($"{z.Name} cell {f.li}: {why}"); }
        });
        rep.Cells = flat.Count; rep.Accepted = acc; rep.Rejected = rej; rep.Delegated = del; rep.DelegatedOk = delOk; rep.DomainWitnessCells = domCells;
        foreach (var m in msgs) rep.Problems.Add(m);
        // cells whose zoom could not be built are not counted as accepted
        return rep;
    }

    /// <summary>Test hook: check one (possibly mutated) leaf on a cell; returns acceptance and, for controls, an exact point-evaluation falsity certificate.</summary>
    public static bool CheckOneCell(Cover c, int zi, Leaf leaf, Q5[] lo, Q5[] hi, out string why)
    {
        var bz = c.Build(c.Zooms[zi]);
        return CheckLeaf(c, c.Zooms[zi], zi, leaf, bz, lo, hi, new ConcurrentDictionary<(int, int), Poly>(), out why, out _);
    }
    public static (Poly p, Poly N, Cover.BuiltZoom bz) WitnessPolys(Cover c, int zi, Leaf leaf)
    {
        var z = c.Zooms[zi]; var bz = c.Build(z); var w = c.Witnesses[leaf.Witness];
        Poly p = w.Kind == "ineq" ? Geo.DomainIneqHomogeneous(w.Ineq, bz.U, bz.R) : Geo.GapPoly(NOfWitness(w, bz.U), bz.R, Geo.V[w.Vertex], Geo.V[w.Contact]);
        Poly N = p.DivisibleBy(leaf.Factor) ? p.DivideByMonomial(leaf.Factor) : null;
        return (p, N, bz);
    }
    public static List<(Q5[] lo, Q5[] hi)> CellsOfZoom(Cover c, int zi)
    {
        var z = c.Zooms[zi]; var bz = c.Build(z); int p = 0; var tree = ParseTree(z.TreeStr, ref p);
        var l = new List<(Q5[], Q5[])>(); Cells(tree, bz.Lo, bz.Hi, l); return l;
    }
    static bool CheckLeaf(Cover c, Zoom z, int zi, Leaf leaf, Cover.BuiltZoom bz, Q5[] lo, Q5[] hi, ConcurrentDictionary<(int, int), Poly> cache, out string why, out bool isDelegated)
    {
        why = ""; isDelegated = leaf.Delegated;
        if (leaf.Delegated)
        {
            // Hand-over lemma: cell of an A zoom on the window base face with o(y) = rho*fhat + shear (units of mu) inside rho0' * Phi
            if (!(c.HasWindow && z.Kind == "A" && z.BaseAxis == c.WinAxis && z.BaseSide == c.WinSide)) { why = "delegated cell outside window family A"; return false; }
            var y = Enumerable.Range(0, 5).Select(Poly.Var).ToArray();
            // rebuild rho*fhat: rho = y1; fhat from zoom structure: free coords after (mu,rho,bfree...)
            int pos = 2 + (c.NB - 1);
            var fh = new Poly[c.NF];
            for (int k = 0; k < c.NF; k++) { if (k == z.OffAxis) fh[k] = Poly.Const(z.OffSide); else { fh[k] = y[pos]; pos++; } }
            for (int k = 0; k < c.NF; k++)
            {
                var o = y[1] * fh[k];
                for (int j = 0; j < c.NB; j++) { var bhat = (j == z.BaseAxis) ? Poly.Const(z.BaseSide) : throw new Exception("window needs 1-D base"); o = o + c.Shear[k, j] * bhat; }
                var (rl, rh) = o.IntervalRange(lo, hi);
                var pl = c.WinRadius * c.PhiBox[k][0]; var ph = c.WinRadius * c.PhiBox[k][1];
                if (rl < pl || rh > ph) { why = $"o[{k}] range outside rho0'*Phi"; return false; }
            }
            return true;
        }
        if (leaf.Witness < 0 || leaf.Witness >= c.Witnesses.Count) { why = "bad witness index"; return false; }
        var w = c.Witnesses[leaf.Witness];
        // zoom factor supported on distance coordinates only
        for (int i = 0; i < 5; i++) if (leaf.Factor[i] != 0 && !bz.Dist.Contains(i)) { why = "zoom factor on non-distance coordinate"; return false; }
        var p = cache.GetOrAdd((zi, leaf.Witness), _ =>
        {
            if (w.Kind == "ineq") return Geo.DomainIneqHomogeneous(w.Ineq, bz.U, bz.R);
            var n = NOfWitness(w, bz.U);
            return Geo.GapPoly(n, bz.R, Geo.V[w.Vertex], Geo.V[w.Contact]); // plug vertex = 'vertex', hole (supporting) vertex = 'contact'
        });
        if (!p.DivisibleBy(leaf.Factor)) { why = "gap polynomial not divisible by zoom factor"; return false; }
        var N = p.DivideByMonomial(leaf.Factor);
        if (w.Kind != "ineq")
        {
            // validity conditions: n(u).(w' - v) <= 0 for all hole vertices w', at all 32 corners of the cell
            var nP = NOfWitness(w, bz.U);
            for (int mask = 0; mask < 32; mask++)
            {
                var yc = new Q5[5]; for (int i = 0; i < 5; i++) yc[i] = ((mask >> i) & 1) == 1 ? hi[i] : lo[i];
                var nv = nP.Select(q => q.Eval(yc)).ToArray();
                var hv = Geo.V[w.Contact];
                for (int k = 0; k < 60; k++)
                {
                    var s = Q5.Zero; for (int i = 0; i < 3; i++) s = s + nv[i] * (Geo.V[k][i] - hv[i]);
                    if (s.Sign() > 0) { why = "validity condition violated at a corner"; return false; }
                }
            }
        }
        if (!N.BernsteinAllStrict(lo, hi, +1)) { why = "Bernstein coefficient of quotient not strictly positive"; return false; }
        return true;
    }
}
