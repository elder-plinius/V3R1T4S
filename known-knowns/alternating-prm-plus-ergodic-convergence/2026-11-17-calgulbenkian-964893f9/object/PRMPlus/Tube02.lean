import PRMPlus.Params

namespace PRMPlus

lemma slabs_02 : checkSlabRange tubeParams 4 4 = true := by decide +kernel

lemma tube_slabs_02 : ∀ k, 4 ≤ k → k < 8 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 4 slabs_02

end PRMPlus
