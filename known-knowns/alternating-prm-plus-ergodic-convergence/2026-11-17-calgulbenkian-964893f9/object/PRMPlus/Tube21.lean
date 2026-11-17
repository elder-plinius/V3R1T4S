import PRMPlus.Params

namespace PRMPlus

lemma slabs_21 : checkSlabRange tubeParams 80 4 = true := by decide +kernel

lemma tube_slabs_21 : ∀ k, 80 ≤ k → k < 84 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 80 slabs_21

end PRMPlus
