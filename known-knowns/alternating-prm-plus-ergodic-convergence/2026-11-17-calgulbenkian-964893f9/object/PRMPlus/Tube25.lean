import PRMPlus.Params

namespace PRMPlus

lemma slabs_25 : checkSlabRange tubeParams 96 4 = true := by decide +kernel

lemma tube_slabs_25 : ∀ k, 96 ≤ k → k < 100 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 96 slabs_25

end PRMPlus
