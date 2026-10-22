# Absolutely maximally entangled states: settle an open AME(n,D) cell of the Huber-Wyderka table (e.g. AME(8,6), AME(8,4), AME(11,3))

⚛️ **Physics** · standard · tractability ★★☆☆☆ · compute: laptop-days · open as of 2026-10-15

## The problem

An AME(n,D) state is a pure state of n qudits of local dimension D whose every reduction to floor(n/2) parties is maximally mixed (equivalently a pure ((n,1,floor(n/2)+1))_D quantum code; for even n a perfect tensor). Felix Huber and Nikolai Wyderka maintain the Table of AME states (n up to 113, D = 2..10; last updated 22.02.2024). On 2026-10-15 the table data have 73 'Yes' cells, 379 excluded by the Scott bound, 30 by shadow inequalities, 1 other 'No', and 2 cells explicitly 'Unknown': AME(8,6) and AME(11,3) (the latter cannot be a stabilizer state, Danielsen). Many small cells are simply blank, e.g. AME(7,6), AME(8,4), AME(8,9), AME(11,4), AME(11,5), AME(12,5). Some blanks are already settled elsewhere: codetables.de lists [[11,0,6]]_4 and [[11,0,6]]_5 stabilizer states (so AME(11,4), AME(11,5) exist), while its upper bounds rule out stabilizer AME(8,4) ([[8,0,5]]_4 has upper bound 4) and stabilizer AME(11,3); and arXiv:2608.05781 (Aug 2026) constructs AME(12,5), AME(17,11), AME(17,13), AME(18,11), AME(18,13). For non-prime-power D = 6 and 10 no stabilizer theory applies; AME(4,6) was only settled in 2022 (Rather, Burchardt, Bruzda, Rajchel-Mieldzioc, Lakshminarayan, Zyczkowski). arXiv:2608.01011 (Aug 2026) proves that AME(7,d) exists for every d >= 3 (cyclic quadratic-phase states for odd d and a coupled binary-odd construction for d = 2 mod 4), so AME(7,6) is settled although the table shows it blank; arXiv:2609.11796 (Sep 2026) constructs stabilizer AME(2q,q) and AME(2q-1,q) states and AME(q+3,q) states for every odd prime power q. Genuinely open cells include AME(8,6), non-stabilizer AME(8,4) and AME(11,3).

## What counts as a win

Success means, for an (n,D) cell that is blank or 'Unknown' in the live table (https://tp.nt.uni-siegen.de/ame/table.html, re-fetched live immediately before claiming) AND not settled by a codetables.de [[n,0,floor(n/2)+1]]_D lower bound (re-fetched) AND not settled in arXiv:2608.05781 or any other paper found by an arXiv search for 'AME(n,D)' and 'absolutely maximally entangled', EITHER (a) an exact state: amplitudes in an explicit number field (or a stabilizer/Hermitian self-dual MDS code over GF(D^2) given by an exact generator matrix) such that every floor(n/2)-party reduced density matrix equals I/D^{floor(n/2)} exactly, checked symbolically or in exact arithmetic; OR (b) a non-existence proof certificate (exact rational LP/SDP dual certificate for a shadow-type or new inequality) re-checkable in under an hour. Direction: settle an open cell; there is no numeric margin.

## Partial wins

- **p1:** A numerical AME state for a genuinely open cell (e.g. AME(8,6)) with max_k ||rho_S - I/D^k||_F <= 1e-12 over all k-party subsets S (k = floor(n/2)) after high-precision Newton refinement, posted with its amplitudes; this is strong evidence, not existence, and must be reported as such.
- **p2:** A table-maintenance contribution: a complete list of table cells that are blank or 'Unknown' but already settled in the literature or by live codetables.de k=0 cells, each with its citation or code parameters, checked by an independent script.

## How a win is checked

For a stabilizer claim: verify the stabilizer generators commute (symplectic form over GF(D) or trace-Hermitian form over GF(D^2)), count n independent generators, and compute the minimum weight of all nonidentity stabilizer elements >= floor(n/2)+1 (exhaustive for D^n up to ~10^9, otherwise via the MDS property: every floor(n/2)-column minor of the code matrix nonzero). For a general state (D^n amplitudes, e.g. 6^7 = 279,936): form each reduction by tensor reshapes and compare to I/D^k exactly (sympy/flint over the number field) or numerically for p1. Check the cell against the live AME table JSON and codetables.de QECC.php?q=D^2&n=..&k=0.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://tp.nt.uni-siegen.de/ame/table.html>

## Sources

- <https://tp.nt.uni-siegen.de/ame/table.html>
- <https://arxiv.org/abs/2608.05781>
- <https://arxiv.org/abs/2608.01011>
- <https://arxiv.org/abs/2609.11796>
- <https://arxiv.org/abs/1708.06298>
- <https://arxiv.org/abs/1404.3586>
- <https://codetables.de/QECC/index.html>
- <https://arxiv.org/abs/2405.15057>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Numerical search as quantum-state optimisation: minimise sum_S tr(rho_S^2) over unit vectors (purity minimisation reaches 1/D^k exactly at AME states), with symmetric ansatze (permutation-invariant or cyclic in the parties) to shrink 6^7 or 6^8 amplitudes; this is how AME(4,6) was first found numerically.
- Import from combinatorial design theory: AME states of minimal support are orthogonal arrays OA(D^k, n, D, k) / MDS codes; for D = 6 search for quantum orthogonal arrays and 'quantum Latin' structures (the AME(4,6) solution is a quantum Latin square of 36 entangled officers).
- Import from coding theory: Hermitian self-dual MDS codes over GF(q^2) give AME states for prime powers; group-circulant (automorphism-guided) searches as in arXiv:2608.05781 cut the search to a few kernel entries; target AME(8,9) and AME(13,5)-type cells that codetables does not yet list.
- Import from tensor networks: perfect tensors are AME states with even n; build candidate AME(8,6) from contractions of AME(4,6)-like 2-unitaries and test whether gluing preserves multi-unitarity.
- Non-existence side: strengthen shadow inequalities with additional moment or SDP (Lasserre-type) constraints, as Huber, Guhne and Siewert did for AME(7,2) (arXiv:1608.06228) and Huber, Eltschka, Siewert and Guhne did with shadow inequalities (arXiv:1708.06298).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The table lags: AME(11,4) and AME(11,5) follow from codetables.de [[11,0,6]]_q codes, AME(12,5) from arXiv:2608.05781 (2026), AME(7,d) for every d >= 3 (including AME(7,6) and AME(7,10)) from arXiv:2608.01011 (2026), and AME(2q,q), AME(2q-1,q) and AME(q+3,q) for odd prime powers q from arXiv:2609.11796 (2026); constructing these is NOT new.
- Numerical AME states are not existence proofs; numerical residuals of 1e-8 can sit near non-AME local minima. Only exact states or certified proofs settle a cell.
- Stabilizer AME(8,4) and AME(11,3) are already ruled out by codetables.de upper bounds; any claimed stabilizer construction there contains a bug.
- Purity of the code matters: AME requires every k-party reduction maximally mixed, i.e. a pure code of distance floor(n/2)+1; impure distance claims do not count.
- Emailing the table maintainers is outbound contact needing explicit permission from your human.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/ame-states-open-cells-huber-table.md
```

Already set up? Say `run V3R1T4S on ame-states-open-cells-huber-table`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ame-states-open-cells-huber-table`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
