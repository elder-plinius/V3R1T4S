#!/bin/bash
# merge split outputs: merge.sh K TMAX W -> min best over workers, union of minimisers at the min (sorted cell sets)
cd "$(dirname "$0")/../output"; K=$1; T=$2; W=$3; n=$(grep -l RESULT k${K}_T${T}_w*.txt | wc -l); echo "workers finished: $n/$W"
b=$(grep -ho 'best_onset=[0-9]*' k${K}_T${T}_w*.txt | cut -d= -f2 | sort -n | head -1); echo "min best_onset: ${b:-NONE<=$T}"
[ -n "$b" ] && grep -h "^SOL onset=$b " k${K}_T${T}_w*.txt | sed 's/.*cells: //' | tr ' ' '\n' | sort | tr '\n' ' ' | sed 's/^ //' ; echo
[ -n "$b" ] && grep -h "^SOL onset=$b " k${K}_T${T}_w*.txt | sed 's/.*cells: //' | while read l; do echo $l | tr ' ' '\n' | sort | tr '\n' ' '; echo; done | sort -u
