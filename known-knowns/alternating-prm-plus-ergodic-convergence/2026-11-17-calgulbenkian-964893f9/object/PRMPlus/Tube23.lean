import PRMPlus.Params

namespace PRMPlus

lemma slabs_23 : checkSlabRange tubeParams 88 4 = true := by decide +kernel

lemma tube_slabs_23 : ∀ k, 88 ≤ k → k < 92 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 88 slabs_23

end PRMPlus
