// Forward DRAT checker, written from the definition (RUP, then RAT on the first literal).
// Build (from any folder):
//   "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /optimize+ /out:dratcheck.exe DratCheck.cs
// Usage: dratcheck.exe formula.cnf proof [--binary|--text] [--timeout SECONDS] [--maxmb MB] [--ignore-unit-deletions] [--quiet]
// Exit code: 0 verified, 1 not verified, 2 usage/format error, 3 timeout or memory cap hit.
// C# 5 syntax only.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;

class ByteReader
{
    Stream s;
    byte[] buf = new byte[1 << 20];
    int pos, len;
    public ByteReader(Stream s) { this.s = s; }
    public int Read()
    {
        if (pos == len)
        {
            len = s.Read(buf, 0, buf.Length);
            pos = 0;
            if (len <= 0) { len = 0; return -1; }
        }
        return buf[pos++];
    }
}

static class DratCheck
{
    // clause pool layout at offset c: [c]=size, [c+1]=dead flag, [c+2]=hash chain next (-1 end), [c+3]=hash, [c+4..]=literals
    const int HDR = 4;
    // literal encoding: 2*var + (1 if negative). negation = lit ^ 1.
    static int[] pool = new int[1 << 20];
    static int poolLen = 0;
    static sbyte[] val = new sbyte[16];   // indexed by literal: 1 true, -1 false, 0 undefined
    static int[][] wl = new int[16][];    // watch lists indexed by literal
    static int[] wn = new int[16];
    static int[] reason = new int[8];     // indexed by var, clause offset or -1
    static int[] mark = new int[16];      // indexed by literal, stamp
    static int stamp = 0;
    static int[] trail = new int[8];
    static int trailLen = 0, qhead = 0, topLen = 0;
    static int maxVar = 0;
    static bool inconsistent = false;
    static int[] table = new int[1 << 16];
    static int tableMask = (1 << 16) - 1;
    static int liveCount = 0;
    static bool ignoreUnitDel = false;

    static long nClauses = 0, nAdd = 0, nDel = 0, nRat = 0, nResolvents = 0, nDelNotFound = 0, nDelRebuild = 0, nDelIgnored = 0, nTaut = 0;

    static int[] stepLits = new int[64];
    static int stepN = 0;
    static bool stepDel = false;
    static int[] cl = new int[64];
    static int[] tmp = new int[64];

    static void EnsureVar(int v)
    {
        if (v <= maxVar) return;
        int nv = Math.Max(v, maxVar * 2);
        if (nv < 16) nv = 16;
        Array.Resize(ref val, 2 * nv + 2);
        Array.Resize(ref wl, 2 * nv + 2);
        Array.Resize(ref wn, 2 * nv + 2);
        Array.Resize(ref mark, 2 * nv + 2);
        Array.Resize(ref reason, nv + 1);
        Array.Resize(ref trail, nv + 2);
        maxVar = nv;
    }

    static void AddWatch(int lit, int c)
    {
        int[] a = wl[lit];
        int n = wn[lit];
        if (a == null) { a = new int[4]; wl[lit] = a; }
        else if (n == a.Length) { Array.Resize(ref a, n * 2); wl[lit] = a; }
        a[n] = c;
        wn[lit] = n + 1;
    }

    static void Assign(int lit, int r)
    {
        val[lit] = 1;
        val[lit ^ 1] = -1;
        trail[trailLen++] = lit;
        reason[lit >> 1] = r;
    }

    static void Backtrack(int to)
    {
        while (trailLen > to)
        {
            int l = trail[--trailLen];
            val[l] = 0;
            val[l ^ 1] = 0;
        }
        qhead = to;
    }

    // returns false on conflict
    static bool Propagate()
    {
        while (qhead < trailLen)
        {
            int p = trail[qhead++];
            int f = p ^ 1;
            int[] ws = wl[f];
            if (ws == null) continue;
            int n = wn[f];
            int i = 0, j = 0;
            while (i < n)
            {
                int c = ws[i++];
                if (pool[c + 1] != 0) continue; // dead clause: drop from list
                int b = c + HDR;
                int size = pool[c];
                if (pool[b] == f) { pool[b] = pool[b + 1]; pool[b + 1] = f; }
                int first = pool[b];
                if (val[first] > 0) { ws[j++] = c; continue; }
                bool found = false;
                for (int k = 2; k < size; k++)
                {
                    int l = pool[b + k];
                    if (val[l] >= 0)
                    {
                        pool[b + 1] = l;
                        pool[b + k] = f;
                        AddWatch(l, c);
                        found = true;
                        break;
                    }
                }
                if (found) continue;
                ws[j++] = c;
                if (val[first] < 0)
                {
                    while (i < n) ws[j++] = ws[i++];
                    wn[f] = j;
                    return false;
                }
                Assign(first, c);
            }
            wn[f] = j;
        }
        return true;
    }

