# Condorcet domain on 25 alternatives: 180,870,896 orders

## What

The assignment in claim/assignment.txt (SHA256 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b) defines a Condorcet domain on 25 alternatives containing exactly 180870896 linear orders, exceeding the verified arXiv:2601.07336v1 Table 4 lower bound 160316046 and the largest existing n=25 comparison found in the fresh search, 178950728.

The sentence above is retained verbatim from the contributor panel's original confirmed scope. Its comparison search was dated 2026-10-25; PR #389 is an open, unmerged public claim, not a published comparator. The published comparison bar is Table 4's 160,316,046.

The object is the full domain D(A) of all linear orders satisfying the 2300 never conditions in object/assignment.txt. Panel references to claim/assignment.txt map to object/assignment.txt here; claim/verify_assignment.py maps to verify-it-yourself/check_assignment.py. No full list of 180,870,896 orders is shipped.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder. Python 3 standard library only. Two independently written exact integer counters run in opposite directions, with strict parsers, Fishburn calibrations and full first-nine permutation checks. Expected final line: PASS. Rough laptop time: a few seconds; actual output is in verify-it-yourself/RECEIPTS.md.

## Compared to

| Source checked on 2026-10-25 | Cell | Source value | This object | Fetched UTC |
|---|---|---:|---:|---|
| [arXiv:2601.07336v1, Table 4](https://arxiv.org/html/2601.07336v1), f(n)&h(n) column | n=25 | 160316046 | 180870896 | 2026-10-25T18:36:53.790698Z |
| [psmoros PR #389](https://github.com/elder-plinius/V3R1T4S/pull/389), open, unmerged public claim (not a published comparator) | n=25 | 178950728 | 180870896 | 2026-10-25,18:36–18:39Z |

The gain over the published Table 4 lower bound is 20,554,850 orders. The separate gain over the unmerged n=25 claim in PR #389 is 1,920,168; that PR is comparison metadata only. The 2026-10-25 abstract check listed v1 only. Actual HTTP 200 receipts, hashes and selected response headers are summarized in the-record-we-beat/; original pages are not included. Literature and source-search limits are in the dated panel/novelty.md review. The panel reports retain their original mathematical assessments, with internal execution notes removed and unshipped evidence identified.

## Not claimed

No optimality, upper bound, asymptotic improvement, other n, new construction technique, or independently certified search exclusion is claimed. The dated novelty check covers the public indexed records searched and does not exclude unpublished work. This is not peer review.

## Credits

- Amartya K. Sen: never-condition characterization; [source and references](https://arxiv.org/html/2601.07336v1).
- Peter C. Fishburn: alternating scheme and calibration; [source and references](https://arxiv.org/html/2601.07336v1).
- Alexander Karpov, Klas Markstrom, Soren Riis and Bei Zhou: compatible-overlap construction framework and current Table 4, [arXiv:2601.07336](https://arxiv.org/abs/2601.07336).
- psmoros: the n=24 input assignment from the **open, unmerged [PR #388](https://github.com/elder-plinius/V3R1T4S/pull/388)**, head abc5220fd79f75651d5faadb71df365566201121. We reused all 2,024 original conditions and copied 253 conditions after cloning alternative 11 as alternative 25. Our contribution is the explicit choice of the 23 remaining conditions on triples containing both copies, shipped in how-we-built-it/completion.txt, yielding the n=25 assignment verified here. See how-we-built-it/BUILD.md for the source hash and reconstruction command. Full maintainer review follows review of #388.
- psmoros: the open, unmerged n=25 comparison claim in [PR #389](https://github.com/elder-plinius/V3R1T4S/pull/389); it is not a published comparator.
- Contributor credit: anonymous-b213d7c4.
