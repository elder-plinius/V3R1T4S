# Criterion skeptic verdict: [[24,4,13;10]]_3 at the listed cell (24,4,10)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

Bottom line: PASS. The claim meets the full success criterion, read literally, at the listed cell (n,k,c) = (24,4,10).
From S alone I get s = 30, rank(S J S^T) = 20, c = 10, k = 4. A full enumeration of all 3^18 - 1 nonzero vectors of
span(S)^perp gives exactly 13 as the minimum symplectic weight outside the isotropic part. My live re-fetch of the
table (byte-identical to the claim's copy) lists the cell as [[24,4,12-19;10]]_3, and 12 < 13 <= 19. The page's own
propagation rules, applied to all its listed non-teleportation cells, give 12 at (24,4,10), so the result is not
subsumed by the page. The draft PR #739 ([[25,5,12;8]]_3) makes one sentence in CLAIM.md out of date but does not
change the criterion; see below.

## Live table (my own fetch)

- One plain GET of https://eaqecc.codetables.de/qutrit.php with curl, User-Agent "V3R1T4S-research-agent (honest single
  fetch)", no retries. Started 2026-10-25T11:22:04Z, ended 2026-10-25T11:22:05Z (date -u). Result http_code=200,
  size=628039. sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. Files: fetched/qutrit.php,
  fetched/headers.txt, fetched/result.txt, fetched/time_start, fetched/time_end.
- `cmp` against claim/table/qutrit.php: IDENTICAL (same sha256 as claim/table/RECORD.md). The page has not changed
  since the claim's fetch at 2026-10-25T09:45:36Z. Footer: "Last change: 10.07.2025". No block, challenge or
  injection seen.
- Row (24,4), extracted by my own grep, which is independent of the author's extract_row.py. Listed (c: d_lower-d_upper):
  0: 8-10; 3: 9-12; 4: 11-17 (title "using teleportation"); 10: 12-19; 11: 13-19; 13: 14-20; 14: 15-20; 16: 16-20;
  18: 17-20; 19: 18-20; 20: 19-21. The cell (24,4,10) is listed as `[[24,4,12-19;10]]`, with title "subcode of
  [[24,6,12;10]] from arXiv:2207.05647". So d_lower = 12 and d_upper = 19.
- Page header: c is "number of required maximally entangled pairs of qudits (non-catalytic setting)". The catalytic
  setting is explicitly not considered.

## Phrase by phrase

