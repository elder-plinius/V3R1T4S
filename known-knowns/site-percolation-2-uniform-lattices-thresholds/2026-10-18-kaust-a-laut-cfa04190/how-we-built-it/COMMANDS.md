# Commands

The exact commands are in how-we-built-it/REPRODUCE.md (the claim's own reproduction recipe; see RUN_IT_YOURSELF.md
for how to lay out the folder). The single evaluation of the Monte Carlo data is outputs/one_look.sh, its output
outputs/one_look_output.txt; the transfer-matrix extrapolations are in outputs/extrapolate_tm_output.txt. The rules
were frozen in rules/PREREG.md (2026-10-16T05:22:16Z) and rules/PREREG.v2.md to PREREG.v6.md, each stating when it was
frozen. Requirements: Python 3 with numpy, scipy and mpmath; any C compiler (the run used `python -m ziglang cc -O2`).
