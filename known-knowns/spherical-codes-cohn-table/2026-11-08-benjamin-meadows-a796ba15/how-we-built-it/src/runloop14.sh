#!/bin/bash
cd /work
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for i in $(seq 1 60); do
  python3 chainregen.py > chainregen_last.txt
  n=$(head -1 chainregen_last.txt | awk '{print $1}')
  if [ "$n" = "0" ] || [ ! -s qCnext.txt ]; then
    echo "loop $i: empty queue, stop" >> bLoop14.log
    sleep 300
    continue
  fi
  echo "loop $i: $n rows" >> bLoop14.log
  mv qCnext.txt qCur14.txt
  TP=tpQ14 python3 chain3.py qCur14.txt >> bLoop14.log 2>&1
  rm -f qCur14.txt
done
echo CHAINLOOP_DONE >> bLoop14.log
