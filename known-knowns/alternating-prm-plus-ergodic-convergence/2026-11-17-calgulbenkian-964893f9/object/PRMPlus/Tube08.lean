import PRMPlus.Params

namespace PRMPlus

lemma slabs_08 : checkSlabRange tubeParams 28 4 = true := by decide +kernel

lemma tube_slabs_08 : ∀ k, 28 ≤ k → k < 32 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 28 slabs_08

end PRMPlus
