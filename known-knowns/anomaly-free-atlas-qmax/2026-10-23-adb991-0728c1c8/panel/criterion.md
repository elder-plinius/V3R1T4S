# Criterion skeptic: SMnuR Q_max 17 and 18 census rows

Scope of review: only the claim/ folder (CLAIM.md, status.md, REPRODUCE.md, object/counts.txt, source/, checker/).
Cheap checks were run in a scratch copy of claim/, on 1 core at nice 15.

## What the criterion literally demands

Quoted in CLAIM.md: "extend the exact census of anomaly-free U(1) charge assignments of the Standard Model fermions
(with and without three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the largest `Q_max`
tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution list as the certificate."
Shape: "record (exact counts past the published range) with a complete, independently recountable list."
No enumerated partial wins exist, so this passes only if the full criterion is met.

Literal parts: (a) the census object (anomaly-free U(1) charge assignments, integer, |F| <= Q_max, SM or SM+3nuR);
(b) Q_max beyond ADM's largest tabulated value; (c) new exact counts; (d) the full solution list as certificate.

## Point by point

1. Hidden quantifier "(with and without three right-handed neutrinos)". This claim covers only the "with" column.
   I read the parenthesis as the scope of the census (a table with two content columns), not as a conjunction that
   every extension must satisfy in one claim: "extend the census" is satisfied by new exact rows in a column, and the
   charter's shape ("exact counts past the published range") is per row. Under the strict conjunctive reading this
   claim would fail; I do not adopt it, because it would also make every single-column row fail and turn the
   criterion into a "both columns at once" requirement the text does not state. CLAIM.md says the SM column was
   extended (to 31) in other runs; I cannot see those and do not rely on them. Consequence: confirmed_scope names
   the SM + 3 nu_R content only and does not say the census as a whole is extended for both contents.

2. Census object. The six ACCs in CLAIM.md follow from the stated all-left-handed representations (I rederived the
   coefficients: SU(3)^2 2,1,1; SU(2)^2 3,1; Y^2 1/6,4/3,1/3,1/2,1; Y F^2 1,-2,1,-1,1; grav and F^3 with
   multiplicities 6,3,3,2,1,1). The linear parametrisation used by both counters and the lister
   (a_d=-2a_Q-a_u, a_L=-3a_Q, a_e=2a_Q-a_u, a_nu=4a_Q+a_u) is correct. checklist.c tests the six ACCs directly in
   integer form (Y^2 one multiplied by 6). Bound |F| <= Q_max is the literal "integer charges bounded by Q_max".

3. "Beyond the largest Q_max tabulated by ADM". status.md gives 10 for both contents, but from web-search text;
   the primary sources (JHEP, Zenodo) were refused by the proxy ("PENDING TABLE CHECK"). This is a real, unclosed
   gap in the evidence: the largest tabulated Q_max is not byte-verified. It matters only if ADM tabulated SMnuR at
   Q_max >= 17; the reported Zenodo description ("augments v1.0.0 with the SMnuR solutions up to and including
   Qmax=10") and the published values stopping at 10 give no sign of that. 17 and 18 exceed 10 by a wide margin,
   and also exceed the workspace's own earlier rows (16, per CLAIM.md context). I accept (b) with this caveat.

4. Convention ("inequivalent" = 1 + nonzero gcd-1 solutions modulo independent within-species family permutations
   and overall sign). It is inferred, not read from the atlas (CLAIM.md says so). Null-model check, rerun from
   scratch with source/count.c and source/conventions.py: of the five candidate conventions computed from the same
   raw counts, only prim_incl0 reproduces all ten published values (SM Q_max 1, 3, 5, 7, 10: 8, 82, 626, 3902,
   23800; SMnuR Q_max 6..10: 435305, 1358388, 3612734, 9587085, 21546920). The nearest alternative (prim_excl0)
   misses every one by exactly 1; all_incl0 matches only SM Q_max 1; the no-sign and non-primitive variants miss
   by far. An independent brute-force enumerator I wrote (explicit sorted-triple enumeration, explicit ACCs,
   explicit canonicalisation and gcd, no code shared with the claim) gives 8 and 82 (SM, Q_max 1 and 3) and 38 and
   358 (SMnuR, Q_max 1 and 2), equal to prim_incl0. Ten 3-to-8-digit matches with off-by-one discrimination pin the
   convention numerically; whether ADM phrase it the same way in words is unverified, and the ten reference values
   themselves come from search text (same caveat as point 3). Accepted as "the atlas's convention" in the sense of
   "reproduces every available atlas value", which is how confirmed_scope words it.

5. "New exact counts". 1643386480 (Q_max 17) and 2720672222 (Q_max 18) are exact integers, not estimates, from a
   raw count of all bounded solutions plus exact Burnside (sign) and Moebius (common factor) corrections; fix.py's
   sign-fixed-point count (species triples {-a,0,a}) and the Moebius sum over floor(Q/d) are correct. I checked
   count.c against count2.c (different split and matching) at SMnuR Q_max 12: both give the raw count 191048355.
   My rerun of the Q_max 17 count is in point 9; Q_max 18 was not rerun. counts.txt also names rcount.c and mitm.c as independent counters; they are NOT in claim/, so I give
   them no weight; count.c and count2.c are present and suffice.

6. "The full solution list as the certificate". The lists (1643386479 and 2720672221 lines, on the order of
   100 GB and 160 GB as text) are not stored; they are defined as the deterministic output of source/csenum2.c
   (bytes independent of NPASS/NTHR per its header) and pinned by sha256 in counts.txt. I accept a regenerable,
   hash-identified list as "the full solution list": the hash fixes every byte, and anyone who regenerates it gets
   exactly the certified object and can check it. Tested the mechanism on the two known rows in REPRODUCE.md:
   csenum2 12 1 gives sha256 c92c6342...df84 and csenum2 20 0 gives f8e2ce35...e770, both exactly as stated;
   checklist PASSes both, with 95067545 and 1071440 lines, equal to count.c's convention values minus 1
   (95067546 and 1071441). I did not regenerate the Q_max 17/18 lists (1-2 h each on one core). Literal nit: the
   list omits the zero assignment, which is counted (count - 1 lines); it is stated explicitly and trivially known,
   so I do not treat it as an incomplete list.

7. "Complete, independently recountable" with a single lister. The argument is sound: checklist.c proves every
   line is a valid, nonzero, gcd-1, canonical (one per equivalence class), strictly increasing (hence distinct)
   class; the independent counters (no code shared with the lister; different algorithm: raw count + Burnside +
   Moebius versus direct canonical listing) give the total number of classes; a set of distinct valid classes whose
   size equals the total is the full set. A second lister is not needed for completeness; the counters play that
   role. The risk is a shared conceptual error (same ACCs, same convention), which point 4's calibration and the
   brute-force check address.

8. Subsumption. Nothing in claim/ already states these two values; CLAIM.md's context says earlier SMnuR rows end
   at 16, and rows <= 16 do not imply rows 17 and 18 (the Moebius step needs only Q <= 9 values besides the top
   row, but the top raw count is new). So within what I can see, the claim is not subsumed. The criterion was
   already crossed (Q_max 11 > 10) by earlier rows per CLAIM.md; these rows are further new exact counts past the
   published range, which the per-row shape counts as record entries. If another run already certified SMnuR 17 or
   18, this would be subsumed; nothing in claim/ says so.

9. Rerun of the counter route for SMnuR Q_max 17 on one core (about 15 min): count.c gives raw N = 3294219380;
   with the Q_max <= 12 raw counts above, conventions.py gives prim_incl0 = 1643386480, equal to the claimed count
   and to counts.txt's list line count + 1. Q_max 18 (about 40 min on one core) did not fit before the deadline, so
   the 18 row's count rests on counts.txt as reported, plus the same code path verified at 12 and 17.

## Verdict

The two rows meet the criterion literally for the SM + 3 nu_R content: exact counts at Q_max 17 and 18, beyond the
largest ADM Q_max reported (10), in a convention that reproduces every available ADM value, with a complete,
hash-pinned, regenerable canonical list whose completeness is tied to independent counters. Residual caveats: the
ADM range and reference values come from search text, not the primary table; the 17/18 lists and hashes were not
regenerated by me; only the "with nu_R" column is extended by this claim.

confirmed_scope: For the Standard Model fermions plus three right-handed neutrinos, counting 1 plus the nonzero gcd-1 integer solutions of the six anomaly conditions with |F| <= Q_max modulo independent within-species family permutations and overall sign (the convention that reproduces all ten Allanach-Davighi-Melville values available here, whose largest Q_max is reported as 10 from search text), the exact counts are 1643386480 at Q_max = 17 and 2720672222 at Q_max = 18, each certified by the count-1-line canonical list deterministically regenerated by source/csenum2.c and identified by the sha256 in object/counts.txt, whose line count matches the independent no-list counters source/count.c and source/count2.c.
context: subagent (fresh, saw only claim/)
pass: true
