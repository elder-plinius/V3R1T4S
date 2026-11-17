import PRMPlus.Params

namespace PRMPlus

lemma slabs_18 : checkSlabRange tubeParams 68 4 = true := by decide +kernel

lemma tube_slabs_18 : ∀ k, 68 ≤ k → k < 72 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 68 slabs_18

end PRMPlus
