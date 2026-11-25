#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$ROOT/bin"
if [[ -x "$ROOT/bin/cadical" && -x "$ROOT/bin/drat-trim" ]]; then
  echo "bin/cadical and bin/drat-trim present"
else
  echo "Building CaDiCaL..."
  if [[ ! -d "$ROOT/third_party/cadical" ]]; then
    echo "missing third_party/cadical" >&2; exit 1
  fi
  (cd "$ROOT/third_party/cadical" && ./configure && make -j"$(nproc)")
  cp "$ROOT/third_party/cadical/build/cadical" "$ROOT/bin/"
  if [[ ! -x "$ROOT/bin/drat-trim" ]]; then
    (cd "$ROOT/third_party/drat-trim" && make)
    cp "$ROOT/third_party/drat-trim/drat-trim" "$ROOT/bin/" 2>/dev/null || \
      cp "$ROOT/third_party/drat-trim/drat-trim" "$ROOT/bin/"
  fi
fi
"$ROOT/bin/cadical" --version || true
echo "BUILD OK"
