import PRMPlus.Params

namespace PRMPlus

lemma slabs_14 : checkSlabRange tubeParams 52 4 = true := by decide +kernel

lemma tube_slabs_14 : ∀ k, 52 ≤ k → k < 56 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 52 slabs_14

end PRMPlus
