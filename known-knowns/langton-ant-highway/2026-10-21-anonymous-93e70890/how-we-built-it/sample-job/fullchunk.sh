#!/bin/sh
# PREREG.v2 item 2: full user chunk C rerun with box lant4 (1 thread; sha256 of raw output vs user's chunk sha256)
# and with lantx2 (all CAP; maxtcap, all masks at maxtcap, distinct classes). Single worker. Usage: code/fullchunk.sh C
C=$1; a=$((C*16777216)); b=$((a+16777216))
L4=/workspace/langton6x6-package/lant4; X=../indep-checker/code/lantx2
mkdir -p output/fullchunk
U=$(cat ../../../../data-user/langton6x6-out6/chunk_$C.sum)
sha4=$(nice -n 19 $L4 6 6 $a $b 2000000 1 | sha256sum | cut -c1-64)
nice -n 19 $X range 6 6 $a $b | awk -v c=$C 'BEGIN{mt=-1}
  {n++; if($6=="CAP")cap++; k[$3" "$4" "$5]=1; if($2>mt){mt=$2; mm=$1} else if($2==mt) mm=mm","$1}
  END{nk=0; for(x in k)nk++; printf "lantx2 chunk %d lines %d CAP %d maxtcap %d masks_at_max %s distinct_classes %d\n",c,n,cap,mt,mm,nk}' > output/fullchunk/c$C.lx2
echo "user: $U" > output/fullchunk/c$C.txt
echo "box lant4 sha256 $sha4" >> output/fullchunk/c$C.txt
cat output/fullchunk/c$C.lx2 >> output/fullchunk/c$C.txt
us=$(echo "$U" | awk '{for(i=1;i<NF;i++) if($i=="sha256") print $(i+1)}')
[ "$us" = "$sha4" ] && echo "SHA256 MATCH (user chunk output == box lant4 output)" >> output/fullchunk/c$C.txt || echo "SHA256 DIFFERENT" >> output/fullchunk/c$C.txt
