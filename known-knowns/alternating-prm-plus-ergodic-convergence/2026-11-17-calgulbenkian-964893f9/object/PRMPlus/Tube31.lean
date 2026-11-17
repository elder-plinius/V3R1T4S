import PRMPlus.Params

namespace PRMPlus

lemma slabs_31 : checkSlabRange tubeParams 120 4 = true := by decide +kernel

lemma tube_slabs_31 : ∀ k, 120 ≤ k → k < 124 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 120 slabs_31

end PRMPlus
