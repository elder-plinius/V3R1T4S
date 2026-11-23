import PRMPlus.Params

namespace PRMPlus

lemma slabs_12 : checkSlabRange tubeParams 44 4 = true := by decide +kernel

lemma tube_slabs_12 : ∀ k, 44 ≤ k → k < 48 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 44 slabs_12

end PRMPlus
