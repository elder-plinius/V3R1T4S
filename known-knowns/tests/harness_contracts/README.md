# Wrapper contract regression tests

Run from the repository root:

    python3 known-knowns/tests/harness_contracts/run_regressions.py --output /tmp/veritas-harness-results

Requires Python 3.9+, a POSIX shell and ordinary coreutils. No scientific packages
or compiler are needed. All scientific commands are deterministic test doubles;
only the new standard-library orchestration helper is executed. Each wrapper
process has a five-second timeout and a restricted PATH.

The candidate suite retains the original 21 behavior classes, adds adversarial
output/inventory cases, and verifies positive semantic rejection, full 30+5 quoted
CSV inventory, CRLF, and benign runtime warnings. Run `--implementation baseline`
for the 21-case comparison using byte-verified pinned wrapper fixtures.

`--repo` selects a checkout; `--output` selects where captures/results are saved.
A probe PASS means its assertion reproduced, not that mathematics was verified.
The helper trusts the shipped checker output; these tests do not authenticate
checker output or establish scientific validity. Native computations, large graph
mode and the optional official VNN validator are intentionally unexecuted.

The contributed-sibling-package regression confirms that the original bigger-codes
release preflight permits a separate contributed package at the family root.
Baseline wrapper bytes are pinned to upstream main at
`371938deefd77b9e6a95d2a0c3e2d3c6ead7eaac`; they are unchanged from the original
PR baseline. This does not claim the candidate is already rebased or published.
