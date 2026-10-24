"""Per-gauge view of the 400 null controls: how often does each claimed gauge alone reach the real R
(with |dt_arr| <= 10 min)?  Input: null_controls_<id>.json from null.py (R list order = claimed order)."""
import json, sys
ctrl = json.load(open(sys.argv[1])); claimed = sys.argv[2].split(","); real = [float(x) for x in sys.argv[3].split(",")]
for i, c in enumerate(claimed):
    rs = [x["R"][i] for x in ctrl]
    print("%s: controls %d, max control R %.3f, controls with R > 5: %d, controls with R >= real %.3f: %d"
          % (c, len(rs), max(rs), sum(r > 5 for r in rs), real[i], sum(r >= real[i] for r in rs)))
