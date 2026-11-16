context: Claude Code subagent, fresh context [Sonnet 5.5]

# Novelty check: ZetaHadamard.v1 (claim: Solutions/ZetaHadamard.v1)

All fetches are logged (UTC time, URL or gh command, status, sha256 where a body was saved) in a working copy (not shipped). Check time was 2026-11-16, about 03:38 to 03:45 UTC. Nothing was written to GitHub.

## Primary status source
- 2026-11-16T03:38:00Z, https://raw.githubusercontent.com/teorth/IEANTN/main/STATE.md, HTTP 200. It lists ZetaHadamard.v1 as `active`, conclusion `logDeriv_partial_fractions`, justification `literature`, receipts 0, issue "-".
- IEANTN main head read through gh api: d60421f10c16f5f6c2cb75f1067a72e24e616391 (2026-11-09T08:32:37Z). This is exactly the commit the claim is built against. The live STATE.md now reads 64 node versions and 134 conclusions, against the target text's 63 and 132, but the head commit matches the claim's pin.

## Conditions on live main
1. No Solutions directory: PASS. The recursive tree of main (not shipped in this package) has 22 Solutions entries, none named ZetaHadamard. The only ZetaHadamard paths are the node files under IEANTN/Nodes/ZetaHadamard/v1 and a working file (not shipped).
2. No lean-comparator receipt: PASS. The receipts folder holds ZetaLogDeriv.v1 and ZetaZeroes.v1 entries only, with none for ZetaHadamard.
3. No open issue assigned or claiming it: PASS. All 9 open issues were listed (#50, #52, #56, #63, #183, #184, #214, #215, #232). The assignees are xinjiegit, marcosadriano27, AlstonTZ and elmismisimoxhunca on the four family issues, and nobody on the rest. None concerns ZetaHadamard. Searches for "Hadamard" and "ZetaHadamard" over issues, open and closed, return nothing. The all-state issue list filtered for zeta/hadamard/partial/logderiv returns only #214, which is about ZetaZeroLocations.
4. No open PR touching it: PASS. I listed the file paths of all 35 open PRs and none contains ZetaHadamard or Hadamard. Searches over PRs for Hadamard, logDeriv, "partial fractions" and ZetaHadamard find only merged #108 ("CH2.v1 section 8, and a node for the partial fractions of zeta'/zeta"), which created the node. They also find merged logDeriv PRs for other nodes, plus open #234 (CotangentSeries.v1) and #235 (GammaAsymptotics.v1), which are different nodes.
5. Excluded families: PASS. ZetaHadamard is not a RosserSchoenfeld, BKLNW, FKS, Buthe or DudekPlatt family. The node's maintainer is Terence Tao, and its evidence is literature.
6. lean-eval headline: PASS. In the target text, lean-eval is the leanprover/lean-eval Comparator-based benchmark. I read the recursive tree of that repository (not shipped in this package, 4715 paths) and found no zeta, Hadamard, logDeriv or partial-fraction problem. This check is name-based only; I did not read every problem statement.

## Mathlib at 71a80585ee495fc24472fd0eaffc89d94e4fd8d6
Mathlib/Analysis/Complex/Hadamard.lean is the Hadamard three-lines theorem, unrelated to the product. Mathlib/NumberTheory/LSeries/ZetaZeros.lean has only closedness, discreteness, finiteness on compacts and tendsto lemmas for the zero set. RiemannZeta.lean has the functional equation, completed zeta and the residue. A grep of both for Hadamard, partial and logDeriv found nothing. The recursive tree has no Hadamard-product or xi-factorisation file. The node's own text also says Mathlib lacks the factorisation. The node is therefore not made trivial by Mathlib. The scope of this check is limited: I searched file names and two files in full, and code search for "logDerivZeta" returned nothing.

## Claims in elder-plinius/V3R1T4S
No open or closed PR or issue mentions IEANTN, ZetaHadamard or Hadamard (gh search prs and issues returned empty). TROPHY_CASE.md has 0 mentions of IEANTN or Hadamard (not shipped in this package). The known-knowns folder list has no IEANTN, zeta or Lean-node entry; the only Lean content is the lehmer-past-10-to-the-50 project, and hadamard-maxdet-records is about Hadamard matrices. No prior claim on this node.

## Caveats
- Comments on closed or open issues were not read in full. An informal "claim" comment on an unrelated issue could exist, but no issue mentions the node, and IEANTN's contributing guide calls claiming a courtesy.
- A competing solution could appear in a fork. I did not search forks.
- The criterion requires re-fetching live main immediately before claiming, so this check is a snapshot.

novelty: PASS. ZetaHadamard.v1 is unsolved and unclaimed on live IEANTN main, with every named condition holding.

pass: true
