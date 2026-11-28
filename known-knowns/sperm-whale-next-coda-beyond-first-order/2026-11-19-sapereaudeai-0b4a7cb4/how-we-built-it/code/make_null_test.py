"""Aggregate the null-control files into null_test.md (first block = the main claim's N2, as kit/check_run.py reads
the first 'controls:' etc.). Duplicated control indices (the same seed run twice after a worker restart) are
deduplicated keeping the first line; their values are reported. Usage:
python -I make_null_test.py <nulls_dir> <real_N2_twin_gain> <real_N4_gain> <real_N3_gain> <out.md>"""
import os
import sys

import numpy as np

d, r2, r4, r3, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]


def load(prefix):
    vals, dup = {}, []
    for f in sorted(os.listdir(d)):
        if f.startswith(prefix + "_") and f.endswith(".csv"):
            for line in open(os.path.join(d, f)):
                if line.strip():
                    parts = line.strip().split(",")
                    i = int(parts[0])
                    if i in vals:
                        dup.append((i, vals[i][0], float(parts[1])))
                    else:
                        vals[i] = [float(x) for x in parts[1:]]
    return vals, dup


lines = []
v2, dup2 = load("N2")
g2 = np.array([v2[i][0] for i in sorted(v2)])
gr1 = np.array([v2[i][1] for i in sorted(v2)])
v4, dup4 = load("N4")
g4 = np.array([v4[i][0] for i in sorted(v4)])
v3, dup3 = load("N3")
g3 = np.array([v3[i][0] for i in sorted(v3)]) if v3 else np.array([])

lines += ["# null_test - sperm-whale-next-coda-beyond-first-order (run 2026-11-19-0936)", "",
          "Main claim (full criterion), condition (2): design N2 of PREREG.md (first-order Markov bootstrap of coda "
          "records; statistic = pooled gain of the frozen model over its single-previous-coda twin).", "",
          f"controls: {len(g2)}",
          f"best_control: {float(g2.max())!r}",
          f"real: {r2!r}",
          f"real_beats_all_controls: {'yes' if (len(g2) >= 400 and r2 > g2.max()) else 'no'}",
          "command: python -I attempts/evaluator/code/nulls.py N2 data/csv/sperm-whale-dialogues.csv <first> <last> "
          "attempts/evaluator/nulls/N2_<worker>.csv  (then python -I attempts/evaluator/code/make_null_test.py ...)",
          "",
          f"N2 control gains (full vs twin): mean {g2.mean():.5f}, sd {g2.std():.5f}, min {g2.min():.5f}, "
          f"max {g2.max():.5f}, indices {min(v2)}..{max(v2)}, distinct {len(v2)}",
          f"N2 context only (not a gate): gain full vs R1 under the null: mean {gr1.mean():.5f}, max {gr1.max():.5f} "
          f"(real full vs R1 = 0.6563064778564619)",
          f"N2 duplicated indices (same seed computed twice across worker restarts; first kept): "
          f"{[(i, round(a, 12), round(b, 12)) for i, a, b in dup2]}", "",
          "## p4 claim: design N4 (labels resimulated from the pooled first-order same/switch chain)", "",
          f"p4_controls: {len(g4)}", f"p4_best_control: {float(g4.max())!r}", f"p4_real: {r4!r}",
          f"p4_real_beats_all_controls: {'yes' if (len(g4) >= 400 and r4 > g4.max()) else 'no'}",
          f"p4 control gains: mean {g4.mean():.5f}, sd {g4.std():.5f}, min {g4.min():.5f}, max {g4.max():.5f}",
          "p4_command: python -I attempts/evaluator/code/nulls.py N4 data/csv/sperm-whale-dialogues.csv 0 400 "
          "attempts/evaluator/nulls/N4_<worker>.csv", "",
          "## p3 claim: design N3 (CodaType sequences resimulated from the pooled first-order transitions)", ""]
if len(g3):
    lines += [f"p3_controls: {len(g3)}", f"p3_best_control: {float(g3.max())!r}", f"p3_real: {r3!r}",
              f"p3_real_beats_all_controls: {'yes' if (len(g3) >= 400 and r3 > g3.max()) else 'no'}",
              f"p3 control gains: mean {g3.mean():.5f}, sd {g3.std():.5f}, min {g3.min():.5f}, max {g3.max():.5f}"]
else:
    lines += ["p3_controls: 0 (not finished)"]
lines += ["p3_command: python -I attempts/evaluator/code/nulls.py N3 data/csv/DominicaCodas.csv <first> <last> "
          "attempts/evaluator/nulls/N3_<worker>.csv", "",
          "## Null-runner speed shims (null runs only; the frozen files were not modified)", "",
          "- scipy.special.ndtr in place of scipy.stats.norm.cdf, and the vectorised feature code "
          "attempts/evaluator/code/fastfeats.py: both checked bit-identical (np.array_equal) to the frozen feats on "
          "all 3,418 real positions at each N2 worker start (attempts/evaluator/nulls/N2_w*.log) and on all 17,090 "
          "position x fold-edge combinations (attempts/evaluator/nulls/verify_fastfeats.txt).",
          "- einsum gradient in place of the broadcast-and-sum gradient (same objective): on real fold 0 it reproduces "
          "the frozen probabilities within 3.1e-9 (full), 2.7e-14 (twin), R1 identical "
          "(attempts/evaluator/nulls/verify_fastgrad_N2.txt) and 7.4e-12 for the p3 model "
          "(verify_fastgrad_N3.txt). The first N2 controls (indices 0-2) ran with the ndtr shim only and a few more "
          "(about 3-9, 134-141, 267-274) with ndtr + einsum before fastfeats existed; N4 ran with no shim; N3 ran "
          "with the einsum gradient. Control 2 was computed twice (ndtr only, then ndtr + einsum): the two values "
          "agree to about 3e-12 bits (see the duplicated-indices line)."]
open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("\n".join(lines))
