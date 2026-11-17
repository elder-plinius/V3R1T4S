import PRMPlus.Params

namespace PRMPlus

lemma slabs_10 : checkSlabRange tubeParams 36 4 = true := by decide +kernel

lemma tube_slabs_10 : ∀ k, 36 ≤ k → k < 40 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 36 slabs_10

end PRMPlus
