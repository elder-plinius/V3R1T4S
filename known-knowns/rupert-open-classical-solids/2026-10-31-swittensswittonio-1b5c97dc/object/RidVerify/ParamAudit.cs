namespace RidVerify;

/// <summary>Audit of the stored cover parameters against the paper's text (appendix B tables, sections 8-10).</summary>
public static class ParamAudit
{
    static Q5 R(long n, long d) => Q5.Rat(n, d);
    static bool Iv(Q5[] iv, Q5 a, Q5 b) => iv[0] == a && iv[1] == b;
    static bool Phi(Q5[][] box, params (long, long)[] ab) { if (box.Length != ab.Length) return false; for (int i = 0; i < ab.Length; i++) if (box[i][0] != Q5.Int(ab[i].Item1) || box[i][1] != Q5.Int(ab[i].Item2)) return false; return true; }
    static bool IdMap(Cover c, Q5[] diag) { for (int i = 0; i < 5; i++) for (int j = 0; j < 5; j++) if (c.Map[i, j] != (i == j ? diag[i] : Q5.Zero)) return false; return true; }
    public static List<string> Run(string coversDir, string texPath, out int checks)
    {
        var bad = new List<string>(); int cnt = 0;
        void Chk(bool ok, string what) { cnt++; if (!ok) bad.Add(what); }
        RecordCover.LoadLocalTable(texPath);
        var one = Q5.One; var eps = R(1, 1024);
        for (int k = 0; k < 30; k++)
        {
            var c = Cover.Load(Path.Combine(coversDir, "local", k + ".json")); var row = RecordCover.LocalRows[k];
            Chk(!c.Arc && c.IsTube && c.Scope == "all" && c.Name == k.ToString(), $"local {k}: header");
            Chk(IdMap(c, new[] { one, one, one, one, one }) && c.Centre.All(x => x.IsZero), $"local {k}: identity map/centre");
            Chk(Phi(c.PhiBox, (-1, 1), (-1, 1), (-1, 1)), $"local {k}: Phi = [-1,1]^3");
            var s0 = Q5.Max(Q5.Zero, row.S0 - eps); var s1 = Q5.Min(R(2, 3), row.S1 + eps); var t0 = Q5.Max(Q5.Zero, row.T0 - eps); var t1 = Q5.Min(R(2, 5), row.T1 + eps);
            Chk(Iv(c.TubeBase[0], s0, s1) && Iv(c.TubeBase[1], t0, t1), $"local {k}: viewing rectangle = table row enlarged by 1/1024 and cut to W0");
            Chk(c.TubeRadius == row.Delta, $"local {k}: delta_max = table");
            Chk(c.Zooms.Count == 6 && c.Witnesses.All(w => w.Kind != "ineq"), $"local {k}: six face zooms, gap-polynomial witnesses only (direction or moving-edge form)");
        }
        var sq = Cover.Load(Path.Combine(coversDir, "exotic", "square.json"));
        Chk(sq.Scope == "domain" && !sq.IsTube && IdMap(sq, new[] { one, one, one, one, one }) && sq.Centre.All(x => x.IsZero) && Phi(sq.SigmaBox, (0, 1), (0, 1)) && Phi(sq.PhiBox, (-1, 1), (-1, 1), (-1, 1)) && sq.Radii.Length == 2 && sq.Radii.All(x => x == R(1, 8)) && sq.Radius == R(1, 8) && sq.Ratio == one && !sq.HasWindow && !sq.HasBeyond, "square parameters");
        Chk(sq.Zooms.Count == 18, "square: 18 zooms");
        var pe = Cover.Load(Path.Combine(coversDir, "exotic", "pentagon.json"));
        {
            var s5 = Q5.Sqrt5; var phi = Geo.Phi; var phib = Geo.PhiBar;
            // centre (s0,t0,0,0,0); map rows: s = s0 + (phi*eta - phibar*xi)/sqrt5 ; t = t0 + (xi - eta)/sqrt5
            var ok = pe.Centre[0] == new Q5(-5, 3, 10) && pe.Centre[1] == new Q5(5, -1, 10) && pe.Centre.Skip(2).All(x => x.IsZero);
            ok &= pe.Map[0, 0] == phi / s5 && pe.Map[0, 1] == -phib / s5 && pe.Map[1, 0] == -(one / s5) && pe.Map[1, 1] == one / s5;
            for (int i = 0; i < 5; i++) for (int j = 0; j < 5; j++) if (i >= 2 || j >= 2) ok &= pe.Map[i, j] == (i == j ? one : Q5.Zero);
            Chk(ok, "pentagon: centre and map equal the paper's inverse change of coordinates (eta,xi)->(s,t)");
            Chk(pe.Scope == "domain" && !pe.IsTube && Phi(pe.SigmaBox, (-1, 1), (-1, 0)) && Phi(pe.PhiBox, (-1, 1), (-1, 1), (-1, 1)) && pe.Radii.Length == 3 && pe.Radii.All(x => x == R(1, 32)) && pe.Radius == R(1, 16) && pe.Ratio == R(2, 1) && !pe.HasWindow, "pentagon: Sigma=[-1,1]x[-1,0], mu_max=1/32, delta_max=1/16, rho0=2");
            Chk(pe.HasBeyond && pe.BeyondAxis == 1 && pe.BeyondIneq == 0, "pentagon: beyond xi>0 is eliminated by inequality 0 (viewing triangle)");
            Chk(pe.Zooms.Count == 24, "pentagon: 24 zooms");
        }
        foreach (var sgn in new[] { "+", "-" })
        {
            int sigma = sgn == "+" ? 1 : -1;
            var d = new[] { one, Q5.Int(2), one, one, one };
            var a = Cover.Load(Path.Combine(coversDir, "exotic", $"arc{sgn}.json"));
            Chk(a.Arc && a.Sigma == sigma && a.IsTube && IdMap(a, d) && a.Centre.All(x => x.IsZero) && Iv(a.TubeBase[0], R(3, 64), R(3, 16)) && a.PhiBox.Length == 4 && a.PhiBox[0][0] == Q5.Zero && a.PhiBox[0][1] == one && a.TubeRadius == R(1, 32) && a.Zooms.Count == 7, $"arc{sgn}: parameters");
            var ep = Cover.Load(Path.Combine(coversDir, "exotic", $"endpoint{sgn}.json"));
            Chk(ep.Arc && ep.Sigma == sigma && !ep.IsTube && IdMap(ep, d) && ep.Centre[0] == new Q5(-2, 1, 1) && ep.Centre.Skip(1).All(x => x.IsZero) && Phi(ep.SigmaBox, (-1, 1)) && ep.Radii.Length == 2 && ep.Radii[0] == R(1, 16) && ep.Radii[1] == R(1, 32) && ep.Radius == R(1, 32) && ep.Ratio == one && !ep.HasWindow && ep.Zooms.Count == 21, $"endpoint{sgn}: parameters (e*=sqrt5-2, radii 1/16 and 1/32, delta 1/32, rho0=1)");
            var cr = Cover.Load(Path.Combine(coversDir, "exotic", $"crossing{sgn}.json"));
            Chk(cr.Arc && cr.Sigma == sigma && !cr.IsTube && IdMap(cr, new[] { one, R(5, 4), one, one, one }) && cr.Centre.All(x => x.IsZero) && Phi(cr.SigmaBox, (-1, 1)) && cr.Radii.All(x => x == R(1, 16)) && cr.Radius == R(1, 16) && cr.Ratio == R(5, 4) && cr.HasWindow && cr.WinAxis == 0 && cr.WinSide == 1 && cr.WinRadius == R(1, 4) && cr.Shear[1, 0] == one && cr.Shear[0, 0].IsZero && cr.Shear[2, 0].IsZero && cr.Shear[3, 0].IsZero && cr.Zooms.Count == 28, $"crossing{sgn}: parameters (4v/5 weight, rho0=5/4, rho0'=1/4, shear theta'=theta+e)");
        }
        checks = cnt; return bad;
    }
}