    // RUP check of the clause given by lits[0..n): assign negations, propagate, expect conflict. State restored.
    static bool RupCheck(int[] lits, int n)
    {
        bool conflict = false;
        for (int i = 0; i < n; i++)
        {
            int l = lits[i];
            int v = val[l];
            if (v > 0) { conflict = true; break; }
            if (v < 0) continue;
            Assign(l ^ 1, -1);
        }
        if (!conflict) conflict = !Propagate();
        Backtrack(topLen);
        return conflict;
    }

    static bool RatCheck(int[] c0, int n)
    {
        if (n == 0) return false;
        int np = c0[0] ^ 1;
        for (int c = 0; c < poolLen; c += HDR + pool[c])
        {
            if (pool[c + 1] != 0) continue;
            int s = pool[c];
            bool has = false;
            for (int k = 0; k < s; k++) if (pool[c + HDR + k] == np) { has = true; break; }
            if (!has) continue;
            if (tmp.Length < n + s + 2) tmp = new int[(n + s + 2) * 2];
            int m = 0;
            for (int i = 1; i < n; i++) tmp[m++] = c0[i];
            for (int k = 0; k < s; k++) { int l = pool[c + HDR + k]; if (l != np) tmp[m++] = l; }
            nResolvents++;
            if (!RupCheck(tmp, m)) return false;
        }
        return true;
    }

    static uint HashLit(int l)
    {
        uint m = (uint)l * 2654435761u;
        m ^= m >> 15;
        m *= 2246822519u;
        m ^= m >> 13;
        return m;
    }

    static int HashClause(int[] lits, int n)
    {
        uint s = 0, x = 0;
        for (int i = 0; i < n; i++) { uint m = HashLit(lits[i]); s += m; x ^= m * 3266489917u; }
        return (int)(s * 31u + x);
    }

    static void Rehash()
    {
        int ns = table.Length * 2;
        table = new int[ns];
        tableMask = ns - 1;
        for (int i = 0; i < ns; i++) table[i] = -1;
        for (int c = 0; c < poolLen; c += HDR + pool[c])
        {
            if (pool[c + 1] != 0) continue;
            int h = pool[c + 3] & tableMask;
            pool[c + 2] = table[h];
            table[h] = c;
        }
    }

    static void TopPropagate()
    {
        if (!Propagate()) inconsistent = true;
        else topLen = trailLen;
    }

    // lits are distinct, not tautological. Attach as an alive clause, update top-level state.
    static void AddClause(int[] lits, int n)
    {
        for (int i = 0; i < n; i++) EnsureVar(lits[i] >> 1);
        if (n == 0) { inconsistent = true; return; }
        if (liveCount + 1 > table.Length) Rehash();
        if (poolLen + HDR + n + 1 >= pool.Length)
        {
            int nl = pool.Length * 2;
            while (poolLen + HDR + n + 1 >= nl) nl *= 2;
            Array.Resize(ref pool, nl);
        }
        int off = poolLen;
        poolLen += HDR + n;
        pool[off] = n;
        pool[off + 1] = 0;
        int h = HashClause(lits, n);
        pool[off + 3] = h;
        int w = off + HDR;
        for (int pass = 1; pass >= -1; pass--)
            for (int i = 0; i < n; i++)
                if (val[lits[i]] == pass) pool[w++] = lits[i];
        liveCount++;
        int hi = h & tableMask;
        pool[off + 2] = table[hi];
        table[hi] = off;
        // note: table is filled with -1 at start (see Main)
        if (n == 1)
        {
            int l = pool[off + HDR];
            if (val[l] < 0) { inconsistent = true; return; }
            if (val[l] == 0) { Assign(l, off); TopPropagate(); }
            return;
        }
        int l0 = pool[off + HDR], l1 = pool[off + HDR + 1];
        AddWatch(l0, off);
        AddWatch(l1, off);
        if (val[l0] < 0) { inconsistent = true; return; }
        if (val[l0] == 0 && val[l1] < 0) { Assign(l0, off); TopPropagate(); }
    }

