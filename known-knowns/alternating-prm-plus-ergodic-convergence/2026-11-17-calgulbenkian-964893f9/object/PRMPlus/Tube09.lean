import PRMPlus.Params

namespace PRMPlus

lemma slabs_09 : checkSlabRange tubeParams 32 4 = true := by decide +kernel

lemma tube_slabs_09 : ∀ k, 32 ≤ k → k < 36 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 32 slabs_09

end PRMPlus
