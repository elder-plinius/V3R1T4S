import PRMPlus.Params

namespace PRMPlus

lemma slabs_07 : checkSlabRange tubeParams 24 4 = true := by decide +kernel

lemma tube_slabs_07 : ∀ k, 24 ≤ k → k < 28 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 24 slabs_07

end PRMPlus
