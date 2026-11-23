import PRMPlus.Params

namespace PRMPlus

lemma slabs_39 : checkSlabRange tubeParams 152 4 = true := by decide +kernel

lemma tube_slabs_39 : ∀ k, 152 ≤ k → k < 156 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 152 slabs_39

end PRMPlus