    static void RebuildTopLevel()
    {
        Backtrack(0);
        for (int c = 0; c < poolLen && !inconsistent; c += HDR + pool[c])
        {
            if (pool[c + 1] != 0 || pool[c] != 1) continue;
            int l = pool[c + HDR];
            if (val[l] < 0) { inconsistent = true; break; }
            if (val[l] == 0) Assign(l, c);
        }
        if (!inconsistent) { if (!Propagate()) inconsistent = true; }
        if (!inconsistent) topLen = trailLen;
    }

    static void DeleteClause(int[] lits, int n)
    {
        for (int i = 0; i < n; i++) EnsureVar(lits[i] >> 1);
        stamp++;
        for (int i = 0; i < n; i++) mark[lits[i]] = stamp;
        int h = HashClause(lits, n);
        int hi = h & tableMask;
        int prev = -1;
        int c = table[hi];
        while (c != -1)
        {
            if (pool[c + 3] == h && pool[c] == n)
            {
                bool eq = true;
                for (int k = 0; k < n; k++) if (mark[pool[c + HDR + k]] != stamp) { eq = false; break; }
                if (eq) break;
            }
            prev = c;
            c = pool[c + 2];
        }
        if (c == -1) { nDelNotFound++; return; }
        // is it the reason of a top-level assignment?
        int l0 = pool[c + HDR];
        bool isReason = val[l0] > 0 && reason[l0 >> 1] == c;
        if (isReason && ignoreUnitDel) { nDelIgnored++; return; }
        if (prev == -1) table[hi] = pool[c + 2]; else pool[prev + 2] = pool[c + 2];
        pool[c + 1] = 1;
        liveCount--;
        if (isReason) { nDelRebuild++; RebuildTopLevel(); }
    }

    // ---------------- input ----------------
    static void AppendStep(int lit)
    {
        if (stepN == stepLits.Length) Array.Resize(ref stepLits, stepN * 2);
        stepLits[stepN++] = lit;
    }

    // returns 1 step read, 0 eof, -1 bad format, -2 truncated
    static int ReadStepBin(ByteReader r)
    {
        int b = r.Read();
        if (b < 0) return 0;
        if (b == 0x61) stepDel = false;
        else if (b == 0x64) stepDel = true;
        else return -1;
        stepN = 0;
        while (true)
        {
            long v = 0;
            int shift = 0;
            while (true)
            {
                int x = r.Read();
                if (x < 0) return -2;
                v |= (long)(x & 0x7f) << shift;
                shift += 7;
                if ((x & 0x80) == 0) break;
                if (shift > 35) return -1;
            }
            if (v == 0) break;
            if (v < 2 || v > int.MaxValue) return -1;
            AppendStep((int)v);
        }
        return 1;
    }

