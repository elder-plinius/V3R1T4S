import PRMPlus.Params

namespace PRMPlus

lemma slabs_50 : checkSlabRange tubeParams 196 4 = true := by decide +kernel

lemma tube_slabs_50 : ∀ k, 196 ≤ k → k < 200 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 196 slabs_50

end PRMPlus
