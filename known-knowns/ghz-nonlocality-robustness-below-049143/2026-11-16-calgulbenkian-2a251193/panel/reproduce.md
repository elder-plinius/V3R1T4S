context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report: GHZ3 (18, 24, 72) functional
[Edited 2026-11-17 at the maintainer's request on the pull request: corrected the margin below 0.49143 from about 2.03e-5 to about 3.29e-5 (0.49143 minus 0.4913971114... is 3.2889e-5). The checks and verdict are unchanged; the margin figure is the only number that changed.]


Role rule followed: I wrote my own checkers from the definition before reading any author code. I did not run or read the author's C++ or Python (verify-it-yourself/*); nothing was run as a cross-check. Python ran with -I, no network, nothing posted. Heavy runs used nice -n 19 and 8 threads, each under 2 minutes.

## Definition checked against
From the target's verification method: "for a full-correlation functional, L = max over a in {+-1}^mA, b in {+-1}^mB of sum_k |sum_ij M_ijk a_i b_j| ... v* = (L - Q_noise)/(Q_GHZ - Q_noise) ... recomputed in exact or 40-digit interval arithmetic, is STRICTLY LESS than 0.49143 ... by at least 1e-5 (v* <= 0.49142)." The noise must be I/8.
Tensor law (object/bell_ghz3_18x24x72.json, tensor_law and w_int): M[i][j][k] = F((4i+3j+k) mod 144), F(s)=w_int[s] for 0<=s<=35, F(36)=0, F(s)=-w_int[72-s] for 37<=s<=72, F(s)=F(144-s) for 73<=s<=143. The JSON states marginals_1body_2body = 0, so the functional is full-correlation only. I rebuilt F from w_int and asserted F(s+72)=-F(s) and F(-s)=F(s): passed.

## 1. Local bound L (exact, exhaustive)
Reduction (my own proof):
- For fixed a, b the best c_k is sign(S_k), where S_k = sum_ij M_ijk a_i b_j, so the max over c is exactly sum_k |S_k|. Hence L = max over (a,b) of sum_k |S_k(a,b)|. This is exact.
- Negacyclic shift of b (b'_j = b_{j+1} for j<23, b'_23 = -b_0). Using F(s+72) = -F(s), the j=23 term gives -F(4i+69+k) = F(4i+141+k) = F(4i-3+k), so S_k(a,b') = S_{k-3}(a,b), where S_{k+72} = -S_k. The multiset {|S_k|} over k in Z_72 is therefore unchanged, so L(a,b') = L(a,b). The same argument with step 4 gives invariance under the a-shift. The global sign flip b -> -b also leaves L unchanged. So b can be restricted to one representative per negacyclic orbit (C48), and a likewise (C36). I did not need the author's reflection symmetry.
- Numerical test of the lemma: 60 random pairs, 0 violations (not shipped in this package).

Exhaustive runs (C, integer arithmetic, int32 per k, int64 sum; no sampling):
- Run 0: a reps (7286 orbits) x b reps (349536 orbits) = 2,546,719,296 pairs. Output: `L = 130692616`. Wall time 2.6 s.
- Run 1, cross-check that does not use the a-shift: all 2^18 a x b reps = 91,628,765,184 pairs. Output: `L = 130692616`.
- Run 2, cross-check that does not use the b-shift: a reps x all 2^24 b = 122,238,795,776 pairs. Output: `L = 130692616`.
Orbit counts (7286 and 349536) agree with the claim's Burnside numbers. Runs 1 and 2 each rely on only one of the two shift lemmas (proved the same way), and run 0 uses both; all three agree, so the maximum over all 2^42 (a,b) is 130692616, equal to the claimed exact_L. Also L(all +, all +) = 130692616 by direct evaluation. All runs are deterministic and agree.

## 2. Quantum values
- Observables: A_i, B_j, C_k = cos(phi) sx + sin(phi) sy with phi = i pi/18, j pi/24, k pi/72. Checked explicitly as 2x2 matrices (all 18+24+72 = 114): Hermitian, O^2 = I (hence eigenvalues +-1), traceless. Failures: 0.
- Contraction on |GHZ3>: explicit 8x8 contraction for all 31104 triples versus cos((4i+3j+k) pi/72): max deviation 2.0e-15 (double precision).
- Q_noise = Tr((I/8) B) = (1/8) sum M Tr(A)Tr(B)Tr(C) = 0 exactly (each factor traceless).
- Q_GHZ in 80-digit Decimal arithmetic (own Machin pi and Taylor cosine, truncation 1e-85; about 31104 terms of size at most 2e5, so rounding error is below 1e-60): `Q_GHZ 265961302.9070304670689578715170022035851420082093`. This lies inside the claimed 55-digit interval [265961302.907030467068957871517, ...518] and matches the JSON Q_GHZ_45d to 44 characters.
- v* = L/Q_GHZ = `0.491397111427465671323902139112596694367765925619`. This matches the claimed 0.4913971114274656713239021 to 0.4913971114274656713239022 and the JSON v_star digits. Test v* <= 0.49142: True. Margin below 0.49143 is about 3.29e-5 (above the 1e-5 requirement).
- Noise model: white noise is I/8 (value 0 on every term), as required.

## Limits of this check
I verified the numbers, the local bound and the quantum value. I did not re-fetch arXiv:2310.20677 Table III or check for newer upstream results (no network allowed for this role), so the "strictly below the live table" comparison rests on the 0.49143 quoted in the claim folder; other panelists own that part. The tensor has no marginal terms, so no third-party best-response over marginals was needed.

Scratch files: my own C and Python programs and their outputs, kept in a working folder that is not shipped in this package.

pass: true
