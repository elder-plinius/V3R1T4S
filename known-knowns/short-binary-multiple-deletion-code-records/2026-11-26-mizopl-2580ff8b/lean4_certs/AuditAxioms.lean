/-
  AuditAxioms.lean — Machine-checkable axiom audit for every headline theorem in DeletionCode.
  All theorems must depend ONLY on standard Lean 4 axioms (subset of [propext, Classical.choice, Quot.sound]):
  ZERO sorryAx, ZERO Lean.ofReduceBool, ZERO Lean.trustCompiler!
-/
import DeletionCode

#print axioms DeletionCode.disjoint_delBall_iff_no_common_subseq
#print axioms DeletionCode.card_le_of_clique_cover
#print axioms DeletionCode.Cert_15_2.valid
#print axioms DeletionCode.Cert_15_2.inclusion_maximal
#print axioms DeletionCode.Cert_15_3.valid
#print axioms DeletionCode.Cert_15_3.inclusion_maximal
#print axioms DeletionCode.Cert_16_3.valid
#print axioms DeletionCode.Cert_16_3.inclusion_maximal
#print axioms DeletionCode.Cert_16_2.valid
#print axioms DeletionCode.Cert_16_2.inclusion_maximal
#print axioms DeletionCode.DualLP.exact_opt_7_2
#print axioms DeletionCode.DualLP.exact_opt_9_3
#print axioms DeletionCode.DualLP.cert_16_3_klein4_invariant
