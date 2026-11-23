#!/bin/sh
# 7 BH jobs, 300 s each, two at a time; one JSON line per job into output/results_Pb.jsonl
PY=$1; cd "$(dirname "$0")/.."
job() { $PY code/bh.py Pb $1 300 $2 output start/$3 >> output/results_Pb.jsonl 2>> output/err.log; }
job 119 11 Pb_119_seed.xyz & job 119 12 Pb_119_seed.xyz; wait
job 120 11 Pb_120_seed.xyz & job 120 12 Pb_120_seed.xyz; wait
job 121 11 Pb_121_obj.xyz & job 121 12 Pb_121_obj.xyz; wait
job 103 11 Pb_103_seed.xyz; wait
