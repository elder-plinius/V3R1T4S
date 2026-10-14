# Independent CRITERION review

context: Separate fresh subagent invocation, canonical agent identifier `/root/criterion`, requested with `fork_turns=none`; same underlying model as the coordinating agent, shared filesystem, independently written checks, no inherited author reasoning.

transcript_reference: The conversation supplies the canonical agent identifier but no durable transcript URL, transcript filename, or provider invocation UUID to this reviewer; none is invented or claimed to exist.

reviewed_at: 2026-10-14T02:46:39.679830+00:00 (observed command output).

verdict: PASS for the full constant-weight-codes success criterion against the independently retrieved current sources; this is a criterion-panel verdict, not an honesty-gate status or external certification.

confirmed_scope: The explicit file `claim/A34_8_7_603.txt` with SHA-256 `18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad` contains 603 distinct binary words of length 34 and weight 7 with minimum pairwise Hamming distance 8, establishing A(34,8,7) ≥ 603.

## Scope and independence

I opened only the supplied claim-only files, my role protocol, independently fetched original public sources, and my own outputs. I did not inspect another reviewer report, author search notes, staging archive, or parent history. This is an independent model context, not a human reviewer, outside institution, distinct model, or independent machine. No communications with other reviewers, publication, or uploads occurred.

The original repository's current `main` tree resolved through GitHub's API to `7aca3835635e5323b48cdf3b5b59fcde502cab28`, saved in `validation/criterion/tree.json`. This happens to equal the claim's pinned revision. I independently fetched its bank, kit rules, policy, run and submission protocols, honesty checker source, trophy table, and code index. My checker confirms the claim's quoted success criterion exactly equals the current bank text.

## Exact object and literal criterion

PROVED-HERE: Run from the review archive root:

```sh
python validation/criterion/check.py
```

The standalone standard-library checker uses sets of occupied coordinates, rather than an author's checker. Raw output is `validation/criterion/check_output.json`. It exhaustively checked all 181,503 pairs, not a sample. All 603 words are distinct binary strings of length 34, each weight 7; the distance histogram is `{8: 32695, 10: 44893, 12: 76073, 14: 27842}`. Every one of the 21,105 four-subsets occurs at most once. Complementing all coordinates produces weight 27 with exactly the same pair-distance histogram. Thus the mirror is exactly the same extremal problem: complement is an invertible isometry, not an additional independent win.

KNOWN, independently retrieved comparisons:

| Required comparison | Observation | Consequence |
|---|---|---|
| [Brouwer live table](https://aeb.win.tue.nl/codes/Andw.html), `Values of A(n,8,7)`, n=34 | `601` with attribution `Bo`, upper bound `1175` | 603 is strictly above 601 and does not exceed 1175 |
| Mirror A(34,8,27) | No separate weight-27 cell occurs in the retrieved table; complementation identifies it with weight 7 | The same bounds apply; the mirror cannot be counted separately |
| [Echols, arXiv:2608.13906](https://arxiv.org/html/2608.13906v1), Table 1 | n=34, d=8, w=7: old 594, new 600 | 603 > 600 |
| [Lysenstøen, arXiv:2607.19550](https://arxiv.org/html/2607.19550v1) | Results concern other cells; no improvement to this cell or its mirror | No subsumption found |
| [Original trophy table](https://github.com/elder-plinius/V3R1T4S/blob/7aca3835635e5323b48cdf3b5b59fcde502cab28/TROPHY_CASE.md), row 26; code index | 602 for this cell | 603 improves the repository baseline by one |
| [Open pull requests](https://github.com/elder-plinius/V3R1T4S/pulls) | Two open PRs: matrix-multiplication rank and malformed null-control counts | Neither claims this code cell |

The arXiv abstract pages list only v1 for both named papers. The full current HTML bodies were also fetched and preserved; extracted table rows are in `validation/criterion/paper_tables.txt`. The repository baseline fetched from the original public repository is byte-for-byte equal to the supplied 602-word file, with hash `1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e`.

## Literature and hidden quantifiers

Searches covered recent constant-weight-code lower bounds, both explicit parameter spellings and the complementary cell, including a last-24-month search. They found no equal-or-larger construction for this cell. Newer relevant papers inspected were [Chee, arXiv:2610.10973](https://arxiv.org/pdf/2610.10973), concerning asymptotic invariant packings, and [Akhiiarov et al., arXiv:2609.23869](https://arxiv.org/pdf/2609.23869), concerning upper-bound envelopes. Neither supplies a larger finite lower-bound value for this cell. I also inspected the improvement table in [Rosin, arXiv:2603.00174](https://arxiv.org/html/2603.00174v1); it does not contain this cell. Search results, primary-source excerpts, version histories, and source-access results are preserved in `validation/criterion/sources1.json` through `sources4.json`.

The newer papers' HTML endpoints returned tool internal errors; their PDF endpoints were accessible and inspected. There is no unresolved inaccessible primary status source in this review. Brouwer's table was initially opened through the default web client; subsequent find/open operations addressed the retrieved source. No challenge bypass, impersonated client, cookie replay, or access evasion was used. The tool exposes a same-day crawl, not a raw origin HTTP status or exact origin retrieval timestamp; no stronger freshness metadata is claimed.

The literature conclusion is a documented search against available sources, not a logical proof that no unindexed, private, or future construction exists. No first-ever, optimality, maximum-size, or external record recognition claim is licensed. Passing the mathematical criterion does not determine priority by a discovery timestamp.

Neither enumerated partial win applies: p1 requires a previously missing explicit certificate, whereas this cell already has explicit codes; p2 requires a rational upper-bound certificate, which this claim does not provide. This is the full explicit-lower-bound criterion, not a redefinition of a partial win.

## Null model, provenance, and kit honesty constraints

PROVED-HERE: The supplied delta removes 38 baseline words and adds 39, preserving 564 words and reconstructing precisely the target set. This is a one-word net improvement on imported work, not an independently originated 603-word construction. Credit belongs to the V3R1T4S 602-word source and its credited seed source, Jordan Boisclair's `a34.8.7.601H`, with Brouwer's table and Echols' comparison acknowledged. The delta is a deterministic reconstruction; it does not establish when or by what search algorithm it was found.

KNOWN: Current `kit/RUN.md` step 3b explicitly allows the null-test exemption for an explicit object verified deterministically against a table. That exemption applies here. Random controls cannot invalidate an exact existence witness, and this claim makes no statistical, search-efficiency, or beats-chance assertion. A run's PREREG must nevertheless record its exemption honestly.

The kit separately requires authentic pre-result preregistration, three fresh reviewers, the main session's honesty gate, and `CHECK_RUN: PASS` before confirmed packaging. Those author-run records are outside the permitted claim-only review and were not audited here. Their absence from the intentionally minimal claim package is not evidence that they never existed; equally, this report does not certify that they did. The coordinator must not fabricate or retroactively date them, present this one review as a three-reviewer panel, invent a durable transcript reference, or treat this verdict as authorization to publish. I do not assign `CONFIRMED_SOLUTION` or `CONFIRMED_PARTIAL`.

Signed off by the fresh CRITERION reviewer, canonical agent `/root/criterion`, on the evidence and scope above.

pass: true
