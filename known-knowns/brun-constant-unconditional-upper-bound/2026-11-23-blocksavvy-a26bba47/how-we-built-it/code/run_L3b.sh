#!/bin/sh
# L3(b) runs: q-dependent GRH constant (Grenie-Molteni Cor. 1.2 with log q <= 2 log z), all else as Dunn, plus robustness variants.
# Run from attempts/replay/. Outputs in ../improve/out/.
P=${PY:-python3}
for prec in 128 256; do
  $P code/replay.py --cpi q --prec $prec --out ../improve/out/L3b_q_dunnbracket_p$prec.json
  $P code/replay.py --cpi q --c1 li --vlemma own --prec $prec --out ../improve/out/L3b_q_li_ownV_p$prec.json
done
