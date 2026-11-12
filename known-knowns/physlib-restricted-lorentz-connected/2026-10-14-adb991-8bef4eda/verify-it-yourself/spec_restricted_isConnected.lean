import Physlib

/-! Frozen statement: Physlib `semiformal_result "FXNL5" restricted_isConnected`
(Physlib/Relativity/LorentzGroup/Restricted/Basic.lean, line 62 of the fetched status page). -/
def V3R1T4S.spec : Prop :=
  ∀ {d : ℕ}, IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d))
