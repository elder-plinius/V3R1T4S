# Certificate format for N >= 17 (object/small/ uses it at N = 3, 4, 5, 8)

Three files per certificate, all little-endian, no headers. K and the claimed m are given on the command line.

- cN.counts: 2^(N-1) unsigned 32-bit integers. Entry b is the number of states whose window, read as an integer, is b (bit p of b = b_p, position p = 0..N-1). Top bit b_{N-1} is 0, which is the canonical form of PROOF.md section 4. No entry can exceed 2^N, and the checkers reject one that does. object/PROOF_v2.md writes the window as w (w_p = b_p here); PROOF.md and the checkers' code call it b.
- cN.states: 3 bytes per state. Read as an integer e (first byte lowest): low 23 bits are h (bit p = h_p), bit 23 is the policy (1 = ROW, 0 = SHIFT). States come ordered by b ascending and, within one b, by h strictly ascending. The file holds exactly the sum of the counts entries.
- cN.V: signed 32-bit integers (two's complement), one per state in the same order. This is the potential V.

object/small/, K = 16777216: c3 N=3 m=12326115, c4 N=4 m=12621691, c5 N=5 m=12776965, c8 N=8 m=13020558.
