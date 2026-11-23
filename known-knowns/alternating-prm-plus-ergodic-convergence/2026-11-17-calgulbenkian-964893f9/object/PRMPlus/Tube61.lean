import PRMPlus.Params

namespace PRMPlus

lemma slabs_61 : checkSlabRange tubeParams 240 4 = true := by decide +kernel

lemma tube_slabs_61 : ∀ k, 240 ≤ k → k < 244 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 240 slabs_61

end PRMPlus
