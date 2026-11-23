import PRMPlus.Params

namespace PRMPlus

lemma slabs_49 : checkSlabRange tubeParams 192 4 = true := by decide +kernel

lemma tube_slabs_49 : ∀ k, 192 ≤ k → k < 196 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 192 slabs_49

end PRMPlus
