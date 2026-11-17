import PRMPlus.Params

namespace PRMPlus

lemma slabs_35 : checkSlabRange tubeParams 136 4 = true := by decide +kernel

lemma tube_slabs_35 : ∀ k, 136 ≤ k → k < 140 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 136 slabs_35

end PRMPlus
