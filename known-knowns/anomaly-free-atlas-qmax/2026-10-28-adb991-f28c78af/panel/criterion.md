# Criterion skeptic

context: subagent (fresh context, Claude Code Agent tool)

Read only the claim package (claim/). Spot computations in panel_work/criterion/ (nice -n 10, effectively one core,
PIDs in pids.txt).

## The criterion, literally

"extend the exact census of anomaly-free U(1) charge assignments of the Standard Model fermions (with and without
three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the largest `Q_max` tabulated by
Allanach, Davighi and Melville; new exact counts, with the full solution list as the certificate."
Shape: "record (exact counts past the published range) with a complete, independently recountable list."
No partial wins are listed, so it is the full criterion or nothing. Its clauses, checked one by one:

1. **Same census (convention).** The claim's convention is 1 + #(nonzero, gcd-1 integer solutions with |F| <= Q_max,
   modulo per-species family permutations and F -> -F). I checked this against the paper text, not only against
   status.md:
   - Paper section 2 item 3 (source/atlas/arXiv-1812.04602v5.txt) quotients by per-species family permutations. Section 4.1
     identifies F with -F and drops assignments with a common factor. Tables 2 and 3 have the caption "Each row contains the
     all-zero charge solution, as well as the solutions indicated in the rows above", i.e. cumulative in Q_max, zero
     included.
   - A subtlety: the paper's text says the common-factor test uses "the same prime number less than Qmax". Read literally,
     that would keep 2x(Q_max=1 solutions) at Q_max=2. The tables do not do that. I ran the lister's alternative modes
     (acclist count-only modes 0..3). SM Q_max=2 gives 21 (primitive, zero excluded), 29 (no sign identification), 28
     (non-primitive kept) and 22 (primitive + zero). SM Q_max=10 gives 23799, 47017, 24582 and 23800. Only the claim's
     convention gives the published 22 and 23800. So the tables, which are the census, use gcd 1 at prime Q_max as
     well (2, 3, 5, 7 are all in the reproduced set), and the convention carries over to Q_max=19 (prime) without
     ambiguity.
   - source/atlas/table_comparison.txt reproduces all 40 published values (SM and SMnuR, Q_max 1..10, solutions and
     symmetric). I compared several of them by eye with the extracted Tables 2 and 3 and erratum Table 1. They agree.
   - The ACCs in CLAIM.md are correct for the all-left-handed basis: I rechecked the hypercharge weights (1/6, 4/3,
     1/3, 1/2, 1 and 1, -2, 1, -1, 1). The derived linear-sum relations used by all programs (s_d=-2s_Q-s_u,
     s_L=-3s_Q, s_e=2s_Q-s_u, s_nu=4s_Q+s_u) are also correct.
   - Verdict: the convention is literally the atlas's census convention. The symmetry (CIS) column is not extended,
     but the criterion asks for counts of the assignments, not of CIS solutions. Not a gap.

2. **"beyond the largest Q_max tabulated by ADM".** The paper says the atlas covers "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the
   SMνR" (line 784), and the erratum extends SMnuR to 7..10 only. So the largest tabulated value is 10 for both contents.
   SMnuR 19 and SM 32..35 are all > 10. Met. Residual: I could not check the Zenodo record's current contents, which
   is outside the package. The criterion names the tabulation, and the package's arXiv abstract fetch (v5, no v6) shows
   no later version.

3. **"with and without three right-handed neutrinos".** Both contents are present: one SMnuR row (19) and four SM rows
   (32..35). The rows sit at different Q_max, which follows from the very different growth rates (about 4e9
   solutions at SMnuR 19 against about 2e7 at SM 35). The criterion does not ask for a common Q_max. Putting both
   contents in one claim follows the charter's single both-contents criterion. Each content's rows go past both the
   published range and that content's previously confirmed workspace rows. I see no stretched bundling. Neither
   content is padded by the other, and each would be a record on its own.

4. **"new exact counts" / non-subsumption.** CLAIM.md states that the confirmed workspace rows are SMnuR 11..18 and
   SM 11..31. The claimed rows are SMnuR 19 and SM 32..35. These are disjoint from those rows and from the
   publication, and the earlier rows do not determine them: the counts at a new Q_max are new information, not a
   restatement. So the claim is a genuine further extension of the record frontier, not a subset of earlier work.
   The criterion is a record criterion, so adding rows past the current frontier is exactly the kind of win it
   describes. Caveats I cannot close from inside the package: (a) the workspace registry of earlier confirmations is
   known to me only through CLAIM.md; (b) CLAIM.md says the same hashes were "recorded" on 2026-10-21/22 but not
   confirmed, which does not make them subsumed; (c) the package does not survey literature after the atlas. The
   criterion's reference point is ADM, so this is a novelty risk outside the literal criterion.

