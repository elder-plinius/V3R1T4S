import PRMPlus.Params

namespace PRMPlus

lemma slabs_19 : checkSlabRange tubeParams 72 4 = true := by decide +kernel

lemma tube_slabs_19 : ∀ k, 72 ≤ k → k < 76 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 72 slabs_19

end PRMPlus
