import PRMPlus.Params

namespace PRMPlus

lemma slabs_53 : checkSlabRange tubeParams 208 4 = true := by decide +kernel

lemma tube_slabs_53 : ∀ k, 208 ≤ k → k < 212 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 208 slabs_53

end PRMPlus
