using System;
using System.Diagnostics;
using System.IO;
using System.Numerics;

public sealed class DirectConstraintWide
{
    int n, q, activeRoot, lastCompletedRoot, rootStart, rootEnd;
    int[] a, b, witnessA, witnessB;
    bool parity, found, timedOut;
    bool[,] parityPairs;
    UInt128 full, oddBits;
    long nodesA, nodesB, completeA, nextTick;
    double seconds, nextProgress;
    Stopwatch timer;
    StreamWriter progress;

    int Pop(UInt128 bits) { return BitOperations.PopCount((ulong)(bits & ulong.MaxValue))+BitOperations.PopCount((ulong)(bits >> 64)); }
    int Low(UInt128 bits) { ulong low=(ulong)(bits & ulong.MaxValue); return low!=0 ? BitOperations.TrailingZeroCount(low) : 64+BitOperations.TrailingZeroCount((ulong)(bits >> 64)); }
    UInt128 BackShift(UInt128 bits, int amount)
    {
        if (amount == 0) return bits;
        return ((bits >> amount) | (bits << (q-amount))) & full;
    }
    UInt128 Higher(int x) { return full & (UInt128.MaxValue << (x+1)); }

    bool Tick()
    {
        long total = nodesA + nodesB;
        if (total < nextTick) return found || timedOut;
        nextTick = total + 32768;
        if (timer.Elapsed.TotalSeconds >= seconds) timedOut = true;
        if (timer.Elapsed.TotalSeconds >= nextProgress || timedOut)
        {
            Log("progress");
            nextProgress = timer.Elapsed.TotalSeconds + 20;
        }
        return found || timedOut;
    }

    void Log(string kind)
    {
        Process p = Process.GetCurrentProcess();
        p.Refresh();
        string row = "{\"event\":\""+kind+"\",\"utc\":\""+DateTime.UtcNow.ToString("o")+
            "\",\"pid\":"+p.Id+",\"n\":"+n+",\"parity\":"+parity.ToString().ToLowerInvariant()+
            ",\"elapsed_seconds\":"+timer.Elapsed.TotalSeconds.ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+
            ",\"nodes_a\":"+nodesA+",\"nodes_b\":"+nodesB+",\"complete_a\":"+completeA+
            ",\"active_root\":"+activeRoot+",\"last_completed_root\":"+lastCompletedRoot+
            ",\"root_start\":"+rootStart+",\"root_end\":"+rootEnd+
            ",\"peak_working_set_bytes\":"+p.PeakWorkingSet64+
            ",\"found\":"+found.ToString().ToLowerInvariant()+",\"timed_out\":"+timedOut.ToString().ToLowerInvariant()+"}";
        progress.WriteLine(row); progress.Flush();
    }

    bool OddReachable(int depth, int odds, UInt128 candidates, int firstOdds)
    {
        if (!parity) return true;
        int remaining = n-depth;
        int canOdd = Pop(candidates & oddBits);
        int canEven = Pop(candidates & ~oddBits);
        int lo = odds + Math.Max(0,remaining-canEven);
        int hi = odds + Math.Min(remaining,canOdd);
        for (int final=lo; final<=hi; final++)
        {
            if (firstOdds >= 0) { if (parityPairs[firstOdds,final]) return true; }
            else for (int other=0; other<n; other++) if (parityPairs[final,other]) return true;
        }
        return false;
    }

    UInt128 Extend(int[] clique, int depth, UInt128 used, UInt128 candidates, int x, out UInt128 usedNew)
    {
        UInt128 added = 0;
        for (int i=0;i<depth;i++) added |= (UInt128)1 << ((x+clique[i])%q);
        // x was in a candidate set already checked against all old vertices and sums.
        usedNew = used | added;
        UInt128 next = candidates & Higher(x) & ~BackShift(usedNew,x);
        for (int i=0;i<depth;i++) next &= ~BackShift(added,clique[i]);
        return next & full;
    }