    static int ReadStepText(ByteReader r)
    {
        stepDel = false;
        stepN = 0;
        bool any = false;
        while (true)
        {
            int ch = r.Read();
            while (ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n') ch = r.Read();
            if (ch < 0) return any ? -2 : 0;
            if (ch == 'c')
            {
                while (ch >= 0 && ch != '\n') ch = r.Read();
                continue;
            }
            if (ch == 'd') { stepDel = true; any = true; continue; }
            bool neg = false;
            if (ch == '-') { neg = true; ch = r.Read(); }
            if (ch < '0' || ch > '9') return -1;
            long v = 0;
            while (ch >= '0' && ch <= '9') { v = v * 10 + (ch - '0'); if (v > int.MaxValue / 2) return -1; ch = r.Read(); }
            any = true;
            if (v == 0) return 1;
            AppendStep((int)(neg ? 2 * v + 1 : 2 * v));
        }
    }

    static bool LoadCnf(string path)
    {
        ByteReader r = new ByteReader(new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read, 1 << 16));
        int[] lits = new int[64];
        int n = 0;
        while (true)
        {
            int ch = r.Read();
            while (ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n') ch = r.Read();
            if (ch < 0) break;
            if (ch == 'c' || ch == 'p')
            {
                while (ch >= 0 && ch != '\n') ch = r.Read();
                continue;
            }
            if (ch == '%') break;
            bool neg = false;
            if (ch == '-') { neg = true; ch = r.Read(); }
            if (ch < '0' || ch > '9') { Console.WriteLine("c bad CNF character " + ch); return false; }
            long v = 0;
            while (ch >= '0' && ch <= '9') { v = v * 10 + (ch - '0'); ch = r.Read(); }
            if (v == 0)
            {
                nClauses++;
                if (!inconsistent) AddNormalized(lits, n);
                n = 0;
            }
            else
            {
                if (n == lits.Length) Array.Resize(ref lits, n * 2);
                lits[n++] = (int)(neg ? 2 * v + 1 : 2 * v);
            }
        }
        return true;
    }

    // dedupe and drop tautologies, then AddClause. Returns false if tautology (not added).
    static bool AddNormalized(int[] lits, int n)
    {
        for (int i = 0; i < n; i++) EnsureVar(lits[i] >> 1);
        if (cl.Length < n + 1) cl = new int[(n + 1) * 2];
        stamp++;
        int m = 0;
        for (int i = 0; i < n; i++)
        {
            int l = lits[i];
            if (mark[l] == stamp) continue;
            if (mark[l ^ 1] == stamp) { nTaut++; return false; }
            mark[l] = stamp;
            cl[m++] = l;
        }
        AddClause(cl, m);
        return true;
    }

    static string Fmt(int[] lits, int n)
    {
        System.Text.StringBuilder sb = new System.Text.StringBuilder();
        for (int i = 0; i < n && i < 30; i++)
        {
            int l = lits[i];
            sb.Append((l & 1) != 0 ? "-" : "").Append(l >> 1).Append(' ');
        }
        if (n > 30) sb.Append("...");
        sb.Append('0');
        return sb.ToString();
    }

    static double CpuSeconds()
    {
        return Process.GetCurrentProcess().TotalProcessorTime.TotalSeconds;
    }

    static int Finish(string verdict, int code, Stopwatch sw, bool quiet)
    {
        Process p = Process.GetCurrentProcess();
        Console.WriteLine("c clauses " + nClauses + " additions " + nAdd + " deletions " + nDel + " rat_checks " + nRat
            + " rat_resolvents " + nResolvents + " del_not_found " + nDelNotFound + " del_top_reason_rebuilds " + nDelRebuild
            + " del_ignored " + nDelIgnored + " tautologies " + nTaut);
        Console.WriteLine("c time_wall " + sw.Elapsed.TotalSeconds.ToString("F2") + " cpu " + CpuSeconds().ToString("F2")
            + " peak_ws_mb " + (p.PeakWorkingSet64 / (1024 * 1024)) + " peak_private_mb " + (p.PeakPagedMemorySize64 / (1024 * 1024)));
        Console.WriteLine(verdict);
        return code;
    }

    static int Main(string[] args)
    {
        string cnf = null, proof = null;
        int forced = 0; // 1 binary, 2 text
        double timeout = 1e9;
        double maxmb = 1e9;
        bool quiet = false;
        for (int i = 0; i < args.Length; i++)
        {
            string a = args[i];
            if (a == "--binary") forced = 1;
            else if (a == "--text") forced = 2;
            else if (a == "--timeout") timeout = double.Parse(args[++i]);
            else if (a == "--maxmb") maxmb = double.Parse(args[++i]);
            else if (a == "--ignore-unit-deletions") ignoreUnitDel = true;
            else if (a == "--quiet") quiet = true;
            else if (cnf == null) cnf = a;
            else if (proof == null) proof = a;
        }
        if (cnf == null || proof == null) { Console.WriteLine("usage: dratcheck formula.cnf proof [--binary|--text] [--timeout S] [--maxmb MB] [--ignore-unit-deletions]"); return 2; }
        Stopwatch sw = Stopwatch.StartNew();
        for (int i = 0; i < table.Length; i++) table[i] = -1;
        EnsureVar(16);
        if (!LoadCnf(cnf)) return 2;
        Console.WriteLine("c formula loaded: " + nClauses + " clauses, vars " + maxVar + ", top-level conflict " + inconsistent);
        if (inconsistent)
        {
            Console.WriteLine("c unit propagation on the formula alone yields a top-level conflict");
            return Finish("s VERIFIED", 0, sw, quiet);
        }
        bool binary;
        if (forced == 1) binary = true;
        else if (forced == 2) binary = false;
        else
        {
            byte[] head = new byte[32];
            int hn;
            using (FileStream fs = new FileStream(proof, FileMode.Open, FileAccess.Read, FileShare.Read)) { hn = fs.Read(head, 0, 32); }
            binary = false;
            for (int i = 0; i < hn; i++)
            {
                byte b = head[i];
                bool textc = (b >= '0' && b <= '9') || b == ' ' || b == '-' || b == 'd' || b == '\n' || b == '\r' || b == '\t';
                if (!textc) { binary = true; break; }
            }
        }
        Console.WriteLine("c proof format " + (binary ? "binary" : "text"));
        ByteReader pr = new ByteReader(new FileStream(proof, FileMode.Open, FileAccess.Read, FileShare.Read, 1 << 16));
        long step = 0;
        while (true)
        {
            int rc = binary ? ReadStepBin(pr) : ReadStepText(pr);
            if (rc == 0) break;
            if (rc == -1) { Console.WriteLine("c bad proof format at step " + (step + 1)); return Finish("s NOT VERIFIED", 1, sw, quiet); }
            if (rc == -2) { Console.WriteLine("c truncated proof at step " + (step + 1)); break; }
            step++;
            if ((step & 1023) == 0)
            {
                if (CpuSeconds() > timeout) { Console.WriteLine("c TIMEOUT after " + step + " steps (cpu limit " + timeout + " s)"); return Finish("s TIMEOUT", 3, sw, quiet); }
                if (GC.GetTotalMemory(false) / (1024.0 * 1024.0) > maxmb) { Console.WriteLine("c MEMORY CAP after " + step + " steps"); return Finish("s MEMLIMIT", 3, sw, quiet); }
            }
            for (int i = 0; i < stepN; i++) EnsureVar(stepLits[i] >> 1);
            if (stepDel)
            {
                nDel++;
                // dedupe so that set comparison is exact
                stamp++;
                int m = 0;
                if (cl.Length < stepN + 1) cl = new int[(stepN + 1) * 2];
                for (int i = 0; i < stepN; i++) { int l = stepLits[i]; if (mark[l] == stamp) continue; mark[l] = stamp; cl[m++] = l; }
                if (m == 0) { nDelNotFound++; continue; }
                DeleteClause(cl, m);
                if (inconsistent)
                {
                    Console.WriteLine("c top-level conflict after deletion rebuild at step " + step);
                    return Finish("s VERIFIED", 0, sw, quiet);
                }
                continue;
            }
            nAdd++;
            // dedupe keeping order; first literal is the RAT pivot
            if (cl.Length < stepN + 1) cl = new int[(stepN + 1) * 2];
            stamp++;
            int n = 0;
            bool taut = false;
            for (int i = 0; i < stepN; i++)
            {
                int l = stepLits[i];
                if (mark[l] == stamp) continue;
                if (mark[l ^ 1] == stamp) { taut = true; break; }
                mark[l] = stamp;
                cl[n++] = l;
            }
            if (taut) { nTaut++; continue; }
            bool ok = RupCheck(cl, n);
            if (!ok)
            {
                nRat++;
                ok = RatCheck(cl, n);
            }
            if (!ok)
            {
                Console.WriteLine("c REJECT: addition #" + nAdd + " (proof step " + step + ") is neither RUP nor RAT on its first literal: " + Fmt(cl, n));
                return Finish("s NOT VERIFIED", 1, sw, quiet);
            }
            if (n == 0)
            {
                Console.WriteLine("c empty clause added and checked at proof step " + step);
                return Finish("s VERIFIED", 0, sw, quiet);
            }
            AddClause(cl, n);
            if (inconsistent)
            {
                Console.WriteLine("c top-level unit propagation conflict reached after proof step " + step);
                return Finish("s VERIFIED", 0, sw, quiet);
            }
        }
        Console.WriteLine("c end of proof reached without empty clause and without top-level conflict");
        return Finish("s NOT VERIFIED", 1, sw, quiet);
    }
}
