import PRMPlus.Params

namespace PRMPlus

lemma slabs_28 : checkSlabRange tubeParams 108 4 = true := by decide +kernel

lemma tube_slabs_28 : ∀ k, 108 ≤ k → k < 112 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 108 slabs_28

end PRMPlus
