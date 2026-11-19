#!/bin/bash
# Program B on all CONNECTED graphs with 10 vertices, 8 geng residue classes, nice, 2 h cap each.
G=${GENG:-geng}   # the run used a local build of nauty 2.8.8 geng; path removed for publication
for r in 0 1 2 3 4 5 6 7; do
  ( nice -n 15 timeout 7200 bash -c "$G -cq 10 $r/8 | ./code/lifeB > out/B_order10_part$r.txt"; echo "exit $?" >> out/B_order10_part$r.txt ) &
  echo "part $r pid $!" >> out/pids.txt
done
wait
