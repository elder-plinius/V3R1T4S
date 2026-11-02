#!/bin/bash
# strip_search.sh T cap suffix e1 e2 [baseSubdir]  one strip
T=$1;CAP=$2;SUF=$3;e1=$4;e2=$5
D=strips/s${e1}_${e2}; L=${LD:-$D/lib}
o=$(nice -n 10 perl -e 'alarm shift; exec @ARGV' $CAP code/search cover $L $D/c$SUF $T $e1 0 256 $CAP 1 1 40 2>/dev/null | tail -1 | cut -c1-210)
echo "[$e1,$e2] T=$T :: $o"
