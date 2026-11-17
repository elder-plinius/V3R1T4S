import PRMPlus.Params

namespace PRMPlus

lemma slabs_06 : checkSlabRange tubeParams 20 4 = true := by decide +kernel

lemma tube_slabs_06 : ∀ k, 20 ≤ k → k < 24 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 20 slabs_06

end PRMPlus
