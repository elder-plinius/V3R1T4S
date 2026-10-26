#!/bin/sh
# Builds the reference (ref/lant_ref), the multithreaded CPU solver (lant4), the CPU emulation of the GPU kernel (lant_cuda_emu),
# and, if nvcc exists, the CUDA solver (lant_cuda).   Usage: ./build.sh [sm_arch, default sm_86 = RTX 3090]
set -e; cd "$(dirname "$0")"
CC=${CC:-gcc}
$CC -O3 -o ref/lant_ref ref/lant_ref.c
$CC -O3 -march=native -pthread -o lant4 src/lant4.c
$CC -O2 -x c -DLANT_EMULATE -Isrc -o lant_cuda_emu src/lant_cuda.cu
if command -v nvcc >/dev/null 2>&1; then nvcc -O3 -arch=${1:-sm_86} -Isrc -o lant_cuda src/lant_cuda.cu && echo "built lant_cuda"; else echo "nvcc not found: lant_cuda not built (lant_cuda_emu = CPU emulation of the same kernel code was built)"; fi
echo "built: ref/lant_ref lant4 lant_cuda_emu"
