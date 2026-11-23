import PRMPlus.Params

namespace PRMPlus

lemma slabs_57 : checkSlabRange tubeParams 224 4 = true := by decide +kernel

lemma tube_slabs_57 : ∀ k, 224 ≤ k → k < 228 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 224 slabs_57

end PRMPlus
