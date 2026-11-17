import PRMPlus.Params

namespace PRMPlus

lemma slabs_11 : checkSlabRange tubeParams 40 4 = true := by decide +kernel

lemma tube_slabs_11 : ∀ k, 40 ≤ k → k < 44 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 40 slabs_11

end PRMPlus
