using System;
using System.Collections.Generic;
using System.Numerics;
using System.Text;
using System.Text.Json;

public sealed class Leaf {
    public string type, method, leafId, frontierId, boxLoText, boxHiText;
    public string[] lo = new string[0], hi = new string[0];
    public int disk, r3, r5, prec, depth, hullHint, leafCount = -1;
    public string claimedLower;
    public Int128[] eLo, eHi;           // exact decimal endpoints, scaled by 10^34
}

public static class Parse {
    public const int SCALE = 34;
    static readonly Int128[] P10 = MakeP10();
    static Int128[] MakeP10() { var a = new Int128[SCALE + 1]; a[0] = 1; for (int i = 1; i <= SCALE; i++) a[i] = a[i - 1] * 10; return a; }
    // Exact conversion of a decimal text (digits, '.', optional exponent) into integer scaled by 10^34. Throws if inexact/overflow.
    public static Int128 Scaled(string t) {
        int i = 0; bool neg = false;
        if (t[i] == '-') { neg = true; i++; } else if (t[i] == '+') i++;
        BigInteger mant = BigInteger.Zero; int frac = 0; bool dot = false; int exp = 0;
        for (; i < t.Length; i++) {
            char c = t[i];
            if (c >= '0' && c <= '9') { mant = mant * 10 + (c - '0'); if (dot) frac++; }
            else if (c == '.') dot = true;
            else if (c == 'e' || c == 'E') { exp = int.Parse(t.Substring(i + 1)); break; }
            else throw new FormatException("bad decimal " + t);
        }
        int e10 = SCALE - frac + exp;             // value = mant * 10^(exp-frac) ; scaled = mant*10^(SCALE+exp-frac)
        BigInteger v;
        if (e10 >= 0) v = mant * BigInteger.Pow(10, e10);
        else { var d = BigInteger.Pow(10, -e10); v = BigInteger.DivRem(mant, d, out var rem); if (!rem.IsZero) throw new Exception("inexact scaled " + t); }
        if (v > (BigInteger)Int128.MaxValue) throw new Exception("overflow " + t);
        Int128 r = (Int128)v; return neg ? -r : r;
    }

    public static Leaf Line(byte[] line) {
        var L = new Leaf();
        var rd = new Utf8JsonReader(line);
        string cur = null; int depthArr = 0; string which = null; bool inBox = false;
        var loL = new List<string>(); var hiL = new List<string>();
        while (rd.Read()) {
            if (rd.TokenType == JsonTokenType.PropertyName) {
                cur = rd.GetString();
                if (cur == "box" || cur == "root_box") inBox = true;
                else if (cur == "lo" || cur == "hi") { if (inBox) which = cur; }
                else if (cur == "run_meta") { rd.Read(); rd.Skip(); }
                continue;
            }
            if (rd.TokenType == JsonTokenType.StartArray) { depthArr++; continue; }
            if (rd.TokenType == JsonTokenType.EndArray) { depthArr--; if (depthArr == 0) which = null; continue; }
            if (rd.TokenType == JsonTokenType.EndObject) { if (inBox && which == null && depthArr == 0) inBox = false; continue; }
            if (rd.TokenType == JsonTokenType.Number && which != null && depthArr == 1) {
                var s = Encoding.UTF8.GetString(rd.ValueSpan);
                if (which == "lo") loL.Add(s); else hiL.Add(s);
                continue;
            }
            switch (cur) {
                case "record_type": if (rd.TokenType == JsonTokenType.String) L.type = rd.GetString(); break;
                case "method": if (rd.TokenType == JsonTokenType.String) L.method = rd.GetString(); break;
                case "leaf_id": if (rd.TokenType == JsonTokenType.String) L.leafId = rd.GetString(); break;
                case "frontier_id": if (rd.TokenType == JsonTokenType.String) L.frontierId = rd.GetString(); break;
                case "lower_bound": if (rd.TokenType == JsonTokenType.String) L.claimedLower = rd.GetString(); break;
                case "disk_samples": L.disk = rd.GetInt32(); break;
                case "r3_samples": L.r3 = rd.GetInt32(); break;
                case "r5_samples": L.r5 = rd.GetInt32(); break;
                case "reuleaux_samples": L.r3 = rd.GetInt32(); break;
                case "precision_bits": L.prec = rd.GetInt32(); break;
                case "depth": L.depth = rd.GetInt32(); break;
                case "leaf_count": L.leafCount = rd.GetInt32(); break;
                case "hull_vertices": L.hullHint = rd.GetInt32(); break;
            }
        }
        L.lo = loL.ToArray(); L.hi = hiL.ToArray();
        return L;
    }
}
