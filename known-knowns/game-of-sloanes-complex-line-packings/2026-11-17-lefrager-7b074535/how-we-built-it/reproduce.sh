#!/bin/sh
set -eu
mkdir -p repro_build
g++ -O3 -fopenmp -march=native how-we-built-it/fast_rrr_turbo.cpp -o repro_build/fast_rrr_turbo
g++ -O3 -fopenmp -march=native how-we-built-it/gram_alm.cpp -o repro_build/gram_alm
g++ -O3 -fopenmp -march=native how-we-built-it/fine_alm_ld.cpp -o repro_build/fine_alm_ld

repro_build/fast_rrr_turbo 3 34 2400 0.75683480 0.753 repro_build/stage1_3x34.txt 100
repro_build/gram_alm 3 34 polish repro_build/stage1_3x34.txt repro_build/double_3x34.txt
repro_build/fine_alm_ld 3 34 polish repro_build/double_3x34.txt repro_build/final_3x34.txt
python3 verify-it-yourself/check_submission.py repro_build/final_3x34.txt --skip-hash
