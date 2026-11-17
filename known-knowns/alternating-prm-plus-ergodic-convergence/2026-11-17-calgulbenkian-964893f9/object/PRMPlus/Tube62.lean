import PRMPlus.Params

namespace PRMPlus

lemma slabs_62 : checkSlabRange tubeParams 244 4 = true := by decide +kernel

lemma tube_slabs_62 : ∀ k, 244 ≤ k → k < 248 → checkSlab tubeParams k = true :=
  checkSlabRange_sound tubeParams 4 244 slabs_62

end PRMPlus
