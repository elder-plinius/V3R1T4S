import PRMPlus.Params

namespace PRMPlus

lemma slabs_15 : checkSlabRange tubeParams 56 4 = true := by decide +kernel

lemma tube_slabs_15 : ∀ k, 56 ≤ k → k < 60 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 56 slabs_15

end PRMPlus