    void SearchA(int depth, UInt128 used, UInt128 candidates, int odds)
    {
        nodesA++;
        if (Tick()) return;
        if (depth==n)
        {
            completeA++;
            SearchB(1, used, full & ~used & ~(UInt128)1, 0, odds);
            return;
        }
        if (Pop(candidates)<n-depth || !OddReachable(depth,odds,candidates,-1)) return;
        while (candidates!=0)
        {
            int x=Low(candidates);
            candidates &= candidates-1;
            if (Pop(candidates)<n-depth-1) break;
            UInt128 usedNew;
            UInt128 next=Extend(a,depth,used,candidates,x,out usedNew);
            a[depth]=x;
            SearchA(depth+1,usedNew,next,odds+(x&1));
            if (found || timedOut) return;
        }
    }

    void SearchB(int depth, UInt128 used, UInt128 candidates, int odds, int firstOdds)
    {
        nodesB++;
        if (Tick()) return;
        if (depth==n)
        {
            if (used!=full) throw new Exception("Terminal edge sums did not fill group");
            found=true;
            witnessA=(int[])a.Clone(); witnessB=(int[])b.Clone();
            return;
        }
        if (Pop(candidates)<n-depth || !OddReachable(depth,odds,candidates,firstOdds)) return;
        while (candidates!=0)
        {
            int x=Low(candidates);
            candidates &= candidates-1;
            if (Pop(candidates)<n-depth-1) break;
            UInt128 usedNew;
            UInt128 next=Extend(b,depth,used,candidates,x,out usedNew);
            b[depth]=x;
            SearchB(depth+1,usedNew,next,odds+(x&1),firstOdds);
            if (found || timedOut) return;
        }
    }

    public static string Run(int order, bool useParity, double capSeconds, string progressPath, int firstRoot=1, int finalRoot=0)
    {
        var s=new DirectConstraintWide();
        s.n=order; s.q=order*(order-1);
        if (order<3 || s.q>127) throw new ArgumentOutOfRangeException("order");
        s.parity=useParity; s.seconds=capSeconds;
        s.a=new int[order]; s.b=new int[order];
        s.full=((UInt128)1<<s.q)-1;
        for(int x=1;x<s.q;x+=2) s.oddBits|=(UInt128)1<<x;
        s.parityPairs=new bool[order,order];
        for(int x=0;x<order;x++) for(int y=0;y<order;y++)
            s.parityPairs[x,y]=x*(order-x)+y*(order-y)==s.q/2;
        s.rootStart=firstRoot; s.rootEnd=finalRoot==0 ? s.q-order+1 : finalRoot;
        s.lastCompletedRoot=firstRoot-1;
        s.timer=Stopwatch.StartNew();
        s.progress=new StreamWriter(progressPath, true);
        s.nextProgress=20;
        s.Log("start");
        for(int x=s.rootStart;x<=s.rootEnd;x++)
        {
            s.activeRoot=x; s.a[1]=x;
            UInt128 used=(UInt128)1<<x;
            UInt128 candidates=s.Higher(x) & ~s.BackShift(used,x) & ~used;
            s.SearchA(2,used,candidates,x&1);
            if (s.found || s.timedOut) break;
            s.lastCompletedRoot=x;
            s.Log("completed_root");
            if(s.timer.Elapsed.TotalSeconds>=s.seconds){s.timedOut=true;break;}
        }
        s.Log("finish");
        s.progress.Dispose();
        bool complete=!s.timedOut && !s.found && s.lastCompletedRoot==s.rootEnd;
        return "{\"n\":"+order+",\"q\":"+s.q+",\"parity\":"+useParity.ToString().ToLowerInvariant()+
            ",\"found\":"+s.found.ToString().ToLowerInvariant()+",\"range_complete\":"+complete.ToString().ToLowerInvariant()+
            ",\"full_domain\":"+(s.rootStart==1&&s.rootEnd==s.q-s.n+1).ToString().ToLowerInvariant()+
            ",\"timed_out\":"+s.timedOut.ToString().ToLowerInvariant()+
            ",\"witness_a\":"+(s.witnessA==null ? "null" : "["+String.Join(",",s.witnessA)+"]")+
            ",\"witness_b\":"+(s.witnessB==null ? "null" : "["+String.Join(",",s.witnessB)+"]")+"}";
    }
}
