#!/bin/sh
# Chunked, resumable exhaustive run.
# usage: scripts/run_chunks.sh OUTDIR [W H CHUNK_LOG2 ENGINE THREADS MAX_MINUTES]
#   defaults: 6 6 24 lant4 <ncores> unlimited.  ENGINE = lant4 | lant_cuda (| lant_cuda_emu for tests)
# Chunk c covers masks [c*2^L, (c+1)*2^L). For each chunk: run the engine, replace WINDOW_OVERFLOW lines by the reference output,
# and write OUTDIR/chunk_<c>.sum (+ chunk_<c>.noncap = every line whose status is not CAP, + chunk_<c>.full.gz only if KEEP_FULL=1).
# A chunk is "done" only when chunk_<c>.sum exists (written atomically last), so you can kill the script at any time and re-run
# the same command: finished chunks are skipped, the interrupted chunk is redone. Create OUTDIR/STOP to stop after the current chunk.
# Env C0=first chunk, C1=one past last chunk restrict the range (e.g. CPU takes 0..2000, GPU takes C0=2000 C1=4096 with its own OUTDIR).
# Chunk summary line: chunk c first last lines CAP UNCAP OOB maxtcap maxtcap_mask distinct_(vx,vy,dir) sha256_of_full_output engine
D="$(cd "$(dirname "$0")/.." && pwd)"; O=${1:?outdir}; W=${2:-6}; H=${3:-6}; L=${4:-24}; E=${5:-lant4}
T=${6:-$(nproc 2>/dev/null || echo 4)}; MAXM=${7:-0}; CAP=2000000
mkdir -p "$O"; N=$((W*H)); NCH=$(( (1<<N) >> L )); [ $NCH -lt 1 ] && NCH=1
start=$(date +%s); done_now=0
echo "W=$W H=$H CAP=$CAP chunk=2^$L masks, $NCH chunks, engine=$E threads=$T" > "$O/CONFIG.txt"
c=${C0:-0}; [ -n "$C1" ] && [ $C1 -lt $NCH ] && NCH_END=$C1 || NCH_END=$NCH
while [ $c -lt $NCH_END ]; do
  [ -e "$O/STOP" ] && { echo "STOP file seen"; break; }
  if [ $MAXM -gt 0 ] && [ $(( ($(date +%s)-start)/60 )) -ge $MAXM ]; then echo "time budget reached"; break; fi
  if [ ! -e "$O/chunk_$c.sum" ]; then
    S=$(( c << L )); EE=$(( S + (1<<L) )); [ $EE -gt $((1<<N)) ] && EE=$((1<<N))
    "$D/$E" $W $H $S $EE $CAP $T > "$O/chunk_$c.raw" || { echo "engine failed on chunk $c"; exit 1; }
    "$D/scripts/fixup.sh" $W $H $CAP < "$O/chunk_$c.raw" > "$O/chunk_$c.full" || exit 1
    nov=$(grep -c WINDOW_OVERFLOW "$O/chunk_$c.raw"); rm -f "$O/chunk_$c.raw"
    awk '$7!="CAP"' "$O/chunk_$c.full" > "$O/chunk_$c.noncap"
    sha=$(sha256sum "$O/chunk_$c.full" | cut -d' ' -f1)
    awk -v c=$c -v e=$E -v sha=$sha -v nov=$nov 'BEGIN{mt=-1}
      NR==1{f=$1} {l=$1; if($7=="CAP")cap++; else if($7=="UNCAPTURED_WITHIN_CAP")unc++; else oob++; if($2+0>mt){mt=$2+0;mm=$1} k=$3","$4","$5; if(!(k in s)){s[k]=1;nk++} }
      END{printf "chunk %d first %s last %s lines %d CAP %d UNCAP %d OOB %d maxtcap %d maxtcap_mask %s distinct_classes %d overflow_fixups %d sha256 %s engine %s\n",c,f,l,NR,cap,unc,oob,mt,mm,nk,nov,sha,e}' "$O/chunk_$c.full" > "$O/chunk_$c.sum.tmp"
    if [ "${KEEP_FULL:-0}" = 1 ]; then gzip -f "$O/chunk_$c.full"; else rm -f "$O/chunk_$c.full"; fi
    mv "$O/chunk_$c.sum.tmp" "$O/chunk_$c.sum"; done_now=$((done_now+1))
    echo "chunk $c/$NCH done: $(cat "$O/chunk_$c.sum" | cut -d' ' -f1-14)"
  fi
  c=$((c+1))
done
cat "$O"/chunk_*.sum > "$O/ALL.sum" 2>/dev/null
echo "chunks finished this invocation: $done_now ; chunks complete in total: $(ls "$O"/chunk_*.sum 2>/dev/null | wc -l)/$NCH"
