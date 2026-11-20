# Condorcet domain on 25 alternatives: 186,310,276 orders

## What

The full set D(A) of all linear orders on 1..25 satisfying object/assignment.txt has exactly 186310276 elements and is a Condorcet domain for every odd voter profile, strictly exceeding the latest-version Table 4 n=25 lower bound 160316046 identified by the supplied current arXiv metadata, the public open and unmerged n=25 claims 180870896 and 178950728, and the supplied prior local threshold 186216544, with novelty limited to the dated sources searched.

Contributor panel status: CONFIRMED_SOLUTION. This is our own three-skeptic assessment, not maintainer acceptance or peer review.

The What sentence above is quoted verbatim from the frozen verification gate. Its source comparisons were checked on 2026-11-04, before this PR update: the 180,870,896 value refers to the prior revision of PR #762 at commit 651a2f7872214ef33728f32c08e4e1d89a9c177d. It is retained as a dated comparison, not the current value of this updated PR.

**Review dependency:** our construction derives from psmoros's **open, unmerged [PR #388](https://github.com/elder-plinius/V3R1T4S/pull/388)**. Full maintainer review of #762 follows review of #388, as stated in the [maintainer feedback](https://github.com/elder-plinius/V3R1T4S/pull/762#issuecomment-6611587539). This update retains that dependency.

## Check it yourself

From this folder run `sh verify-it-yourself/run_checks.sh`. Python 3.10+ standard library only; expected last line: PASS. Two independently implemented exact counters and exhaustive small-case calibrations take a few seconds on a laptop. RUN_IT_YOURSELF.md also gives a portable byte-identical finder replay using the saved inputs and a C++17 compiler.

## Compared to

| Dated comparison | n=25 value | Gain |
|---|---:|---:|
| [Latest identified paper, v1 Table 4 f(n)&h(n)](https://arxiv.org/html/2601.07336v1) | 160316046 | 25994230 |
| [Prior revision of this PR](https://github.com/elder-plinius/V3R1T4S/pull/762/commits/651a2f7872214ef33728f32c08e4e1d89a9c177d), open and unmerged at source check | 180870896 | 5439380 |
| [Open, unmerged PR389](https://github.com/elder-plinius/V3R1T4S/pull/389) | 178950728 | 7359548 |
| Prior local assignment, SHA256 be05fe9ea7f4f6f33777cdf17e1c97d5d6869419838005b0ca949adca6fc2483 | 186216544 | 93732 |

Latest-version metadata was received2026-11-04T02:29:33.436710Z; Table4 was received2026-11-04T02:30:05.952223Z. The published-preprint construction cell and public unmerged claims remain separate comparisons. The formula column195312500 is not the specified construction lower bound. The exact source and cache qualifications are in the-record-we-beat/TABLE_SNAPSHOT.json and the unchanged panel reports.

## Not claimed

No global optimality, upper bound, asymptotic result, other n, certified search exclusion, or universal coverage of unpublished/unindexed work. Raw third-party pages, PDFs, search payloads and reviewer working programs are not included. This package updates PR #762; no maintainer acceptance, merge, or peer review is claimed.

## Credits

- Amartya K. Sen: never-condition characterization; [source and references](https://arxiv.org/html/2601.07336v1).
- Peter C. Fishburn: alternating-scheme calibration; [source and references](https://arxiv.org/html/2601.07336v1).
- Alexander Karpov, Klas Markström, Søren Riis and Bei Zhou: construction framework and [published-preprint table](https://arxiv.org/abs/2601.07336).
- psmoros: the n=24 assignment from the **open, unmerged [PR #388](https://github.com/elder-plinius/V3R1T4S/pull/388)**, head abc5220fd79f75651d5faadb71df365566201121, assignment SHA256 bfb224984f1f45bf52635b80f73a5cd237736940c0d9a0804f029988df6ccc2e. It is the upstream source of this construction; full maintainer review of #762 follows #388.
- The original 180,870,896-order revision of this PR cloned alternative 11 of that n=24 assignment as alternative 25, reused its 2,024 original conditions, copied 253 conditions to the clone, and chose 23 conditions containing both copies. Further optimization produced the prior local 186,216,544-order assignment, bundled here as how-we-built-it/source-assignment.txt. The present contribution changes 304 condition rows from that immediate input and supplies the new explicit 186,310,276-order certificate, exact checks and portable replay. These counts describe the saved lineage; the optimized certificate is independently checked in full. See how-we-built-it/BUILD.md.
- psmoros: the [open, unmerged PR #389](https://github.com/elder-plinius/V3R1T4S/pull/389) n=25 comparison claim; it is separate from the published Table 4 comparator.
- Contributor: anonymous-b213d7c4. The contribution here is the improved explicit assignment and its checkable reproduction.

Panel paths refer to the reviewed claim packet. object/assignment.txt and verify-it-yourself/ map directly; criterion.md maps to how-we-built-it/criterion.md and PREREG.md maps to how-we-built-it/PREREG-verification.md. Role working directories and raw source/novelty-data/ files remain local and unshipped. The factual novelty-source.json is included unchanged under panel/. The package verifier is separate from those reviewer work artifacts.

The three reviewer reports are copied byte-for-byte from the completed verification. The delivery copy of panel/gate.md preserves its status and confirmed_scope verbatim, labels their owner, and omits internal phase bookkeeping. The original gate remains unchanged in the local verification record. Source snapshots and reviewer statements about PR #762 describe its prior revision at the dated check.
