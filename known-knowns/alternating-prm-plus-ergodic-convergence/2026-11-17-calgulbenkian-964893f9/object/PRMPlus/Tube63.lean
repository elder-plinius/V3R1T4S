import PRMPlus.Params

namespace PRMPlus

lemma slabs_63 : checkSlabRange tubeParams 248 4 = true := by decide +kernel

lemma tube_slabs_63 : ∀ k, 248 ≤ k → k < 252 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 248 slabs_63

end PRMPlus
