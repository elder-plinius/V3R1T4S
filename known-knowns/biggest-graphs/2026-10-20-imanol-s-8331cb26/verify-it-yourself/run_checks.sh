#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
obj=object/G_14_4_n8425.edges
if ! shasum -a 256 -c SHA256SUMS >/dev/null; then echo FAIL; exit 1; fi
actual=$(shasum -a 256 "$obj" | cut -d' ' -f1)
if [ "$actual" != "8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7" ]; then echo FAIL; exit 1; fi
tmp=".checker.$$"
trap 'rm -f "$tmp"' EXIT
"${CXX:-c++}" -O3 -std=c++17 verify-it-yourself/checker.cpp -o "$tmp"
"./$tmp" "$obj" 8425 14 4
