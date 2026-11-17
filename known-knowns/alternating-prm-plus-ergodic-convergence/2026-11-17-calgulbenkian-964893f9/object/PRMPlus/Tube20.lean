import PRMPlus.Params

namespace PRMPlus

lemma slabs_20 : checkSlabRange tubeParams 76 4 = true := by decide +kernel

lemma tube_slabs_20 : ∀ k, 76 ≤ k → k < 80 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 76 slabs_20

end PRMPlus
