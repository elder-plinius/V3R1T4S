# Criterion skeptic: anomaly-free-atlas-qmax

Scope of review: only the claim/ folder. The checks below were run in a scratch copy of claim/, outside the run tree.

Criterion (verbatim, CLAIM.md): "extend the exact census of anomaly-free U(1) charge assignments of the Standard
Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the
largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution list as the
certificate." There are no enumerated partial wins, so the only possible pass is the full criterion.

## Checks run (scratch copy)

1. SM list: `acclist 11 0` regenerated a stream whose sha256 is 723e21fb...80667d68, identical to the shipped
   object/SM_q11.txt.gz. The checker on the shipped list printed "valid solutions: 37005" and PASS.
2. SMnuR list: `acclist 11 1` regenerated a stream (847 s, streamed straight into hashing and the checker) with
   sha256 f4e16ec8613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4, which matches object/counts.txt.
   The checker printed "valid solutions: 45378377" and PASS.
3. Independent counts (REPRODUCE.md step 3): `count` for Q_max 1..11 and both contents, with `count2` agreeing at
   SM Q_max 11 (raw N = 74566). Under prim_incl0, conventions.py reproduces all 10 published values: SM 8, 82, 626,
   3902, 23800 and SMnuR 435305, 1358388, 3612734, 9587085, 21546920. At Q_max 11 it gives 37006 and 45378378,
   which equal the list line counts + 1. Two algorithms agree here. The list enumerator (meet-in-the-middle,
   explicit canonical forms) and the Burnside/Moebius counter (raw sorted-triple solutions) work differently, so
   the list is complete as well as valid.
4. My own null check of the basis and convention. I wrote a separate brute force in the paper's right-handed
   basis, with my own ACCs and canonicalisation (per-species sorting, sign identification, gcd 1, zero included).
   It gives SM 8, 22, 82 at Q_max 1, 2, 3 and SMnuR 38 at Q_max 1. These equal the claim's prim_incl0 values,
   including the unpublished Q_max 2 value of 22.

## Point by point

- **Is Q_max = 11 "beyond the largest tabulated"?** Literally yes, if the largest ADM value is 10 for both contents.
  That fact comes from search-tool text plus a quoted Zenodo sentence ("up to and including Qmax=10"). It is not a
  byte-exact read: status.md says PENDING TABLE CHECK. Mitigation: that same source's ten numeric values are
  reproduced exactly by an independent computation, so the source is demonstrably accurate on the numbers. Under a
  null model of an unreliable source, matching all ten numbers by chance is implausible, so its range statement is
  credible too. Residual risk: an ADM table past 10 that the source missed. I found nothing in the claim pointing
  to one. The confirmed scope therefore names the secondary source. The win is the minimal extension, one step
  (10 -> 11), but the criterion says "beyond", not "well beyond", so there is no hidden quantifier on size.
- **Both contents?** "(with and without three right-handed neutrinos)" is a hidden conjunction, and it is met: both
  SM and SMnuR are given at Q_max 11. "New exact counts" (plural) is met by the two counts.
- **Convention inferred, not read: is it a stretched definition?** No, for the numbers. "Extend the census" requires
  the atlas's own convention, and the chosen one is the only candidate among the five tested that hits all 10
  published values. The alternatives miss by a lot: all_incl0 at SM 10 is 24583 against 23800, and the sign
  variants are about twice as large. Since the convention is a fixed rule independent of Q_max (permutations x
  sign, primitive, +1), it cannot be fitted per point. One residual ambiguity: the "+1" is interpreted as the zero
  assignment, but the only evidence is that published = primitive nonzero classes + 1 at every point. Any other
  single extra class would give identical counts, so the counts do not depend on this interpretation. The list
  certificates omit the zero line (37005 and 45378377 lines), which is consistent with the stated count = lines + 1.
- **Including zero: is that faithful?** Only in the calibrated sense. It reproduces the published counts, and
  excluding it would contradict all 10 published values by exactly 1. Accepted.
- **Left-handed basis and sign change: harmless?** Yes. Flipping the sign of a whole species is a bijection on
  bounded integer solutions. It commutes with family permutations, with overall sign and with gcd. My right-handed
  brute force (point 4) confirms identical counts. The ACCs as written in CLAIM.md check out: dimension x
  hypercharge factors 1/6, 4/3, 1/3, 1/2, 1 and 1, -2, 1, -1, 1, and multiplicities 6, 3, 3, 2, 1, 1.
- **Is a regenerable list identified by sha256 "the full solution list as the certificate"?** For SM, the list
  itself is shipped, verified and complete. For SMnuR, the list is not in the folder (417 MB gzip). It is a
  deterministic generator plus a sha256 commitment. This is the stretched point. I accept it for three reasons.
  (a) Regenerating fixes the object byte for byte: I regenerated it and the hash matched.
  (b) The checker, a separate script that does not trust the generator, then verifies every line: ACCs, bound,
  canonical form, gcd 1 and strict ordering.
  (c) Completeness is established by the independent counter, not by the list.
  Anyone can therefore recount the certified object, which is what the charter's shape asks for ("a complete,
  independently recountable list"). A strict reader who requires a deposited file would fail the SMnuR half. The
  confirmed scope states the actual form of the certificate so that it is not overstated.
- **Non-subsumed?** Within what the criterion names (ADM's tabulation), Q_max 11 is not covered. Whether some other
  later work counted past 10 is outside the criterion's wording and not checkable from claim/. The novelty
  skeptic owns that question.

## Verdict

The result meets the full criterion literally, with two qualifications carried in the scope. First, "largest
tabulated = 10" rests on a secondary, non-byte-exact source whose numbers I independently corroborated. Second, the
SMnuR certificate is a hash-identified deterministic regeneration rather than a shipped file; I regenerated and
checked it.

confirmed_scope: In the counting convention that exactly reproduces all ten published Allanach-Davighi-Melville counts available to the claim (SM Q_max 1, 3, 5, 7, 10; SMnuR Q_max 6-10), the number of inequivalent anomaly-free integer U(1) charge assignments with |F| <= 11 is 37006 for the SM and 45378378 for the SM plus three right-handed neutrinos, certified by the included SM list (37005 nonzero classes) and by an SMnuR list of 45378377 nonzero classes that is deterministically regenerated and identified by sha256 f4e16ec8...96dbdaf4, one step beyond Q_max = 10, the largest ADM value according to the claim's secondary (not byte-exact) source.
context: subagent (fresh, saw only claim/)
pass: true
