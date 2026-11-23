import PRMPlus.Params

namespace PRMPlus

lemma slabs_29 : checkSlabRange tubeParams 112 4 = true := by decide +kernel

lemma tube_slabs_29 : ∀ k, 112 ≤ k → k < 116 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 112 slabs_29

end PRMPlus
