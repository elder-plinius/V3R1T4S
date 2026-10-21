#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
obj="object/best_n6637_s3108_c0.edges"
if command -v sha256sum >/dev/null 2>&1; then
  actual=$(sha256sum "$obj" | cut -d' ' -f1)
else
  actual=$(shasum -a 256 "$obj" | cut -d' ' -f1)
fi
if [ "$actual" != "00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059" ]; then
  echo "FAIL object SHA-256 mismatch"
  exit 1
fi
cxx=${CXX:-c++}
tmp=".checker.$$"
trap 'rm -f "$tmp"' EXIT
"$cxx" -O3 -std=c++17 verify-it-yourself/checker.cpp -o "$tmp"
"./$tmp" "$obj" 6637 13 4
