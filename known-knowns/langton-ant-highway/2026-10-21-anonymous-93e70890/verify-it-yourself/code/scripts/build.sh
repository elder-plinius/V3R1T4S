#!/bin/sh
# Build both simulators into bin/ (run from anywhere). Needs gcc.
set -e; cd "$(dirname "$0")/../.."; mkdir -p bin
gcc -O3 -march=native -o bin/lantx2 code/lantx2/lantx2.c
gcc -O3 -march=native -pthread -o bin/lant4 code/lant4pkg/src/lant4.c
gcc -O3 -o bin/lant_ref code/lant4pkg/ref/lant_ref.c
echo "built bin/lantx2 bin/lant4 bin/lant_ref"
