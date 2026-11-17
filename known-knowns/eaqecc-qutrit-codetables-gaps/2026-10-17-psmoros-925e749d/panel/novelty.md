saved by the main session from the subagent's returned text (NOVELTY skeptic, model opus, returned 2026-10-17 about 19:05Z)
context: NOVELTY skeptic, fresh subagent (Claude Agent tool), model opus, sees only claim/

# Novelty check: [[33,1,31;24]]_3, target eaqecc-qutrit-codetables-gaps

## Status page: one GET with the shared fetch helper, lens novelty-skeptic
- URL: https://eaqecc.codetables.de/qutrit.php
- Fetched at 2026-10-17T18:49:50Z (UTC). HTTP 200, 628039 bytes.
- sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is the same as claim/data/qutrit.php.html and the hash in claim/TABLE_RECORD.md.
- The page says "Last change: 10.07.2025". I parsed 3,888 cells, n = 1..36.
- Cell (n,k,c) = (33,1,24): `[[33,1,25-32;24]]_3`, so d_lower = 25 and d_upper = 32. Its title reads: "lengthening of [[25,1,25;24]] increasing dimension of [[25,0,25;23]] from arXiv:2207.05647".
- Before each request I checked the session stop list and every other stop list. No request was blocked and no challenge page came back, so the session stop list is still empty. No fetched page contained instruction-like text (injection_suspected: none).

## Does anything in the table already imply the cell?
- The table holds no qutrit code with k >= 1, c <= 24 and d_lower >= 31. For k = 1, the smallest c that reaches d_lower >= 31 is 30, at every n from 31 to 36.
- I checked every predecessor through the eight propagation rules of arXiv:2207.05647 and through the rule [[n,k,d;c]] -> [[n,k-1,d;c-1]] of arXiv:2010.07902. The effective table values are:
  - (32,1,24) = 25, (33,2,24) = 22, (33,2,25) = 22, (33,1,23) = 24, (34,1,24) = 25
  - (34,1,23) = 25, (35,1,22) = 26, (36,1,21) = 27, (34,0,24) = 22, (33,0,23) = 21
  - None of them implies d >= 31.
- [[33,0,31;23]] and [[34,0,32;24]] cannot exist: both are pure codes whose dual has size 3^10, and Singleton allows at most 9^3.

## Structural finding: changes the margin, not the verdict
- **The k = 1 extension rule.** For q >= 3, any [[n,1,d;c]]_q gives [[n+1,1,d+1;c+1]]_q. Add the generators (Z_L, X) and (X_L, -Z) on a new qudit; the pairing between them must be -1, which is why the rule fails for qubits. I checked the rule by computation: [[5,1,3]]_3 extended step by step gives [[10,1,8;5]]_3 with exact distances.
- **What the rule gives from known codes.** Starting from the table's teleportation codes [[10,1,7;1]], [[11,1,8;1]] or [[12,1,9;1]]_3, the rule reaches [[33,1,30;24]]_3. So the table's 25 understates what known codes give directly. The real margin is d = 31 against 30 (+1), not against 25 (+6).
- **What the claimed object is.** I wrote my own checker and ran it; none of the code in claim/ was run. claim/object/S_33_1_31_24.txt (sha256 925e749d...9edc) gives n = 33, s = 56, c = 24, k = 1, isotropic dimension 8, d = 31. The isotropic part lives on only 12 coordinates. Restricted to those, the code is [[12,1,10;3]]_3. On the other 21 coordinates every nonzero logical has full weight, so the object is that 12-qutrit core extended 21 times.
- **The core cell.** The core beats the table cell (12,1,3), whose effective value is d_lower 9 and d_upper 11. That cell is not claimed in this package.
- **Which cores would imply the claim.** Through this rule the claim follows only from a known [[n0,1,n0-2;n0-9]]_3 with n0 <= 33. No such code is in the table: along that diagonal every cell falls 1 to 6 short.

