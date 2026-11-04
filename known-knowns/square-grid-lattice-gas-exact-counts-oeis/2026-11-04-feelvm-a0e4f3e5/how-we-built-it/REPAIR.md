# REPAIR NOTE (repair round 1, criterion lane)

Written by the run's main session after the first panel. It addresses exactly the defect the first
CRITERION skeptic identified. It is NOT an instruction to pass: judge independently, pass: false stays
a fully acceptable outcome.

## The defect as found (first criterion lane, pass: false)

The first criterion skeptic verified every arithmetic clause (two disjoint-prime runs agreeing exactly;
both codes reproducing a(1)..a(14); N=15 correctly derived; digit count) and found ONE failing clause:
the literal growth-tolerance check, "a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant".
Their finding, quoted: it "fails at N=15 for any correct value, as witnessed by the published a(14)"
(published a(14) deviates 0.0055 from Lieb's constant; the claimed a(15) deviates 0.0048; the finite-size
deviation n^2 * delta(n) is 1.077-1.09 across every published term n = 4..14 and the claimed a(15)
continues it at 1.0769). The skeptic called it "a criterion defect, not a value defect" and judged the
literal clause as inherited by the partial win.

## The textual question the first lane did not resolve

The bank's full success criterion (quoted in claim/CLAIM.md) contains several clauses:
1. exact integer of the first unknown term, N one more than the largest live index;
2. two independent runs agreeing exactly (different primes/CRT sets AND a different decomposition);
3. the same code reproducing every published term for n <= N-1 exactly;
4. consistency with the known growth constant (the 1e-3 clause).

The bank's partial win p1 for THIS claim (quoted verbatim in claim/CLAIM.md) says:

    "The next unknown term(s) of A054759 (square ice on the n x n torus) or A027683 (hard squares on
    the n x n torus), same two-run and reproduction rules; A054759 is expected to be easy (row transfer
    matrix with 2^n states plus one tracked boundary edge) and is a partial only."

The first lane treated clause 4 as inherited by p1 ("same two-run and reproduction rules" read as
"same rules"). The alternative reading: p1 names exactly WHICH rules are inherited - the two-run rule
(clause 2) and the reproduction rule (clause 3) - and clause 4 belongs to the full-criterion sentence
that p1 partially exempts ("is a partial only"). Both readings are grammatically available; the bank
does not spell out the inheritance scope.

## Facts the fresh skeptic should weigh (all reproducible from claim/)

- Under reading A (all clauses inherited): the growth clause is unsatisfiable at N = 15 for ANY correct
  value - the PUBLISHED a(14) fails it by more than the claimed a(15) does (0.0055 vs 0.0048), and it
  first becomes attainable around N >= 33 for this sequence (extrapolating the stable 1.08/n^2
  finite-size correction). No computation could satisfy reading A's clause 4 at N = 15.
- Under reading B (p1 inherits clauses 2 and 3 only): every inherited clause passes, verified
  arithmetically by the first skeptic.
- Independently of the reading question, the claimed value IS consistent with the entropy constant
  under the finite-size model that the published terms themselves follow: ln a(n) = W2 n^2 + A + B/n
  with W2 fixed at Lieb's 0.431523058 predicts a(15) with log-ratio 1.35e-4; a free three-parameter fit
  gives exponent 0.431533 vs Lieb 0.431523 (1e-5 relative). These checks are in claim/growth.json.
- A bank-amendment proposal (finite-size model check for small-N partials) is being prepared as a
  separate draft PR; the criterion lane judges the bank text AS IT IS, not the proposal.

## Your task

Judge the criterion for the partial win AS NAMED IN THE BANK (p1), resolving the inheritance question
yourself from the bank's own words (both readings above are stated so you can pick). Write your
confirmed_scope sentence no wider than the evidence. You may pass: false - in particular, if you find
the inheritance question genuinely undecidable from the bank text, or if you find the stretched reading
to be exactly the "stretched criterion" the kit warns about, fail the lane and say so.
