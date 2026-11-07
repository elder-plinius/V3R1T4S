using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.Text.Json;

public static class ComplementSearch
{
    private sealed class Search
    {
        public int N,Q,FirstMin,FirstMax,ActiveFirst,LastCompleted;
        public double CapSeconds,MemoryCapMiB;
        public string OutputPrefix;
        public UInt128 FullMask;
        public int[] Labels;
        public long Nodes,Candidates,Leaves,DuplicateMasks;
        public Dictionary<UInt128,UInt128> Representatives = new Dictionary<UInt128,UInt128>();
        public Stopwatch Timer = Stopwatch.StartNew();
        public double LastProgress;
        public string StopReason;
        public UInt128 FoundA,FoundB;
        public List<int> Completed = new List<int>();

        public void Emit(string kind)
        {
            Process p=Process.GetCurrentProcess(); p.Refresh();
            var record=new {
                kind=kind,utc=DateTime.UtcNow.ToString("O"),pid=p.Id,n=N,q=Q,
                elapsed_seconds=Timer.Elapsed.TotalSeconds,nodes=Nodes,candidates=Candidates,
                leaves=Leaves,distinct_masks=Representatives.Count,duplicate_masks=DuplicateMasks,
                first_min=FirstMin,first_max=FirstMax,active_first=ActiveFirst,
                completed_firsts=Completed.ToArray(),stop_reason=StopReason,
                managed_bytes=GC.GetTotalMemory(false),working_set_bytes=p.WorkingSet64,
                peak_working_set_bytes=p.PeakWorkingSet64,
                solution_a=Decode(FoundA,Q),solution_b=Decode(FoundB,Q)
            };
            string json=JsonSerializer.Serialize(record);
            Console.WriteLine(json);
            File.AppendAllText(OutputPrefix+".progress.jsonl",json+Environment.NewLine);
            File.WriteAllText(OutputPrefix+".checkpoint.json",json+Environment.NewLine);
        }
        public bool CheckLimits()
        {
            double elapsed=Timer.Elapsed.TotalSeconds;
            if (elapsed>=CapSeconds) StopReason="time_cap";
            if (GC.GetTotalMemory(false)>MemoryCapMiB*1048576.0) StopReason="memory_cap";
            if (elapsed-LastProgress>=15.0) { Emit("progress"); LastProgress=elapsed; }
            return StopReason!=null;
        }
        public void DFS(int depth,int start,UInt128 sumMask,UInt128 labelMask)
        {
            Nodes++;
            if ((Nodes&65535)==0 && CheckLimits()) return;
            if (depth==N)
            {
                Leaves++;
                UInt128 partner;
                if(Representatives.TryGetValue(FullMask^sumMask,out partner))
                {
                    FoundA=partner;FoundB=labelMask;StopReason="found";return;
                }
                if(!Representatives.ContainsKey(sumMask)) Representatives.Add(sumMask,labelMask);
                else DuplicateMasks++;
                return;
            }
            int max=Q-(N-depth);
            for(int x=start;x<=max;x++)
            {
                Candidates++;
                UInt128 add=0;
                bool valid=true;
                for(int j=0;j<depth;j++)
                {
                    int s=x+Labels[j]; if(s>=Q) s-=Q;
                    UInt128 bit=((UInt128)1)<<s;
                    if(((sumMask|add)&bit)!=0) {valid=false;break;}
                    add|=bit;
                }
                if(!valid) continue;
                Labels[depth]=x;
                DFS(depth+1,x+1,sumMask|add,labelMask|(((UInt128)1)<<x));
                if(StopReason!=null) return;
            }
        }
        public void Execute()
        {
            Emit("start");
            for(int first=FirstMin;first<=FirstMax;first++)
            {
                ActiveFirst=first;Labels[1]=first;
                DFS(2,first+1,((UInt128)1)<<first,((UInt128)1)|(((UInt128)1)<<first));
                if(StopReason!=null) break;
                Completed.Add(first); LastCompleted=first;
                Emit("prefix_complete");
            }
            if(StopReason==null) StopReason=(FirstMin==1 && FirstMax==Q-N+1)?"exhaustive_no_pair":"restricted_complete_no_pair";
            Emit("finish");
        }
    }
    private static int[] Decode(UInt128 mask,int q)
    {
        var result=new List<int>(); for(int i=0;i<q;i++) if((mask&(((UInt128)1)<<i))!=0) result.Add(i);
        return result.ToArray();
    }
    public static void Run(int n,double capSeconds,double memoryCapMiB,int firstMin,int firstMax,string outputPrefix)
    {
        int q=n*(n-1);
        if(n<3 || q>127) throw new ArgumentException("Requires n>=3 and q<=127");
        UInt128 bitTest=0;
        for(int i=0;i<q;i++)
        {
            UInt128 bit=((UInt128)1)<<i;
            if(bit==0 || (bitTest&bit)!=0) throw new InvalidOperationException("Bit position collision");
            bitTest|=bit;
        }
        if(bitTest!=((((UInt128)1)<<q)-1)) throw new InvalidOperationException("Full mask mismatch");
        if(firstMax<=0) firstMax=q-n+1;
        Process.GetCurrentProcess().PriorityClass=ProcessPriorityClass.BelowNormal;
        var search=new Search {N=n,Q=q,Labels=new int[n],FullMask=(((UInt128)1)<<q)-1,
            CapSeconds=capSeconds,MemoryCapMiB=memoryCapMiB,FirstMin=firstMin,FirstMax=firstMax,
            OutputPrefix=outputPrefix};
        search.Execute();
    }
}
