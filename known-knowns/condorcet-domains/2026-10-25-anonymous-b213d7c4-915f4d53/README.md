# Condorcet domain on 25 alternatives: 180,870,896 orders

## What

The assignment in claim/assignment.txt (SHA256 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b) defines a Condorcet domain on 25 alternatives containing exactly 180870896 linear orders, exceeding the verified arXiv:2601.07336v1 Table 4 lower bound 160316046 and the largest existing n=25 comparison found in the fresh search, 178950728.

The object is the full domain D(A) of all linear orders satisfying the 2300 never conditions in object/assignment.txt. Panel references to claim/assignment.txt map to object/assignment.txt here; claim/verify_assignment.py maps to verify-it-yourself/check_assignment.py. No full list of 180,870,896 orders is shipped.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder. Python 3 standard library only. Two independently written exact integer counters run in opposite directions, with strict parsers, Fishburn calibrations and full first-nine permutation checks. Expected final line: PASS. Rough laptop time: a few seconds; actual output is in verify-it-yourself/RECEIPTS.md.

## Compared to

| Current source | Cell | Source value | This object | Fetched UTC |
|---|---|---:|---:|---|
| [arXiv:2601.07336v1, Table 4](https://arxiv.org/html/2601.07336v1), f(n)&h(n) column | n=25 | 160316046 | 180870896 | 2026-10-25T18:36:53.790698Z |
| [psmoros PR #389](https://github.com/elder-plinius/V3R1T4S/pull/389), open public claim | n=25 | 178950728 | 180870896 | 2026-10-25,18:36–18:39Z |

The exact gains are 20,554,850 over Table 4 and 1,920,168 over the largest existing same-n public claim found. Fresh abstract history lists v1 only. Actual HTTP 200 receipts, hashes and selected response headers are summarized in the-record-we-beat/; original pages stay local. Literature and source-search limits are in the unedited novelty report.

## Not claimed

No optimality, upper bound, asymptotic improvement, other n, new construction technique, or independently certified search exclusion is claimed. The dated novelty check covers the public indexed records searched and does not exclude unpublished work. This is not peer review.

## Credits

- Amartya K. Sen: never-condition characterization; [source and references](https://arxiv.org/html/2601.07336v1).
- Peter C. Fishburn: alternating scheme and calibration; [source and references](https://arxiv.org/html/2601.07336v1).
- Alexander Karpov, Klas Markstrom, Soren Riis and Bei Zhou: compatible-overlap construction framework and current Table 4, [arXiv:2601.07336](https://arxiv.org/abs/2601.07336).
- psmoros: published n24 input assignment from [PR #388](https://github.com/elder-plinius/V3R1T4S/pull/388), head abc5220fd79f75651d5faadb71df365566201121, and the n25 comparison [PR #389](https://github.com/elder-plinius/V3R1T4S/pull/389).
- Contributor credit: anonymous-b213d7c4. Research used two independent Astra/high lenses and separate Sol/xhigh verification contexts under V3R1T4S.
