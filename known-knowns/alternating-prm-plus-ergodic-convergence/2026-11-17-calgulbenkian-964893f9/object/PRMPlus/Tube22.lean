import PRMPlus.Params

namespace PRMPlus

lemma slabs_22 : checkSlabRange tubeParams 84 4 = true := by decide +kernel

lemma tube_slabs_22 : ∀ k, 84 ≤ k → k < 88 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 84 slabs_22

end PRMPlus
