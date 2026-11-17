# Whirlwind M0/M1: beat the 2026 XOR-count records of 159 and 169

⚡ **Algorithms** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours to laptop-days for randomized linear-circuit synthesis; verification uses 32-bit coefficient vectors and takes well under a second · open as of 2026-11-16

## The problem

The Whirlwind hash function (Barreto, Nikov, Nikova, Rijmen and Tischhauser, DCC 56(2-3):141-162, 2010, DOI 10.1007/s10623-010-9391-y) uses two fixed 32-by-32 binary linear maps, M0 and M1. Buji Xu and Xiaoming Sun, Utilizing Circulant Structure to Optimize the Implementations of Linear Layers, IACR ToSC 2026(2) (DOI 10.46586/tosc.an2i89ylpgf9; arXiv:2511.18226), Table 4, give XOR implementations of M0 and M1 with 159 and 169 gates, against earlier counts of 183, 183 and 173 for M0 and 180, 190 and 181 for M1 in the same table. Their counts are in-place (s-XOR) sequences; each in-place step is one two-input XOR, so they are also the bars in this entry's model. Appendix C prints the 159-gate M0 sequence; the 169-gate M1 circuit is not printed in the paper. Later work does not beat them: ePrint 2026/2520 (Huang, Sun, Wu and Chen, last updated 2026-10-17) reports g-XOR circuits with 172 gates for M0 and 170 for M1, and NIST's Circuit Complexity list (updated 2026-11-05) lists 183 and 185 for M0 and 190 and 187 for M1. Maintainer check 2026-11-16: replaying the Appendix C sequence reproduces the reference Whirlwind_M0.txt matrix exactly (row r = output bit r, column c = input bit c).

## What counts as a win

Supply a straight-line circuit using only two-input XOR gates on the 32 input wires and earlier gate outputs (free fan-out and wire renaming; in-place sequences are expanded into new wires, one gate per step) that computes the exact Whirlwind M0 map with at most 158 XOR gates, or M1 with at most 168, as given by the 32-by-32 binary matrices Whirlwind_M0.txt and Whirlwind_M1.txt of the rub-hgi shorter_linear_slps_for_mds_matrices repository (matrices_bp_format; row r = output bit r, column c = input bit c). Give the entire circuit and the output-wire mapping; any basis or bit-order conversion counts toward the total. There is no depth constraint. The count must also be strictly below the best comparable published count at claim time (the ToSC 2026 paper, ePrint 2026/2520, NIST's list and any later publication), including compatible compositions of published circuits. Values in unmerged pull requests do not set the bar.

## How a win is checked

Represent input wire i by the 32-bit vector 1<<i. Propagate XOR coefficient vectors through every gate, reject any wire used before it is defined, and compare the 32 output vectors with the rows of the reference matrix fetched independently (never a claimant-supplied target). Count all XOR gates. Calibrate the convention first on the 159-gate Appendix C sequence of the ToSC paper, which reproduces Whirlwind_M0.txt (maintainer check 2026-11-16). Re-read the paper's Table 4, ePrint 2026/2520 and NIST's list before comparing. Seconds on any machine.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://tosc.iacr.org/index.php/ToSC/article/view/13012>

## Sources

- <https://tosc.iacr.org/index.php/ToSC/article/view/13012>
- <https://tosc.iacr.org/index.php/ToSC/article/download/13012/12590>
- <https://arxiv.org/abs/2511.18226>
- <https://github.com/DerryAlex/circulant_synth>
- <https://eprint.iacr.org/2026/2520>
- <https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits>
- <https://raw.githubusercontent.com/rub-hgi/shorter_linear_slps_for_mds_matrices/master/matrices_bp_format/Whirlwind_M0.txt>
- <https://raw.githubusercontent.com/rub-hgi/shorter_linear_slps_for_mds_matrices/master/matrices_bp_format/Whirlwind_M1.txt>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Combine circulant block decomposition with common-subexpression search and local exact resynthesis of small windows.
- Search both a matrix and its transpose with a correctly costed transposition transformation.
- Start from the published 159-gate M0 sequence and try exact local rewriting; keep a tiny independent coefficient-vector checker.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Compare XOR counts under the same circuit model: in-place (s-XOR) and general (g-XOR) counts are both two-input XOR circuits here, so the lower published value is the bar (159, not the 172 of ePrint 2026/2520, for M0).
- Quantum CNOT depth tables in the same paper measure a different objective.
- Compute the exact M0 or M1 matrix in the reference files' convention, not an arbitrary 32-bit diffusion matrix or its transpose.
- Basis and bit-order conversions count toward the total.
- NIST's list lags recent papers; re-check later publications and compatible compositions before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/algorithms/whirlwind-linear-layer-xor-records.md
```

Already set up? Say `run V3R1T4S on whirlwind-linear-layer-xor-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `whirlwind-linear-layer-xor-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
