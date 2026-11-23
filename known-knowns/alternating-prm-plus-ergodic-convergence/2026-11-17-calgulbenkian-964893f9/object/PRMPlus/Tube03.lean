import PRMPlus.Params

namespace PRMPlus

lemma slabs_03 : checkSlabRange tubeParams 8 4 = true := by decide +kernel

lemma tube_slabs_03 : ∀ k, 8 ≤ k → k < 12 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 8 slabs_03

end PRMPlus
