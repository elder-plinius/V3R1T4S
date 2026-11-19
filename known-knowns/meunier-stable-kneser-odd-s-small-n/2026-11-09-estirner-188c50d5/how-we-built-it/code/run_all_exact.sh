#!/bin/sh
for spec in "9 3 3" "10 3 3" "11 3 3" "12 3 3" "13 3 3" "14 3 3" "17 3 5" "18 3 5" "19 3 5" "20 3 5" "21 3 5" "22 3 5"; do
  set -- $spec; C=$(($1 - $3*$2 + $3 - 1))
  timeout 1800 python3 exact_colour.py $1 $2 $3 $C
  timeout 1800 python3 exact_colour.py $1 $2 $3 $((C + 1))
done
