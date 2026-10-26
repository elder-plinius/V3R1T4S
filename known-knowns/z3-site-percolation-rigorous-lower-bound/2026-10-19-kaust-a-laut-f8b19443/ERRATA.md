# Errata (found by the panel, at the gate, or by the hostile proof audit after the gate)

Apart from the citation in item 1, the object is unchanged from what the panel checked. PROOF.md, REPRODUCE.md, code/
and outputs/ are byte-identical to it; panel/reproduce.md lists their sha256 values.

1. Citation of the record. The panelled claim said the 0.2522 source was arXiv-only ("no journal version found").
   The journal paper, Combin. Probab. Comput. 32 (2023) 912-955, states the bound as Theorem 7.1. At the gate the
   citation in object/result/bound.json was corrected. The record value is unchanged (panel/gate.md).
2. object/code/par/go.mod says `go 1.26.4`, the toolchain used, while object/REPRODUCE.md says "any recent version".
   With an older Go, GOTOOLCHAIN=auto (the default) fetches 1.26.4. Older toolchains were not tested.
3. "All N-step walks" in the run's documents means this: the enumerator visits sign-flip orbit representatives and
   weights each by its orbit size 2^|axes used|. PROOF.md Lemma 4 proves the two are equivalent, and the
   no-symmetry checkers of the panel and of verify-it-yourself/check_fast.py agree with it.
4. The older bound 1/mu = 1/4.7387 = 0.2110283 is quoted as 0.21103 (rounded to nearest). As a lower bound,
   0.21102 would be the safe rounding. It is not used anywhere in the argument.
5. object/result/bound.json gives "certificate_file": "outputs/p20.txt", which is relative to object/.
6. object/outputs/small/ (N = 3..14) was generated at packaging time with object/code/par, on the same machine with
   the same Go toolchain. It is byte-identical to the REPRODUCE skeptic's runs of the same program for N = 3..14.
   These tables help verification and are not part of the panelled claim.
7. object/outputs/verify_N20.txt, k18.txt and k20.txt have CRLF line endings, because they were written by Python on
   Windows. The tables p16.txt, p18.txt and p20.txt are LF.
8. Found by a hostile proof audit after the gate. A fresh reviewer read only object/PROOF.md; its report is
   how-we-built-it/hostile_audit/REPORT.md. Verdict: GAPS (fixable). It found no error in the argument and no
   counterexample at N = 20.
   - object/PROOF.md defines a NAW by "v_i ~ v_j only for |i - j| = 1" and adds "in particular it is
     self-avoiding". That remark is false at N = 2: the walk (0, e, 0) satisfies the condition.
   - The definition should read "a self-avoiding walk with v_i ~ v_j only for |i - j| = 1". For N >= 3 the
     condition already forces self-avoidance.
   - No number changes:
     - the enumerator and verify-it-yourself/check_fast.py both require self-avoidance;
     - the 6 extra N = 2 walks have no extensions;
     - the tables start at N = 3.
   The text should also say:
   - 0 is open (otherwise C(0) is empty);
   - in Lemma 2, "y not in gamma" follows from d(y) = N + 1;
   - B_{gamma,y} is measurable with respect to the sites outside gamma u F (an intersection over n of finite
     cylinder events), which gives the independence in Lemma 3.
   These and the audit's wording points are corrected in the paper version. object/PROOF.md is left as the panel
   checked it.