5. **"the full solution list as the certificate" / "complete, independently recountable list".** The lists are not
   stored. They are pinned by sha256 and regenerated by deterministic listers (source/acclist.c for SM,
   source/csenum2.c for SMnuR), and the bytes can be checked by checker/checklist.c (or checker/check_list.py).
   Hidden quantifiers I checked:
   - *Soundness of each line*: the checker independently verifies all six ACCs (hypercharge-squared one in integer
     form x6), |F| <= Q_max, nonzero, canonical form (species sorted, the lex-larger of F and -F), gcd 1, and strictly
     increasing order. Strict order plus canonical form rules out duplicates and equivalent pairs. So lines = a
     certified lower bound of the count minus 1.
   - *Completeness*: a list cannot certify itself as complete, and the published atlas lists cannot either. It rests on
     (i) the listers' exhaustive construction (I read both: exhaustive over sorted triples per species, all (s_Q,s_u)
     blocks, sign and pass logic consistent; hash-key collisions could only add lines, which the checker would
     reject) and (ii) agreement with an independent counter of different design: source/mitm.c counts multiset tuples
     with a different split (Q,L,nu | u,d,e), Moebius inversion over gcd and Burnside over sign, and never lists.
     For all five rows, mitm = list lines + 1 (object/receipts/mitm_*.txt against *.checker.txt). This is the same
     standard of evidence the atlas had, made stronger by the two-method agreement.
   - *count - 1 identity*: the zero assignment is counted but not listed. This is stated in the claim and consistent
     in all five rows (counts.txt column 4 = column 3 - 1; checker "valid solutions" = count - 1).
   - *Independent recountability*: anyone can regenerate the stream, compare the hash, and count it with the checker.
     That makes it a reproducible certificate. It is not a deposited file. The SMnuR 19 list would be roughly 200 GB
     uncompressed, so not storing it is a practical choice. I accept "regenerated + hashed + checked" as meeting "the
     full solution list as the certificate", because the list is fully determined, byte-pinned and checkable on demand.
     A stricter reader who demands a deposited file would disagree. I flag it as the main interpretive risk, but not a
     stretch of the evidence.
   - The two listers are byte-identical where both apply: in my runs, SMnuR Q_max 8 (csenum2 and acclist both
     71d1b799...) and SM Q_max 20 (both f8e2ce35..., equal to the REPRODUCE/receipts value). SMnuR 12 from csenum2 gives
     c92c6342..., equal to receipts/test_SMnuR12.sha256. So the canonical format is the same across both listers.

6. **My regeneration (SM Q_max 32).** `acclist 32 0 | tee sha256, wc | checklist 32 0`, with pipefail, took 221 s:
   sha256 3a5d7d1695cd98e6aa70ecc3c0ff9121f9312a11f0123ec6e6cec7a8ad408a07 (equal to object/counts.txt and
   receipts/SM32.sha256), 15866881 lines, checker "valid solutions: 15866881", PASS, exit 0. `mitm SM 32` gives
   RESULT 15866882 = lines + 1. I did not regenerate SMnuR 19 (about 80 min on 3 threads) or SM 33..35. For those I
   checked the receipts: enum log passes sum to 4247050204, and the final log line reports lines 4247050204 and
   count(+1) 4247050205 with no ERRORS flag. The checker reports PASS and pipeline exit 0. mitm gives 4247050205. SM
   33..35 have consistent checker, sha256 and mitm receipts.

7. **Null models.** The relevant null is a wrong or alternative convention that produces plausible but non-comparable
   numbers. It is excluded: the four alternatives give different values at Q_max 2 and 10, and only the claimed
   convention reproduces the published values (item 1). A second null is a lister that silently drops a class of
   solutions. This is excluded as far as computation can exclude it, by an independent non-listing counter agreeing
   exactly on all five rows. A third null is that the new values are implausible extrapolations. The SM growth from
   32 to 35 is consistent with roughly Q^6 scaling plus gcd-driven fluctuation. That is only a sanity check, not
   evidence.

8. **Minor, not criterion-relevant.** REPRODUCE.md says the SMnuR 19 run needs "< 3 GB", but receipts/SMnuR19.enum.log
   shows bucket memory up to 4.35 GB. The documentation understates the memory needed. checklist.c does not compare
   with an expected count. REPRODUCE.md says so explicitly.

## Decision

The claim meets the full criterion literally. It is the atlas's own census convention (verified to discriminate
against the alternatives), at Q_max beyond the largest tabulated value (10) for both contents. It gives new exact
counts, not subsumed by the confirmed rows SMnuR 11..18 and SM 11..31. Each count comes with a complete canonical
list that is fully determined, sha256-pinned, independently checkable line by line, and recounted by an independent
method. One row (SM 32) was regenerated here bit-for-bit. Main risks: completeness rests on the two-method
agreement, not on a self-certifying object; the list is reproducible, not deposited; and novelty against literature
after the atlas, beyond ADM, is outside what the package shows.

confirmed_scope: In the Allanach-Davighi-Melville census convention (1 + number of nonzero gcd-1 integer solutions of the six anomaly equations with |F| <= Q_max, modulo per-species family permutations and overall sign), the counts are 4247050205 for the SM plus three right-handed neutrinos at Q_max = 19 and 15866882, 19550225, 22847889, 26469950 for the SM fermions at Q_max = 32, 33, 34, 35, each equal to one plus the line count of a checker-passing canonical list with the sha256 recorded in object/counts.txt and to an independent non-listing count, beyond the published Q_max <= 10 and beyond the workspace's previously confirmed rows (SMnuR 11..18, SM 11..31).

pass: true
