import PRMPlus.Params

namespace PRMPlus

lemma slabs_52 : checkSlabRange tubeParams 204 4 = true := by decide +kernel

lemma tube_slabs_52 : ∀ k, 204 ≤ k → k < 208 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 204 slabs_52

end PRMPlus
