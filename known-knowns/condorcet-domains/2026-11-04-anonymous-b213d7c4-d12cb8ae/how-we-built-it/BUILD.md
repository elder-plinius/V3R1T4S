# Construction provenance and reproduction

Contributor text. The exact certificate and count are checked independently by the shipped verifiers.

## Upstream source and review dependency

psmoros supplied the n=24 assignment in the **open, unmerged [PR #388](https://github.com/elder-plinius/V3R1T4S/pull/388)**, head abc5220fd79f75651d5faadb71df365566201121. The public source file is [object/n24_assignment.txt at that commit](https://github.com/psmoros/V3R1T4S/blob/abc5220fd79f75651d5faadb71df365566201121/known-knowns/condorcet-domains/2026-10-18-psmoros-bfb22498/object/n24_assignment.txt), SHA256 bfb224984f1f45bf52635b80f73a5cd237736940c0d9a0804f029988df6ccc2e. That third-party source is not bundled here. Our result derives from it, and full maintainer review of PR #762 remains dependent on review of #388.

The original 180,870,896-order [revision of PR #762](https://github.com/elder-plinius/V3R1T4S/pull/762/commits/651a2f7872214ef33728f32c08e4e1d89a9c177d) cloned alternative 11 as alternative 25. It reused all 2,024 original conditions, copied 253 conditions to the clone, and supplied 23 choices on triples containing both copies. Its assignment SHA256 is 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b.

Subsequent optimization produced the prior local 186,216,544-order assignment, included here as source-assignment.txt with SHA256 be05fe9ea7f4f6f33777cdf17e1c97d5d6869419838005b0ca949adca6fc2483. It is a frozen finder input, not a second claimed result in this package.

## New contribution

The present certificate changes 304 condition rows relative to that immediate input. Its full 2,300-rule assignment is object/assignment.txt, SHA256 d12cb8aee658a8e3657c8607ba722531604366ba65a97f8fd357aea7d482131e, and independently counts to 186,310,276 orders. The optimizations can change conditions across the assignment; the original n=24 certificate is the credited starting lineage, not an assertion that its restriction is unchanged in this final object.

The frozen binary-choice search uses source-assignment.txt and marginal-alternatives.csv. Run from the package root with Python 3.10+ and a C++17 compiler:

    python3 how-we-built-it/regenerate.py ../condorcet-replay-new

The output directory must be new and outside this package. Expected last line: PASS, with regenerated assignment SHA256 d12cb8aee658a8e3657c8607ba722531604366ba65a97f8fd357aea7d482131e. This replays the saved finite search with relative resource caps; it makes no global optimization or search-exclusion claim.

For a definition-based exact check, independent of the finder:

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. It counts the full domain with prefix and suffix implementations and runs exhaustive small-case calibrations. See RUN_IT_YOURSELF.md and verify-it-yourself/RECEIPTS.md.
