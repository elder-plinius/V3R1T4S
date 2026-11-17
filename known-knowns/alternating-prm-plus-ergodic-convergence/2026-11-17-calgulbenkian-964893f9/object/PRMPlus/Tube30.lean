import PRMPlus.Params

namespace PRMPlus

lemma slabs_30 : checkSlabRange tubeParams 116 4 = true := by decide +kernel

lemma tube_slabs_30 : ∀ k, 116 ≤ k → k < 120 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 116 slabs_30

end PRMPlus