## Crowd check: pull requests and repo
- `gh pr list --state all --search "eaqecc OR qutrit OR entanglement-assisted"` returned 100 PRs, but the OR query leaked to other repositories; only one hit was in the V3R1T4S repo. So I re-ran each term on its own, restricted to the repo: "eaqecc", "qutrit", "entanglement-assisted", "entanglement assisted", "codetables", "EAQECC in:body", "33,1,31", "[[33", and the target id.
- The only qutrit EAQECC PR is #331 (OPEN, 2026-10-17). It claims [[14,3,8;5]]_3 for cell (14,3,5), names only that cell, and lists its propagation consequences as k = 0 cells. It does not touch (33,1,24) or the k = 1 diagonal.
- The repo has 352 PRs in all states. None has [[33,1,...;24]]_3.
- TROPHY_CASE.md has no EAQECC or qutrit entry; I checked both the local checkout and origin at 04fdfba (2026-10-17). known-knowns/ has no eaqecc-qutrit folder; its only EAQECC mentions concern other targets.

## Literature: every paper below was opened; nothing else is relied on
- **arXiv:2007.01249** (Grassl, PRA 103, L020601), full PDF. Teleportation scheme [[n,k,n-2k+1;k]]_q from MDS codes, and [[l(q+1),1,lq;1]]_q. For q = 3 the best is [[33,1,24;1]], which is the table's c = 1 entry. No [[n,1,n-2;c]] family with small c.
- **arXiv:2010.07902** (Grassl, Huber and Winter, IEEE TIT 2022), full PDF:
  - Bounds (39) to (41). For (33,1,31), bound (41) gives k <= 2.68, so the claim is allowed.
  - The rule [[n,k,d;c]] -> [[n,k-1,d;c-1]].
  - Theorem 10 (pure [[n+c,k,d]] -> [[n,k,d;c]]). It would need a pure [[57,1,31]]_3, which Singleton rules out.
  - EAQMDS codes [[n,n-d+1,d;d-1]] exist only for large q.
  - Nothing covers the claim.
- **arXiv:2207.05647** (Luo, Ezerman, Grassl and Ling, QIP 2024), full PDF. In Table 2 (qutrit, n <= 36) the k = 1 entries are [[10,1,6;1]], [[13,1,10;8]], [[16,1,11;7]], [[16,1,12;9]], [[21,1,16;14]], [[22,1,17;15]], [[27,1,20;18]] and [[28,1,21;19]]. Its rules (1) to (8) do not reach 31 at c = 24.
- **arXiv:2206.09782** (Luo, Ezerman and Ling), full PDF. Its new rules only reduce length ([[n-s,κ,δ;c+s]], [[n-s,κ+s,δ-s;c]]). Nothing at this cell.
- **arXiv:2607.02170** (Li, Ezerman, Li, Ling and Sun, July 2026, inside the 24-month window), full PDF. Its qutrit codes stop at n <= 25 (for example [[7,1,7;6]], [[8,1,8;7]], [[25,2,22;23]]). Lengthening keeps d, so none reaches 31.
- **arXiv:2603.03182** (EA codes outside the stabilizer framework, March 2026) and **arXiv:2501.04921** (EA concatenated codes, January 2025): abstracts only. Neither lists qutrit parameters at this cell.
- **Grassl's arXiv author listing** (newest 2603.08563). No newer EAQECC code paper.
- **WebSearch** (6 queries) for the exact parameters [[33,1,31;24]], [[10,1,8;1]], [[11,1,9;2]], [[12,1,10;3]] and for k = 1, d = n-2 EA families: no hit.
- Every page came from arxiv.org with one GET each, HTTP 200, no blocks.

novelty: d = 31 strictly beats the live table's d_lower of 25 for (33,1,24). It also beats the 30 that known codes give with the elementary k = 1 extension rule. No table cell, PR or paper I opened has the code or implies it, so the claim is novel; the real margin is +1 over what is easily derived, and the new ingredient is the [[12,1,10;3]]_3 core.

pass: true
