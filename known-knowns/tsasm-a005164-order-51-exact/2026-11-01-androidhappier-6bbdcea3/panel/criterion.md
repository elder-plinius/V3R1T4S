# Criterion skeptic: tsasm-a005164-order-51-exact
context: subagent (parent Task)

Worked from a fresh copy of claim/ at /workspace/v3crit_0205_2597807/claim. I did not read REPORT, NOTES, attempts, LOG or any other panel file.

## Clause-by-clause check (literal reading of the success criterion)
1. **Exact integer A005164(25) from exact enumeration, not the Hagendorf-Lienardy formula.** Pass. Both C programs are transfer-matrix DPs over the reduced quadrant (a symmetric n x n {-1,0,1} matrix, row prefix sums in {0,1}, row i sums to i mod 2). They do only additions over states. Nothing in them evaluates a contour integral or any closed form. I recompiled both and reran them for n=0..25 (about 3 min on 8 cores). Both gave a(25)=30533896243799704017627552102998416 (115 bits).
2. **The same program reproduces a(0)..a(13) exactly.** Pass, for Program A and for Program B.
3. **Reproduce a(14)..a(24) or report each disagreement, confirmed by a second program.** Pass by reproduction. compare.py printed OEIS=yes for every n from 0 to 24, with no disagreements. The disagreement branch is therefore empty.
4. **Two independent runs agree on a(25), with different prime sets or exact big integers, and a different sweep order or state encoding.** Pass.
   - Program A: row-major sweep, in-place pairing, shrinking state. Primes P_A are 4 primes below 2^62. CRT on 3 of them (186-bit modulus) and the 4th is a check prime: check=OK.
   - Program B: column-major sweep, growing state with a different bit layout, separate old/new arrays. Primes P_B are 4 primes below 2^61: CRT check=OK. Its exact run modulo 2^128 also gives the same value. Because a(25) < 2^128 and the program only adds, that value is exactly a(25).
   - The prime sets are disjoint. My per-prime residues match result/residues.txt for n=25.
5. **a(25) must not be in the DATA or a b-file when re-fetched.** Pass. I made one GET at 2026-11-01T03:03:53Z (Oct 31 23:03 EDT) to https://oeis.org/search?q=id:A005164&fmt=text. It returned HTTP 200, revision #41 (Sep 21 2022), and DATA ends at a(24). The sha256 is 3f428b9e…3e37, the same as the claimant's copy, and the a(25) string does not appear. The b-file in the claim is "synthesized from sequence entry" and ends at n=24. I did not re-fetch it because I was limited to one GET; since it is generated from the entry, it cannot hold a(25) either. The draft page in the claim says there are no pending changes.

## Hidden quantifiers, stretched definitions and null models
- **Definition.** The claim's object is the sequence's own definition: ASMs of order 2n+1 invariant under all of D4. tsasm_check.py brute-forces straight from that definition, without the reduction. Its fixtures behave correctly (a positive case and two kinds of negative case), and I got a(0..6) = 1,1,1,2,4,13,46, which matches the DPs. So the quadrant reduction is checked independently for small n.
- **Independence.** Both programs rest on the same quadrant reduction and probably share an author, so a reduction bug would be shared. The criterion's independence test is only about prime sets or big-integer arithmetic and sweep order or state encoding, and both are met. Separately, the reduction reproduces 25 published terms, a(14)-a(24) from an independent source (Liénardy), and the brute force. The null model that the reduction gives a different sequence matching all 25 terms and diverging only at n=25 is not credible.
- **Modular wraparound.** Program B reports intermediate wraparound in the 2^128 mode. That is harmless: the run only adds, so the result is exact mod 2^128, and the final value has 115 bits.
- **CRT.** The modulus (183-186 bits) is well above the 115-bit value, and a held-out prime verifies it in both programs.
- **a(26).** It is listed but not claimed, and I did not count it toward the pass.

## Verdict
This is the full success criterion, not a partial win, and it is not subsumed: a(25) is absent from OEIS DATA as of 03:03 UTC Nov 1 2026.

confirmed_scope: A005164(25), the number of 51 x 51 alternating sign matrices invariant under all eight symmetries of the square, equals 30533896243799704017627552102998416 by exact transfer-matrix enumeration in two programs with different sweep orders and disjoint prime sets (plus exact mod-2^128 arithmetic). Both programs also reproduce the published a(0)..a(24), and the value was absent from OEIS A005164 DATA when re-fetched at 2026-11-01T03:03:53Z.

pass: true
