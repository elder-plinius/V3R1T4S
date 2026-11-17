import PRMPlus.Params

namespace PRMPlus

lemma slabs_58 : checkSlabRange tubeParams 228 4 = true := by decide +kernel

lemma tube_slabs_58 : ∀ k, 228 ≤ k → k < 232 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 228 slabs_58

end PRMPlus