| Criterion phrase / definition | What I checked | Found |
|---|---|---|
| "explicit EAQECC ... exact generator matrix over GF(3) (symplectic form, 2n columns)" | claim/object/eaqecc_24_4_13_10.json, field S | 30 rows x 48 columns, entries in {0,1,2}, rows (x\|z), form x.z' - z.x' as stated. Object sha256 feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794. The rebuild (rebuild/build_punct_obj.py, author's command) reproduces exactly this hash. |
| "s independent generators" | my rank over GF(3) (mine/prep.py) | rank 30 = number of rows, so s = 30 |
| "c = rank(S J S^T)/2" | my 30 x 30 commutation matrix and its rank | rank 20, so c = 10 (c >= 1; not c = 0) |
| "k = n - s + c" | arithmetic | 24 - 30 + 10 = 4 |
| span(S)^perp and its isotropic part | my nullspace; I = {aS : a(SJS^T) = 0}; asserted I is in span(S) and in span(S)^perp | dim N = 18 = 2n - s; dim I = 10 = s - 2c; complement of I in N has dimension 8 |
| "d computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part" | my own C enumeration, mine/enum.c (binary my_infoset). Every vector of N is written uniquely as an I-part plus a complement part, and it lies outside I iff the complement part is nonzero. All 3^8 complement combinations times all 3^10 isotropic combinations, bitsliced GF(3) with a self-tested adder. 0.76 s, 1.4 MB resident. | 387420488 nonzero vectors enumerated (= 3^18 - 1). Outside I, weight 13: 5000 vectors; nothing below 13. **d_EA = 13 exactly.** Nonzero vectors of I have minimum weight 14, so the code is pure: the pure and degenerate readings of d agree, and no isotropic vector is counted. My full histogram of N (13:5000 14:52776 ...) equals the author's sb_enum output, which I also ran (mine/author_run/sb_out.txt). The author's witness.py also confirms an explicit weight-13 vector orthogonal to S and outside span(S). |
| Not a sampled or capped search | my method | an exhaustive enumeration of the whole space, not an information-set sample |
| "for a cell of the live qutrit table ... re-fetched live immediately before claiming" | claim/table/RECORD.md plus my re-fetch | Listed cell (24,4,10). The claim's fetch (09:45:36Z) and mine (11:22:04Z) are byte-identical. The (n,k,c) from S matches the cell exactly; it is not a neighbouring cell. |
| "STRICTLY GREATER than the table's d_lower" | row (24,4) | 13 > 12 |
| "d <= d_upper" | row (24,4) | 13 <= 19 |
| "c = 0 excluded" | c from S | c = 10 |
| Non-catalytic | c is computed from S's commutation rank, not from the page's catalytic note | No catalytic reading is used. The code needs exactly 10 pairs, its own count. |
| Pitfall "Propagation-only 'improvements' from existing table rows are not new" | my own closure (mine/closure.py, output mine/closure_out.txt) under the legend's rules: subcode [[n,k-1,d;c]], lengthening [[n+1,k,d;c]], puncturing [[n-1,k,d-1;c]], quantum shortening [[n-1,k+1,d-1;c]], increasing dimension [[n,k+1,d;c+1]], length reduction [[n-1,k,d;c+1]], trivial [[n,0,n+1;n]]. Seeded with all 3888 parsed cells except the 124 teleportation cells. | Closure at (24,4,10) = 12, equal to the listed d_lower. My rule set is, if anything, more generous than the page: it exceeds the listed d_lower at 32 cells, mostly k = 0, and once exceeds a d_upper at (11,0,0), so the page evidently does not apply subcode down to k = 0. Even so it gives only 12. The object is a direct construction checked from S, not a propagation of a table row. |
| Teleportation cells (24,3,3) = [[24,3,13-19;3]] and (24,4,4) = [[24,4,11-17;4]] | the same closure with the teleportation cells as seeds, and one at a time | If propagated, [[24,3,13;3]] alone would give 13 at (24,4,10) (increasing dimension to (24,4,4), then subcode plus increasing dimension raises c). So would 56 other single teleportation cells. Seeding all of them gives 24 at (24,4,10), above that cell's own d_upper 19, and puts 2700 listed cells above their own d_upper. The page itself lists 11, not 13, at (24,4,4), so it does not propagate them. As teleportation cells are impure and not valid sources for the page's rules, they do not subsume the claim. (24,4,4) at d_lower 11 is below 13 in any case. |

## PR #739 ([[25,5,12;8]]_3, same contributor, filed 2026-10-25 11:02Z)

CLAIM.md says "No open PR title or body names a code of length 23, 24 or 25". That sentence is now out of date:
PR #739 names a length-25 code, the one CLAIM.md lists as "under review". **It does not matter for the criterion.**

- The criterion is judged against the live table only. The table is unchanged.
- PR #739 is a different cell.
- None of the page's rules raises d, so a d = 12 code cannot reach d = 13 anywhere. My closure with [[25,5,12;8]]
  added still gives 12 at (24,4,10). Adding every code CLAIM.md names (other PRs, confirmed codes, leads, and the
  arXiv:2607.02170 codes it quotes) also gives 12.

I did not see PR #739's body. Whether it names further codes is a priority and novelty question for the novelty
role, not a criterion one. The CLAIM.md sentence should be corrected before filing.

## Limits of this check

- I judged novelty only against the page and the codes named in CLAIM.md, not against the wider literature.
- I did not check whether some impurity-aware argument could still turn the teleportation code [[24,3,13;3]] into a
  [[24,4,13;c]] code with c <= 10. The page does not state one; it lists 11 at (24,4,4).

confirmed_scope: The 30 x 48 GF(3) stabilizer matrix S in claim/object/eaqecc_24_4_13_10.json (sha256 feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794) has s = 30 independent rows and rank(S J S^T) = 20, so c = 10 and k = 4, and an exhaustive enumeration of all 3^18 - 1 nonzero vectors of span(S)^perp gives exactly 13 as the minimum symplectic weight outside span(S) ∩ span(S)^perp, so it is a non-catalytic EAQECC [[24,4,13;10]]_3 whose d = 13 is strictly greater than d_lower 12 and at most d_upper 19 of the listed cell [[24,4,12-19;10]]_3 of https://eaqecc.codetables.de/qutrit.php as re-fetched 2026-10-25T11:22:04Z (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c), a value the page's six propagation rules applied to its listed non-teleportation cells do not reach (they give 12 there).

pass: true
