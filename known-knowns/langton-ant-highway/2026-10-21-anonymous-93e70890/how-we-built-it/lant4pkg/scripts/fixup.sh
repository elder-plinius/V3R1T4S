#!/bin/sh
# usage: fixup.sh W H CAP < lant4_or_cuda_output > reference_identical_output
# Replaces every WINDOW_OVERFLOW line by the output of the reference program for that single mask.
D="$(cd "$(dirname "$0")/.." && pwd)"; W=$1; H=$2; CAP=$3
T=$(mktemp); cat > "$T"
if ! grep -q WINDOW_OVERFLOW "$T"; then cat "$T"; rm -f "$T"; exit 0; fi
while IFS= read -r line; do
  case "$line" in
    *WINDOW_OVERFLOW) m=${line%% *}; "$D/ref/lant_ref" enumr $W $H $m $((m+1)) $CAP ;;
    *) printf '%s\n' "$line" ;;
  esac
done < "$T"
rm -f "$T"
