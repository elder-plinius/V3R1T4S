# REPRODUCE (claim v3; fresh shell, Linux/macOS, Python 3.10+)
python3 -m venv v && . v/bin/activate && pip install python-flint==0.9.0
sha256sum -c SHA256SUMS.txt
# 1. zeros n = 1..99,200 (covers gamma < 74000; ~20 min on 3 cores, ~1 h on 1 core). Writer: plain arb strings.
python code/zeros.py 1 99200 400 3 zeros
# 2. completeness + certified values for all 19 rows (~30 s)
python code/verify_p1.py zeros > my_values.json
# 3. every ball must overlap the shipped result
python - <<'PY'
import json; from flint import arb, ctx; ctx.prec = 256
a = json.load(open("my_values.json")); b = json.load(open("result/p1_certified_values.json"))
assert a["N_gamma_lt_74000"] == b["N_gamma_lt_74000"] == 98625 and a["N_gamma_lt_14000"] == b["N_gamma_lt_14000"] == 14950
assert len(a["values"]) == len(b["values"]) == 19
for x, y in zip(a["values"], b["values"]):
    assert x["y"] == y["y"] and arb(x["h_320"]).overlaps(arb(y["h_320"])), x["y"]
print("REPRODUCED", len(a["values"]))
PY
# 4. the 19-row comparison with the printed values under BOTH conventions (no flint needed).
#    Expect: rounding 8 MISMATCH, truncation 6 MISMATCH, 0 AMBIGUOUS either way;
#    corrections (wrong under either convention): Table 2 rows 1, 4, 12, 14.
#    The script parses printed values from inputs/kn_arxiv_v1_tables_excerpt.txt (check against the PDF).
python check/compare_printed.py
# 5. (optional, ~2 min) the more=True spot check needs the v1-format zero files; with v2/v3 files from step 1
#    it checks the writer against itself and the 512-bit reference: python check/spot_check_zeros.py zeros
